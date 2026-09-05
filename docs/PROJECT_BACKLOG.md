# PROJECT BACKLOG — Sovereign AI stack

Living task list for the autonomous manager loop (`.claude/skills/master-project`).
Ordered by priority. A task is **done** only when its `Verify` command output is pasted
under it with a date. Reality beats prior docs — several existing status docs overstate
what is actually working (see B8).

**Baseline snapshot (2026-09-05, session start):**
- Running: postgres (healthy), anone, langgraph, prometheus, grafana, ollama (unhealthy)
- Down: litellm (Exited 3) — loading LiteLLM's built-in azure example config, not ours
- No GPU: `nvidia-smi` fails; DKMS shows nvidia/580.159.03 but no usable device. CPU-only.
- Ollama models actually present: `mistral:7b`, `dolphin-mixtral:latest`
- `.env` has ANTHROPIC_API_KEY non-empty (not yet verified end-to-end)

---

## B13 — RGPD: Agent Anone anonymisation is broken (CRITICAL)
Found by the B5 test subagent + confirmed live 2026-09-05.

### B13a — fail-closed T5 path [DONE 2026-09-05]
**Problem:** `anone_api` GLiNER is **not loaded** (`ner is None`) → `/anonymize` returns
`{"status":"error"}` with **HTTP 200**. `main.py` checked only the status code, then did
`anon_data.get("anonymized_text", query)` → **fell back to the raw query and sent PII to the
cloud.** Direct violation of CLAUDE.md ("jamais en clair vers cloud", "OBLIGATOIRE").
**Fix (api/main.py):** `route_t5_with_anonymization` is now fail-closed — the cloud is called
only when Anone returns `status == "ok"` AND an `anonymized_text`. Any other case →
`_fallback_local()` (T4). New tests `api/tests/test_t5_failclosed.py` (2) assert the Anthropic
client is never even instantiated in those cases.
**Verify (2026-09-05):** `POST /query complexity=5.0` with a name + NIR →
`"T5 non appelé (anonymisation non confirmée: GLiNER not loaded); repli local sur T4"`,
`model_used=dolphin-mixtral`. PII stayed local. `pytest tests/ -q` → 12 passed.

### B13b — make Agent Anone actually anonymise [DONE? no]  ← NEXT / TOP PRIORITY
**Blocked-by:** needs `pip`/network in the anone image build (available during `docker build`).
**Problems (api/anone_api.py):**
1. `pipeline("token-classification", model="urchade/gliner_multi_pii-v1")` is the wrong API —
   GLiNER needs the `gliner` package (`from gliner import GLiNER`), absent from
   `requirements.anone.txt`. So `ner` is always `None`.
2. Bare `except:` hides the load error.
3. `/anonymize` returns **no `pii_mapping`** and uses **non-unique** placeholders (`[person]`),
   so `/deanonymize` can never restore — the T5 user gets a masked response.
4. Offset drift: substitutions use original offsets after the string length changed → only
   correct for single-entity input. (Fix: apply entities sorted by `start` descending.)
5. `/anonymize` returns HTTP 200 on internal error (should be 503/500).
**Do:** add `gliner` to `requirements.anone.txt`; load `GLiNER.from_pretrained("urchade/gliner_multi_pii-v1")`;
detect with a fixed PII label set (person, email, phone, NIR/SSN, address, IBAN…); replace each
occurrence with a **unique** token (`<PERSON_0>`) and return `pii_mapping`; splice right-to-left;
return 503 when the model is unavailable. Keep `main.py`'s fail-closed check.
**Verify:**
```
docker compose build anone && docker compose up -d anone && sleep 60
curl -s localhost:8080/anonymize -d '{"text":"Jean Dupont (jean.dupont@gov.pf) conteste"}' \
  → status ok, anonymized_text has <PERSON_0> and <EMAIL_0>, pii_mapping maps them back, raw absent
curl -s localhost:8080/deanonymize -d '{"text":"<PERSON_0> ok","pii_mapping":{"<PERSON_0>":"Jean Dupont"}}'
  → "Jean Dupont ok"
# then the full B4 verify (needs a real ANTHROPIC_API_KEY — D5)
```

---

## B1 — Fix LiteLLM gateway (port 4000) [DONE 2026-09-05]
**Blocked-by:** none
**Problem:** two bugs. (1) The image ENTRYPOINT is shell-form
(`litellm --config /app/proxy_server_config.yaml --port 4000`) so the compose `command:` was
silently ignored and it loaded LiteLLM's bundled Azure example config → exit 3.
(2) `config/litellm_config.yaml` was invalid — `router_settings` was a list, model tags did not
exist, stale Claude id.
**Fix:**
- `docker-compose.yml`: replaced `command:` with `entrypoint:` pointing at our config; passed
  `ANTHROPIC_API_KEY` + `VLLM_API_KEY` into the container env.
- `config/litellm_config.yaml`: rewritten — T1 `ollama/mistral:7b`, T2 `ollama/llama2:7b`
  (interim, D2), T5 `claude-sonnet-5` with `api_key: os.environ/ANTHROPIC_API_KEY`. vLLM T3/T4
  left as commented tiers (D1). `general_settings.master_key` wired.
**Verify (run 2026-09-05):**
```
docker inspect -f '{{.State.Status}} {{.State.ExitCode}}' sovereign-ai-litellm-1  → running 0
curl -s -o/dev/null -w '%{http_code}' -H "Authorization: Bearer $LITELLM_MASTER_KEY" http://localhost:4000/health  → 200
curl -s .../v1/models  → lists mistral-7b, llama-3.3-8b, claude-sonnet
curl -s .../v1/chat/completions -d '{"model":"mistral-7b",...}'  → 200, content " Paris"
```
Note: this LiteLLM build has no `/health/liveliness` (404) — use `/health` (needs auth header).

## B2 — Fix Ollama container healthcheck [DONE 2026-09-05]
**Problem:** healthcheck ran `curl -f http://localhost:11434/api/tags`; `ollama/ollama` has
neither `curl` nor `wget`, so the container was permanently `unhealthy`.
**Fix:** `docker-compose.yml` healthcheck test → `["CMD", "ollama", "ps"]` (rc 0 when the
server responds), added `start_period: 40s`.
**Verify (run 2026-09-05):**
```
docker compose up -d ollama ; docker inspect --format '{{.State.Health.Status}}' sovereign-ai-ollama-1
  → healthy (3 consecutive passing checks); litellm /health still 200; langgraph still healthy
```

## B3 — Cascade code vs. real model names (api/main.py) [DONE 2026-09-05]
**Problems found:** (1) `calculate_complexity` capped at 4.0 but the T5 branch needed ≥4.5 →
**T5 was unreachable by auto-routing**. (2) The documented `complexity` request field did not
exist on `QueryRequest` — it was silently ignored by every curl test in the docs. (3) On a model
error `query_ollama` returned an error *string* with HTTP 200 — no fallback.
**Fix (api/main.py):**
- `QueryRequest` gains optional `complexity: float` override.
- Single `TIERS` list (T1→T5) is the one source of truth for tier→model.
- `calculate_complexity` cap → 5.0; length-bonus elif order fixed.
- `route()` returns `(model, complexity, tier)`; forced-model map derived from `TIERS`.
- New `query_ollama_with_fallback(start_tier, prompt)` walks the chain downward; `query_ollama`
  now raises `OllamaError`. `/query` response gains a `tier` field.
**Verify (run 2026-09-05, pre-load-thrash sweep + post-restart single):**
```
complexity 1.0 → T1 mistral:7b   status ok   (post-restart, 7.8s, coherent FR)
complexity 2.5 → T3 neural-chat  status ok
complexity 4.0 → T4 dolphin-mixtral  status ok
complexity 5.0 → T5 → 401 (key disabled, B4) → graceful fallback to T4 dolphin-mixtral, status ok
forced model "t9" (bogus) → defaults to T1, status ok
```
**Incident note:** running 3+ concurrent curl loops against a CPU-only Ollama (4 models,
MAX_LOADED_MODELS=2, incl. 46B dolphin-mixtral) wedged Ollama (model stuck "Stopping...").
`docker compose restart ollama` cleared it. → new backlog B12; loop must serialise inference tests.

## B4 — T5 path + mandatory PII anonymisation gate [CODE DONE 2026-09-05 · LIVE TEST BLOCKED]
**Blocked-by:** live cloud test blocked on `ANTHROPIC_API_KEY` (see below)
**Done:**
- Traced `route_t5_with_anonymization` in `api/main.py`: order is `/anonymize` (Agent Anone) →
  Claude API → `/deanonymize`. If Anone is unreachable or non-200, the function returns an error
  and never calls the cloud — the gate holds.
- Claude model id `claude-3-5-sonnet-20241022` → `T5_MODEL` env var, default `claude-sonnet-5`
  (verified current via the `claude-api` skill; CLAUDE.md T5 = "Claude Sonnet").
- On `anthropic.APIError` T5 now falls back to `query_ollama_with_fallback("T4", …)` → clean
  local degradation instead of a bare error dict.
**BLOCKER:** `.env` has `ANTHROPIC_API_KEY=disabled` (literal string). Every T5 call → 401
`authentication_error`. Cloud T5 is effectively OFF. Recorded in DECISIONS_NEEDED D5.
**Verify (partial, 2026-09-05):**
```
POST /query complexity=5.0 → message: "T5 indisponible (401 ... invalid x-api-key); repli local sur T4"
  status=ok, model_used=dolphin-mixtral   ← fallback path proven
```
Remaining to verify once a real key is supplied: anone `/anonymize` hit in the log window +
raw PII never present in an outbound-cloud log line.

## B5 — pytest suite under api/tests/ [DONE 2026-09-05]
Created `api/tests/` (test_routing.py ×5, test_fallback.py ×2, test_anone.py ×3,
test_t5_failclosed.py ×2) + `api/requirements.dev.txt` + `conftest.py` (stubs `transformers`).
Host has no `pip`/`venv`/network → suite runs inside `sovereign-ai-langgraph:latest`:
`docker run --rm -v $PWD/api:/work -w /work sovereign-ai-langgraph:latest sh -c "pip install -q -r requirements.dev.txt && python -m pytest tests/ -q"` → **12 passed**.
Surfaced the B13 anonymisation bugs.

## B6 — Prometheus /metrics endpoints [DONE? no]
**Blocked-by:** B3
**Problem:** `config/prometheus.yml` scrapes langgraph/anone/litellm but none expose `/metrics`,
so Grafana dashboards are empty.
**Do:** Add a `/metrics` endpoint (prometheus_client) to `api/main.py` and `api/anone_api.py`
exposing at minimum: request count, request latency histogram, per-tier selection count.
Keep it minimal.
**Verify:**
```
curl -sf http://localhost:8888/metrics | head -5
curl -sf http://localhost:8080/metrics | head -5
curl -sf 'http://localhost:9090/api/v1/targets' | grep -o '"health":"[a-z]*"' | sort | uniq -c
```
Both `/metrics` return prometheus text; at least langgraph + anone targets show `"health":"up"`.

## B7 — Documentation accuracy pass [DONE? no]
**Blocked-by:** B1, B2, B3, B4, B6
**Problem:** `docs/FINAL_STATUS.md`, `docs/VALIDATION_REPORT.md`, `REBUILD_SUMMARY.txt` claim
"ALL SYSTEMS OPERATIONAL", "7/7 services", specific models "Loaded" that are not, latency
numbers with no run behind them.
**Do:** Reconcile every status doc against the verified state after B1–B6. Keep the structure;
correct the claims; add a "Verified on <date> by autonomous loop" line with the commands used.
Do not delete history docs (GPU_RECOVERY_LOG etc.) — annotate.
**Verify:** `grep -rniE '7/7|ALL SYSTEMS OPERATIONAL|production-ready' docs/ *.md` — each remaining
hit is either removed or immediately followed by the evidence line.

## B8 — .env.example completeness [DONE? no]
**Blocked-by:** none
**Do:** Ensure `.env.example` lists every key referenced in `docker-compose.yml` and the code,
with placeholder values and a one-line comment each. No real secrets.
**Verify:**
```
comm -23 <(grep -oE '\$\{[A-Z_]+' docker-compose.yml | tr -d '${' | sort -u) \
         <(grep -oE '^[A-Z_]+' .env.example | sort -u)
```
Output empty (every compose var has an example entry).

## B9 — GPU driver + GPU mode (operator priority 4) [DONE? no]
**Blocked-by:** none (operator authorised driver install 2026-09-05; sudo may still be unavailable to the loop)
**Problem:** `nvidia-smi` fails. DKMS shows `nvidia/580.159.03` built for kernel 6.17.0-35.
Unknown whether a physical GPU is attached. Secure Boot reported disabled (PHASE_2_RESULTS).
**Do (in order, stop at the first blocker and record it):**
1. `lspci | grep -i nvidia` — is there a GPU device at all? If none → this is a VM without GPU
   passthrough; record in DECISIONS_NEEDED D1 and STOP (nothing else here is possible).
2. If a device exists: `modprobe nvidia` / check `dmesg | grep -i nvidia`. Try
   `nvidia-modprobe` before assuming a reinstall is needed.
3. If the module truly needs a rebuild and `sudo` works non-interactively:
   `sudo dkms autoinstall` then re-test `nvidia-smi`. Do NOT reboot.
4. If `sudo` prompts / a reboot is required → record exact commands for the operator in
   DECISIONS_NEEDED D1 and STOP.
5. On `nvidia-smi` success: `./scripts/switch_mode.sh gpu`, then re-run the B3 cascade verify.
**Verify:** `nvidia-smi` returns 0 AND `docker compose exec ollama nvidia-smi` works from the container.

## B10 — PostgreSQL automated backups (operator priority 6) [DONE? no]
**Blocked-by:** none
**Do:** Add a `pg_dump`-based backup: a script `scripts/pg_backup.sh` writing timestamped
gzip dumps to `data/backups/`, keeping the last 7; wire it into `scripts/health_monitor_loop.sh`
(or a documented cron line). Minimal — no external backup service.
**Verify:** `bash scripts/pg_backup.sh && ls -1 data/backups/*.sql.gz | tail -1` shows a fresh dump;
`gunzip -t` on it passes.

## B11 — TLS / reverse proxy in front of the stack (operator priority 6) [DONE? no]
**Blocked-by:** B1, B3, B4
**Do:** Add an nginx (or caddy) reverse-proxy compose service terminating TLS with a
self-signed cert (documented swap for a real cert), routing `/` → langgraph:8888,
`/gateway` → litellm:4000, `/grafana` → grafana:3000. Keep internal ports unpublished where
possible. This is infra scaffolding — do not break the current plain-HTTP dev flow; put it
behind a compose profile (`--profile tls`).
**Verify:** `docker compose --profile tls up -d proxy && curl -sk https://localhost/health`
returns langgraph health JSON.

## B12 — Ollama CPU-mode concurrency tuning [DONE? no]
**Blocked-by:** none
**Problem:** CPU-only host with 4 pulled models (incl. 46B dolphin-mixtral) + default
`OLLAMA_MAX_LOADED_MODELS=2` / `OLLAMA_NUM_PARALLEL=2` → model thrashing and a wedged unload
under light concurrency (observed 2026-09-05 during B3 testing).
**Do:** In `docker-compose.yml` default `OLLAMA_MAX_LOADED_MODELS` to 1 and `OLLAMA_NUM_PARALLEL`
to 1 for CPU mode (keep them env-overridable so GPU mode can raise them). Document in
`docs/CPU_GPU_MODES.md`. Consider `keep_alive` tuning.
**Verify:** after the change, run 3 sequential `/query` calls (complexity 1.0, 2.0, 4.0) with a
2s gap — all return `status: ok` and `ollama ps` never shows a stuck "Stopping..." entry.

---

## Parked — needs operator decision (see docs/DECISIONS_NEEDED.md)
- **D1** — confirm whether this host has a real GPU (blocks B9 steps 2+ and vLLM T3/T4)
- **D2** — model cascade: dolphin-mixtral / llama2 vs CLAUDE.md frozen spec; whether to pull
  `llama3.3:8b` (CPU-friendly) now
- **D4** — git remote embeds a GitHub PAT in cleartext. Operator wants GitHub kept updated
  (priority 7) so the loop DOES push via the existing remote, but the token should be rotated.
