"""Filtres déterministes en amont de tout modèle (voie de sauvegarde + hors-périmètre).

Chargé au démarrage depuis config/screening.yaml (fail-soft : si le fichier manque, on
tombe sur des valeurs par défaut minimales — jamais d'exception qui casse /query).
"""
from __future__ import annotations

import os
import unicodedata

import yaml

SCREENING_PATH = os.getenv("SCREENING_PATH", "/app/config/screening.yaml")

_DEFAULT = {
    "safeguarding": {
        "patterns": ["suicide", "me suicider", "envie d'en finir", "me faire du mal", "me tuer"],
        "card": ("⚠️ Situation sensible. Cet outil ne traite pas ce type de demande.\n"
                 "Urgences : SAMU 15 · Police/Gendarmerie 17 · Pompiers 18\n"
                 "SOS Suicide Polynésie : 40 44 47 48"),
    },
    "out_of_scope": {"patterns": [], "scope_lexicon": [],
                     "card": "Cette demande sort du périmètre du support CPA."},
}


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s.lower())
    return "".join(c for c in s if not unicodedata.combining(c))


def _load(path: str) -> dict:
    try:
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
    except (OSError, yaml.YAMLError):
        return _DEFAULT
    for k in ("safeguarding", "out_of_scope"):
        data.setdefault(k, _DEFAULT[k])
    return data


_CFG = _load(SCREENING_PATH)
_SG_PATTERNS = [_norm(p) for p in (_CFG["safeguarding"].get("patterns") or [])]
_SG_CARD = _CFG["safeguarding"].get("card", _DEFAULT["safeguarding"]["card"]).strip()
_OOS_PATTERNS = [_norm(p) for p in (_CFG["out_of_scope"].get("patterns") or [])]
_SCOPE_LEX = [_norm(w) for w in (_CFG["out_of_scope"].get("scope_lexicon") or [])]
_OOS_CARD = _CFG["out_of_scope"].get("card", _DEFAULT["out_of_scope"]["card"]).strip()

CONFIG_FINGERPRINT = None
try:
    import hashlib
    with open(SCREENING_PATH, "rb") as _f:
        CONFIG_FINGERPRINT = hashlib.sha256(_f.read()).hexdigest()[:12]
except OSError:
    pass


def safeguarding(query: str) -> dict | None:
    """Signal de détresse → carte d'aide. AUCUN modèle appelé. Priorité absolue."""
    q = _norm(query)
    if any(p in q for p in _SG_PATTERNS):
        return {
            "status": "ok",
            "query": query,
            "response": _SG_CARD,
            "tier": "sauvegarde",
            "label": "Voie de sauvegarde",
            "model_used": None,
            "message": "Filtre de sauvegarde déclenché — aucun modèle appelé.",
        }
    return None


def looks_in_scope(query: str) -> bool:
    """True si la requête contient au moins un terme du vocabulaire support CPA."""
    q = _norm(query)
    return any(w in q for w in _SCOPE_LEX)


def is_out_of_scope(query: str) -> bool:
    """True si la requête matche un motif hors-périmètre ET aucun terme support."""
    q = _norm(query)
    return any(p in q for p in _OOS_PATTERNS) and not any(w in q for w in _SCOPE_LEX)


def out_of_scope_card(query: str) -> dict:
    return {
        "status": "ok",
        "query": query,
        "response": _OOS_CARD,
        "tier": "hors-perimetre",
        "label": "Hors périmètre",
        "model_used": None,
        "message": "Requête hors du périmètre support CPA — aucun modèle appelé.",
    }
