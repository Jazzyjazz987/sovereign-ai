"""Périmètres de connaissance (Jalon B) — atelier (interne, tout) vs téléassistance
(prestataire externe, liste blanche). Chargé depuis config/rag/audiences.yaml.
"""
from __future__ import annotations

import hashlib
import os

import yaml

PATH = os.getenv("RAG_AUDIENCES_PATH", "/app/config/rag/audiences.yaml")

_cfg: dict = {}
try:
    with open(PATH, encoding="utf-8") as _f:
        _cfg = yaml.safe_load(_f) or {}
except (OSError, yaml.YAMLError):
    _cfg = {}

VALIDATED: bool = bool(_cfg.get("validated", False))
_TA = _cfg.get("teleassistance") or {}
TELEASSISTANCE_FICHES: set[str] = {str(c).upper() for c in (_TA.get("fiches") or [])}
TELEASSISTANCE_HIDE_SOURCE: bool = bool(_TA.get("hide_source", True))
PROFILES = ("atelier", "teleassistance")

FINGERPRINT = None
try:
    with open(PATH, "rb") as _f:
        FINGERPRINT = hashlib.sha256(_f.read()).hexdigest()[:12]
except OSError:
    pass


def audience_for(proc_code: str | None) -> str:
    """Tag d'audience d'un chunk : 'teleassistance' si la fiche est en liste blanche,
    sinon 'atelier' (= interne uniquement)."""
    if proc_code and proc_code.upper() in TELEASSISTANCE_FICHES:
        return "teleassistance"
    return "atelier"


def normalize(profile: str | None) -> str:
    p = (profile or "atelier").strip().lower()
    return p if p in PROFILES else "atelier"
