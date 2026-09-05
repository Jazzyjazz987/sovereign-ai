# Sovereign AI Stack Autonomous Completion Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) to implement tasks in parallel. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Complete sovereign AI stack deployment: restore GPU acceleration, integrate T5 cloud fallback with PII anonymization, set up production monitoring, and establish autonomous health loops.

**Architecture:** 
1. **GPU Recovery (Phase 1):** Diagnose kernel module state, rebuild NVIDIA driver module, verify nvidia-smi.
2. **T5 Cloud Integration (Phase 2):** Extend LangGraph cascade with T5 tier (Anthropic API), wire Agent Anone PII anonymization proxy before cloud calls, add complexity routing threshold.
3. **Production Monitoring (Phase 3):** Build Grafana dashboards (model latency, GPU utilization, cascade decisions), define alerts, document SLOs.
4. **Autonomous Loops (Phase 4):** Deploy background health monitors, token-aware resume scheduling, autonomous recovery handlers.

**Tech Stack:** Docker, NVIDIA CUDA 12.x, Python 3.11, LangGraph, Anthropic SDK, Agent Anone (GLiNER), Prometheus, Grafana, PostgreSQL

---

## Phase 1: GPU Driver Recovery

### Task 1: Diagnose GPU/Kernel Module State

**Files:**
- Create: `scripts/diagnose_gpu.sh`
- Create: `docs/GPU_RECOVERY_LOG.md`

- [ ] **Step 1: Write GPU diagnostic script**

```bash
#!/bin/bash
# scripts/diagnose_gpu.sh
set -e

echo "=== GPU Diagnostic Report ===" > /tmp/gpu_diag.log
echo "Timestamp: $(date)" >> /tmp/gpu_diag.log
echo "" >> /tmp/gpu_diag.log

echo "1. Checking GPU hardware:" >> /tmp/gpu_diag.log
lspci | grep -i nvidia >> /tmp/gpu_diag.log || echo "No GPU detected" >> /tmp/gpu_diag.log

echo "" >> /tmp/gpu_diag.log
echo "2. NVIDIA drivers installed:" >> /tmp/gpu_diag.log
dpkg -l | grep nvidia-driver >> /tmp/gpu_diag.log || echo "No nvidia-driver packages" >> /tmp/gpu_diag.log

echo "" >> /tmp/gpu_diag.log
echo "3. Kernel modules (nvidia):" >> /tmp/gpu_diag.log
lsmod | grep nvidia >> /tmp/gpu_diag.log || echo "nvidia module not loaded" >> /tmp/gpu_diag.log

echo "" >> /tmp/gpu_diag.log
echo "4. nvidia-smi status:" >> /tmp/gpu_diag.log
nvidia-smi >> /tmp/gpu_diag.log 2>&1 || echo "nvidia-smi failed" >> /tmp/gpu_diag.log

echo "" >> /tmp/gpu_diag.log
echo "5. DKMS status (nvidia):" >> /tmp/gpu_diag.log
dkms status | grep nvidia >> /tmp/gpu_diag.log 2>&1 || echo "No DKMS status for nvidia" >> /tmp/gpu_diag.log

echo "" >> /tmp/gpu_diag.log
echo "6. Secure Boot status:" >> /tmp/gpu_diag.log
mokutil --sb-state >> /tmp/gpu_diag.log 2>&1 || echo "mokutil not available" >> /tmp/gpu_diag.log

cat /tmp/gpu_diag.log
cat /tmp/gpu_diag.log > docs/GPU_RECOVERY_LOG.md
```

- [ ] **Step 2: Make script executable and run it**

```bash
chmod +x scripts/diagnose_gpu.sh
./scripts/diagnose_gpu.sh
```

Expected output: Diagnostic log written to `docs/GPU_RECOVERY_LOG.md`

- [ ] **Step 3: Commit diagnostic**

```bash
git add scripts/diagnose_gpu.sh docs/GPU_RECOVERY_LOG.md
git commit -m "docs: add GPU diagnostic tooling and initial status"
```

---

### Task 2: Check DKMS Kernel Module Build Status

**Files:**
- Create: `scripts/rebuild_gpu_module.sh`

- [ ] **Step 1: Write DKMS rebuild script (non-destructive check first)**

```bash
#!/bin/bash
# scripts/rebuild_gpu_module.sh
# Non-interactive GPU module rebuild for NVIDIA driver

set -e

echo "=== NVIDIA DKMS Module Rebuild ==="

# Check current status
echo "1. Checking DKMS status..."
dkms status | grep nvidia || echo "No DKMS entry found"

# Check kernel version
KERNEL_VERSION=$(uname -r)
echo "2. Current kernel: $KERNEL_VERSION"

# Check if driver is installed
NVIDIA_DRIVER=$(dpkg -l | grep "nvidia-driver-" | grep -oP 'nvidia-driver-\K[0-9]+' | head -1)
if [ -z "$NVIDIA_DRIVER" ]; then
  echo "ERROR: No nvidia-driver package found"
  exit 1
fi
echo "3. Driver version: nvidia-driver-$NVIDIA_DRIVER"

# Try to rebuild module (requires sudo)
echo "4. Checking if rebuild is needed..."
if dkms status | grep -q "installed"; then
  echo "✓ DKMS module already built and installed"
  exit 0
else
  echo "⚠ DKMS module needs rebuild"
  echo "   Attempting rebuild (this requires sudo)..."
  echo "   Command: sudo dkms install -m nvidia -v $(dkms status | grep nvidia | grep -oP '\K[0-9.]+' | head -1) -k $KERNEL_VERSION"
  echo "   OR run: sudo dkms autoinstall"
  exit 2  # Exit code 2 = needs sudo intervention
fi
```

- [ ] **Step 2: Test script (check if rebuild needed)**

```bash
chmod +x scripts/rebuild_gpu_module.sh
./scripts/rebuild_gpu_module.sh
```

Expected: Exit code 0 (OK) or 2 (needs sudo) — capture output

- [ ] **Step 3: Commit**

```bash
git add scripts/rebuild_gpu_module.sh
git commit -m "scripts: add GPU kernel module rebuild helper"
```

---

### Task 3: Docker Compose GPU Health Check

**Files:**
- Modify: `docker-compose.yml` (restore GPU sections)
- Create: `scripts/check_docker_gpu.sh`

- [ ] **Step 1: Restore GPU support in docker-compose.yml (Ollama only, start with Ollama)**

Replace the Ollama section to re-enable GPU:

```yaml
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
      - ./scripts/ollama_init.sh:/docker-entrypoint.d/init.sh
    environment:
      - OLLAMA_NUM_PARALLEL=2
      - OLLAMA_MAX_LOADED_MODELS=2
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    networks:
      - sovereign-ai
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:11434/api/tags"]
      interval: 10s
      timeout: 5s
      retries: 5
```

- [ ] **Step 2: Write Docker GPU verification script**

```bash
#!/bin/bash
# scripts/check_docker_gpu.sh
# Check if Docker can access NVIDIA GPU

echo "=== Docker GPU Capability Check ==="

echo "1. NVIDIA Container Toolkit version:"
which nvidia-container-cli && nvidia-container-cli --version || echo "nvidia-container-cli not found"

echo ""
echo "2. Docker NVIDIA runtime:"
docker run --rm --gpus all ubuntu nvidia-smi 2>&1 | head -20 || echo "Docker GPU access failed"

echo ""
echo "3. Test container with GPU flag:"
docker run --rm --gpus=1 --entrypoint nvidia-smi ubuntu:latest || echo "Failed (GPU not available)"
```

- [ ] **Step 3: Make executable and test**

```bash
chmod +x scripts/check_docker_gpu.sh
./scripts/check_docker_gpu.sh
```

Expected: Shows `nvidia-smi` output OR error "GPU not available"

- [ ] **Step 4: Commit**

```bash
git add docker-compose.yml scripts/check_docker_gpu.sh
git commit -m "infra: restore GPU support for Ollama, add Docker GPU checks"
```

---

## Phase 2: T5 Cloud Fallback + Agent Anone Integration

### Task 4: Extend LangGraph Cascade Router with T5 Tier

**Files:**
- Modify: `api/main.py` (cascade_router function)
- Modify: `api/requirements.langgraph.txt` (add anthropic SDK)

- [ ] **Step 1: Add Anthropic SDK to requirements**

```txt
# api/requirements.langgraph.txt (append)
anthropic==0.39.0
```

- [ ] **Step 2: Read current main.py cascade router**

```bash
head -100 api/main.py  # See current cascade logic
```

Expected: Identify the `cascade_router` or `route_complexity` function

- [ ] **Step 3: Extend cascade router with T5 tier**

Add to `api/main.py` after the existing T1-T4 logic:

```python
import anthropic
import os

# Add to cascade_router function after T4 check:
async def cascade_router(query: str, complexity: float) -> dict:
    """Route query through T1→T2→T3→T4→T5 cascade"""
    
    # Existing T1-T4 logic...
    if complexity <= 1.2:
        model = "mistral:7b"  # T1
    elif complexity <= 2.4:
        model = "llama2:7b"    # T2
    elif complexity <= 3.4:
        model = "neural-chat:latest"  # T3
    elif complexity <= 4.5:
        model = "dolphin-mixtral"     # T4
    else:
        # T5: Cloud Anthropic (requires Agent Anone anonymization first)
        return await route_t5_with_anonymization(query)
    
    # Existing T1-T4 Ollama call
    # ...

async def route_t5_with_anonymization(query: str) -> dict:
    """Route to T5 (Claude Sonnet) via Agent Anone PII anonymization"""
    
    import requests
    
    # Step 1: Anonymize via Agent Anone
    anone_response = requests.post(
        "http://anone:8080/anonymize",
        json={"text": query},
        timeout=10
    )
    
    if anone_response.status_code != 200:
        return {"error": "PII anonymization failed", "status": "error"}
    
    anon_data = anone_response.json()
    anonymized_query = anon_data.get("anonymized_text", query)
    pii_mapping = anon_data.get("pii_mapping", {})
    
    # Step 2: Call T5 (Claude Sonnet) via Anthropic API
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": f"""You are a French-language AI assistant for the Polynésie française DSI.
Context: Government information system (RGPD-compliant, sovereign).
Query: {anonymized_query}
Respond in French. Be precise and official."""
                }
            ]
        )
        
        response_text = message.content[0].text
        
        # Step 3: De-anonymize response (restore PII from mapping)
        deanon_response = requests.post(
            "http://anone:8080/deanonymize",
            json={"text": response_text, "pii_mapping": pii_mapping},
            timeout=10
        )
        
        final_response = deanon_response.json().get("text", response_text)
        
        return {
            "status": "ok",
            "query": query,
            "response": final_response,
            "model_used": "claude-3-5-sonnet-20241022",
            "complexity": 5.0,
            "anonymized": True,
            "message": "Processed with T5 (Anthropic Claude) + Agent Anone"
        }
    except anthropic.APIError as e:
        return {"error": str(e), "status": "error", "model": "T5"}
```

- [ ] **Step 4: Test import (verify no syntax errors)**

```bash
cd /opt/claude/sovereign-ai/api
python3 -c "import anthropic; print('Anthropic SDK imported OK')"
```

- [ ] **Step 5: Commit**

```bash
git add api/main.py api/requirements.langgraph.txt
git commit -m "feat: add T5 cascade tier with Agent Anone anonymization"
```

---

### Task 5: Implement Agent Anone PII Anonymization Endpoint

**Files:**
- Modify: `api/anone_api.py` (add /deanonymize endpoint)
- Verify: `api/requirements.anone.txt` has `transformers` and `gliner`

- [ ] **Step 1: Check current Anone implementation**

```bash
head -50 api/anone_api.py  # Review existing /anonymize endpoint
```

- [ ] **Step 2: Add de-anonymization endpoint to anone_api.py**

```python
# Add to anone_api.py after existing /anonymize endpoint:

from fastapi import FastAPI, HTTPException
import json

app = FastAPI()

# Existing /anonymize endpoint...

@app.post("/deanonymize")
async def deanonymize(request: dict):
    """
    Reverse PII anonymization by restoring original values from mapping.
    
    Input: {
        "text": "Jean at jean@company.fr contacted us",
        "pii_mapping": {
            "PERSON-0": "Jean Dupont",
            "EMAIL-0": "jean.dupont@company.fr"
        }
    }
    
    Output: {
        "text": "Jean Dupont at jean.dupont@company.fr contacted us"
    }
    """
    try:
        text = request.get("text", "")
        mapping = request.get("pii_mapping", {})
        
        if not text or not mapping:
            return {"text": text, "status": "no_mapping"}
        
        # Simple token replacement: replace anonymized markers with originals
        result = text
        for anonymized_token, original_value in mapping.items():
            # Replace anonymized token (e.g., PERSON-0, EMAIL-0) with original
            result = result.replace(anonymized_token, original_value)
        
        return {"text": result, "status": "ok"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "anone"}
```

- [ ] **Step 3: Test endpoint locally (if running)**

```bash
# In one terminal (if Anone is running):
curl -X POST http://localhost:8080/deanonymize \
  -H "Content-Type: application/json" \
  -d '{
    "text": "PERSON-0 works at EMAIL-0",
    "pii_mapping": {"PERSON-0": "Jean Dupont", "EMAIL-0": "jean@example.com"}
  }' | jq .
```

Expected: `{"text": "Jean Dupont works at jean@example.com", "status": "ok"}`

- [ ] **Step 4: Commit**

```bash
git add api/anone_api.py
git commit -m "feat: add /deanonymize endpoint for PII restoration"
```

---

## Phase 3: Production Monitoring Setup

### Task 6: Build Grafana Dashboards

**Files:**
- Create: `config/grafana_dashboard_cascade.json`
- Create: `config/grafana_dashboard_gpu.json`
- Modify: `config/grafana_datasources.yml`

- [ ] **Step 1: Verify Prometheus datasource**

Ensure `config/grafana_datasources.yml` has:

```yaml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: true
```

- [ ] **Step 2: Create Cascade Metrics Dashboard**

Create `config/grafana_dashboard_cascade.json`:

```json
{
  "dashboard": {
    "title": "Sovereign AI Cascade (T1→T5)",
    "panels": [
      {
        "title": "Model Selection by Complexity",
        "targets": [
          {
            "expr": "rate(cascade_router_calls_total[5m])",
            "legendFormat": "{{model}}"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Average Response Time (ms)",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, cascade_response_time_seconds) * 1000",
            "legendFormat": "{{model}}"
          }
        ],
        "type": "graph"
      },
      {
        "title": "T5 API Error Rate",
        "targets": [
          {
            "expr": "rate(anthropic_api_errors_total[5m])",
            "legendFormat": "Error Type"
          }
        ],
        "type": "stat"
      },
      {
        "title": "PII Anonymization Success Rate",
        "targets": [
          {
            "expr": "rate(anone_success_total[5m]) / (rate(anone_attempts_total[5m]) + 0.001) * 100",
            "legendFormat": "Success %"
          }
        ],
        "type": "stat"
      }
    ]
  },
  "overwrite": true
}
```

- [ ] **Step 3: Create GPU Metrics Dashboard**

Create `config/grafana_dashboard_gpu.json`:

```json
{
  "dashboard": {
    "title": "GPU Utilization & VRAM",
    "panels": [
      {
        "title": "GPU Memory Usage (%)",
        "targets": [
          {
            "expr": "nvidia_smi_memory_used_percent",
            "legendFormat": "{{index}}"
          }
        ],
        "type": "graph"
      },
      {
        "title": "GPU Temperature (°C)",
        "targets": [
          {
            "expr": "nvidia_smi_temperature_gpu",
            "legendFormat": "GPU {{index}}"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Ollama Model Load Time (s)",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, ollama_model_load_duration_seconds)",
            "legendFormat": "{{model}}"
          }
        ],
        "type": "stat"
      }
    ]
  },
  "overwrite": true
}
```

- [ ] **Step 4: Import dashboards via curl**

```bash
# Import Cascade dashboard
curl -X POST http://localhost:3000/api/dashboards/db \
  -H "Content-Type: application/json" \
  -d @config/grafana_dashboard_cascade.json \
  -u admin:${GRAFANA_PASSWORD}

# Import GPU dashboard
curl -X POST http://localhost:3000/api/dashboards/db \
  -H "Content-Type: application/json" \
  -d @config/grafana_dashboard_gpu.json \
  -u admin:${GRAFANA_PASSWORD}
```

- [ ] **Step 5: Commit**

```bash
git add config/grafana_dashboard_*.json
git commit -m "ops: add production Grafana dashboards (cascade, GPU metrics)"
```

---

### Task 7: Define Prometheus Alert Rules

**Files:**
- Create: `config/prometheus_alerts.yml`
- Modify: `config/prometheus.yml` (add alert rules file)

- [ ] **Step 1: Create alert rules**

Create `config/prometheus_alerts.yml`:

```yaml
groups:
  - name: sovereign_ai_alerts
    interval: 30s
    rules:
      - alert: HighGPUMemoryUsage
        expr: nvidia_smi_memory_used_percent > 90
        for: 2m
        annotations:
          summary: "GPU memory usage > 90%"
          description: "GPU {{ $labels.index }} memory at {{ $value }}%"
      
      - alert: T5APIErrors
        expr: rate(anthropic_api_errors_total[5m]) > 0.1
        for: 1m
        annotations:
          summary: "T5 (Anthropic) API errors detected"
          description: "Error rate: {{ $value }} errors/sec"
      
      - alert: CascadeHighLatency
        expr: histogram_quantile(0.95, cascade_response_time_seconds) > 5
        for: 3m
        annotations:
          summary: "Cascade response latency > 5s (p95)"
          description: "{{ $value }}s latency detected"
      
      - alert: PostgreSQLDown
        expr: pg_up == 0
        for: 1m
        annotations:
          summary: "PostgreSQL database is down"
      
      - alert: OllamaHealthCheck
        expr: up{job="ollama"} == 0
        for: 2m
        annotations:
          summary: "Ollama service unhealthy"
```

- [ ] **Step 2: Update prometheus.yml to load alert rules**

Modify `config/prometheus.yml` — add after `scrape_configs:`:

```yaml
rule_files:
  - '/etc/prometheus/alerts.yml'

alerting:
  alertmanagers:
    - static_configs:
        - targets: []
```

- [ ] **Step 3: Copy alert rules into Prometheus config**

```bash
cp config/prometheus_alerts.yml config/prometheus_alerts.yml
# When rebuilding, this will be mounted in Docker
```

- [ ] **Step 4: Rebuild Prometheus container**

```bash
docker compose up -d prometheus --force-recreate
docker compose logs -f prometheus  # Verify alert rules loaded
```

Expected log output: "Loaded X rules"

- [ ] **Step 5: Commit**

```bash
git add config/prometheus_alerts.yml config/prometheus.yml
git commit -m "ops: define Prometheus alert rules for cascade and infrastructure"
```

---

## Phase 4: Autonomous Health Loops & Token-Aware Scheduling

### Task 8: Implement Autonomous Health Monitoring

**Files:**
- Create: `scripts/health_monitor_loop.sh`
- Create: `docs/AUTONOMOUS_MONITORING.md`

- [ ] **Step 1: Write health monitoring loop script**

```bash
#!/bin/bash
# scripts/health_monitor_loop.sh
# Autonomous health monitoring with autonomous recovery

set -e

HEALTH_LOG="logs/health_monitor_$(date +%Y%m%d_%H%M%S).log"
mkdir -p logs

echo "Starting autonomous health monitor..." >> $HEALTH_LOG
echo "Timestamp: $(date)" >> $HEALTH_LOG

monitor_loop() {
    while true; do
        echo "" >> $HEALTH_LOG
        echo "=== Health Check: $(date) ===" >> $HEALTH_LOG
        
        # Check each service
        echo "1. PostgreSQL:" >> $HEALTH_LOG
        docker exec sovereign-ai-postgres-1 pg_isready -U claude >> $HEALTH_LOG 2>&1 && \
            echo "✓ PostgreSQL OK" >> $HEALTH_LOG || echo "✗ PostgreSQL DOWN" >> $HEALTH_LOG
        
        echo "2. Ollama:" >> $HEALTH_LOG
        curl -s http://localhost:11434/api/tags | jq '.models | length' >> $HEALTH_LOG 2>&1 && \
            echo "✓ Ollama OK" >> $HEALTH_LOG || echo "✗ Ollama DOWN" >> $HEALTH_LOG
        
        echo "3. Prometheus:" >> $HEALTH_LOG
        curl -s http://localhost:9090/-/healthy >> $HEALTH_LOG 2>&1 && \
            echo "✓ Prometheus OK" >> $HEALTH_LOG || echo "✗ Prometheus DOWN" >> $HEALTH_LOG
        
        echo "4. LangGraph Cascade:" >> $HEALTH_LOG
        curl -s http://localhost:8888/health | jq '.status' >> $HEALTH_LOG 2>&1 && \
            echo "✓ LangGraph OK" >> $HEALTH_LOG || echo "✗ LangGraph DOWN" >> $HEALTH_LOG
        
        echo "5. T5 API Ready:" >> $HEALTH_LOG
        [ -n "$ANTHROPIC_API_KEY" ] && echo "✓ ANTHROPIC_API_KEY set" >> $HEALTH_LOG || \
            echo "✗ ANTHROPIC_API_KEY missing" >> $HEALTH_LOG
        
        # Autonomous recovery: restart unhealthy services
        if grep -q "DOWN" $HEALTH_LOG; then
            echo "" >> $HEALTH_LOG
            echo "⚠ Unhealthy services detected. Attempting recovery..." >> $HEALTH_LOG
            docker compose restart >> $HEALTH_LOG 2>&1
            sleep 10
        fi
        
        # Sleep 5 minutes before next check
        sleep 300
    done
}

monitor_loop
```

- [ ] **Step 2: Make executable**

```bash
chmod +x scripts/health_monitor_loop.sh
```

- [ ] **Step 3: Create monitoring documentation**

Create `docs/AUTONOMOUS_MONITORING.md`:

```markdown
# Autonomous Health Monitoring

## Overview
The sovereign AI stack includes autonomous health monitoring that:
- Checks all 7 services every 5 minutes
- Logs results to `logs/health_monitor_*.log`
- Automatically restarts unhealthy services
- No human intervention required

## Running the Monitor

### Option 1: Long-Running Process
\`\`\`bash
cd /opt/claude/sovereign-ai
./scripts/health_monitor_loop.sh &
\`\`\`

### Option 2: Background Daemon (with nohup)
\`\`\`bash
nohup ./scripts/health_monitor_loop.sh > logs/monitor.out 2>&1 &
\`\`\`

### Option 3: Kubernetes CronJob (future)
Deploy as a scheduled monitoring pod.

## Health Checks

| Service | Check | Timeout | Recovery |
|---------|-------|---------|----------|
| PostgreSQL | \`pg_isready\` | 5s | \`docker restart\` |
| Ollama | \`/api/tags\` | 10s | \`docker restart\` |
| Prometheus | \`/-/healthy\` | 5s | \`docker restart\` |
| LangGraph | \`/health\` | 10s | \`docker restart\` |
| Anthropic API | Env var check | - | Manual (API key) |

## Logs

Health logs are written to \`logs/health_monitor_YYYYMMDD_HHMMSS.log\`

Grep for failures:
\`\`\`bash
grep "DOWN" logs/health_monitor_*.log
\`\`\`

## SLO Targets
- Service availability: 99.5% (≤3.6 hours downtime/month)
- T1-T2 cascade: <500ms p95 latency
- T5 cloud fallback: <5s p95 (including anonymization)
- PII anonymization success: >99.9%
\`\`\`

- [ ] **Step 4: Commit**

```bash
git add scripts/health_monitor_loop.sh docs/AUTONOMOUS_MONITORING.md
git commit -m "ops: add autonomous health monitoring with self-recovery"
```

---

### Task 9: Document Resume Plan & Phase 2

**Files:**
- Create: `docs/RESUME_PLAN.md`
- Create: `scripts/resume_phase2.sh`

- [ ] **Step 1: Write resume plan documentation**

```markdown
# Token-Aware Autonomous Resume Plan

## How It Works

After Claude reaches token budget limit during autonomous work:

1. **Checkpoint:** Save all progress to git
2. **Schedule Resume:** Use \`/schedule\` skill to queue next phase
3. **Token Recharge:** Wait for token refresh
4. **Auto-Resume:** Scheduled agent wakes and continues from checkpoint

## Implementation

### Phase 1 (Current Session): Setup Complete
- ✅ GPU driver diagnostics script deployed
- ✅ T5 cascade tier + Agent Anone integration implemented
- ✅ Prometheus alert rules defined
- ✅ Autonomous health monitor deployed
- ✅ All changes committed to git

### Phase 2 (Scheduled Resume): Validation & Execution
**Trigger:** Token limit reached
**Command:** \`/schedule\` to spawn fresh agent
**Tasks:**
1. Verify GPU driver recovery attempts (check \`docs/GPU_RECOVERY_LOG.md\`)
2. Test T5 cascade with complex query
3. Run health monitor for 1 cycle, validate alerting
4. Upload dashboards to Grafana
5. Document completion status

**Duration:** ~45-60 min
**Effort:** Low (verification + light testing)

### Phase 3 (Optional): Production Hardening
- Kubernetes deployment manifests (future)
- TLS/mTLS for inter-service communication
- Secrets management (HashiCorp Vault or AWS Secrets Manager)
- Automated backups for PostgreSQL

## Checkpoint Strategy

After each major milestone, run:
\`\`\`bash
git status
git add .
git commit -m "checkpoint: <phase> complete, ready for resume"
\`\`\`

Uncommitted changes block autonomous resume.

## Token Budget Management

**Per-task estimate:**
- GPU diagnostics: 2k tokens
- T5 + Anone: 4k tokens
- Grafana setup: 2k tokens
- Health monitor: 2k tokens
- Resume planning: 1k tokens

**Total Phase 1:** ~11k tokens

**Available for Phase 2:** Remaining budget after token recharge
\`\`\`

- [ ] **Step 2: Create Resume Script Template**

Create `scripts/resume_phase2.sh`:

```bash
#!/bin/bash
# scripts/resume_phase2.sh
# Resume sovereign AI project after token recharge
# Run this when resuming from /schedule wakeup

echo "=== Sovereign AI Stack - Phase 2 Resumption ==="
echo "Timestamp: $(date)"
echo ""

# Verify git state (no uncommitted changes)
if [ -n "$(git status --porcelain)" ]; then
    echo "ERROR: Uncommitted changes found. Commit before resume."
    git status
    exit 1
fi

echo "✓ Git state clean"
echo ""

# Phase 2: Validation
echo "=== Phase 2: Validation & Testing ==="

# 1. Check GPU recovery status
echo "1. Checking GPU recovery status..."
if [ -f "docs/GPU_RECOVERY_LOG.md" ]; then
    echo "   GPU Diagnostic log exists:"
    tail -5 docs/GPU_RECOVERY_LOG.md
else
    echo "   ⚠ GPU diagnostic not run yet"
fi

# 2. Test cascade
echo ""
echo "2. Testing T1→T5 cascade..."
curl -X POST http://localhost:8888/query \
  -H "Content-Type: application/json" \
  -d '{"query":"Bonjour, test de relance après token recharge","complexity":1.5}' | jq '.model_used'

# 3. Run health monitor once
echo ""
echo "3. Running health check cycle..."
./scripts/health_monitor_loop.sh | head -30

echo ""
echo "=== Phase 2 Resumption Complete ==="
echo "Next: Run 'git log --oneline -10' to verify all commits"
```

- [ ] **Step 3: Commit resume plan**

```bash
git add docs/RESUME_PLAN.md scripts/resume_phase2.sh
git commit -m "docs: add token-aware resume plan for autonomous continuation"
```

---

### Task 10: Final Verification & Checkpoint

**Files:**
- None (verification only)

- [ ] **Step 1: Verify all commits are clean**

```bash
git log --oneline -10  # Should show 10 recent commits from this session
git status  # Should show "working tree clean"
```

- [ ] **Step 2: Create project completion checkpoint**

```bash
git tag -a "phase-1-complete" -m "GPU recovery, T5 integration, monitoring setup, autonomous loops"
git log --graph --oneline --all | head -20
```

- [ ] **Step 3: Document autonomous project handoff**

Add to `README.md`:

```markdown
## Autonomous Continuation

This project is designed for autonomous execution via subagents.

### Current Status
- **Phase 1 (Complete):** GPU diagnostics, T5 cloud integration, health monitoring
- **Phase 2 (Scheduled):** Validation, testing, Grafana dashboard upload
- **Phase 3 (Future):** Production hardening, Kubernetes deployment

### Resuming Work
\`\`\`bash
./scripts/resume_phase2.sh  # Pick up from Phase 2
\`\`\`

### Health Monitoring (Always On)
\`\`\`bash
./scripts/health_monitor_loop.sh &
\`\`\`
```

- [ ] **Step 4: Final commit**

```bash
git add README.md
git commit -m "docs: add autonomous project handoff documentation"
git log --oneline -5  # Verify final commit
```

---

## Plan Summary

✅ **10 Tasks across 4 Phases**
✅ **GPU Recovery** → T5 Integration → Monitoring → Autonomous Loops
✅ **All tasks have exact code, commands, expected outputs**
✅ **Checkpoints at each phase for token-aware resume**
