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

---

## Answered decisions
_(none yet — add answers here and the loop will pick them up next iteration)_
