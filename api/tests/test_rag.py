"""Tests de l'étape RAG (portail à fiches citées) dans main.py."""
import pytest

import main


def test_smalltalk_regex_matche_les_salutations():
    for s in ["bonjour", "Salut, ça va ?", "merci beaucoup", "qui es-tu ?",
              "tu fais quoi comme travail", "c'est quoi ton rôle"]:
        assert main._SMALLTALK.match(s), s
    for s in ["comment créer un compte utilisateur", "procédure de réforme d'un poste"]:
        assert not main._SMALLTALK.match(s), s


@pytest.mark.asyncio
async def test_rag_answer_none_sur_smalltalk(monkeypatch):
    """Une salutation courte ne déclenche jamais d'appel au service RAG."""
    called = False

    async def _boom(*a, **k):
        nonlocal called
        called = True
        raise AssertionError("le RAG ne doit pas être interrogé")

    monkeypatch.setattr(main.httpx, "AsyncClient", _boom)
    assert await main._rag_answer("bonjour") is None
    assert called is False


@pytest.mark.asyncio
async def test_rag_answer_none_si_service_injoignable(monkeypatch):
    """Service RAG KO -> None (fail-open) : la cascade prend le relais."""
    monkeypatch.setattr(main, "RAG_ENABLED", True)
    monkeypatch.setattr(main, "RAG_URL", "http://127.0.0.1:9")  # port fermé -> échec rapide
    assert await main._rag_answer("comment créer une boîte aux lettres partagée ?") is None


@pytest.mark.asyncio
async def test_rag_answer_none_si_aucune_fiche_au_dessus_du_seuil(monkeypatch):
    """Des hits tous sous RAG_MIN_RERANK -> None."""
    class _Resp:
        def raise_for_status(self): pass
        def json(self):
            return {"hits": [
                {"proc_code": "PROC-X", "section": "Étapes", "text": "p: x\ncorps",
                 "rerank_score": -5.0, "domaine": "Test"},
            ]}

    class _Client:
        async def __aenter__(self): return self
        async def __aexit__(self, *a): return False
        async def post(self, *a, **k): return _Resp()

    monkeypatch.setattr(main, "RAG_ENABLED", True)
    monkeypatch.setattr(main, "RAG_MIN_RERANK", 0.0)
    monkeypatch.setattr(main.httpx, "AsyncClient", lambda *a, **k: _Client())
    assert await main._rag_answer("question quelconque") is None
