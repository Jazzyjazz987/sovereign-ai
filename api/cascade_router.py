#!/usr/bin/env python3
"""
Intelligent cascade routing: T1 → T2 → T3 → T4 → T5
Starts with fast model, escalates for complex queries
"""
from api.ollama_client import OllamaClient
from api.vllm_client import VLLMClient
import logging

logger = logging.getLogger(__name__)


class CascadeRouter:
    """Routes queries through model cascade based on complexity."""

    TIERS = [
        {"key": "t1", "name": "mistral:7b", "tier": 1, "latency": "3-4s", "engine": "ollama", "port": 11434},
        {"key": "t2", "name": "llama2:7b", "tier": 2, "latency": "4-5s", "engine": "ollama", "port": 11434},
        {"key": "t3", "name": "mistral-7b-instruct", "tier": 3, "latency": "5-8s", "engine": "vllm", "port": 8001},
    ]

    # Keywords that suggest query complexity
    COMPLEX_KEYWORDS = {
        # T2 triggers (moderate complexity: 1.8-2.4)
        "code": 2,
        "fonction": 2,
        "program": 2,
        "architecture": 2,
        "algorithme": 2,
        "complexe": 2,
        "détail": 2,
        "profond": 2,
        "rgpd": 2,
        "légal": 2,
        "conformité": 2,
        "crypto": 2,
        "sécurité": 1.5,
        "analyse": 1.5,
        "explique": 1.5,
        # T3+ triggers (advanced: 2.5+)
        "powershell": 2.5,
        "graph api": 2.5,
        "implémentation": 2.5,
        "microservices": 2.5,
        "kubernetes": 2.5,
        "docker": 2.5,
        "ansible": 2.5,
        "terraform": 2.5,
        "api rest": 2.3,
        "oauth": 2.3,
        "saml": 2.3,
    }

    def __init__(self):
        self.ollama_client = OllamaClient()
        self.vllm_clients = {}

        # Initialize vLLM clients if available
        for tier in ["t3", "t4"]:
            try:
                self.vllm_clients[tier] = VLLMClient(tier)
            except Exception as e:
                logger.warning(f"⚠️ {tier.upper()} unavailable: {str(e)}")

    def calculate_complexity(self, prompt: str) -> float:
        """Calculate query complexity (1.0 = T1, 2.0 = T2, 2.5+ = T3)."""
        prompt_lower = prompt.lower()
        max_complexity = 1.0

        for keyword, complexity in self.COMPLEX_KEYWORDS.items():
            if keyword in prompt_lower:
                max_complexity = max(max_complexity, complexity)

        # Length also indicates complexity
        word_count = len(prompt.split())
        if word_count > 30:
            max_complexity = max(max_complexity, 1.3)
        if word_count > 50:
            max_complexity = max(max_complexity, 1.8)
        if word_count > 80:
            max_complexity = max(max_complexity, 2.2)

        return min(max_complexity, 3.0)  # Allow T3+

    def select_model(self, prompt: str) -> dict:
        """Select model based on prompt complexity."""
        complexity = self.calculate_complexity(prompt)

        # T3 for advanced code/architecture (if available)
        if complexity >= 2.5:
            return {"key": "t3", "tier": 3, "reason": "very_complex_query"}
        # T2 for complex queries
        elif complexity >= 1.8:
            return {"key": "t2", "tier": 2, "reason": "complex_query"}
        # T1 for medium/simple
        elif complexity >= 1.3:
            return {"key": "t1", "tier": 1, "reason": "medium_query"}
        else:
            return {"key": "t1", "tier": 1, "reason": "simple_query"}

    def query(self, prompt: str, force_model: str = None, system: str = None):
        """
        Route query through cascade.

        Args:
            prompt: User query
            force_model: Force specific model ("t1", "t2", "t3") or None for auto
            system: Optional system message
        """
        if force_model:
            model_key = force_model
            selection = {"key": force_model, "tier": 1, "reason": "forced"}
            if force_model == "t2":
                selection["tier"] = 2
            elif force_model == "t3":
                selection["tier"] = 3
        else:
            selection = self.select_model(prompt)
            model_key = selection["key"]

        logger.info(f"🔀 Route: {selection['reason']} → {model_key.upper()}")

        # Add system instructions if not provided
        if not system:
            system = self._get_system_prompt(model_key)

        # Select appropriate client based on tier
        if model_key in ["t3", "t4"]:
            if model_key in self.vllm_clients:
                try:
                    client = self.vllm_clients[model_key]
                    response = client.query(prompt, system)
                except Exception as e:
                    logger.warning(f"⚠️ {model_key.upper()} query failed: {str(e)[:60]}... falling back to T2")
                    response = self.ollama_client.query("t2", prompt, system)
                    selection["reason"] = f"{selection['reason']}_fallback_to_t2"
            else:
                # Fallback to T2 if T3/T4 unavailable
                logger.warning(f"⚠️ {model_key.upper()} unavailable, falling back to T2")
                response = self.ollama_client.query("t2", prompt, system)
                selection["reason"] = f"{selection['reason']}_fallback_to_t2"
        else:
            # Ollama for T1/T2
            response = self.ollama_client.query(model_key, prompt, system)

        return {
            "response": response,
            "model": model_key,
            "tier": selection.get("tier", 1),
            "complexity": self.calculate_complexity(prompt),
            "reason": selection.get("reason"),
        }

    def _get_system_prompt(self, model_key: str) -> str:
        """Get system prompt with formatting instructions."""
        return """Tu es un assistant IA utile. Formate tes réponses de manière claire et lisible:

• Utilise des paragraphes séparés pour différentes idées
• Utilise des points de liste (•) ou listes numérotées (1., 2., 3.) pour les énumérations
• Ajoute des sauts de ligne appropriés au lieu de longs blocs de texte
• Utilise **gras** pour les termes importants
• Utilise des en-têtes quand tu discutes de plusieurs sujets
• Garde les réponses bien organisées et faciles à scanner
• Ajoute des emojis pertinents pour améliorer la lecture:
  ✅ pour les avantages, points positifs
  ❌ pour les inconvénients, problèmes
  💡 pour les idées, suggestions
  ⚡ pour la performance, vitesse
  🔒 pour la sécurité
  📊 pour les données, statistiques
  🛠️ pour les outils, configuration
  🎯 pour les objectifs
  ⚠️ pour les avertissements
  ℹ️ pour les informations

Réponds toujours en français sauf demande contraire. Priorité absolue à la clarté et à la lisibilité."""

    def query_stream(self, prompt: str, force_model: str = None, system: str = None):
        """Stream query response through cascade."""
        if force_model:
            model_key = force_model
        else:
            selection = self.select_model(prompt)
            model_key = selection["key"]

        logger.info(f"🔀 Stream: {model_key.upper()}")

        # Add system instructions if not provided
        if not system:
            system = self._get_system_prompt(model_key)

        # Select appropriate client for streaming
        if model_key in ["t3", "t4"]:
            if model_key in self.vllm_clients:
                try:
                    client = self.vllm_clients[model_key]
                    return client.query_stream(prompt, system)
                except Exception as e:
                    logger.warning(f"⚠️ {model_key.upper()} stream failed: {str(e)[:60]}... falling back to T2")
                    return self.ollama_client.query_stream("t2", prompt, system)
            else:
                # Fallback to T2 if T3/T4 unavailable
                logger.warning(f"⚠️ {model_key.upper()} unavailable, falling back to T2 stream")
                return self.ollama_client.query_stream("t2", prompt, system)
        else:
            # Ollama for T1/T2
            return self.ollama_client.query_stream(model_key, prompt, system)


if __name__ == "__main__":
    router = CascadeRouter()

    # Test simple query
    print("=== Simple Query (T1) ===")
    result = router.query("Bonjour")
    print(f"Model: {result['model']}, Reason: {result['reason']}")
    print(f"Response: {result['response'][:100]}...\n")

    # Test complex query
    print("=== Complex Query (T2) ===")
    result = router.query("Écris une fonction Python pour valider un email avec regex")
    print(f"Model: {result['model']}, Reason: {result['reason']}")
    print(f"Response: {result['response'][:100]}...\n")

    # Test RGPD (legal)
    print("=== Legal Query (T2) ===")
    result = router.query("Quels sont les défis RGPD pour un gouvernement?")
    print(f"Model: {result['model']}, Reason: {result['reason']}")
    print(f"Response: {result['response'][:100]}...")
