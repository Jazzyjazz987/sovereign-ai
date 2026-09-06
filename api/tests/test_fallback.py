"""Tests du repli de cascade (query_ollama_with_fallback, main.py).

`query_ollama` est monkeypatché — aucun appel réseau. On utilise `asyncio.run`
plutôt que pytest-asyncio : c'est plus simple et sans configuration.
"""
import asyncio

import pytest

import main
from main import OllamaError, query_ollama_with_fallback


# TIERS de test : modèles distincts par tier pour vérifier la logique de repli
# indépendamment de la config de prod (où plusieurs tiers peuvent partager un modèle).
_TEST_TIERS = [
    ("T1", "m1"), ("T2", "m2"), ("T3", "m3"), ("T4", "m4"), ("T5", "claude-sonnet"),
]


def test_repli_vers_le_tier_inferieur(monkeypatch):
    """Le tier de départ (T4) échoue, T3 répond -> réponse de T3, préfixée [repli T4→T3]."""
    monkeypatch.setattr(main, "TIERS", _TEST_TIERS)

    async def fake_query_ollama(model, prompt, tier=None):
        if model == "m4":  # T4
            raise OllamaError("T4 simulé indisponible")
        return f"réponse de {model}"

    monkeypatch.setattr(main, "query_ollama", fake_query_ollama)

    text, model, tier = asyncio.run(query_ollama_with_fallback("T4", "bonjour"))

    assert tier == "T3"
    assert model == "m3"
    assert text.startswith("[repli T4→T3]")


def test_tous_les_tiers_echouent(monkeypatch):
    """Si tous les tiers locaux lèvent OllamaError, l'erreur est propagée."""

    async def fake_query_ollama(model, prompt, tier=None):
        raise OllamaError(f"{model} KO")

    monkeypatch.setattr(main, "query_ollama", fake_query_ollama)

    with pytest.raises(OllamaError):
        asyncio.run(query_ollama_with_fallback("T4", "bonjour"))
