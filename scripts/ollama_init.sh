#!/bin/bash
# Ollama Model Initialization - Load T1-T4 Models on Startup

set -e

echo "=== Ollama Model Initialization ==="

# Wait for Ollama to be ready
echo "Waiting for Ollama to be ready..."
for i in {1..30}; do
  if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✅ Ollama ready"
    break
  fi
  echo "  Attempt $i/30..."
  sleep 2
done

# Load models (non-blocking, will load on-demand if not present)
echo "Loading models..."

# T1: Mistral 7B (fast, general purpose)
echo "[T1] Pulling mistral:7b..."
ollama pull mistral:7b 2>&1 | tail -1 &
T1_PID=$!

# T2: Llama 2 8B (analysis, RGPD)
echo "[T2] Pulling llama2:7b..."
ollama pull llama2:7b 2>&1 | tail -1 &
T2_PID=$!

# T3: Neural Chat (coding)
echo "[T3] Pulling neural-chat..."
ollama pull neural-chat 2>&1 | tail -1 &
T3_PID=$!

# T4: Dolphin (analysis/design)
echo "[T4] Pulling dolphin-mixtral..."
ollama pull dolphin-mixtral 2>&1 | tail -1 &
T4_PID=$!

# Wait for all to complete
wait $T1_PID $T2_PID $T3_PID $T4_PID 2>/dev/null || true

echo "✅ Model initialization complete"
echo "Available models:"
curl -s http://localhost:11434/api/tags | jq '.models[].name' 2>/dev/null | head -10

exit 0
