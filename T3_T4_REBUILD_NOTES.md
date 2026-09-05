# T3/T4 Rebuild for 16GB VRAM (2026-06-11)

## Configuration Changes

### T3 → DeepSeek-Coder 6.7B (Code-focused)
- **Model:** `deepseek-ai/deepseek-coder-6.7b-instruct`
- **Purpose:** Code completion, code analysis, file review, technical writing
- **VRAM:** ~6.7GB (40% of 16GB)
- **Port:** 8001
- **Strengths:** Specifically trained on code, excellent for programming tasks

### T4 → Qwen 7B Chat (Analysis-focused)
- **Model:** `Qwen/Qwen-7B-Chat`
- **Purpose:** Design analysis, architecture review, general reasoning, RGPD/legal
- **VRAM:** ~7GB (40% of 16GB)
- **Port:** 8002
- **Strengths:** Excellent reasoning, multilingual, good for analysis

### Total VRAM Budget
```
T1 (Ollama Mistral 7B):  ~3GB
T2 (Ollama Llama 8B):    ~3GB
T3 (DeepSeek 6.7B):      ~6.7GB
T4 (Qwen 7B):            ~7GB
─────────────────────────
Total:                   ~19.7GB (can coexist, may spill to system RAM)
Per-model allocation:    40% GPU (6.4GB each for T3/T4)
```

## Expected Startup Timeline

### T3 (DeepSeek-Coder 6.7B)
```
0:00 - Start, download model weights
0:15 - Model loaded (6-7GB GPU)
0:25 - Compilation complete, "Application startup complete"
0:30 - API ready, first response to /v1/models
```

### T4 (Qwen 7B)
```
0:00 - Start, download model weights
0:20 - Model loaded (7GB GPU)
0:30 - Compilation complete, "Application startup complete"
0:35 - API ready, first response to /v1/models
```

## Monitoring

Automatic monitoring running for 10 minutes:
- Logs: `/opt/claude/sovereign-ai/logs/t3_rebuild_*.log`
- Logs: `/opt/claude/sovereign-ai/logs/t4_rebuild_*.log`
- Logs: `/opt/claude/sovereign-ai/logs/gpu_rebuild_*.log` (GPU metrics every 3 sec)

Watch for:
1. **GPU memory spike** in gpu_rebuild_*.log (~6-7GB = model loaded)
2. **"Application startup complete"** in t3/t4_rebuild_*.log
3. **"✅ Ready"** messages in gpu_rebuild_*.log

## Usage Examples

### T3 (Code Analysis)
```bash
curl -X POST http://localhost:8001/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-coder-6.7b-instruct",
    "prompt": "def fibonacci(n):",
    "max_tokens": 200
  }'
```

### T4 (Design Analysis)
```bash
curl -X POST http://localhost:8002/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen-7B-Chat",
    "messages": [{"role": "user", "content": "Analyze this architecture..."}],
    "max_tokens": 500
  }'
```

## Complexity Threshold Updates

Update cascade_router.py keywords:

**T3 Keywords (Trigger 2.5+ complexity):**
- code, function, algorithm, debug, optimize
- powerpoint, design, architecture, pattern
- refactor, test, script, python, sql, rest, api

**T4 Keywords (Trigger 3.0+ complexity):**
- analyze, design, review, evaluate
- rgpd, legal, compliance, governance
- strategy, planning, documentation

## Next Steps

1. **Wait for monitoring to complete** (10 min)
2. **Check logs:** `ls -ltr /opt/claude/sovereign-ai/logs/`
3. **Test manually:**
   ```bash
   curl http://localhost:8001/v1/models | jq .
   curl http://localhost:8002/v1/models | jq .
   ```
4. **Update cascade_router.py** with new model keywords
5. **Test web UI** at http://localhost:8888

## Troubleshooting

### If T3/T4 still hang:
- Check GPU: `nvidia-smi` (should show 6-7GB per model)
- Check logs: `tail -50 logs/t3_rebuild_*.log`
- Reduce GPU_MEMORY: `0.40` → `0.35` in docker-compose.yml
- Check HF_TOKEN: `grep HF_TOKEN .env | wc -c` (should be > 100 chars)

### If models don't exist:
- DeepSeek: https://huggingface.co/deepseek-ai/deepseek-coder-6.7b-instruct
- Qwen: https://huggingface.co/Qwen/Qwen-7B-Chat

### If VRAM exceeded:
- Can run T1/T2 offline during T3/T4 inference
- Or reduce GPU_MEMORY to 0.30-0.35 per model
