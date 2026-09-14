"""Clarification déterministe pour les termes ambigus (D8 bis).

« poste » désigne soit un poste informatique (ordinateur), soit un poste/emploi (RH).
Une requête comme « comment réaffecter un poste » se fait aujourd'hui happer par le
parcours « mutation-agent » (RH) par collision de sous-chaîne sur « reaffect » — silencieux,
sans jamais soupçonner l'autre sens. Ici, si aucun des deux signaux n'est présent, on pose
la question à l'agent CPA plutôt que de trancher au hasard. AUCUN modèle appelé.

Chargé depuis config/disambiguation.yaml (fail-soft — cf. screening.py / parcours.py).
"""
from __future__ import annotations

import hashlib
import os
import unicodedata

import yaml

DISAMBIGUATION_PATH = os.getenv("DISAMBIGUATION_PATH", "/app/config/disambiguation.yaml")


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s.lower())
    return "".join(c for c in s if not unicodedata.combining(c))


def _load(path: str) -> dict:
    try:
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except (OSError, yaml.YAMLError):
        return {}


_CFG = _load(DISAMBIGUATION_PATH)
VALIDATED = bool(_CFG.get("validated", False))
_ENTRIES = []
for e in (_CFG.get("termes") or []):
    _ENTRIES.append({
        "id": e.get("id"),
        "patterns": [_norm(x) for x in (e.get("patterns") or [])],
        "device_signals": [_norm(x) for x in (e.get("device_signals") or [])],
        "job_signals": [_norm(x) for x in (e.get("job_signals") or [])],
        "question": (e.get("question") or "").strip(),
    })

CONFIG_FINGERPRINT = None
try:
    with open(DISAMBIGUATION_PATH, "rb") as _f:
        CONFIG_FINGERPRINT = hashlib.sha256(_f.read()).hexdigest()[:12]
except OSError:
    pass

_WARN = ("\n\n⚠️ Question de clarification non encore relue par le chef de cellule CPA "
         "(disambiguation.yaml : validated).")


def clarify(query: str) -> dict | None:
    q = _norm(query)
    for e in _ENTRIES:
        if not any(pat in q for pat in e["patterns"]):
            continue
        if any(sig in q for sig in e["device_signals"]):
            continue  # contexte déjà clair — pas de clarification
        if any(sig in q for sig in e["job_signals"]):
            continue
        txt = e["question"] + ("" if VALIDATED else _WARN)
        return {
            "status": "ok",
            "query": query,
            "response": txt,
            "model_used": None,
            "tier": "clarification",
            "label": "Clarification nécessaire" if VALIDATED
                     else "Clarification nécessaire — à valider",
            "fiches": [],
            "ambiguity_id": e["id"],
            "message": f"Terme ambigu « {e['id']} » — question posée, aucun modèle appelé.",
        }
    return None
