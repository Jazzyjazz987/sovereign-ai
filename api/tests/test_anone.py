"""Tests du round-trip d'anonymisation Anone (anone_api.py).

GLiNER est stubé dans conftest.py : aucun modèle n'est téléchargé. Pour
/anonymize on injecte un faux `ner` avec `predict_entities`. /deanonymize est
testé tel quel (simple substitution via pii_mapping).

Nouveau contrat (B13b) : /anonymize renvoie un `pii_mapping` {token: valeur}
avec des tokens uniques (`<PERSON_0>`), et HTTP 503 quand le modèle est absent.
"""
from fastapi.testclient import TestClient

import anone_api

client = TestClient(anone_api.app, raise_server_exceptions=False)


class _FakeNER:
    """Imite GLiNER.predict_entities à partir d'une liste d'entités figées."""

    def __init__(self, entities):
        self._entities = entities

    def predict_entities(self, text, labels, threshold=0.5):
        return [dict(e) for e in self._entities]


def test_anonymize_masque_un_nom(monkeypatch):
    """/anonymize remplace l'entité détectée par un token unique et la mappe."""
    monkeypatch.setattr(
        anone_api, "ner",
        _FakeNER([{"start": 0, "end": len("Jean Dupont"), "label": "person"}]),
    )

    r = client.post("/anonymize", json={"text": "Jean Dupont travaille à la DSI"})

    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["anonymized_text"] == "<PERSON_0> travaille à la DSI"
    assert body["pii_mapping"] == {"<PERSON_0>": "Jean Dupont"}
    assert body["entities_found"] == 1
    assert "Jean Dupont" not in body["anonymized_text"]


def test_anonymize_multi_entites_sans_derive_offset(monkeypatch):
    """Plusieurs PII : tokens uniques, splice droite-à-gauche, round-trip complet."""
    text = "Jean Dupont (jean.dupont@gov.pf) écrit à Marie Martin"
    monkeypatch.setattr(
        anone_api, "ner",
        _FakeNER([
            {"start": 0, "end": 11, "label": "person"},
            {"start": 13, "end": 31, "label": "email"},
            {"start": 41, "end": 53, "label": "person"},
        ]),
    )

    r = client.post("/anonymize", json={"text": text})
    body = r.json()

    assert body["status"] == "ok"
    assert body["anonymized_text"] == "<PERSON_0> (<EMAIL_0>) écrit à <PERSON_1>"
    assert body["pii_mapping"] == {
        "<PERSON_0>": "Jean Dupont",
        "<EMAIL_0>": "jean.dupont@gov.pf",
        "<PERSON_1>": "Marie Martin",
    }
    for raw in ("Jean Dupont", "jean.dupont@gov.pf", "Marie Martin"):
        assert raw not in body["anonymized_text"]

    # round-trip via /deanonymize
    d = client.post(
        "/deanonymize",
        json={"text": body["anonymized_text"], "pii_mapping": body["pii_mapping"]},
    )
    assert d.json()["text"] == text


def test_anonymize_503_si_modele_absent(monkeypatch):
    """ner is None -> HTTP 503 (jamais 200), pour le fail-closed de main.py."""
    monkeypatch.setattr(anone_api, "ner", None)

    r = client.post("/anonymize", json={"text": "Jean Dupont"})

    assert r.status_code == 503


def test_deanonymize_restaure_le_nom():
    """/deanonymize restaure les valeurs d'origine depuis pii_mapping."""
    r = client.post(
        "/deanonymize",
        json={
            "text": "<PERSON_0> travaille à la DSI",
            "pii_mapping": {"<PERSON_0>": "Jean Dupont"},
        },
    )

    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["text"] == "Jean Dupont travaille à la DSI"


def test_deanonymize_sans_mapping_renvoie_le_texte_intact():
    """Sans mapping, /deanonymize renvoie le texte inchangé (status no_mapping)."""
    r = client.post("/deanonymize", json={"text": "rien à restaurer"})
    body = r.json()
    assert body == {"text": "rien à restaurer", "status": "no_mapping"}
