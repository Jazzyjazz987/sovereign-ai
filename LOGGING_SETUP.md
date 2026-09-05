# T3 Logging & Debugging Setup

## Quick Start (Resume T3 Debugging)

```bash
cd /opt/claude/sovereign-ai

# 1. Start monitoring (captures logs + GPU metrics + API health)
./scripts/monitor_t3.sh

# 2. In another terminal, restart T3
docker compose restart vllm-t3

# 3. Monitor for 5 minutes, watch for:
#    - GPU memory spike (9-10GB = model loaded)
#    - "Listening" or "Started" in logs
#    - API response in health checks
#    - Any CUDA errors

# 4. Stop monitoring (Ctrl+C) after 5 min
# 5. Review logs in logs/ directory
```

## Log Files Generated

All logs are timestamped and saved to `/opt/claude/sovereign-ai/logs/`:

| Log File | Purpose | What to Check |
|----------|---------|---------------|
| `t3_startup_*.log` | Full vLLM initialization logs | "Listening", "Started", errors, timeouts |
| `gpu_metrics_*.log` | GPU VRAM/utilization over time | Memory plateau = model loaded |
| `api_health_*.log` | HTTP curl attempts to /v1/models | First successful response |
| `stack_startup_*.log` | Overall stack boot (if using startup script) | Service dependencies, timing |

## Debugging Checklist

### Is the model loading?
```bash
tail -f logs/gpu_metrics_*.log
# Look for: memory.used jumping from ~15 MiB to ~9500-9700 MiB
```

### Is the API server starting?
```bash
grep -i "listening\|started\|uvicorn" logs/t3_startup_*.log
# Should see: "Uvicorn running", "Application startup complete", or port binding message
```

### Any CUDA errors?
```bash
grep -i "cuda\|error\|failed\|ooom" logs/t3_startup_*.log
# If found, note exact error and GPU memory state
```

### API ever responds?
```bash
grep -i "200 ok\|data\|models" logs/api_health_*.log | head -5
# If empty, API never became ready
```

## Scripts Provided

### `monitor_t3.sh`
Starts real-time monitoring:
- **Docker logs stream** → captures vLLM output line-by-line
- **GPU metrics sampler** → every 5 sec, GPU memory + utilization
- **Health checker** → every 10 sec, attempts API request

Runs until Ctrl+C, saves all output to timestamped log files.

### `startup_with_logging.sh`
Starts entire stack with logging:
- Logs all pull/build/up actions
- Waits for T1/T2 (Ollama) to be ready
- Checks T3 status (may still be initializing)
- Lists what logs were created

## Expected Behavior (When Working)

### Healthy T3 Startup Timeline
```
t=0:00   → vLLM process starts, Uvicorn binds to 8001
t=0:05   → Model download from HuggingFace starts
t=0:30   → Model weights loaded into GPU (~9.7GB)
t=0:35   → "Application startup complete"
t=0:40   → First API request succeeds (GET /v1/models returns JSON)
```

### Healthy GPU Metrics
```
00:05 - 15 MiB (downloading)
00:30 - 9729 MiB (loaded)
00:40 - 9750 MiB (inference ready)
```

## If T3 Still Hangs

Check these issues (in order):

1. **Low GPU VRAM**
   - Model uses ~9.5 GB on 12GB card
   - Reduce `GPU_MEMORY: "0.35"` to `"0.25"` in docker-compose.yml
   - Rebuild: `docker compose build vllm-t3`

2. **Model download timeout**
   - Check network: `ping huggingface.co`
   - Verify HF_TOKEN set: `grep HF_TOKEN .env`
   - Try smaller model: Change `MODEL_NAME` to `"mistralai/Mistral-7B"`

3. **vLLM compilation deadlock**
   - Disable CUDAGraphs: Add `--disable-cudagraph` to Dockerfile CMD
   - Disable custom all-reduce: Add `--disable-custom-all-reduce`

4. **Port binding issue**
   - Check if port in use: `sudo lsof -i :8001`
   - Check Docker network: `docker network inspect sovereign-ai_sovereign-ai`

## Contact Information

For issues, attach:
1. Last 100 lines of `t3_startup_TIMESTAMP.log`
2. First 50 lines of `gpu_metrics_TIMESTAMP.log`
3. Output of: `docker compose ps`
4. Output of: `nvidia-smi`
