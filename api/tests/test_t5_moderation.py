"""Modération humaine des appels T5 (T5_MODERATION=on).

Chaque appel T5 est mis en attente ; il ne part que s'il est approuvé via
POST /t5/{id}/approve. Sans réponse dans T5_APPROVAL_TIMEOUT → repli local T4.
Aucun appel réseau réel ici : Anone et Anthropic sont monkeypatchés.
"""
import asyncio

import main


class _Resp:
    status_code = 200

    def __init__(self, payload):
        self._payload = payload

    def json(self):
        return self._payload


def _anone_ok(*a, **k):
    return _Resp({"status": "ok", "anonymized_text": "<PERSON_0> conteste",
                  "pii_mapping": {"<PERSON_0>": "X"}})


def test_estimation_cout():
    est = main._estimate_cost("a" * 400, "claude-sonnet-5")
    assert est["input_tokens_est"] == 140  # 400//4 + 40
    assert est["output_tokens_max"] == main.T5_MAX_TOKENS
    assert est["cost_usd_est"] > 0
    # haiku moins cher que sonnet pour le même texte
    assert main._estimate_cost("a" * 400, "claude-haiku-4-5")["cost_usd_est"] < est["cost_usd_est"]


def test_timeout_sans_approbation__repli_t4(monkeypatch):
    monkeypatch.setattr(main, "T5_MODERATION", True)
    monkeypatch.setattr(main, "T5_APPROVAL_TIMEOUT", 0.2)
    monkeypatch.setattr(main.requests, "post", _anone_ok)
    monkeypatch.setattr(main.anthropic, "Anthropic",
                        lambda *a, **k: (_ for _ in ()).throw(AssertionError("cloud interdit sans appro")))

    async def fake_ollama(model, prompt):
        return "réponse locale T4"

    monkeypatch.setattr(main, "query_ollama", fake_ollama)

    out = asyncio.run(main.route_t5_with_anonymization("Jean Dupont conteste"))
    assert out["status"] == "ok"
    assert out["tier"] in {"T1", "T2", "T3", "T4"}
    assert "pas d'approbation" in out["message"]
    assert not main._t5_pending  # la demande a été nettoyée


def test_approbation__appel_cloud(monkeypatch):
    monkeypatch.setattr(main, "T5_MODERATION", True)
    monkeypatch.setattr(main, "T5_APPROVAL_TIMEOUT", 5)
    monkeypatch.setattr(main.requests, "post", _anone_ok)

    class _Msg:
        content = [type("B", (), {"text": "réponse T5"})()]
        usage = type("U", (), {"input_tokens": 10, "output_tokens": 20})()

    monkeypatch.setattr(main.anthropic, "Anthropic",
                        lambda *a, **k: type("C", (), {"messages": type("M", (), {"create": staticmethod(lambda **kw: _Msg())})()})())

    async def scenario():
        task = asyncio.create_task(main.route_t5_with_anonymization("Jean Dupont conteste"))
        await asyncio.sleep(0.05)
        assert len(main._t5_pending) == 1
        rid = next(iter(main._t5_pending))
        main._resolve_t5(rid, True)
        return await task

    out = asyncio.run(scenario())
    assert out["tier"] == "T5"
    assert out["status"] == "ok"


def test_resolve_inconnu__404():
    import fastapi
    try:
        main._resolve_t5("t5-inexistant", True)
        assert False, "devrait lever HTTPException 404"
    except fastapi.HTTPException as e:
        assert e.status_code == 404
