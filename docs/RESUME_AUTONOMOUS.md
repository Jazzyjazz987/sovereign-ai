# RESUME — Autonomous session handoff

**Purpose:** a fresh Claude session reads this file to pick up autonomous work where the last
one stopped (e.g. after a token/budget interruption). Operator: Jazzy (Claude Pro, autonomous
authorization granted 2026-09-05).

## How to resume

```
cd /opt/claude/sovereign-ai
/loop continue autonomous project completion for the Sovereign AI stack
```

That re-enters the `master-project` skill (`.claude/skills/master-project/SKILL.md`), which
reads `docs/AUTONOMOUS_STATE.md` → `docs/PROJECT_BACKLOG.md` → `docs/DECISIONS_NEEDED.md` and
continues one task at a time: delegate to a subagent → verify → commit → push → re-arm.

## Autonomous operating rules (from the operator, 2026-09-05)

- Full authorization to make code changes, run tests, deploy updates, configure systems.
- Keep the stack running 24/7; health monitoring active; CPU mode stable.
- Push every checkpoint to GitHub (`git push origin master`).
- `sudo`/reboot: attempt driver work only if `sudo` is non-interactive AND no reboot is needed;
  otherwise document exact steps for the operator and move on. Never reboot autonomously.
- The CLAUDE.md model cascade is frozen — correct config to reality, don't swap models.
- No aspirational docs — every claim must match a command that was just run.

## Session log

### Session 1 — 2026-09-05 (session_0146Gw93oyAzeQRMBQienYB2)
**Landed:**
- Built the autonomous manager system: `.claude/skills/master-project/`, `PROJECT_BACKLOG.md`
  (B1–B11), `DECISIONS_NEEDED.md` (D1–D4), `AUTONOMOUS_STATE.md`, this file.
- **B1 DONE** — LiteLLM gateway (port 4000) was down (exit 3, loading the image's bundled Azure
  example config because the shell-form ENTRYPOINT ignored `command:`). Fixed:
  `docker-compose.yml` now overrides `entrypoint:` to load `/app/litellm_config.yaml` and passes
  `ANTHROPIC_API_KEY`/`VLLM_API_KEY`; `config/litellm_config.yaml` rewritten (valid, real ollama
  tags, `claude-sonnet-5`, vLLM tiers commented pending GPU). Verified: `/health` 200,
  `/v1/models` lists 3 models, real completion returns "Paris".

- **B2 DONE** — Ollama healthcheck (`curl` absent from image) → `["CMD","ollama","ps"]`; container now `healthy`.
- **B3 DONE** — `api/main.py` cascade rewrite: `TIERS` single source of truth, optional
  `complexity` request override, complexity cap 5.0 (T5 was unreachable), `query_ollama_with_fallback`
  downward chain, `query_ollama` raises `OllamaError`, `/query` returns a `tier` field. Verified.
- **B4 code-complete, live test blocked** — T5 model id → `T5_MODEL` env (default `claude-sonnet-5`);
  anonymise→cloud→deanonymise order confirmed; `anthropic.APIError` now falls back to T4 locally.
  BLOCKER: `.env` `ANTHROPIC_API_KEY=disabled` → 401 on every cloud call. See DECISIONS_NEEDED D5.

**System state at end of session 1:**
- Up (7/7): postgres (healthy), ollama (healthy), litellm, anone, langgraph, prometheus, grafana
- No usable GPU (`nvidia-smi` fails; DKMS nvidia/580.159.03 present; GPU presence unconfirmed — D1)
- Ollama models: `mistral:7b`, `llama2:7b`, `neural-chat:latest`, `dolphin-mixtral:latest`
- CPU-only mode, ~3 tok/s. dolphin-mixtral (46B) as T4 is very slow on CPU.
- **New operator questions:** D5 (T5 key / Opus-5), D6 (docker vs native — hybrid recommended).

**Next task on resume: B5 — pytest suite under `api/tests/`.** Then B6 (/metrics), B12 (ollama
CPU tuning), B7 (doc accuracy), B9 (GPU probe), B10 (pg backups), B11 (TLS proxy).

First commands on resume:
```
cd /opt/claude/sovereign-ai
docker compose ps
cat docs/AUTONOMOUS_STATE.md docs/PROJECT_BACKLOG.md
sed -n '1,140p' api/main.py
```

### Session 2 — <fill in on next resume>

