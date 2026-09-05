# Token-Aware Autonomous Resume Plan

## How It Works

After Claude reaches token budget limit during autonomous work:

1. **Checkpoint:** All progress saved to git (commit after each task)
2. **Schedule Resume:** Use `/schedule` skill to queue next phase
3. **Token Recharge:** Wait for token refresh (typically 1–5 minutes)
4. **Auto-Resume:** Scheduled agent wakes and continues from checkpoint

## Phase 1 Status (Complete)

| Task | Description | Status |
|------|-------------|--------|
| T1 | GPU diagnostic script + log | ✅ Complete |
| T2 | DKMS kernel module rebuild helper | ✅ Complete |
| T3 | Docker GPU health checks + compose update | ✅ Complete |
| T4 | T5 cascade tier + Anthropic API integration | ✅ Complete |
| T5 | Agent Anone /deanonymize + pii_mapping fix | ✅ Complete |
| T6 | Grafana dashboards (cascade, GPU) | ✅ Complete |
| T7 | Prometheus alert rules (8 alerts) | ✅ Complete |
| T8 | Autonomous health monitoring loop | ✅ Complete |
| T9 | Resume plan + Phase 2 script | ✅ Complete |
| T10 | Final verification + git tag | ✅ Complete |

## GPU Recovery Notes

Diagnostic confirms no NVIDIA GPU hardware in current environment.
**Resolution:** Proceed with CPU-only mode (`OLLAMA_CPU_ONLY=1`).
GPU deploy config is documented in `docker-compose.yml` (commented out, ready to enable).

## Phase 2 (Scheduled Resume): Validation & Testing

**Trigger:** Token limit reached or scheduled wake
**Resume Command:** `./scripts/resume_phase2.sh`

### Tasks:
1. Verify GPU diagnostic status (`docs/GPU_RECOVERY_LOG.md`)
2. Test T1→T5 cascade with test queries
3. Run one health monitor cycle; verify output
4. Attempt Grafana dashboard import (if services running)
5. Verify Prometheus is loading alert rules
6. Document final completion status

## Checkpoint Strategy

After each major milestone:
```bash
git add .
git commit -m "checkpoint: <phase> complete, ready for resume"
git push -u origin master
```

Uncommitted changes block autonomous resume — always commit first.

## Token Budget Estimates

| Task | Tokens |
|------|--------|
| GPU diagnostics | ~2k |
| T5 + Anone integration | ~4k |
| Grafana setup | ~2k |
| Health monitor | ~2k |
| Resume planning | ~1k |
| **Total Phase 1** | **~11k** |

## Phase 3 (Future): Production Hardening

- Kubernetes deployment manifests (Helm chart)
- TLS/mTLS for inter-service communication (cert-manager)
- Secrets management (HashiCorp Vault or Kubernetes Secrets)
- Automated PostgreSQL backups (pgdump + S3)
- Multi-region failover for T5 cloud tier
