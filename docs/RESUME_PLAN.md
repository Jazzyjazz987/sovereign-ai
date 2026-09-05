# Token-Aware Autonomous Resume Plan

## Overview

This document describes the token-aware resumption strategy for the Sovereign AI Stack autonomous completion project. After Claude reaches token budget limit during autonomous work, the project automatically:

1. **Checkpoints progress** via git commits
2. **Schedules a resume** using autonomous agents
3. **Awaits token recharge** (typically 1 hour)
4. **Auto-resumes** with fresh context from last checkpoint

---

## How It Works

### The Resume Cycle

```
Session 1 (Initial)
├─ Work on Phase 1 tasks
├─ Commit progress to git
└─ [Token limit reached]
   ├─ Verify all commits clean
   └─ Schedule Phase 2 wake-up

[Token Recharge ~1 hour]

Session 2 (Resumed)
├─ Fresh agent boots
├─ Reads git history
├─ Continues from Phase 2 checkpoint
├─ Runs validation tasks
└─ Commits completion
```

**Key Invariant:** No uncommitted changes allowed. All work must be in git before session ends.

### Why This Works

1. **Git is the source of truth** — All progress persists across sessions
2. **Checkpoint commits are explicit** — Agent only resumes with clean state
3. **Token budget is respected** — New session starts fresh with full allocation
4. **Deterministic restart** — No manual intervention needed

---

## Implementation Strategy

### Phase 1 (Current/Completed): Setup & Integration

**Goal:** Deploy core infrastructure and autonomous monitoring

**Tasks:**
- ✅ GPU driver diagnostics script (`scripts/diagnose_gpu.sh`)
- ✅ DKMS kernel module rebuild helper (`scripts/rebuild_gpu_module.sh`)
- ✅ Docker Compose GPU health check (`scripts/check_docker_gpu.sh`)
- ✅ T5 cloud integration with Anthropic SDK
- ✅ Agent Anone PII anonymization proxy (endpoints: `/anonymize`, `/deanonymize`)
- ✅ LangGraph cascade router with complexity threshold
- ✅ Prometheus alert rules for GPU/cascade metrics
- ✅ Autonomous health monitor with self-recovery (`scripts/health_monitor_loop.sh`)
- ✅ All changes committed to git

**Estimated Tokens:** ~11k (diagnostics, API integration, monitoring setup, script creation)

**Success Criteria:**
- `git status` shows clean working tree
- `git log --oneline` shows 8+ commits from this session
- All `.sh` scripts in `/scripts/` are executable
- No uncommitted `.py` files in `/api/`

### Phase 2 (Scheduled Resume): Validation & Testing

**Trigger:** Token limit reached in Phase 1, automatic wake-up via scheduled agent

**Goals:**
1. Verify GPU recovery attempts
2. Validate T5 cascade routing
3. Test PII anonymization chain
4. Run health monitor for 1 full cycle
5. Upload Grafana dashboards

**Tasks:**
1. **GPU Recovery Validation**
   - Run: `scripts/diagnose_gpu.sh`
   - Check: Compare `docs/GPU_RECOVERY_LOG.md` against Phase 1 baseline
   - Expected: Either `nvidia-smi` success, or clear error message for manual intervention

2. **T5 Cascade Test**
   - Send query with `complexity=2.5` to `http://localhost:8888/query`
   - Expected: Response includes `model_used: "claude-sonnet"` or fallback to `mistral-22b`

3. **Anonymization Chain**
   - Test `/anonymize` endpoint with GDPR-sensitive text
   - Test `/deanonymize` endpoint with tokens
   - Expected: PII correctly masked → restored

4. **Health Monitor**
   - Run `scripts/health_monitor_loop.sh` for 1 cycle (2 min)
   - Check: Prometheus metrics ingested, alerts defined
   - Expected: No critical errors, disk space > 10%

5. **Grafana Dashboard Upload**
   - Import: `config/grafana_dashboard_cascade.json`
   - Import: `config/grafana_dashboard_gpu.json`
   - Verify: Both dashboards visible at `http://localhost:3000`

**Estimated Tokens:** ~8k (validation queries, monitoring, dashboard verification)

**Success Criteria:**
- All 5 tasks complete with documented results
- `docker compose ps` shows all services running
- Cascade router handles 3+ consecutive requests without error
- Git commits logged with results

### Phase 3 (Optional/Future): Production Hardening

**Goals:**
- Kubernetes deployment manifests
- mTLS inter-service communication
- Secrets management (Vault/AWS Secrets Manager)
- Automated PostgreSQL backups

**Estimated Tokens:** ~12k

**Status:** Defined but not required for MVP

---

## Checkpoint Strategy

### When to Commit

Commit after each **major milestone**:
- After Task 1 (GPU diagnostics) ✅
- After Task 3 (Docker GPU check) ✅
- After Task 5 (T5 integration) ✅
- After Task 7 (alert rules) ✅
- After Task 8 (health monitor) ✅
- After Task 9 (resume plan) ← **Current**
- After Task 10 (final verification)

### Commit Template

```bash
git add <files>
git commit -m "docs: <component> ready for autonomous continuation

Phase: <1|2|3>
Status: <in-progress|checkpoint|complete>
Next: <Phase X Task Y>
"
```

### Pre-Resume Checklist

Before starting Phase 2, ensure:

```bash
# 1. No uncommitted changes
git status --porcelain
# Expected output: (empty)

# 2. Recent commit history
git log --oneline -5
# Expected: 8+ commits from Phase 1

# 3. All scripts executable
ls -la scripts/*.sh | awk '{print $1}' | grep -c x
# Expected: count >= 6

# 4. Key files exist
test -f docs/RESUME_PLAN.md && echo "✓ RESUME_PLAN.md"
test -f docs/GPU_RECOVERY_LOG.md && echo "✓ GPU_RECOVERY_LOG.md"
test -f scripts/resume_phase2.sh && echo "✓ resume_phase2.sh"
test -f scripts/health_monitor_loop.sh && echo "✓ health_monitor_loop.sh"
```

---

## Token Budget Management

### Per-Task Estimates (tokens)

| Task | Phase | Tokens | Notes |
|------|-------|--------|-------|
| GPU diagnostics | 1 | 2k | Script + doc writing |
| DKMS rebuild | 1 | 1.5k | Module state checking |
| Docker GPU check | 1 | 1.5k | Compose modification + test |
| T5 integration | 1 | 4k | SDK setup + LangGraph cascade |
| Agent Anone | 1 | 2k | Endpoints + deanonymize logic |
| Grafana dashboards | 1 | 2k | JSON panel definitions |
| Alert rules | 1 | 1.5k | Prometheus YAML |
| Health monitor | 1 | 2k | Bash loop + self-recovery |
| Resume plan | 1 | 1k | This documentation |
| **Phase 1 Total** | **1** | **~18k** | Setup complete |
| | | | |
| GPU validation | 2 | 1k | Diagnostic comparison |
| Cascade testing | 2 | 2k | Query routing + latency |
| Anonymization chain | 2 | 2k | PII flow testing |
| Health monitor cycle | 2 | 1k | 1x run + metric check |
| Dashboard upload | 2 | 2k | Grafana import + verify |
| **Phase 2 Total** | **2** | **~8k** | Validation complete |

### Budget Allocation

- **Session 1:** 15k tokens available → ~18k estimated for Phase 1
  - *Note:* Actual usage likely 12-14k; documentation provides buffer for unforeseen needs
  - If Phase 1 completes early, commit checkpoint and schedule Phase 2
  
- **Session 2:** 20k tokens available → ~8k estimated for Phase 2
  - Remaining budget can extend Phase 3 or add additional testing

### Overflow Strategy

If Phase 1 exceeds 15k tokens:
1. Stop at the current task
2. Commit with message: `"checkpoint: Phase 1 partial, ready for Phase 2 resume"`
3. Do NOT try to squeeze more work in
4. Phase 2 agent will resume immediately

---

## Running the Resume

### From Phase 1 (End of Session 1)

When token limit approaches:

```bash
# 1. Commit current state
git status
git add .
git commit -m "checkpoint: Phase 1 complete, ready for Phase 2 resume"

# 2. Verify clean state
git status  # Should show "working tree clean"
git log --oneline -3  # Should show recent commits

# 3. Document status (for next agent)
echo "Phase 1 complete. All commits pushed. Ready for Phase 2." > PHASE_STATUS.txt
git add PHASE_STATUS.txt
git commit -m "docs: Phase 1 completion checkpoint"

# 4. Schedule Phase 2 (uses /schedule skill if available)
# Or just wait - scheduled agent will wake when tokens refresh
```

### From Phase 2 (Start of Session 2)

When Phase 2 agent starts:

```bash
# 1. Source the environment
cd /opt/claude/sovereign-ai

# 2. Run the resume script (see below)
bash scripts/resume_phase2.sh

# 3. Document results
git add docs/PHASE_2_RESULTS.md
git commit -m "phase-2: validation complete, all services healthy"
```

---

## Example: Phase 2 Resumption

See `scripts/resume_phase2.sh` for the full automation. Key steps:

1. **Verify git state** — Ensure no uncommitted changes
2. **Check GPU status** — Read `GPU_RECOVERY_LOG.md`, compare timestamps
3. **Test cascade** — Send complexity-2.5 query, verify T5 routing
4. **Run health monitor** — 1 full cycle (2 min), check alerts
5. **Validate dashboards** — Confirm Grafana imports successful
6. **Commit results** — All findings to git with timestamps

**Runtime:** ~15-20 min
**Success:** All 5 steps pass without manual intervention

---

## Autonomous Recovery Handlers

If Phase 2 detects failures:

| Failure | Handler | Resolution |
|---------|---------|-----------|
| nvidia-smi still broken | Log to GPU_RECOVERY_LOG.md | Manual driver reinstall required |
| T5 API unavailable | Fallback to T4 (Mistral Small) | Health monitor routes automatically |
| PII anonymization fails | Log error + sample | Debug Agent Anone endpoints |
| Prometheus alerts missing | Re-import alert rules | Re-run `docker compose up prometheus` |
| Disk space low | Alert in health monitor | Cleanup old logs, Docker images |

**Escalation:** If 3+ handlers trigger, Phase 2 agent documents and stops. Manual review required.

---

## Verification Checklist (Phase 1 → Phase 2 Handoff)

- [ ] All task commits present: `git log --oneline | wc -l` ≥ 10
- [ ] No uncommitted changes: `git status --porcelain` = empty
- [ ] GPU_RECOVERY_LOG.md created and dated
- [ ] All scripts executable: `test -x scripts/*.sh`
- [ ] resume_phase2.sh created and syntax valid
- [ ] RESUME_PLAN.md (this file) complete
- [ ] Docker Compose health: `docker compose ps | grep -c Up` ≥ 5
- [ ] T5 config wired: grep -q "claude-sonnet" api/main.py
- [ ] Agent Anone ready: test -f api/anone_api.py
- [ ] Prometheus alerts defined: test -f config/prometheus_alerts.yml
- [ ] Health monitor deployed: test -f scripts/health_monitor_loop.sh

All checks passing = **Phase 1 complete, Phase 2 ready to resume**

---

## Questions & Edge Cases

### Q: What if a commit fails?
**A:** Phase 1 will detect uncommitted changes and refuse to end. Fix the underlying issue (usually merge conflict or permission), then commit again.

### Q: What if Phase 2 agent doesn't start?
**A:** Manual trigger via `/schedule` command, or manually `bash scripts/resume_phase2.sh` after ensuring clean git state.

### Q: What if GPU still fails in Phase 2?
**A:** Log findings to GPU_RECOVERY_LOG.md. NVIDIA driver installation requires manual intervention (sudo, reboot). Document blocker and stop.

### Q: What if we want to skip Phase 2 and go to Phase 3?
**A:** Allowed if Phase 2 completes successfully. Phase 3 agent reads all Phase 1+2 commits and continues from there.

### Q: Can we run Phase 1 & Phase 2 in the same session?
**A:** Yes, if token budget permits (~26k total). But checkpoint explicitly between phases for clarity.

---

## References

- `docs/GPU_RECOVERY_LOG.md` — GPU diagnostic baseline
- `scripts/health_monitor_loop.sh` — Autonomous health checks
- `api/main.py` — LangGraph cascade with complexity routing
- `api/anone_api.py` — PII anonymization endpoints
- `config/prometheus_alerts.yml` — Alert rule definitions
- `docker-compose.yml` — Service orchestration
- `CLAUDE.md` — Project behavioral guidelines

---

**Last Updated:** 2026-09-04
**Version:** 1.0
**Author:** Sovereign AI Stack Phase 4 Task 9
**Status:** Ready for autonomous continuation
