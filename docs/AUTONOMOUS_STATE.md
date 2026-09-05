# AUTONOMOUS STATE — manager loop checkpoint

**Last iteration:** 2026-09-05 (session_0146Gw93oyAzeQRMBQienYB2)
**Loop skill:** `.claude/skills/master-project`
**Loop prompt:** `/loop continue autonomous project completion for the Sovereign AI stack`
**Full handoff:** `docs/RESUME_AUTONOMOUS.md`

## RESUME HERE
Next task: **B6 — Prometheus `/metrics` endpoints** on langgraph + anone (dashboards are empty;
prometheus logs a `/metrics` 404 every few seconds). Then B12 (ollama CPU tuning), B14 (HF cache
volume), B7 (doc accuracy pass), B8, B9 (GPU probe), B10, B11.
**If the operator says "clé posée":** first run the full B4 E2E — recreate langgraph+litellm
(NOT anone — it re-downloads 1.2 GB, B14), test key validity, then a PII query through T5 with
a log check that no raw name leaves for the cloud.
First commands:
```
cd /opt/claude/sovereign-ai
grep -n metrics config/prometheus.yml
cat api/main.py | sed -n '1,20p'   # add prometheus_client /metrics
```

## In flight
- Nothing uncommitted after this checkpoint.

## Done this session
- Bootstrapped autonomous manager (skill + BACKLOG + DECISIONS D1–D6 + RESUME_AUTONOMOUS).
- **B1 ✅** LiteLLM gateway fixed (entrypoint override + config rewrite), verified.
- **B2 ✅** Ollama healthcheck fixed (`ollama ps`), container now `healthy`.
- **B3 ✅** Cascade routing rewritten: `TIERS` single source, `complexity` override, cap 5.0,
  `query_ollama_with_fallback` chain, `tier` field.
- **B4 ~** T5 code complete (`claude-sonnet-5` via `T5_MODEL`). LIVE test blocked: `.env`
  `ANTHROPIC_API_KEY=disabled` → D5.
- **B5 ✅** pytest suite `api/tests/` — 12 passed (run in the langgraph image).
- **B13a ✅ (CRITICAL RGPD)** — `main.py` was sending raw PII to the cloud when Anone errored.
  `route_t5_with_anonymization` now fail-closed (cloud only if `status==ok` + `anonymized_text`).
- **B13b ✅** — Agent Anone rewritten: GLiNER loads (`model_loaded: true`), `/anonymize` returns
  unique `<PERSON_0>` tokens + `pii_mapping`, HTTP 503 on failure. 14 tests pass. The T5 gate
  now passes real anonymised text (stops only at the 401 from the disabled key).
- **B14 filed** — HF model cache (~1.2 GB) not on a volume → re-downloads on `anone` recreate.

## Standing constraints
- CPU-only host, no confirmed GPU. Never reboot. sudo only if non-interactive + no reboot.
- Model cascade frozen. Verify every doc claim against a live command.
- Commit AND `git push origin master` every checkpoint.
- **Serialise inference tests** (see skill "Inference-testing rules"). Restart ollama if wedged.
- Open decisions: D1 GPU presence, D2 model spec, D4 git token, D5 T5 key, D6 docker-vs-native.

## Backlog status
B1 ✅  B2 ✅  B3 ✅  B4 ~(blocked D5 — key)  B5 ✅  B13a ✅  B13b ✅
B6 ☐←NEXT  B7 ☐  B8 ☐  B9 ☐(GPU)  B10 ☐(pg backup)  B11 ☐(TLS)  B12 ☐(ollama CPU)  B14 ☐(HF cache)
