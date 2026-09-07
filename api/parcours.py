"""Réponses canoniques « parcours agent » (D8) — arrivée / départ / mutation.

Ces événements croisent plusieurs procédures de domaines différents ; le RAG ne les
synthétise pas de façon fiable. Réponse rédigée, tracée aux fiches, servie avant le RAG.
Chargé depuis config/parcours.yaml (fail-soft).
"""
from __future__ import annotations

import hashlib
import os
import unicodedata

import yaml

PARCOURS_PATH = os.getenv("PARCOURS_PATH", "/app/config/parcours.yaml")


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s.lower())
    return "".join(c for c in s if not unicodedata.combining(c))


def _load(path: str) -> dict:
    try:
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except (OSError, yaml.YAMLError):
        return {}


_CFG = _load(PARCOURS_PATH)
VALIDATED = bool(_CFG.get("validated", False))
_ENTRIES = []
for p in (_CFG.get("parcours") or []):
    _ENTRIES.append({
        "id": p.get("id"),
        "titre": p.get("titre"),
        "patterns": [_norm(x) for x in (p.get("patterns") or [])],
        "anti": [_norm(x) for x in (p.get("anti") or [])],
        "fiches": list(p.get("fiches") or []),
        "reponse": (p.get("reponse") or "").strip(),
    })

CONFIG_FINGERPRINT = None
try:
    with open(PARCOURS_PATH, "rb") as _f:
        CONFIG_FINGERPRINT = hashlib.sha256(_f.read()).hexdigest()[:12]
except OSError:
    pass

_WARN = ("\n\n⚠️ Réponse de référence non encore validée par le chef de cellule CPA "
         "(parcours.yaml : validated).")


def match(query: str) -> dict | None:
    q = _norm(query)
    for e in _ENTRIES:
        if any(a in q for a in e["anti"]):
            continue
        if any(pat in q for pat in e["patterns"]):
            txt = e["reponse"] + ("" if VALIDATED else _WARN)
            return {
                "status": "ok",
                "query": query,
                "response": txt,
                "model_used": None,
                "tier": "parcours",
                "label": "Parcours de référence CPA" if VALIDATED
                         else "Parcours de référence CPA — à valider",
                "fiches": [{"code": c} for c in e["fiches"]],
                "parcours_id": e["id"],
                "message": f"Réponse canonique « {e['titre']} » — aucun modèle appelé.",
            }
    return None
