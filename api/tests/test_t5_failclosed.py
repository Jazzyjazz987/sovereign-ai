"""RGPD — le chemin T5 doit être fail-closed.

Si Agent Anone ne confirme pas l'anonymisation (GLiNER absent, HTTP != 200,
status != "ok", pas d'`anonymized_text`), `route_t5_with_anonymization` NE DOIT
PAS appeler le cloud : elle bascule en repli local. On vérifie ici qu'aucun
appel réseau vers Anthropic n'est tenté et que la requête brute ne « fuit » pas.
"""
import asyncio

import main


class _Resp:
    def __init__(self, code, payload):
        self.status_code = code
        self._payload = payload

    def json(self):
        return self._payload


def _run(query):
    return asyncio.run(main.route_t5_with_anonymization(query))


def test_anone_erreur_gliner_absent__pas_d_appel_cloud(monkeypatch):
    """Anone répond 200 mais status=error -> repli local, cloud jamais appelé."""
    monkeypatch.setattr(
        main.requests, "post",
        lambda *a, **k: _Resp(200, {"status": "error", "message": "GLiNER not loaded"}),
    )

    def _boom(*a, **k):
        raise AssertionError("le client Anthropic ne doit pas être instancié")

    monkeypatch.setattr(main.anthropic, "Anthropic", _boom)

    async def fake_fallback(model, prompt):
        return "réponse locale"

    monkeypatch.setattr(main, "query_ollama", fake_fallback)

    out = _run("Jean Dupont conteste une sanction")
    assert out["status"] == "ok"
    assert out["tier"] in {"T1", "T2", "T3", "T4"}
    assert out["anonymized"] is False
    assert "anonymisation non confirmée" in out["message"]


def test_anone_injoignable__repli_local(monkeypatch):
    """Anone injoignable -> repli local, pas d'exception qui remonte."""
    def _raise(*a, **k):
        raise main.requests.exceptions.RequestException("connection refused")

    monkeypatch.setattr(main.requests, "post", _raise)
    monkeypatch.setattr(main.anthropic, "Anthropic",
                        lambda *a, **k: (_ for _ in ()).throw(AssertionError("cloud interdit")))

    async def fake_fallback(model, prompt):
        return "réponse locale"

    monkeypatch.setattr(main, "query_ollama", fake_fallback)

    out = _run("requête avec PII")
    assert out["status"] == "ok"
    assert "Agent Anone injoignable" in out["message"]
