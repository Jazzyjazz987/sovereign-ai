"""Tests du round-trip d'anonymisation Anone (anone_api.py).

Le pipeline GLiNER (transformers/torch) est stubé dans conftest.py : aucun
modèle n'est téléchargé. Pour /anonymize on injecte un faux NER ; /deanonymize
est testé tel quel (simple substitution via pii_mapping).

Limite connue (voir rapport B5) : /anonymize ne renvoie PAS de `pii_mapping` et
utilise des placeholders non uniques (`[person]`), alors que
`route_t5_with_anonymization` (main.py) lit `anon_data["pii_mapping"]`. Les deux
endpoints ne se composent donc pas automatiquement ; le round-trip est testé ici
sur chaque helper séparément.
"""
from fastapi.testclient import TestClient

import anone_api

client = TestClient(anone_api.app)


def test_anonymize_masque_un_nom(monkeypatch):
    """/anonymize remplace l'entité détectée par [type]."""

    def fake_ner(text):
        # Ce que GLiNER renverrait pour "Jean Dupont" (offsets 0..11).
        return [{"entity_group": "person", "start": 0, "end": len("Jean Dupont")}]

    monkeypatch.setattr(anone_api, "ner", fake_ner)

    r = client.post("/anonymize", json={"text": "Jean Dupont travaille à la DSI"})

    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert "Jean Dupont" not in body["anonymized_text"]
    assert body["anonymized_text"] == "[person] travaille à la DSI"


def test_deanonymize_restaure_le_nom():
    """/deanonymize restaure les valeurs d'origine depuis pii_mapping."""
    r = client.post(
        "/deanonymize",
        json={
            "text": "[person] travaille à la DSI",
            "pii_mapping": {"[person]": "Jean Dupont"},
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
