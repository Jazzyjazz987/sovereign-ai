# Sovereign AI Stack - Python Client Usage

Your T1/T2 models are accessible via the `OllamaClient` class.

## Quick Start

```python
from api.ollama_client import OllamaClient

client = OllamaClient()

# Simple query
response = client.query("t1", "Explique RGPD")
print(response)
```

## API Reference

### Basic Query (Synchronous)

```python
response = client.query(
    model="t1",              # or "t2"
    prompt="Your question",
    system="Optional context"  # System message for context
)
```

**Models:**
- `"t1"` — Mistral 7B (Fast, 3-4s latency)
- `"t2"` — Llama2 7B (Deep analysis, 4-5s latency)

---

### Streaming Query (Real-time chunks)

```python
print("Response: ", end="", flush=True)
for chunk in client.query_stream("t1", "Explain AI"):
    print(chunk, end="", flush=True)
print()
```

Use streaming for:
- Long responses (better UX)
- Real-time chat interfaces
- Feedback during generation

---

### Batch Processing (Multiple queries)

```python
prompts = [
    "What is RGPD?",
    "Who controls sovereign AI?",
    "How does encryption work?"
]

results = client.batch_query("t1", prompts)
for prompt, result in zip(prompts, results):
    print(f"Q: {prompt}\nA: {result}\n")
```

---

## Real-World Examples

### 1. Government DSI Assistant

```python
from api.ollama_client import OllamaClient

client = OllamaClient()

# System context for government use
system = "You are a French government AI assistant for DSI (Direction du Système d'Information). Answer in French."

# Query about regulations
response = client.query(
    "t1",
    "Quels sont les défis RGPD pour un système d'information gouvernemental ?",
    system=system
)
print(response)
```

### 2. Code Generation Pipeline

```python
client = OllamaClient()

code_prompts = [
    "Écris une fonction Python pour valider un email",
    "Comment implémenter OAuth 2.0 en Python ?",
    "Montre un exemple de requête PostgreSQL sécurisée"
]

for prompt in code_prompts:
    print(f"\nPrompt: {prompt}")
    print("-" * 50)
    # Use T2 for deeper analysis
    result = client.query("t2", prompt)
    print(result)
```

### 3. Multi-Model Comparison

```python
client = OllamaClient()

test_prompt = "Explique l'IA souveraine"

print("T1 (Fast - Mistral):")
print(client.query("t1", test_prompt))
print("\n" + "="*60 + "\n")

print("T2 (Deep - Llama2):")
print(client.query("t2", test_prompt))
```

### 4. Chat Interface

```python
from api.ollama_client import OllamaClient

client = OllamaClient()
model = "t1"
history = []

while True:
    user_input = input("\n>>> ").strip()
    if user_input.lower() == "quit":
        break
    
    response = client.query(model, user_input)
    history.append((user_input, response))
    print(f"\nAssistant: {response}")
```

### 5. Streaming for Chat UI

```python
from api.ollama_client import OllamaClient

client = OllamaClient()

user_prompt = "What is sovereign AI?"
print("Assistant: ", end="", flush=True)

for chunk in client.query_stream("t1", user_prompt):
    print(chunk, end="", flush=True)

print("\n")
```

---

## Integration with Your App

### Flask Example

```python
from flask import Flask, request, jsonify
from api.ollama_client import OllamaClient

app = Flask(__name__)
client = OllamaClient()

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    model = data.get("model", "t1")
    prompt = data.get("prompt")
    
    try:
        response = client.query(model, prompt)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
```

**Usage:**
```bash
curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d '{"model":"t1","prompt":"Bonjour"}'
```

### FastAPI Example

```python
from fastapi import FastAPI
from pydantic import BaseModel
from api.ollama_client import OllamaClient

app = FastAPI()
client = OllamaClient()

class Query(BaseModel):
    model: str = "t1"
    prompt: str

@app.post("/query")
async def query_model(query: Query):
    response = client.query(query.model, query.prompt)
    return {"response": response}

# Run: uvicorn main:app --reload
```

---

## Model Selection Guide

| Use Case | Recommended | Reason |
|----------|-------------|--------|
| Quick responses, chat | T1 (Mistral) | Fast (3-4s), good French |
| Code generation | T2 (Llama2) | Detailed, logical thinking |
| Legal/RGPD analysis | T1 (Mistral) | Clear, structured responses |
| Complex reasoning | T2 (Llama2) | Deeper analysis |
| Real-time chat | T1 (Mistral) | Lower latency |
| Batch processing | T2 (Llama2) | Accuracy over speed |

---

## Performance Tips

1. **Reuse client instance:**
   ```python
   client = OllamaClient()  # Create once
   # Reuse for multiple queries
   ```

2. **Use streaming for long responses:**
   ```python
   # Don't: Wait for full response
   response = client.query("t1", long_prompt)
   
   # Do: Stream and display immediately
   for chunk in client.query_stream("t1", long_prompt):
       print(chunk, end="", flush=True)
   ```

3. **Batch similar queries:**
   ```python
   results = client.batch_query("t1", [q1, q2, q3])
   ```

4. **Monitor logs:**
   The client logs all queries with timing info.

---

## Error Handling

```python
from api.ollama_client import OllamaClient
import logging

logging.basicConfig(level=logging.INFO)

try:
    client = OllamaClient()
    response = client.query("t1", "test")
except ConnectionError:
    print("Cannot connect to Ollama server")
except Exception as e:
    print(f"Error: {e}")
```

---

## Next Steps

1. ✅ Client ready to use
2. 📦 Integrate into your app (Flask/FastAPI/Django)
3. 🔐 Add Agent Anone for PII detection before T5 (Claude)
4. 📊 Monitor via Grafana (port 3000)
