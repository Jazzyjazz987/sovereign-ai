# AUTONOMOUS STATE — manager loop checkpoint

**Last iteration:** 2026-09-05 (session_0146Gw93oyAzeQRMBQienYB2)
**Loop skill:** `.claude/skills/master-project`
**Loop prompt:** `/loop continue autonomous project completion for the Sovereign AI stack`
**Full handoff:** `docs/RESUME_AUTONOMOUS.md`

## RESUME HERE
Next task: **B6 — Prometheus `/metrics` endpoints** on langgraph + anone (dashboards are empty;
prometheus logs a `/metrics` 404 every few seconds). Then B12 (ollama CPU tuning), B14 (HF cache
volume), B7 (doc accuracy pass), B8, B9 (GPU probe), B10, B11.
First commands:
```
cd /opt/claude/sovereign-ai
grep -n metrics config/prometheus.yml
sed -n '1,20p' api/main.py   # add prometheus_client /metrics
```

## In flight
- Nothing uncommitted in git.
- `.env` (untracked): operator's real `ANTHROPIC_API_KEY` + `T5_MODERATION=on`,
  `T5_APPROVAL_TIMEOUT=300` (added by Claude Code). T5 moderation is LIVE.
- This session holds a persistent Monitor (`b02wjazyo`) on the `[T5] Approbation requise`
  log line → PushNotifies the operator on a real T5 request; they reply here to approve/deny
  (`curl -X POST localhost:8888/t5/{id}/approve|deny`). Monitor dies with the session; after
  that every T5 call just times out (300s) to T4 — safe, no un-approved cloud spend.

## Done this session
- Bootstrapped autonomous manager (skill + BACKLOG + DECISIONS D1–D6 + RESUME_AUTONOMOUS).
- **B1 ✅** LiteLLM gateway fixed (entrypoint override + config rewrite), verified.
- **B2 ✅** Ollama healthcheck fixed (`ollama ps`), container now `healthy`.
- **B3 ✅** Cascade routing rewritten: `TIERS` single source, `complexity` override, cap 5.0,
  `query_ollama_with_fallback` chain, `tier` field.
- **B4 ✅** T5 E2E verified — operator supplied a real key. PII query → masked
  (`<PERSON_0>`/`<NIR_0>`/`<ORG_0>`) → `claude-sonnet-5` → de-anonymised response → 0 PII in
  any service log. Full T1→T5 cascade operational with the RGPD gate. D5 resolved.
- **B5 ✅** pytest suite `api/tests/` — 12 passed (run in the langgraph image).
- **B13a ✅ (CRITICAL RGPD)** — `main.py` was sending raw PII to the cloud when Anone errored.
  `route_t5_with_anonymization` now fail-closed (cloud only if `status==ok` + `anonymized_text`).
- **B13b ✅** — Agent Anone rewritten: GLiNER loads (`model_loaded: true`), `/anonymize` returns
  unique `<PERSON_0>` tokens + `pii_mapping`, HTTP 503 on failure. 14 tests pass. The T5 gate
  now passes real anonymised text (stops only at the 401 from the disabled key).
- **B14 filed** — HF model cache (~1.2 GB) not on a volume → re-downloads on `anone` recreate.
- **B16 ✅** T5 cost guardrails (`T5_MAX_TOKENS`/`T5_MAX_CALLS`) + human moderation gate
  (`T5_MODERATION`, `/t5/pending`, `/t5/{id}/approve|deny`, webhook). E2E verified with a real
  T5 call ($0.0009). **B17 open** — notification channel (Claude-session relay armed; ntfy.sh
  is the robust alternative).
- **SECURITY (D4)** — `.env` was git-tracked; a real key briefly hit a local commit, push
  protection blocked it, rewound. `.env` now untracked + `.gitignore` fixed. STILL: `.env` in
  pushed history (`b02c2dd`) + PAT in remote URL → operator must rotate secrets + purge history.

## Standing constraints
- CPU-only host, no confirmed GPU. Never reboot. sudo only if non-interactive + no reboot.
- Model cascade frozen. Verify every doc claim against a live command.
- Commit AND `git push origin master` every checkpoint.
- **Serialise inference tests** (see skill "Inference-testing rules"). Restart ollama if wedged.
- Open decisions: D1 GPU presence, D2 model spec, D4 git token, D5 T5 key, D6 docker-vs-native.

## Backlog status
B1 ✅ B2 ✅ B3 ✅ B4 ✅ B5 ✅ B13a ✅ B13b ✅ B16 ✅(T5 cost+moderation)
B6 ☐←NEXT  B7 ☐  B8 ☐  B9 ☐(GPU)  B10 ☐(pg backup)  B11 ☐(TLS)  B12 ☐(ollama CPU)
B14 ☐(HF cache)  B17 ☐(T5 notif channel)
