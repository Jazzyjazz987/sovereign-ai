"""
LangGraph Orchestrateur Cascade T1→T5
Port 8888 - API + Web UI
"""
import os
import time
import httpx
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import re
import hashlib
import anthropic
import requests
import yaml
from prometheus_client import Counter, Histogram, CONTENT_TYPE_LATEST, generate_latest

app = FastAPI(title="Sovereign AI Cascade Router", version="1.0")

# Configuration
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")
litellm_api_key = os.getenv("LITELLM_API_KEY")

# --- Prompt pack (POC A2) — un prompt système par tier, chargé au démarrage (fail-fast) ------
PROMPTS_PATH = os.getenv("PROMPTS_PATH", "/app/config/prompts.yaml")


def _load_prompts(path: str) -> tuple[dict, str]:
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    data = yaml.safe_load(raw)
    commun = (data.get("commun") or "").strip()
    tiers = {t: (body or "").format(commun=commun).strip()
             for t, body in (data.get("tiers") or {}).items()}
    if not tiers:
        raise ValueError(f"{path} : aucun prompt de tier")
    fp = hashlib.sha256(raw.encode()).hexdigest()[:12]
    return tiers, fp


TIER_PROMPTS, PROMPT_SET_FP = _load_prompts(PROMPTS_PATH)
# Modèle T5 (cloud Anthropic). CLAUDE.md : "Claude Sonnet". Surchargeable via l'env.
# Budget serré : mettre T5_MODEL=claude-haiku-4-5 dans .env (~5x moins cher en sortie).
T5_MODEL = os.getenv("T5_MODEL", "claude-sonnet-5")
# Garde-fous de coût pour l'API Anthropic (budget opérateur ~5 USD).
T5_MAX_TOKENS = int(os.getenv("T5_MAX_TOKENS", "700"))
T5_MAX_CALLS = int(os.getenv("T5_MAX_CALLS", "150"))  # plafond d'appels cloud par process
_t5_calls = 0

# --- Métriques Prometheus (B6) — exposées sur GET /metrics ---------------------------
QUERY_REQUESTS = Counter(
    "query_requests_total", "Requêtes /query traitées", ["tier", "status"]
)
QUERY_LATENCY = Histogram(
    "query_latency_seconds", "Latence de traitement d'une requête /query (secondes)"
)
T5_CLOUD_CALLS = Counter(
    "t5_cloud_calls_total", "Appels cloud T5 (API Anthropic) effectués"
)

# --- Modération humaine des appels T5 -------------------------------------------------
# Si activée, chaque appel T5 est mis en attente : une notification part (webhook), et
# l'appel n'est fait que s'il est approuvé via POST /t5/{id}/approve. Sans réponse dans
# T5_APPROVAL_TIMEOUT secondes → repli local T4.
T5_MODERATION = os.getenv("T5_MODERATION", "off").lower() in ("1", "true", "on", "yes")
T5_APPROVAL_TIMEOUT = float(os.getenv("T5_APPROVAL_TIMEOUT", "60"))
T5_NOTIFY_WEBHOOK = os.getenv("T5_NOTIFY_WEBHOOK", "").strip()

# Tarifs API Anthropic — USD par million de tokens (entrée, sortie). Source : skill claude-api.
T5_PRICES = {
    "claude-sonnet-5": (2.0, 10.0),
    "claude-haiku-4-5": (1.0, 5.0),
    "claude-opus-5": (5.0, 25.0),
}


def _estimate_cost(text: str, model: str) -> dict:
    """Estimation grossière : ~4 caractères/token en entrée, T5_MAX_TOKENS en sortie."""
    in_tok = len(text) // 4 + 40  # +40 pour le prompt système
    out_tok = T5_MAX_TOKENS
    p_in, p_out = T5_PRICES.get(model, T5_PRICES["claude-sonnet-5"])
    usd = in_tok / 1e6 * p_in + out_tok / 1e6 * p_out
    return {"model": model, "input_tokens_est": in_tok, "output_tokens_max": out_tok,
            "cost_usd_est": round(usd, 4)}


# File d'attente d'approbation T5 : {id: {id, anonymized, estimate, created, future}}
_t5_pending: dict = {}
_t5_seq = 0


async def _notify_t5(rid: str, estimate: dict) -> None:
    """Notifie une demande d'approbation T5 (log + webhook best-effort)."""
    msg = (f"[T5] Approbation requise {rid} — modèle {estimate['model']}, "
           f"~{estimate['input_tokens_est']} tok in / {estimate['output_tokens_max']} max out, "
           f"coût estimé ~{estimate['cost_usd_est']} USD. Repli T4 dans "
           f"{int(T5_APPROVAL_TIMEOUT)}s sans réponse.")
    print(msg, flush=True)
    if not T5_NOTIFY_WEBHOOK:
        return
    payload = {"type": "t5_approval_request", "request_id": rid,
               "timeout_s": T5_APPROVAL_TIMEOUT,
               "approve_path": f"/t5/{rid}/approve", "deny_path": f"/t5/{rid}/deny",
               **estimate}
    try:
        await asyncio.to_thread(requests.post, T5_NOTIFY_WEBHOOK, json=payload, timeout=5)
    except Exception as e:  # noqa: BLE001 — la notif ne doit jamais casser la requête
        print(f"[T5] webhook notif KO: {e}", flush=True)


async def _await_t5_approval(anonymized_query: str) -> tuple[bool, dict]:
    """Crée une demande d'approbation, notifie, attend la décision ou le timeout."""
    global _t5_seq
    _t5_seq += 1
    rid = f"t5-{_t5_seq}"
    estimate = _estimate_cost(anonymized_query, T5_MODEL)
    fut: asyncio.Future = asyncio.get_running_loop().create_future()
    _t5_pending[rid] = {"id": rid, "anonymized": anonymized_query, "estimate": estimate,
                        "created": time.time(), "future": fut}
    await _notify_t5(rid, estimate)
    try:
        approved = await asyncio.wait_for(fut, timeout=T5_APPROVAL_TIMEOUT)
        reason = "approuvé" if approved else "refusé"
    except asyncio.TimeoutError:
        approved, reason = False, f"pas d'approbation en {int(T5_APPROVAL_TIMEOUT)}s"
    finally:
        _t5_pending.pop(rid, None)
    return approved, {"request_id": rid, "reason": reason, "estimate": estimate}

# Pydantic models
class QueryRequest(BaseModel):
    query: str
    model: str = "auto"
    # Override optionnel du score de complexité (1.0–5.0). Si absent, il est calculé
    # à partir des mots-clés de la requête. Utile pour les tests de cascade déterministes.
    complexity: Optional[float] = None

# Cascade — cible (voir docs/DESIGN_REVIEW.md § POC SHORTLIST + config/models.yaml).
# Chaque tier pointe vers un tag Ollama, sauf T5 (réseau). L'ordre sert aussi de chaîne de repli.
# 2026-09-05 :
#  - `dolphin-mixtral` / `neural-chat` retirés (fine-tunes non censurés).
#  - guillaumetell-7b / albert-spp-8b (Albert/DINUM) testés → RAG-only, inutilisables nus
#    (voir docs/design-review/model-comparison-2026-09-05.md). Repris quand la couche RAG existe.
#  - Modèle local = **qwen2.5:7b** (Apache-2.0, fort FR, suit le prompt système, refuse
#    d'halluciner les réfs juridiques — comparé à mistral:7b qui invente le CGCT pour la PF).
#  - Tiers non encore différenciés (même modèle partout) : le vrai levier = base de fiches
#    canoniques + portail à fiches citées (POC SHORTLIST B). Un modèle code dédié plus tard.
TIERS = [
    ("T1", "qwen2.5:7b"),
    ("T2", "qwen2.5:7b"),
    ("T3", "qwen2.5:7b"),
    ("T4", "qwen2.5:7b"),
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
            model, label = forced_map.get(forced_model.lower(), ("qwen2.5:7b", "T1"))
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

async def query_ollama(model: str, prompt: str, tier: str = None) -> str:
    """Interroge un modèle Ollama avec le prompt système du tier. Lève OllamaError si échec."""
    payload = {"model": model, "prompt": prompt, "stream": False}
    system = TIER_PROMPTS.get(tier)
    if system:
        payload["system"] = system
    try:
        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(f"{OLLAMA_URL}/api/generate", json=payload)
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
            text = await query_ollama(model, prompt, tier=label)
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

    # Step 1b: modération humaine optionnelle (T5_MODERATION=on)
    if T5_MODERATION:
        approved, info = await _await_t5_approval(anonymized_query)
        if not approved:
            return await _fallback_local(
                query, f"T5 {info['reason']} (est. {info['estimate']['cost_usd_est']} USD)")

    # Step 2: Call T5 (Claude) via Anthropic API
    try:
        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

        _t5_calls += 1
        T5_CLOUD_CALLS.inc()
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
@app.get("/metrics")
async def metrics():
    """Métriques Prometheus (B6) — scrapées par le job 'langgraph'."""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/query")
async def query_cascade(request: QueryRequest):
    """Route et répond à une requête via la cascade T1→T5.

    Fine enveloppe autour de `_query_cascade` : mesure la latence et incrémente
    les compteurs Prometheus (tier + statut) sans toucher à la logique de cascade.
    """
    start = time.perf_counter()
    result = await _query_cascade(request)
    QUERY_LATENCY.observe(time.perf_counter() - start)
    QUERY_REQUESTS.labels(
        tier=str(result.get("tier", "?")), status=result.get("status", "error")
    ).inc()
    return result


async def _query_cascade(request: QueryRequest):
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
        "prompt_set": PROMPT_SET_FP,
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
        "prompt_set": PROMPT_SET_FP,
        "t5": {"model": T5_MODEL, "calls": _t5_calls, "max_calls": T5_MAX_CALLS,
               "max_tokens": T5_MAX_TOKENS, "moderation": T5_MODERATION,
               "pending": len(_t5_pending)}
    }


# --- Modération T5 : file d'attente + décisions -------------------------------------
@app.get("/t5/pending")
async def t5_pending():
    """Demandes T5 en attente d'approbation humaine."""
    return {"pending": [
        {"id": p["id"], "estimate": p["estimate"],
         "waiting_s": round(time.time() - p["created"], 1),
         "anonymized_preview": p["anonymized"][:200]}
        for p in _t5_pending.values()
    ]}


def _resolve_t5(rid: str, approved: bool) -> dict:
    p = _t5_pending.get(rid)
    if p is None:
        raise HTTPException(status_code=404, detail=f"aucune demande T5 en attente: {rid}")
    if not p["future"].done():
        p["future"].set_result(approved)
    return {"id": rid, "approved": approved}


@app.post("/t5/{rid}/approve")
async def t5_approve(rid: str):
    """Autorise l'appel cloud T5 en attente."""
    return _resolve_t5(rid, True)


@app.post("/t5/{rid}/deny")
async def t5_deny(rid: str):
    """Refuse l'appel cloud T5 → repli local T4."""
    return _resolve_t5(rid, False)

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

    return {"models": [{"name": m} for _, m in TIERS if m != "claude-sonnet"]}

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
