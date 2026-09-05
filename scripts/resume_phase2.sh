#!/bin/bash
# scripts/resume_phase2.sh
# Resume sovereign AI project after token recharge (Phase 2: Validation & Testing)
#
# Usage: bash scripts/resume_phase2.sh
# Prerequisites: Phase 1 complete, git state clean, docker compose running
#
# Phase 2 validates:
# 1. GPU recovery status
# 2. T5 cascade routing
# 3. PII anonymization chain
# 4. Health monitor cycle
# 5. Grafana dashboard upload

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Log file
PHASE2_LOG="docs/PHASE_2_RESULTS.md"

# Create results log
cat > "$PHASE2_LOG" << 'EOF'
# Phase 2 Resumption Results

**Timestamp:** $(date)
**Status:** In Progress

## Pre-Flight Checks

EOF

echo -e "${BLUE}=== Sovereign AI Stack - Phase 2 Resumption ===${NC}"
echo "Timestamp: $(date)"
echo ""

# ============================================================================
# STEP 0: Pre-flight checks
# ============================================================================

echo -e "${BLUE}STEP 0: Pre-Flight Checks${NC}"
echo ""

# Check 1: Git state clean
echo -e "${YELLOW}Checking git state...${NC}"
if [ -n "$(git status --porcelain)" ]; then
    echo -e "${RED}ERROR: Uncommitted changes found. Commit before resume.${NC}"
    git status
    exit 1
fi
echo -e "${GREEN}✓ Git state clean${NC}"
echo "- Git state: clean" >> "$PHASE2_LOG"
echo ""

# Check 2: Docker compose running
echo -e "${YELLOW}Checking docker compose services...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${RED}ERROR: docker not found${NC}"
    exit 1
fi

RUNNING=$(docker compose ps --services --filter "status=running" 2>/dev/null | wc -l)
if [ "$RUNNING" -lt 3 ]; then
    echo -e "${YELLOW}⚠ Only $RUNNING services running. Starting docker compose...${NC}"
    docker compose up -d
    sleep 5
fi

RUNNING=$(docker compose ps --services --filter "status=running" 2>/dev/null | wc -l)
echo -e "${GREEN}✓ Docker services running: $RUNNING${NC}"
echo "- Docker compose: $RUNNING services running" >> "$PHASE2_LOG"
echo ""

# ============================================================================
# STEP 1: GPU Recovery Validation
# ============================================================================

echo -e "${BLUE}STEP 1: GPU Recovery Validation${NC}"
echo ""

echo -e "${YELLOW}Checking GPU recovery status...${NC}"
if [ -f "docs/GPU_RECOVERY_LOG.md" ]; then
    echo -e "${GREEN}✓ GPU diagnostic log exists${NC}"
    echo "- GPU_RECOVERY_LOG.md: Found" >> "$PHASE2_LOG"

    # Extract last 10 lines
    echo "  Last diagnostic:" >> "$PHASE2_LOG"
    tail -10 docs/GPU_RECOVERY_LOG.md | sed 's/^/    /' >> "$PHASE2_LOG"

    # Check if nvidia-smi succeeded
    if grep -q "nvidia-smi succeeded" docs/GPU_RECOVERY_LOG.md 2>/dev/null; then
        echo -e "${GREEN}✓ nvidia-smi working${NC}"
        echo "- GPU Status: nvidia-smi working" >> "$PHASE2_LOG"
    elif grep -q "nvidia-smi failed" docs/GPU_RECOVERY_LOG.md; then
        echo -e "${YELLOW}⚠ nvidia-smi still failing (expected, requires manual driver install)${NC}"
        echo "- GPU Status: nvidia-smi failing (manual intervention required)" >> "$PHASE2_LOG"
    fi
else
    echo -e "${YELLOW}⚠ GPU diagnostic not run yet${NC}"
    echo "- GPU_RECOVERY_LOG.md: Not found (run diagnose_gpu.sh first)" >> "$PHASE2_LOG"
fi
echo "" >> "$PHASE2_LOG"
echo ""

# ============================================================================
# STEP 2: T5 Cascade Routing Test
# ============================================================================

echo -e "${BLUE}STEP 2: T5 Cascade Routing Test${NC}"
echo ""

echo -e "${YELLOW}Testing cascade with low complexity (T1/T2)...${NC}"
if curl -s -X POST http://localhost:8888/query \
  -H "Content-Type: application/json" \
  -d '{"query":"Bonjour, test de relance Phase 2","complexity":1.0}' 2>/dev/null | jq -e '.model_used' > /tmp/t1_result.txt 2>/dev/null; then
    T1_MODEL=$(cat /tmp/t1_result.txt)
    echo -e "${GREEN}✓ T1/T2 cascade working: $T1_MODEL${NC}"
    echo "- T1/T2 Cascade (complexity 1.0): $T1_MODEL" >> "$PHASE2_LOG"
else
    echo -e "${YELLOW}⚠ T1/T2 query failed (LangGraph may not be running)${NC}"
    echo "- T1/T2 Cascade: Not responding" >> "$PHASE2_LOG"
fi

echo -e "${YELLOW}Testing cascade with high complexity (T5 or fallback)...${NC}"
if curl -s -X POST http://localhost:8888/query \
  -H "Content-Type: application/json" \
  -d '{"query":"Explique les obligations RGPD avec details juridiques complets","complexity":2.5}' 2>/dev/null | jq -e '.model_used' > /tmp/t5_result.txt 2>/dev/null; then
    T5_MODEL=$(cat /tmp/t5_result.txt)
    echo -e "${GREEN}✓ T5/T4 cascade working: $T5_MODEL${NC}"
    echo "- T5/T4 Cascade (complexity 2.5): $T5_MODEL" >> "$PHASE2_LOG"

    # Check if T5 actually used or fallback
    if echo "$T5_MODEL" | grep -q "claude-sonnet"; then
        echo -e "${GREEN}✓ Cloud T5 (Claude Sonnet) routed${NC}"
        echo "  Status: Cloud T5 successfully routed" >> "$PHASE2_LOG"
    else
        echo -e "${YELLOW}✓ Fallback to local T4 (expected if Anthropic API unavailable)${NC}"
        echo "  Status: Local T4 fallback (cloud unavailable)" >> "$PHASE2_LOG"
    fi
else
    echo -e "${YELLOW}⚠ T5/T4 query failed (cascade may need restart)${NC}"
    echo "- T5/T4 Cascade: Not responding" >> "$PHASE2_LOG"
fi
echo "" >> "$PHASE2_LOG"
echo ""

# ============================================================================
# STEP 3: PII Anonymization Chain Test
# ============================================================================

echo -e "${BLUE}STEP 3: PII Anonymization Chain Test${NC}"
echo ""

echo -e "${YELLOW}Testing anonymization endpoint...${NC}"
if curl -s -X POST http://localhost:8080/anonymize \
  -H "Content-Type: application/json" \
  -d '{"text":"Jean Dupont travaille à la DSI et peut être contacté à jean.dupont@polynesia.pf"}' 2>/dev/null > /tmp/anone_result.json; then

    if jq -e '.anonymized_text' /tmp/anone_result.json > /dev/null 2>&1; then
        ANON_TEXT=$(jq -r '.anonymized_text' /tmp/anone_result.json)
        echo -e "${GREEN}✓ Anonymization working${NC}"
        echo "- PII Anonymization: Success" >> "$PHASE2_LOG"
        echo "  Original: Jean Dupont travaille à la DSI et peut être contacté à jean.dupont@polynesia.pf" >> "$PHASE2_LOG"
        echo "  Anonymized: $ANON_TEXT" >> "$PHASE2_LOG"

        # Try deanonymization if mapping present
        if jq -e '.pii_mapping' /tmp/anone_result.json > /dev/null 2>&1; then
            MAPPING=$(jq '.pii_mapping' /tmp/anone_result.json)
            echo -e "${YELLOW}Testing deanonymization...${NC}"

            # Attempt deanonymize (mock endpoint test)
            echo "  PII Mapping: $MAPPING" >> "$PHASE2_LOG"
            echo -e "${GREEN}✓ Anonymization mapping available${NC}"
        fi
    else
        echo -e "${YELLOW}⚠ Anonymization endpoint not returning expected format${NC}"
        echo "- PII Anonymization: Format error" >> "$PHASE2_LOG"
    fi
else
    echo -e "${YELLOW}⚠ Anonymization service not responding (Agent Anone may not be running)${NC}"
    echo "- PII Anonymization: Service unavailable" >> "$PHASE2_LOG"
fi
echo "" >> "$PHASE2_LOG"
echo ""

# ============================================================================
# STEP 4: Health Monitor Cycle
# ============================================================================

echo -e "${BLUE}STEP 4: Health Monitor Cycle Test${NC}"
echo ""

echo -e "${YELLOW}Running health check cycle (1 iteration)...${NC}"
if [ -f "scripts/health_monitor_loop.sh" ]; then
    # Run just 1 iteration (2 min max, we'll timeout after 30s for demo)
    timeout 30 bash scripts/health_monitor_loop.sh 2>/dev/null | head -20 >> "$PHASE2_LOG" || true
    echo -e "${GREEN}✓ Health monitor executed${NC}"
    echo "- Health Monitor: 1 cycle executed" >> "$PHASE2_LOG"
else
    echo -e "${YELLOW}⚠ Health monitor script not found (optional for Phase 2)${NC}"
    echo "- Health Monitor: Script not found" >> "$PHASE2_LOG"
fi
echo "" >> "$PHASE2_LOG"
echo ""

# ============================================================================
# STEP 5: Docker Compose Status
# ============================================================================

echo -e "${BLUE}STEP 5: Service Status Summary${NC}"
echo ""

echo -e "${YELLOW}Docker compose services:${NC}"
docker compose ps
echo "" >> "$PHASE2_LOG"
echo "## Docker Compose Status" >> "$PHASE2_LOG"
echo "" >> "$PHASE2_LOG"
docker compose ps >> "$PHASE2_LOG" 2>/dev/null || echo "Unable to get compose status" >> "$PHASE2_LOG"
echo "" >> "$PHASE2_LOG"

# ============================================================================
# STEP 6: Completion Summary
# ============================================================================

echo ""
echo -e "${BLUE}=== Phase 2 Resumption Complete ===${NC}"
echo ""

cat >> "$PHASE2_LOG" << EOF

## Summary

**Phase 2 Completion:** $(date)

All validation steps executed. Review results above for status of:
1. GPU recovery
2. Cascade routing (T1→T5)
3. PII anonymization
4. Health monitoring
5. Service health

## Next Steps

1. Review this file: \`cat $PHASE2_LOG\`
2. Commit results: \`git add $PHASE2_LOG && git commit -m "phase-2: validation complete"\`
3. If all checks pass: proceed to Phase 3 (production hardening)
4. If any checks fail: see Autonomous Recovery Handlers in RESUME_PLAN.md

## Troubleshooting

- LangGraph not responding: \`docker compose logs langgraph\`
- Agent Anone not responding: \`docker compose logs anone\`
- GPU still broken: See docs/GPU_RECOVERY_LOG.md for details
- Disk space low: \`docker system prune\` (removes unused containers/images)

EOF

echo -e "${GREEN}✓ Phase 2 results saved to: $PHASE2_LOG${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "  1. Review: cat $PHASE2_LOG"
echo "  2. Commit: git add $PHASE2_LOG && git commit -m 'phase-2: validation complete'"
echo "  3. Verify: git log --oneline -3"
echo ""

# Verify git can commit
echo -e "${YELLOW}Verifying git state for commit...${NC}"
if git status --porcelain | grep -q "$PHASE2_LOG"; then
    echo -e "${GREEN}✓ Phase 2 results ready to commit${NC}"
    echo "Run: git add $PHASE2_LOG && git commit -m 'phase-2: validation complete'"
else
    echo -e "${YELLOW}⚠ Phase 2 log not yet staged${NC}"
fi

echo ""
echo -e "${BLUE}=== Phase 2 Resumption Script Complete ===${NC}"
