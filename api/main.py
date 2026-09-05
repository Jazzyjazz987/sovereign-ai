"""
LangGraph Orchestrateur Cascade T1→T5
Port 8888 - API + Web UI
"""
import os
import httpx
import asyncio
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import re
import anthropic
import requests

app = FastAPI(title="Sovereign AI Cascade Router", version="1.0")

# Configuration
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")
litellm_api_key = os.getenv("LITELLM_API_KEY")
# Modèle T5 (cloud Anthropic). CLAUDE.md : "Claude Sonnet". Surchargeable via l'env.
# Budget serré : mettre T5_MODEL=claude-haiku-4-5 dans .env (~5x moins cher en sortie).
T5_MODEL = os.getenv("T5_MODEL", "claude-sonnet-5")
# Garde-fous de coût pour l'API Anthropic (budget opérateur ~5 USD).
T5_MAX_TOKENS = int(os.getenv("T5_MAX_TOKENS", "700"))
T5_MAX_CALLS = int(os.getenv("T5_MAX_CALLS", "150"))  # plafond d'appels cloud par process
_t5_calls = 0

# Pydantic models
class QueryRequest(BaseModel):
    query: str
    model: str = "auto"
    # Override optionnel du score de complexité (1.0–5.0). Si absent, il est calculé
    # à partir des mots-clés de la requête. Utile pour les tests de cascade déterministes.
    complexity: Optional[float] = None

# Cascade figée (CLAUDE.md). Chaque tier pointe vers un tag Ollama, sauf T5 (cloud).
# L'ordre sert aussi de chaîne de repli : si un tier échoue, on descend d'un cran.
TIERS = [
    ("T1", "mistral:7b"),
    ("T2", "llama2:7b"),
    ("T3", "neural-chat"),
    ("T4", "dolphin-mixtral"),
    ("T5", "claude-sonnet"),
]

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
        """Calcule un score de complexité (1.0 - 5.0)"""
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

        # Length bonus (tester le seuil le plus élevé d'abord)
        if word_count > 50:
            complexity += 1.0
        elif word_count > 20:
            complexity += 0.5

        return min(5.0, complexity)  # Cap at 5.0 (T5 atteignable)

    def route(self, query: str, forced_model: str = None,
              complexity_override: float = None) -> tuple[str, float, str]:
        """Route la requête. Retourne (model, complexity, tier_label)."""
        if forced_model and forced_model != "auto":
            forced_map = {label.lower(): (model, label) for label, model in TIERS}
            model, label = forced_map.get(forced_model.lower(), ("mistral:7b", "T1"))
            return model, 2.0, label

        complexity = complexity_override if complexity_override is not None \
            else self.calculate_complexity(query)

        # Route par complexité vers un tier
        if complexity < 1.5:
            idx = 0   # T1
        elif complexity < 2.5:
            idx = 1   # T2
        elif complexity < 3.5:
            idx = 2   # T3
        elif complexity < 4.5:
            idx = 3   # T4
        else:
            idx = 4   # T5
        label, model = TIERS[idx]
        return model, complexity, label

router = CascadeRouter()

# Ollama Client
class OllamaError(Exception):
    """Erreur d'appel Ollama — déclenche le repli vers le tier inférieur."""

async def query_ollama(model: str, prompt: str) -> str:
    """Interroge un modèle Ollama. Lève OllamaError en cas d'échec."""
    try:
        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(
                f"{OLLAMA_URL}/api/generate",
                json={"model": model, "prompt": prompt, "stream": False}
            )
    except Exception as e:
        raise OllamaError(f"connexion Ollama impossible: {e}")

    if response.status_code != 200:
        raise OllamaError(f"Ollama HTTP {response.status_code} pour {model}: {response.text[:200]}")
    text = response.json().get("response", "").strip()
    if not text:
        raise OllamaError(f"réponse vide de {model}")
    return text


async def query_ollama_with_fallback(start_tier: str, prompt: str) -> tuple[str, str, str]:
    """Essaie le tier demandé puis descend la cascade. Retourne (texte, model, tier)."""
    start_idx = next((i for i, (label, _) in enumerate(TIERS) if label == start_tier), 0)
    errors = []
    for label, model in TIERS[start_idx::-1]:  # du tier courant vers T1
        if label == "T5":
            continue  # T5 est géré séparément (anonymisation)
        try:
            text = await query_ollama(model, prompt)
            if errors:
                text = f"[repli {start_tier}→{label}] {text}"
            return text, model, label
        except OllamaError as e:
            errors.append(str(e))
    raise OllamaError("tous les tiers locaux ont échoué: " + " | ".join(errors))

# T5 Handler with Anonymization
async def _fallback_local(query: str, raison: str) -> dict:
    """Repli local T4 quand T5 ne peut pas être appelé en toute sécurité."""
    try:
        text, model, tier = await query_ollama_with_fallback("T4", query)
        return {"status": "ok", "query": query, "response": text, "model_used": model,
                "tier": tier, "complexity": 5.0, "anonymized": False,
                "message": f"T5 non appelé ({raison}); repli local sur {tier}"}
    except OllamaError as oe:
        return {"status": "error", "model": "T5",
                "error": f"T5 non appelé ({raison}); repli local KO ({oe})"}


async def route_t5_with_anonymization(query: str) -> dict:
    """Route vers T5 (Claude) via l'anonymisation PII Agent Anone.

    RGPD — CLAUDE.md : l'anonymisation est OBLIGATOIRE. En cas de doute on
    N'APPELLE PAS le cloud (fail-closed) : repli local à la place.
    """
    global _t5_calls

    # Step 0: garde-fou budget — au-delà du plafond, on reste en local.
    if _t5_calls >= T5_MAX_CALLS:
        return await _fallback_local(query, f"plafond T5 atteint ({T5_MAX_CALLS} appels)")

    # Step 1: Anonymisation via Agent Anone — fail-closed
    try:
        anone_response = requests.post(
            "http://anone:8080/anonymize",
            json={"text": query},
            timeout=10
        )
    except requests.exceptions.RequestException as e:
        return await _fallback_local(query, f"Agent Anone injoignable: {e}")

    if anone_response.status_code != 200:
        return await _fallback_local(query, f"Anone HTTP {anone_response.status_code}")

    anon_data = anone_response.json()
    # L'anonymisation doit avoir explicitement réussi ET renvoyer un texte anonymisé.
    # Pas de repli silencieux sur la requête brute (= fuite PII vers le cloud).
    if anon_data.get("status") != "ok" or "anonymized_text" not in anon_data:
        return await _fallback_local(
            query, f"anonymisation non confirmée: {anon_data.get('message', anon_data.get('status'))}")

    anonymized_query = anon_data["anonymized_text"]
    pii_mapping = anon_data.get("pii_mapping", {})

    # Step 2: Call T5 (Claude) via Anthropic API
    try:
        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

        _t5_calls += 1
        message = client.messages.create(
            model=T5_MODEL,
            max_tokens=T5_MAX_TOKENS,
            system="Assistant IA francophone pour la DSI de Polynésie française "
                   "(SI gouvernemental, RGPD, souverain). Réponds en français, "
                   "de façon précise, officielle et concise.",
            messages=[{"role": "user", "content": anonymized_query}],
        )

        response_text = message.content[0].text

        # Step 3: De-anonymize response (restore PII from mapping)
        try:
            deanon_response = requests.post(
                "http://anone:8080/deanonymize",
                json={"text": response_text, "pii_mapping": pii_mapping},
                timeout=10
            )

            final_response = deanon_response.json().get("text", response_text)
        except requests.exceptions.RequestException:
            # If de-anonymization fails, return anonymized response
            final_response = response_text

        usage = getattr(message, "usage", None)
        return {
            "status": "ok",
            "query": query,
            "response": final_response,
            "model_used": T5_MODEL,
            "tier": "T5",
            "complexity": 5.0,
            "anonymized": True,
            "t5_calls": _t5_calls,
            "usage": {"input_tokens": getattr(usage, "input_tokens", None),
                      "output_tokens": getattr(usage, "output_tokens", None)} if usage else None,
            "message": f"Traité par T5 ({T5_MODEL}) + Agent Anone"
        }
    except anthropic.APIError as e:
        return await _fallback_local(query, f"API Anthropic indisponible: {e}")

# API Endpoints
@app.post("/query")
async def query_cascade(request: QueryRequest):
    """Route et répond à une requête via la cascade T1→T5."""
    forced = request.model if request.model != "auto" else None
    model, complexity, tier = router.route(request.query, forced, request.complexity)

    # T5 (Claude Sonnet) : passage obligatoire par l'anonymisation Agent Anone.
    if tier == "T5":
        return await route_t5_with_anonymization(request.query)

    # T1–T4 : Ollama avec repli automatique vers le tier inférieur.
    try:
        response, model, tier = await query_ollama_with_fallback(tier, request.query)
    except OllamaError as e:
        return {"status": "error", "query": request.query, "error": str(e),
                "model_used": model, "complexity": round(complexity, 2)}

    return {
        "status": "ok",
        "query": request.query,
        "response": response,
        "model_used": model,
        "tier": tier,
        "complexity": round(complexity, 2),
        "message": f"Traité par {tier} ({model})"
    }

@app.get("/health")
async def health():
    """Health check"""
    return {
        "status": "healthy",
        "service": "langgraph",
        "version": "2.0",
        "cascade": "T1→T2→T3→T4→T5",
        "t5": {"model": T5_MODEL, "calls": _t5_calls, "max_calls": T5_MAX_CALLS,
               "max_tokens": T5_MAX_TOKENS}
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
            .model-btn.t5 { border-color: #ff6b9d; }
            .model-btn.t5.active { background: #ff6b9d; border-color: #ff6b9d; }
            .status { margin-top: 10px; padding: 10px; border-radius: 4px; }
            .success { background: #d4edda; color: #155724; }
            .error { background: #f8d7da; color: #721c24; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Sovereign AI Cascade Router</h1>
            <p>T1 (Mistral) → T2 (Llama) → T3 (Neural-Chat) → T4 (Dolphin) → T5 (Claude Sonnet)</p>

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
                {id: 't4', label: 'T4'},
                {id: 't5', label: 'T5', special: true}
            ];

            models.forEach(m => {
                const btn = document.createElement('button');
                btn.className = 'model-btn' + (m.id === 'auto' ? ' active' : '') + (m.special ? ' t5' : '');
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
