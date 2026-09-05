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

## B1 — Fix LiteLLM gateway (port 4000) [DONE? no]
**Blocked-by:** none
**Problem:** `config/litellm_config.yaml` is invalid — `router_settings` is a YAML list (must
be a mapping); model entries point at tags that do not exist (`ollama/mistral:7b-instruct-q4_k_m`,
`ollama/llama2:8b`); `claude-sonnet` uses a stale model id; vLLM T3/T4 backends are not running.
Container exits with code 3 and falls back to LiteLLM's azure example config.
**Do:** Rewrite the config to reference only reachable backends (ollama tags that exist + the
Claude model). Keep tier names aligned to CLAUDE.md. Mark vLLM entries with a comment that they
are inactive until a GPU host exists — do not delete the tier concept.
**Verify:**
```
docker compose up -d litellm && sleep 20 && \
  curl -sf http://localhost:4000/health && echo && \
  curl -sf http://localhost:4000/v1/models
```
Both must return 200 with JSON; `/v1/models` lists the configured models.

## B2 — Fix Ollama container healthcheck [DONE? no]
**Blocked-by:** none
**Problem:** compose healthcheck runs `curl -f http://localhost:11434/api/tags`; the
`ollama/ollama` image has no `curl`, so the container is permanently `unhealthy` even though
the API works. Anything with `depends_on: condition: service_healthy` is affected.
**Do:** Replace the healthcheck test with one using a binary present in the image
(e.g. `ollama list`, or a bash `/dev/tcp` probe).
**Verify:**
```
docker compose up -d ollama && sleep 30 && \
  docker inspect --format '{{.State.Health.Status}}' sovereign-ai-ollama-1
```
Must print `healthy`.

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

---

## Parked — needs operator decision (see docs/DECISIONS_NEEDED.md)
- GPU driver 570 install + vLLM T3/T4 bring-up (sudo, reboot, GPU hardware)
- Model cascade reconciliation: dolphin-mixtral vs CLAUDE.md frozen spec; pull llama3.3:8b / qwen / mistral-small
- Production deployment target (TLS, PostgreSQL backups, infra host)
- git remote embeds a GitHub PAT in the URL — credential hygiene
