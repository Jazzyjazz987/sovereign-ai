# DECISIONS NEEDED — for Jazzy

The autonomous manager loop parked these because they need a human call, hardware, or root.
The loop will NOT act on any of these without an explicit instruction.

---

## D1 — GPU acceleration (driver 570 + vLLM T3/T4)
**Status:** blocked — needs root + reboot + physical GPU
`nvidia-smi` fails on this host. DKMS reports `nvidia/580.159.03` installed for kernel
6.17.0-35 but no usable device responds — this looks like a VM with no GPU passthrough, not a
missing driver. vLLM T3 (Qwen 14B AWQ) and T4 (Mistral Small 22B AWQ) cannot run without it.
**Options:**
- (a) Confirm whether this box has a real RTX 3090 attached / passed through. If not, the "7x
  speed boost" is not available here regardless of driver work.
- (b) If GPU exists: `sudo apt install nvidia-driver-570 && sudo reboot`, then wire `vllm-t3`
  / `vllm-t4` services into `docker-compose.yml` (Dockerfile.vllm exists, services do not).
**Needed from you:** which host is the real inference server, and do you want the loop to
prepare the vLLM compose services (inactive) in the meantime?

## D2 — Model cascade vs. frozen spec
**Status:** blocked — deviates from CLAUDE.md "cascade figée"
CLAUDE.md freezes: T1 Mistral 7B · T2 Llama 3.3 8B · T3 Qwen 3 14B · T4 Mistral Small 22B.
Reality: Ollama has `mistral:7b` and `dolphin-mixtral:latest` only. `dolphin-mixtral` is not
in the spec at all. Llama 3.3, Qwen, Mistral Small are not pulled; T3/T4 need vLLM+GPU anyway.
**Options:**
- (a) Pull `llama3.3:8b` via Ollama now (CPU-friendly, ~5 GB) to make T2 spec-compliant;
  keep `dolphin-mixtral` as an interim T3/T4 stand-in on CPU.
- (b) Keep current models, and formally amend the CLAUDE.md cascade table.
- (c) Wait for the GPU host and run the exact spec.
**Needed from you:** pick a/b/c. Until then the loop only makes the code reference models that
actually exist and fall back gracefully.

## D3 — Production deployment
**Status:** partially unblocked 2026-09-05 — operator set priorities (backups 6, TLS 6, monitoring)
The loop will now do the infra scaffolding it can locally: B10 (pg_dump backups), B11
(nginx TLS reverse proxy behind a compose profile), B6 (real /metrics). Still needs a human
call on: the actual deployment host/orchestrator, moving `.env` secrets to a vault, and a
CNIL/RGPD sign-off on the T5 cloud path before production traffic.
**Needed from you:** deployment target, vault yes/no, RGPD sign-off owner.

## D4 — Git credential hygiene
**Status:** operator wants GitHub kept updated (priority 7) → the loop now DOES push to the
existing `origin`. The remote URL still embeds a GitHub PAT in cleartext in `.git/config`.
**Recommendation:** rotate that token and move to SSH or a credential helper. The loop will not
rewrite the remote URL on its own — say the word and it will.
**Needed from you:** rotate the token; confirm if the loop should switch the remote to SSH.

## D5 — T5 cloud key is disabled (operator priority 5)
**Status:** BLOCKER for priority 5 ("T5 cloud integration testing").
`.env` contains `ANTHROPIC_API_KEY=disabled` (literal 8-char string). Every T5 call returns
401 `invalid x-api-key`. The code is ready (anonymise → cloud → deanonymise, `claude-sonnet-5`,
graceful T4 fallback), but cloud T5 cannot be tested without a real key.
**Options:**
- (a) Provide a real Anthropic API key in `.env` (`ANTHROPIC_API_KEY=sk-ant-...`) → the loop
  will run the full B4 verification (PII gate + no-leak check).
- (b) Keep cloud OFF by design (pure-sovereign posture) — then say so and the loop will mark T5
  as "intentionally disabled, local-only" and stop treating it as a gap.
**Your mid-session note:** "in case it is not set, use opus 5 model for this session." Two
readings: (i) set `T5_MODEL=claude-opus-5` for the stack's cloud tier — done-able now via `.env`,
but still needs a valid key; (ii) run THIS Claude Code session on Opus 5 — that is a client
setting (`/model opus`), not something the loop can change. Please clarify which.

## D6 — Docker vs native — "l'utilisation de docker alourdit-elle notre IA ?"
**Status:** open architecture question raised by operator 2026-09-05.
**Analysis (short):** Docker adds ~0% to inference math — the 3 tok/s we see is 100% CPU with
no GPU driver, not containerisation. Docker *does* add: GPU-passthrough friction
(nvidia-container-toolkit, CUDA image matching), duplicated Python runtimes per service, the
heavy `nvidia/cuda:12.1` base for Anone, and a slow build→restart dev loop (felt today).
**Recommendation — hybrid:**
- Run **Ollama natively** on the GPU host (systemd) — removes the biggest friction point, gives
  it direct VRAM access; this is Ollama's own recommended deployment.
- Keep the **plumbing** (LiteLLM, PostgreSQL, Prometheus, Grafana, Anone, LangGraph) in Compose
  — light, benefits from isolation, easy to redeploy.
- Do **API dev** (`main.py`, `anone_api.py`) in the `venv-*` from CLAUDE.md with `--reload`,
  containerise only for integration/deploy.
- vLLM: fine in Docker (official image), but needs a GPU regardless.
**The real weight today is not Docker:** no GPU driver, and `dolphin-mixtral` (46B) as T4 on CPU.
**Needed from you:** approve the hybrid split, or say keep everything in Compose.

---

## Answered decisions
_(none yet — add answers here and the loop will pick them up next iteration)_
