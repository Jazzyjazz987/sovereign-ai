#!/bin/bash
# Quick Test: T1, T2, T3, T4 Models
# Usage: ./scripts/quick_test.sh

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║          SOVEREIGN AI STACK - QUICK TEST                   ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# Check Ollama is running
echo -e "${BLUE}[1/5] Checking Ollama service...${NC}"
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo -e "${RED}❌ Ollama not responding${NC}"
    echo "Start with: docker compose up -d ollama"
    exit 1
fi
echo -e "${GREEN}✅ Ollama running${NC}"
echo ""

# Check available models
echo -e "${BLUE}[2/5] Available models:${NC}"
MODELS=$(curl -s http://localhost:11434/api/tags | jq -r '.models[].name' 2>/dev/null)
echo "$MODELS"
echo ""

# Test T1: Mistral
echo -e "${BLUE}[3/5] Testing T1 (Mistral 7B)...${NC}"
RESPONSE=$(curl -s -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model": "mistral:7b", "prompt": "Say hello in one word", "stream": false}' \
  | jq -r '.response // "ERROR"' 2>/dev/null)
if [[ "$RESPONSE" != "ERROR" && ${#RESPONSE} -gt 2 ]]; then
    echo -e "${GREEN}✅ T1 OK${NC}: ${RESPONSE:0:50}"
else
    echo -e "${RED}❌ T1 FAILED${NC}"
fi
echo ""

# Test T2: Llama
echo -e "${BLUE}[4/5] Testing T2 (Llama 2 7B)...${NC}"
RESPONSE=$(curl -s -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model": "llama2:7b", "prompt": "What is 2+2?", "stream": false}' \
  | jq -r '.response // "ERROR"' 2>/dev/null)
if [[ "$RESPONSE" != "ERROR" && ${#RESPONSE} -gt 2 ]]; then
    echo -e "${GREEN}✅ T2 OK${NC}: ${RESPONSE:0:50}"
else
    echo -e "${RED}❌ T2 FAILED${NC}"
fi
echo ""

# Check GPU status
echo -e "${BLUE}[5/5] GPU Status:${NC}"
GPU_USED=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader 2>/dev/null | awk '{print $1}')
GPU_TOTAL=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader 2>/dev/null | awk '{print $1}')
if [ -n "$GPU_USED" ] && [ -n "$GPU_TOTAL" ]; then
    PERCENT=$((GPU_USED * 100 / GPU_TOTAL))
    echo "VRAM: ${GPU_USED}MB / ${GPU_TOTAL}MB (${PERCENT}%)"
    if [ $PERCENT -lt 80 ]; then
        echo -e "${GREEN}✅ GPU healthy${NC}"
    else
        echo -e "${YELLOW}⚠️ GPU near capacity${NC}"
    fi
else
    echo -e "${YELLOW}⚠️ NVIDIA GPU info unavailable${NC}"
fi
echo ""

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  NEXT STEPS:                                               ║"
echo "║  • Test T3/T4: See TESTING_GUIDE.md                        ║"
echo "║  • View logs: docker compose logs -f ollama                ║"
echo "║  • Web UI: http://localhost:8888                           ║"
echo "║  • Monitor GPU: watch -n 1 nvidia-smi                      ║"
echo "╚════════════════════════════════════════════════════════════╝"
