"""Tests du repli de cascade (query_ollama_with_fallback, main.py).

`query_ollama` est monkeypatché — aucun appel réseau. On utilise `asyncio.run`
plutôt que pytest-asyncio : c'est plus simple et sans configuration.
"""
import asyncio

import pytest

import main
from main import OllamaError, query_ollama_with_fallback


def _model_of(tier):
    return next(m for label, m in main.TIERS if label == tier)


def test_repli_vers_le_tier_inferieur(monkeypatch):
    """Le tier de départ (T4) échoue, T3 répond -> réponse de T3, préfixée [repli T4→T3].
    Robuste aux changements de modèles : on lit main.TIERS."""
    t4_model = _model_of("T4")
    t3_model = _model_of("T3")

    async def fake_query_ollama(model, prompt):
        if model == t4_model:
            raise OllamaError("T4 simulé indisponible")
        return f"réponse de {model}"

    monkeypatch.setattr(main, "query_ollama", fake_query_ollama)

    text, model, tier = asyncio.run(query_ollama_with_fallback("T4", "bonjour"))

    assert tier == "T3"
    assert model == t3_model
    assert text.startswith("[repli T4→T3]")


def test_tous_les_tiers_echouent(monkeypatch):
    """Si tous les tiers locaux lèvent OllamaError, l'erreur est propagée."""

    async def fake_query_ollama(model, prompt):
        raise OllamaError(f"{model} KO")

    monkeypatch.setattr(main, "query_ollama", fake_query_ollama)

    with pytest.raises(OllamaError):
        asyncio.run(query_ollama_with_fallback("T4", "bonjour"))
