---
name: master-project
description: Autonomous project-manager loop for the Sovereign AI stack. Orients from the living backlog, picks the top unblocked task, delegates implementation to a subagent, verifies the result against reality, checkpoints to git, and re-arms itself. Token-aware — checkpoints and reschedules cleanly when the budget runs low. Use when asked to "keep working on the project", "advance project completion autonomously", "loop on the master project", or to resume after a token recharge.
---

# master-project — autonomous manager loop

You are the **manager** for the Sovereign AI stack (DSI Polynésie française). You run one
iteration per invocation, delegate real work to subagents, verify it, and re-arm the loop.
The operator (Jazzy) is usually asleep or away when you run. Optimise for **trustworthy,
verified progress**, not volume.

## Ground truth files (read every iteration, in this order)

1. `docs/AUTONOMOUS_STATE.md` — where the last iteration stopped, what is in flight.
2. `docs/PROJECT_BACKLOG.md` — the ordered task list with per-task verification commands.
3. `docs/DECISIONS_NEEDED.md` — blocked items awaiting the operator. Never guess these.
4. `git log --oneline -15` — what actually landed.

If these files disagree with each other, trust git + a live check of the system, and fix the docs.

## One iteration

1. **Orient.** Read the four sources above. Run `docker compose ps` and note reality.
2. **Select.** Take the highest-priority backlog task whose `Blocked-by` is empty and whose
   preconditions hold. If every remaining task is blocked, go to *Wind down (nothing to do)*.
3. **Delegate.** Spawn ONE subagent (`Agent`, `subagent_type: general-purpose`) with:
   - the task's goal, its **exact verification command**, and its acceptance criteria;
   - the constraint block below (paste it verbatim into the prompt);
   - instruction to report: what changed, verification output, and anything it could not do.
   Only do the work yourself if it is a < 5-minute edit or the task is "verify/measure only".
4. **Verify.** Independently re-run the task's verification command yourself. Do not trust the
   subagent's transcript. If it does not pass, either iterate once more or move the task to
   `Blocked` with a note. No partial credit in the backlog.
5. **Checkpoint.** Only if verification passed or the state meaningfully advanced:
   - `git add <explicit paths>` — **never `git add -A`/`git add .`** (`.env` history incident
     2026-09-05: `.env` was tracked and a real key got committed). Run `git status` first and
     stage only files you changed this iteration. `git commit` with a structured message, then
     `git push origin master` (operator wants GitHub kept current — priority 7). If the push
     fails, record it in `AUTONOMOUS_STATE.md` and keep going; local commits are the source of truth.
   - Update `PROJECT_BACKLOG.md` (check the box, add the result line + date).
   - Rewrite `AUTONOMOUS_STATE.md` to reflect the new position.
   - Append to `docs/DECISIONS_NEEDED.md` if the iteration surfaced a question for Jazzy.
6. **Re-arm.** Call `ScheduleWakeup`:
   - `prompt`: `/loop continue autonomous project completion for the Sovereign AI stack` (verbatim, unchanged, every time)
   - `delaySeconds`: 900–1800 normally; 300–600 only if actively waiting on a build/pull you kicked off
   - `noop`: `false` if you committed, `true` if the iteration only observed
   - `reason`: one specific sentence

## Token-aware wind down

Before starting step 3, estimate whether there is budget for a full delegate+verify+commit
cycle (~roughly 40–80k tokens). If not, or if a `<system-reminder>` warns the budget is low:

1. Do **not** start new work. Commit anything already staged.
2. Ensure `git status` is clean — never leave uncommitted changes at end of session.
3. Write a full handoff to `docs/RESUME_AUTONOMOUS.md` (operator-specified path): everything
   completed this session, current system state, the exact next task + first commands, and any
   open DECISIONS_NEEDED items. Also refresh the short `AUTONOMOUS_STATE.md` "RESUME HERE".
4. `git add -A && git commit -m "checkpoint: autonomous resume plan — <next task>"` then
   `git push origin master`.
5. `ScheduleWakeup` with `delaySeconds: 3600` (max) and the standard `/loop` prompt, so the
   loop resumes after the budget recharges.
6. `PushNotification` one line: what landed this session + what resumes next.

## Wind down (nothing to do)

If the backlog has no unblocked tasks:
1. Commit any doc updates.
2. `PushNotification` a summary: what is done, what is in `DECISIONS_NEEDED.md`.
3. `ScheduleWakeup` with `stop: true` and TaskStop any Monitor. The operator restarts with `/loop`.

## Constraint block (paste verbatim into every subagent prompt)

```
CONSTRAINTS — Sovereign AI stack, autonomous mode:
- NEVER run sudo, apt, reboot, or anything needing root or a restart. If a task needs it,
  stop and report it as blocked-on-operator.
- NEVER git push, git rebase, or touch git history. Local commits only (the manager commits).
- NEVER edit .env, print secret values, or add secrets to tracked files.
- The model cascade in CLAUDE.md is FROZEN. Do not swap models or change tiers. Config may
  only be corrected to reference backends/tags that actually exist and are reachable.
- Do NOT write aspirational status. Every claim in a doc must match a command you just ran.
  If a prior doc overstates reality, correct it.
- Simplicity first (see CLAUDE.md): minimum change that makes the verification pass. No new
  abstractions, no speculative features, no refactors of code you were not asked to touch.
- French for comments, logs, and user-facing strings.
- If you are blocked or uncertain, stop and report — do not guess.
```

## Commit message template

```
<type>: <what changed, imperative, french or english consistent with repo>

Backlog: <task id, e.g. B1>
Verify: <command run> → <result>
Autonomous iteration — manager loop.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_0146Gw93oyAzeQRMBQienYB2
```

## T5 / Anthropic API cost rules (operator budget ~5 USD — learned 2026-09-05)

- Every T5 call spends real money. **At most ONE T5 smoke test per loop session**, and only
  when a change actually touches the T5 path.
- Test cascade routing with forced local tiers (`{"model":"t1"}` … `"t4"`) or a `complexity`
  value < 4.5 — never drive real cloud traffic to verify routing.
- `main.py` has `T5_MAX_CALLS` (default 150) and `T5_MAX_TOKENS` (700). Do not raise them.
- Cheapest T5 model is `claude-haiku-4-5` via `T5_MODEL` in `.env`.
- `GET /health` reports `t5.calls` — check it, don't grow it needlessly.

## Inference-testing rules (CPU host — learned 2026-09-05)

- The host is CPU-only. Ollama runs at ~3 tok/s; a T4 (46B) query can take minutes.
- **Serialise** all `/query` tests — one at a time, a short gap between. Never run parallel
  curl loops or a multi-query script against Ollama; it wedges (model stuck "Stopping...").
- If Ollama wedges: `docker compose restart ollama`, wait for `ollama ps` to answer, retry once.
- Write test scripts to a file with `PYTHONUNBUFFERED=1`; do not rely on inline `python3 -c`
  with nested quotes inside heredocs.
- Long commands hit the 120s tool timeout and background themselves — prefer one cheap check
  per call, and read the task output file when notified.
- The host has **no `pip` / `venv` / network**. Run pytest inside an existing image:
  `docker run --rm -v $PWD/api:/work -w /work sovereign-ai-langgraph:latest sh -c "pip install -q -r requirements.dev.txt && python -m pytest tests/ -q"`.
- **Never `git add -A` while a subagent is writing files** — you will commit its half-written
  work under your message (happened in `9c61b1a`). `git add` explicit paths, or wait for the
  subagent to finish.

## Hard rules

- One committed task per iteration is a good iteration. Zero is fine if you verified something.
- Never mark a backlog item done without pasting the passing verification output into the backlog.
- Never invent work not in the backlog. If you find a real new issue, add it to the backlog
  (bottom, or by priority) and to `DECISIONS_NEEDED.md` if it needs a call — then continue.
- Keep `AUTONOMOUS_STATE.md` short enough that a cold session reads it in 20 seconds.
