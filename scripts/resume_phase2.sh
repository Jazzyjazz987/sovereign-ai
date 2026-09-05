#!/bin/bash
# scripts/resume_phase2.sh
# Resume sovereign AI project after token recharge
# Run this when resuming from /schedule wakeup

set -euo pipefail

echo "=== Sovereign AI Stack - Phase 2 Resumption ==="
echo "Timestamp: $(date)"
echo ""

# 1. Verify git state
if [ -n "$(git status --porcelain)" ]; then
    echo "ERROR: Uncommitted changes found. Commit before resume."
    git status
    exit 1
fi
echo "✓ Git state clean"
echo ""

# 2. Show recent commits
echo "=== Recent Commits ==="
git log --oneline -10
echo ""

# 3. Check GPU recovery status
echo "=== GPU Recovery Status ==="
if [ -f "docs/GPU_RECOVERY_LOG.md" ]; then
    echo "GPU Diagnostic log (last 10 lines):"
    tail -10 docs/GPU_RECOVERY_LOG.md
else
    echo "⚠ GPU diagnostic not run yet — run: ./scripts/diagnose_gpu.sh"
fi
echo ""

# 4. Test T1 cascade
echo "=== T1 Cascade Test ==="
T1_RESULT=$(curl -sf -X POST http://localhost:8888/query \
  -H "Content-Type: application/json" \
  -d '{"query":"Bonjour, quel est ton rôle ?","model":"t1"}' 2>/dev/null || echo '{"error":"service not running"}')
echo "T1 Response: $T1_RESULT" | python3 -c "import sys,json; d=json.load(open('/dev/stdin').read() if False else sys.stdin); print('Model:', d.get('model_used','N/A')); print('Status:', d.get('status','N/A'))" 2>/dev/null || echo "$T1_RESULT"
echo ""

# 5. Test T5 cascade (complex query)
echo "=== T5 Cascade Test (complex RGPD query) ==="
T5_RESULT=$(curl -sf -X POST http://localhost:8888/query \
  -H "Content-Type: application/json" \
  -d '{"query":"Jean Dupont demande des clarifications légales sur la CNIL et la RGPD pour le système dinformation gouvernemental","model":"auto"}' 2>/dev/null || echo '{"error":"service not running"}')
echo "$T5_RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print('Model:', d.get('model_used','N/A')); print('Anonymized:', d.get('anonymized',False)); print('Status:', d.get('status','N/A'))" 2>/dev/null || echo "$T5_RESULT"
echo ""

# 6. Test Agent Anone
echo "=== Agent Anone PII Test ==="
ANONE_RESULT=$(curl -sf -X POST http://localhost:8080/anonymize \
  -H "Content-Type: application/json" \
  -d '{"text":"Jean Dupont travaille au 0612345678"}' 2>/dev/null || echo '{"error":"service not running"}')
echo "Anone Response: $ANONE_RESULT"

DEANON_RESULT=$(curl -sf -X POST http://localhost:8080/deanonymize \
  -H "Content-Type: application/json" \
  -d '{"text":"PERSON-0 works at EMAIL-0","pii_mapping":{"PERSON-0":"Jean Dupont","EMAIL-0":"jean@example.com"}}' 2>/dev/null || echo '{"error":"service not running"}')
echo "De-anon Response: $DEANON_RESULT"
echo ""

# 7. Run one health check cycle
echo "=== Service Health Check ==="
for service in "http://localhost:11434/api/tags" "http://localhost:8888/health" "http://localhost:8080/health" "http://localhost:9090/-/healthy"; do
    status=$(curl -sf "$service" &>/dev/null && echo "✓ UP" || echo "✗ DOWN")
    echo "  $service → $status"
done
echo ""

echo "=== Phase 2 Resumption Complete ==="
echo "All checks done. Review above for any failures."
echo "Next: Review docs/RESUME_PLAN.md for Phase 3 tasks"
