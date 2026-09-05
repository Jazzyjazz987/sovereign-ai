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
**Status:** not started — needs target + policy decisions
`docs/DEPLOYMENT.md` exists but production needs: deployment host/orchestrator, TLS/mTLS
between services, PostgreSQL backup strategy + retention, secret management (currently plain
`.env`), and a CNIL/RGPD sign-off on the T5 cloud path.
**Needed from you:** deployment target and whether secrets move to a vault.

## D4 — Git credential hygiene
**Status:** flagged — not fixed (would break your push flow)
The `origin` remote URL in `.git/config` embeds a GitHub Personal Access Token in cleartext
(`https://ghp_...@github.com/...`). Anyone with read access to the working tree can read it.
**Recommendation:** rotate that token, then set the remote to a plain URL and use a credential
helper or SSH. The loop has not touched this and does not push.
**Needed from you:** confirm you want this changed and the loop can rewrite the remote URL.

---

## Answered decisions
_(none yet — add answers here and the loop will pick them up next iteration)_
