# Testing Guide: T1-T4 Cascade & Auto Routing

## Quick Test Commands

### 1. Test Direct Ollama Models (Port 11434)

**T1: Mistral 7B (Fast, Simple)**
```bash
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistral:7b",
    "prompt": "Bonjour, quel est ton rôle?",
    "stream": false
  }' | jq '.response'
```

**T2: Llama 2 7B (Code, Analysis)**
```bash
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama2:7b",
    "prompt": "Écris une fonction Python pour calculer Fibonacci",
    "stream": false
  }' | jq '.response'
```

**T3: Neural-Chat (Coding)**
```bash
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "neural-chat",
    "prompt": "def quicksort(arr):",
    "stream": false
  }' | jq '.response'
```

**T4: Dolphin-Mixtral (Design/Analysis)**
```bash
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "dolphin-mixtral",
    "prompt": "Analyse l'\''architecture microservices d'\''un système distribué",
    "stream": false
  }' | jq '.response'
```

---

## 2. Test Cascade Router (Port 8888)

First, update `cascade_router.py` to use Ollama instead of vLLM:

```python
# In cascade_router.py - change vLLM to Ollama
class OllamaClient:
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url
    
    def query(self, model, prompt, temperature=0.7):
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "temperature": temperature,
                "stream": False
            }
        )
        return response.json()["response"]
```

### Test Auto Routing (Automatic Complexity Detection)

**Simple Query → T1 (Mistral)**
```bash
curl -X POST http://localhost:8888/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Bonjour",
    "model": "auto"
  }' | jq '.'
```
Expected: Uses T1 (Mistral 7B), fast response

**Code Query → T2 (Llama)**
```bash
curl -X POST http://localhost:8888/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Écris une fonction pour trier un array en Python",
    "model": "auto"
  }' | jq '.'
```
Expected: Uses T2 (Llama 2 7B)

**Coding Query → T3 (Neural-Chat)**
```bash
curl -X POST http://localhost:8888/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "def fibonacci(n): return n if n < 2 else",
    "model": "auto"
  }' | jq '.'
```
Expected: Uses T3 (Neural-Chat)

**Complex Analysis → T4 (Dolphin)**
```bash
curl -X POST http://localhost:8888/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Analyse l'\''architecture d'\''un système distribué avec Kubernetes, RGPD, et haute disponibilité",
    "model": "auto"
  }' | jq '.'
```
Expected: Uses T4 (Dolphin-Mixtral)

---

### Force Specific Model

```bash
# Force T1
curl -X POST http://localhost:8888/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Complex architecture question", "model": "t1"}' | jq '.'

# Force T2
curl -X POST http://localhost:8888/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Complex architecture question", "model": "t2"}' | jq '.'

# Force T3
curl -X POST http://localhost:8888/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Complex architecture question", "model": "t3"}' | jq '.'

# Force T4
curl -X POST http://localhost:8888/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Complex architecture question", "model": "t4"}' | jq '.'
```

---

## 3. Test Web UI (Port 8888)

Open in browser:
```
http://localhost:8888
```

Features to test:
- [ ] Model selector dropdown (Auto, T1, T2, T3, T4)
- [ ] Submit query button
- [ ] Response streaming
- [ ] GPU metrics display (if implemented)
- [ ] Model name in response

---

## 4. Monitor GPU During Testing

**In separate terminal:**
```bash
watch -n 1 nvidia-smi
```

**What to observe:**
- **T1/T2 queries:** ~7-8GB memory used
- **T3 query:** ~10-11GB memory (Neural-Chat larger)
- **T4 query:** ~13GB memory (Dolphin-Mixtral, may spill to system RAM)
- **Model switching:** VRAM drops then rises as old model unloads, new loads

---

## 5. Test Suite Script

Save as `test_cascade.sh`:

```bash
#!/bin/bash

echo "=== Testing T1-T4 Cascade ==="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

test_model() {
    local model=$1
    local prompt=$2
    local description=$3
    
    echo -e "${BLUE}Testing ${model}: ${description}${NC}"
    curl -s -X POST http://localhost:11434/api/generate \
        -H "Content-Type: application/json" \
        -d "{\"model\": \"${model}\", \"prompt\": \"${prompt}\", \"stream\": false}" \
        | jq -r '.response' | head -3
    echo ""
}

# Run tests
test_model "mistral:7b" "Bonjour" "T1: Simple greeting"
test_model "llama2:7b" "Écris du code Python" "T2: Code generation"
test_model "neural-chat" "def fibonacci" "T3: Code completion"
test_model "dolphin-mixtral" "Architecture système" "T4: Complex analysis"

echo -e "${GREEN}✅ All models tested${NC}"
```

Run:
```bash
chmod +x test_cascade.sh
./test_cascade.sh
```

---

## 6. Verify Models Loaded

```bash
# Check all loaded models
curl -s http://localhost:11434/api/tags | jq '.models[] | {name, size}'

# Output should show:
# {
#   "name": "mistral:7b",
#   "size": 4372824384
# }
# {
#   "name": "llama2:7b",
#   "size": 3826793677
# }
# (neural-chat and dolphin-mixtral load on first request)
```

---

## 7. Test Streaming Responses

**Non-streaming (current):**
```bash
curl -X POST http://localhost:11434/api/generate \
  -d '{"model": "mistral:7b", "prompt": "Hello", "stream": false}'
```

**Streaming (real-time):**
```bash
curl -X POST http://localhost:11434/api/generate \
  -d '{"model": "mistral:7b", "prompt": "Hello", "stream": true}' \
  | jq -r '.response' 2>/dev/null
```

---

## 8. Performance Benchmarking

Test response times:

```bash
time_model() {
    local model=$1
    echo "Benchmarking ${model}..."
    time curl -s -X POST http://localhost:11434/api/generate \
        -d "{\"model\": \"${model}\", \"prompt\": \"Hello world\", \"stream\": false}" \
        > /dev/null
}

time_model "mistral:7b"    # Expected: ~2-3 sec
time_model "llama2:7b"     # Expected: ~2-3 sec
time_model "neural-chat"   # Expected: ~3-4 sec
time_model "dolphin-mixtral" # Expected: ~5-8 sec
```

---

## 9. Error Handling Tests

**Model doesn't exist:**
```bash
curl -X POST http://localhost:11434/api/generate \
  -d '{"model": "nonexistent", "prompt": "test"}' 2>&1 | head
# Should return error
```

**Ollama not running:**
```bash
curl http://localhost:11434/api/tags 2>&1
# Should fail with "Connection refused"
```

**VRAM full:**
- Load T3 or T4, then try to load another large model
- Ollama should auto-unload least-recent model
- Check with `nvidia-smi`

---

## 10. Cascade Router Logic Test

Add to `cascade_router.py`:

```python
# Test complexity detection
test_queries = [
    ("Bonjour", 1.0, "t1"),           # Simple → T1
    ("Écris du code", 2.0, "t2"),     # Code → T2
    ("def function():", 2.5, "t3"),   # Coding → T3
    ("Architecture RGPD système", 3.5, "t4"), # Complex → T4
]

for query, expected_complexity, expected_model in test_queries:
    complexity = calculate_complexity(query)
    model = route_query(query)
    status = "✅" if model == expected_model else "❌"
    print(f"{status} '{query}' → complexity={complexity}, model={model}")
```

---

## Summary of Test Endpoints

| Component | URL | Method | Purpose |
|-----------|-----|--------|---------|
| Ollama Direct | `http://localhost:11434` | REST | Raw model access |
| Cascade Router | `http://localhost:8888/query` | POST | Auto-routing |
| Web UI | `http://localhost:8888` | GET | Browser interface |
| Health Check | `http://localhost:11434/api/tags` | GET | Model status |
| Postgres | `localhost:5432` | TCP | State persistence |
| Grafana | `http://localhost:3000` | GET | Metrics/dashboards |

---

## Checklist for Full Testing

- [ ] T1 (Mistral) responds in <3 sec
- [ ] T2 (Llama) responds in <3 sec
- [ ] T3 (Neural-Chat) loads on first request
- [ ] T4 (Dolphin) loads on first request
- [ ] Auto-routing detects complexity correctly
- [ ] Forced model selection works (t1, t2, t3, t4)
- [ ] GPU memory stays <12GB (max allocation)
- [ ] Models auto-unload when VRAM full
- [ ] Web UI displays model selector
- [ ] Cascade router logs show correct model routing
- [ ] All models respond in French and English
- [ ] No telemetry or external calls detected

---

**When all checks pass:** System is production-ready! 🚀
