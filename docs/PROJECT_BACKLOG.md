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

## B3 — Cascade code vs. real model names (api/main.py) [DONE? no]
**Blocked-by:** B2
**Problem:** LangGraph reports cascade `T1→T2→T3→T4`. Need to confirm which model id each tier
calls and that every id resolves against the running Ollama (mistral:7b, dolphin-mixtral).
Tiers whose model is not loaded must degrade gracefully (fall back to the nearest lower tier),
not 500.
**Do:** Read `api/main.py` (the file baked into Dockerfile.langgraph). Make tier→model a single
clear mapping. Add a graceful fallback when a model id is unavailable. No model swaps — if the
"correct" model per CLAUDE.md is not pulled, fall back + log a warning; the gap is recorded in
DECISIONS_NEEDED.
**Verify:**
```
for c in 1.0 2.5 4.0; do
  curl -sf -X POST http://localhost:8888/query -H 'Content-Type: application/json' \
    -d "{\"query\":\"Explique en une phrase le rôle de la DSI\",\"complexity\":$c}" ; echo
done
```
All three return 200 with a coherent French `response` and a `model_used` that exists in `ollama list`.

## B4 — T5 path + mandatory PII anonymisation gate [DONE? no]
**Blocked-by:** B1, B3
**Problem:** CLAUDE.md: Agent Anone anonymisation is OBLIGATOIRE before any T5 call. Need to
prove (a) a high-complexity/cloud query reaches Claude, (b) it passes through `/anonymize` first,
(c) the Claude model id is current (load the `claude-api` skill before editing any model id).
**Do:** Trace the T5 code path in `api/main.py`. Confirm anonymise-before-send. Update the Claude
model id to a current one. If ANTHROPIC_API_KEY is invalid, record in DECISIONS_NEEDED and make
T5 fall back to the top local tier cleanly.
**Verify:**
```
curl -sf -X POST http://localhost:8888/query -H 'Content-Type: application/json' \
  -d '{"query":"Jean Dupont (NIR 1 85 09 78 006 084 36) conteste une sanction disciplinaire, analyse juridique CNIL détaillée","complexity":5.0}' ; echo
docker compose logs --since 2m anone | grep -i anonym
```
Response is coherent French legal analysis; anone logs show an anonymise call in the window;
the raw name must NOT appear in any outbound-cloud log line.

## B5 — pytest suite under api/tests/ [DONE? no]
**Blocked-by:** B3
**Problem:** CLAUDE.md documents `pytest api/tests/` but the directory does not exist. Only
ad-hoc `test_*.py` at repo root.
**Do:** Create `api/tests/` with focused unit tests: (1) complexity→tier routing function,
(2) Anone `/anonymize` then `/deanonymize` round-trips a name, (3) tier fallback when a model
id is missing. Mock network where needed. Add `requirements` for pytest if missing.
**Verify:** `cd api && python -m pytest tests/ -v` → all pass.

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

---

## Parked — needs operator decision (see docs/DECISIONS_NEEDED.md)
- **D1** — confirm whether this host has a real GPU (blocks B9 steps 2+ and vLLM T3/T4)
- **D2** — model cascade: dolphin-mixtral / llama2 vs CLAUDE.md frozen spec; whether to pull
  `llama3.3:8b` (CPU-friendly) now
- **D4** — git remote embeds a GitHub PAT in cleartext. Operator wants GitHub kept updated
  (priority 7) so the loop DOES push via the existing remote, but the token should be rotated.
