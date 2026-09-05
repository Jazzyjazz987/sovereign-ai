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

**System state at end of session 1:**
- Up: postgres (healthy), anone, langgraph, prometheus, grafana, ollama, **litellm (now up)**
- No usable GPU (`nvidia-smi` fails; DKMS nvidia/580.159.03 present; GPU presence unconfirmed)
- Ollama models present: `mistral:7b`, `dolphin-mixtral:latest`, `neural-chat:latest`, `llama2:7b`
- CPU-only mode

**Next task on resume: B2 — fix the Ollama container healthcheck** (image has no `curl`, so the
container is permanently `unhealthy`). Then B3 (cascade code vs real model names). See backlog.

First commands on resume:
```
docker compose ps
docker inspect --format '{{.State.Health.Status}}' sovereign-ai-ollama-1
sed -n '/^  ollama:/,/^  postgres:/p' docker-compose.yml
cat docs/AUTONOMOUS_STATE.md
```
