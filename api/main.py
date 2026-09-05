"""
LangGraph Orchestrateur Cascade T1→T4
Port 8888 - API + Web UI
"""
import os
import httpx
import asyncio
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import re

app = FastAPI(title="Sovereign AI Cascade Router", version="1.0")

# Configuration
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")
litellm_api_key = os.getenv("LITELLM_API_KEY")

# Pydantic models
class QueryRequest(BaseModel):
    query: str
    model: str = "auto"

# Cascade Router Logic
class CascadeRouter:
    def __init__(self):
        self.simple_keywords = {
            "bonjour", "hello", "hi", "salut", "ça va",
            "qui es tu", "who are you", "quoi", "what"
        }
        self.code_keywords = {
            "code", "function", "def", "class", "python", "javascript",
            "écris", "write", "implement", "debug", "error", "bug",
            "sql", "api", "rest", "endpoint", "test"
        }
        self.advanced_keywords = {
            "architecture", "design", "pattern", "microservices",
            "kubernetes", "docker", "ansible", "terraform",
            "rgpd", "compliance", "governance", "security", "analyse",
            "strategy", "plan", "evaluate"
        }

    def calculate_complexity(self, query: str) -> float:
        """Calculate query complexity (1.0 - 4.0)"""
        query_lower = query.lower()
        word_count = len(query.split())

        # Base complexity
        complexity = 1.0

        # Keyword matching
        simple_matches = sum(1 for kw in self.simple_keywords if kw in query_lower)
        code_matches = sum(1 for kw in self.code_keywords if kw in query_lower)
        advanced_matches = sum(1 for kw in self.advanced_keywords if kw in query_lower)

        # Adjust complexity
        complexity += simple_matches * 0.1
        complexity += code_matches * 0.4
        complexity += advanced_matches * 0.6

        # Length bonus
        if word_count > 20:
            complexity += 0.5
        elif word_count > 50:
            complexity += 1.0

        return min(4.0, complexity)  # Cap at 4.0

    def route(self, query: str, forced_model: str = None) -> tuple[str, float]:
        """Route query to appropriate model. Returns (model, complexity)"""
        if forced_model and forced_model != "auto":
            model_map = {"t1": "mistral:7b", "t2": "llama2:7b", "t3": "neural-chat", "t4": "dolphin-mixtral"}
            return model_map.get(forced_model, "mistral:7b"), 2.0

        complexity = self.calculate_complexity(query)

        # Route by complexity
        if complexity < 1.5:
            return "mistral:7b", complexity  # T1
        elif complexity < 2.5:
            return "llama2:7b", complexity   # T2
        elif complexity < 3.5:
            return "neural-chat", complexity  # T3
        else:
            return "dolphin-mixtral", complexity  # T4

router = CascadeRouter()

# Ollama Client
async def query_ollama(model: str, prompt: str) -> str:
    """Query Ollama model"""
    try:
        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(
                f"{OLLAMA_URL}/api/generate",
                json={"model": model, "prompt": prompt, "stream": False}
            )
            if response.status_code == 200:
                return response.json().get("response", "No response")
            return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error connecting to Ollama: {str(e)}"

# API Endpoints
@app.post("/query")
async def query_cascade(request: QueryRequest):
    """Route and answer query using cascade"""
    model, complexity = router.route(request.query, request.model if request.model != "auto" else None)

    # Get response from Ollama
    response = await query_ollama(model, request.query)

    return {
        "status": "ok",
        "query": request.query,
        "response": response,
        "model_used": model,
        "complexity": round(complexity, 2),
        "message": f"Processed with {model}"
    }

@app.get("/health")
async def health():
    """Health check"""
    return {
        "status": "healthy",
        "service": "langgraph",
        "version": "1.0",
        "cascade": "T1→T2→T3→T4"
    }

@app.get("/models")
async def list_models():
    """List available models"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{OLLAMA_URL}/api/tags")
            if response.status_code == 200:
                return response.json()
    except:
        pass

    return {
        "models": [
            {"name": "mistral:7b", "size": "4GB"},
            {"name": "llama2:7b", "size": "4GB"},
            {"name": "neural-chat", "size": "4GB"},
            {"name": "dolphin-mixtral", "size": "13GB"}
        ]
    }

# Read HTML template
def get_html_content() -> str:
    """Get Web UI HTML"""
    # Read from file if exists, otherwise return inline
    html_file = os.path.join(os.path.dirname(__file__), "static", "index.html")
    if os.path.exists(html_file):
        with open(html_file, 'r', encoding='utf-8') as f:
            return f.read()

    # Fallback: return inline HTML
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sovereign AI</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width">
        <style>
            body { font-family: Arial; max-width: 900px; margin: 50px auto; padding: 20px; background: #f5f5f5; }
            .container { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #667eea; }
            input, textarea { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 4px; font-family: inherit; }
            button { background: #667eea; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; margin: 10px 5px 10px 0; }
            button:hover { background: #764ba2; }
            .response { background: #f9f9f9; border: 1px solid #ddd; padding: 15px; margin-top: 20px; border-radius: 4px; min-height: 60px; }
            .model-btn { padding: 8px 15px; margin: 5px; border: 2px solid #ddd; background: white; cursor: pointer; border-radius: 4px; }
            .model-btn.active { background: #667eea; color: white; border-color: #667eea; }
            .status { margin-top: 10px; padding: 10px; border-radius: 4px; }
            .success { background: #d4edda; color: #155724; }
            .error { background: #f8d7da; color: #721c24; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Sovereign AI Cascade Router</h1>
            <p>T1 (Mistral) → T2 (Llama) → T3 (Neural-Chat) → T4 (Dolphin)</p>

            <h3>Sélectionner un modèle:</h3>
            <div id="modelButtons"></div>

            <h3>Votre question:</h3>
            <textarea id="query" placeholder="Posez votre question ici..."></textarea>

            <div>
                <button onclick="submitQuery()">Envoyer</button>
                <button onclick="document.getElementById('query').value=''; document.getElementById('response').innerHTML='';">Effacer</button>
            </div>

            <h3>Réponse:</h3>
            <div class="response" id="response"></div>
            <div id="status"></div>
        </div>

        <script>
            let selectedModel = 'auto';

            // Create model buttons
            const models = [
                {id: 'auto', label: 'Auto 🔄'},
                {id: 't1', label: 'T1'},
                {id: 't2', label: 'T2'},
                {id: 't3', label: 'T3'},
                {id: 't4', label: 'T4'}
            ];

            models.forEach(m => {
                const btn = document.createElement('button');
                btn.className = 'model-btn' + (m.id === 'auto' ? ' active' : '');
                btn.textContent = m.label;
                btn.onclick = () => {
                    document.querySelectorAll('.model-btn').forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    selectedModel = m.id;
                };
                document.getElementById('modelButtons').appendChild(btn);
            });

            async function submitQuery() {
                const query = document.getElementById('query').value;
                if (!query.trim()) {
                    alert('Entrez une question');
                    return;
                }

                const response = document.getElementById('response');
                const status = document.getElementById('status');
                response.innerHTML = 'Traitement...';
                status.innerHTML = '';

                try {
                    const result = await fetch('http://localhost:8888/query', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({query, model: selectedModel})
                    });

                    if (!result.ok) throw new Error('Erreur ' + result.status);

                    const data = await result.json();
                    response.textContent = data.response || data.message || JSON.stringify(data, null, 2);

                    let statusHtml = '<div class="status success">✓ Réponse reçue';
                    if (data.model_used) statusHtml += ` (${data.model_used})`;
                    statusHtml += '</div>';
                    status.innerHTML = statusHtml;
                } catch (e) {
                    response.textContent = 'Erreur: ' + e.message;
                    status.innerHTML = '<div class="status error">❌ Erreur: ' + e.message + '</div>';
                }
            }

            document.getElementById('query').onkeypress = (e) => {
                if (e.ctrlKey && e.key === 'Enter') submitQuery();
            };
        </script>
    </body>
    </html>
    """

@app.get("/")
async def root():
    """Web UI Root"""
    from fastapi.responses import HTMLResponse
    return HTMLResponse(content=get_html_content())

@app.get("/ui")
async def ui():
    """Web UI Alternative endpoint"""
    from fastapi.responses import HTMLResponse
    return HTMLResponse(content=get_html_content())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8888)
