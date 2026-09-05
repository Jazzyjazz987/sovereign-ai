# T3 vLLM Initialization Debug Report

## Issue Summary
T3 (vLLM service on port 8001) enters infinite wait loop during model initialization. Process binds to port but API requests get connection reset.

## Known Details

### Environment
- **GPU:** NVIDIA RTX 3080 Ti (12GB VRAM, not 24GB as originally specified)
- **vLLM Version:** 0.22.1
- **CUDA:** 12.1 (in container)
- **NVIDIA Driver:** 580.159.03

### T3 Configuration (Current)
```yaml
Model: mistralai/Mistral-7B-Instruct-v0.1
Port: 8001
GPU Memory: 0.35 (35% of 12GB = ~4.2GB)
Dtype: float16
Tensor Parallel Size: 1
```

### Symptoms
1. **Docker logs show:** Model architecture resolved, FlashAttention enabled, engine initializing
2. **GPU memory:** Stable at ~9.7 GB (model loaded)
3**API response:** Connection reset (port listening but no HTTP response)
4. **Process status:** vLLM process running (23-40% CPU) but not accepting requests
5. **Zombie processes:** Multiple defunct python3 processes in container

### Timeline of Attempts

#### Attempt 1: Qwen 1.5-14B-Chat-AWQ
- **Problem:** Model too large for RTX 3080 Ti (12GB total, Qwen needs ~10.8GB)
- **Result:** API never responds after 2+ minutes

#### Attempt 2: Mistral-7B-Instruct with `--enforce-eager`
- **Problem:** `--enforce-eager` flag causes deadlock in vLLM 0.22.1
- **Result:** Process stuck at FlashAttention initialization

#### Attempt 3: Mistral-7B-Instruct (current)
- **Flags:** Removed `--enforce-eager`, added `--tensor-parallel-size 1`
- **Status:** Model loads but API still not responding
- **Hypothesis:** vLLM compilation/optimization deadlock or port binding issue

## Debugging Strategy

### Run Monitoring Script
```bash
cd /opt/claude/sovereign-ai
chmod +x scripts/monitor_t3.sh
./scripts/monitor_t3.sh
```

This captures:
- **T3 Docker logs** → `/logs/t3_startup_TIMESTAMP.log`
- **GPU metrics** → `/logs/gpu_metrics_TIMESTAMP.log`
- **API health checks** → `/logs/api_health_TIMESTAMP.log`

### What to Look For
1. **"Listening on"** or **"Started server process"** in logs = API started
2. **GPU memory spike** = Model loaded successfully
3. **Connection reset vs timeout** = Port binding vs application crash
4. **Zombie process count** = Multiprocessing cleanup issue
5. **"CUDA error"** or **"OOM"** = Memory exhaustion

## Potential Fixes to Try

### Fix 1: Reduce GPU Memory Utilization
```yaml
# In docker-compose.yml
GPU_MEMORY: "0.25"  # Reduce from 0.35 to 0.25 (25%)
```

### Fix 2: Use Smaller Model
```yaml
MODEL_NAME: "mistralai/Mistral-7B"  # Without "-Instruct" suffix
```

### Fix 3: Increase vLLM Timeouts
```dockerfile
# In Dockerfile.vllm - add to CMD:
--enable-chunked-prefill \
--disable-custom-all-reduce
```

### Fix 4: Check for Port Binding Issues
```bash
# Verify port is actually listening
docker compose exec -T vllm-t3 netstat -tlnp | grep 8001
docker compose exec -T vllm-t3 lsof -i :8001
```

## Next Steps

1. **Start monitoring:** `./scripts/monitor_t3.sh`
2. **Stop and restart T3:** `docker compose restart vllm-t3`
3. **Let it run until ready or timeout (5 min)**
4. **Review logs in `/logs/` directory**
5. **Share findings from:**
   - Last 50 lines of `t3_startup_*.log`
   - `gpu_metrics_*.log` (look for memory plateau)
   - `api_health_*.log` (look for first successful response)

## References
- vLLM docs: https://docs.vllm.ai/en/latest/
- Issue similar to: vLLM #5000+ range (compilation/startup hangs)
