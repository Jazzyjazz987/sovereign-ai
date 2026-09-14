#!/usr/bin/env python3
"""Jeu d'éval RAG — boucle test → diagnostic → correction (docs/RAG_ROADMAP.md § Jalon C).

Interroge les SERVICES (pas les modules) : rien à installer à part pyyaml.

    python eval/run.py                 # récupération seule (rag:8090/search) — rapide
    python eval/run.py --full          # pipeline complet (langgraph:8888/query) — lent
    python eval/run.py --palier 1 -v   # détail des échecs d'un palier

Métriques :
    recall@1 / recall@5   la bonne fiche sort-elle en tête / dans le top-k
    citation_ok           la réponse s'appuie sur une fiche attendue (mode --full)
    attendu_ok            les valeurs exactes attendues figurent dans la réponse
    couverture_ok         palier 3 : toutes les fiches obligatoires sont citées
    interdit_ok           aucun fragment interdit dans la réponse
    tier_ok               paliers 4-5 : la requête a bien été aiguillée (sauvegarde,
                          hors-perimetre…) plutôt que répondue librement
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import unicodedata
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path

import yaml

DATASET = Path(__file__).with_name("dataset.yaml")
RAG_URL = os.getenv("RAG_EVAL_URL", "http://localhost:8090")
API_URL = "http://localhost:8888"

# ordre d'affichage des mesures ; une mesure absente d'un cas est simplement ignorée
MESURES = ["at1", "atk", "citation_ok", "attendu_ok", "interdit_ok", "couverture_ok", "tier_ok"]


def _post(url: str, payload: dict, timeout: int) -> dict:
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def _norm(s: str) -> str:
    """minuscules sans accents — pour comparer les fragments attendus."""
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def _codes(hits: list[dict]) -> list[str]:
    """codes de fiches dans l'ordre, dédoublonnés (plusieurs chunks d'une même fiche)."""
    out = []
    for h in hits:
        c = h.get("proc_code") or h.get("doc_id")
        if c and c not in out:
            out.append(c)
    return out


def eval_retrieval(cas: dict, k: int) -> dict | None:
    """None = cas sans fiche attendue (paliers 4-5) : rien à mesurer en récupération."""
    if not cas.get("gold"):
        return None
    hits = _post(f"{RAG_URL}/search", {"query": cas["q"], "k": k}, 60)["hits"]
    codes = _codes(hits)
    gold = cas["gold"]
    return {
        "at1": bool(codes) and codes[0] in gold,
        "atk": any(c in gold for c in codes),
        "codes": codes,
    }


def eval_full(cas: dict) -> dict:
    res = _post(f"{API_URL}/query", {"query": cas["q"]}, 300)
    codes = [f["code"] for f in res.get("fiches", [])]
    gold = cas.get("gold") or []
    rep = _norm(res.get("response", ""))
    # un « attendu » / « interdit » peut lister des variantes separees par « | »
    manquants = [a for a in cas.get("attendu", [])
                 if not any(_norm(v) in rep for v in a.split("|"))]
    interdits = [i for i in cas.get("interdit", [])
                 if any(_norm(v) in rep for v in i.split("|"))]
    non_couverts = [c for c in cas.get("couvre", []) if c not in codes]
    r = {
        "attendu_ok": not manquants,
        "interdit_ok": not interdits,
        "couverture_ok": not non_couverts,
        "codes": codes,
        "tier": res.get("tier"),
        "manquants": manquants,
        "interdits": interdits,
        "non_couverts": non_couverts,
        "reponse": res.get("response", ""),
    }
    if gold:
        r["at1"] = bool(codes) and codes[0] in gold
        r["atk"] = any(c in gold for c in codes)
        r["citation_ok"] = any(c in gold for c in codes)
    if cas.get("tier_attendu"):
        r["tier_ok"] = res.get("tier") == cas["tier_attendu"]
    return r


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--full", action="store_true", help="pipeline complet via /query")
    ap.add_argument("--palier", type=int, action="append", help="ne garder que ce(s) palier(s)")
    ap.add_argument("-k", type=int, default=5)
    ap.add_argument("-v", "--verbose", action="store_true", help="détailler les échecs")
    args = ap.parse_args()

    cas_list = yaml.safe_load(DATASET.read_text(encoding="utf-8"))
    if args.palier:
        cas_list = [c for c in cas_list if c["palier"] in args.palier]

    par_palier: dict[int, list] = defaultdict(list)
    echecs = []
    for cas in cas_list:
        try:
            r = eval_full(cas) if args.full else eval_retrieval(cas, args.k)
        except (urllib.error.URLError, TimeoutError) as e:
            print(f"!! service injoignable ({e}) — la stack tourne-t-elle ?", file=sys.stderr)
            return 2
        if r is None:
            continue
        par_palier[cas["palier"]].append(r)
        rate = [m for m in MESURES if m in r and not r[m]]
        mark = "✓" if not rate else "✗"
        print(f"{mark} P{cas['palier']} {cas['id']:24s} {'/'.join(r['codes'][:3]) or '—':38s}"
              f"{' KO:' + ','.join(rate) if rate else ''}")
        if rate:
            echecs.append((cas, r))

    print()
    mesures = MESURES if args.full else ["at1", "atk"]
    for p in sorted(par_palier):
        rs = par_palier[p]
        parts = []
        for m in mesures:
            vals = [r[m] for r in rs if m in r]
            if vals:
                nom = {"at1": f"recall@1", "atk": f"recall@{args.k}"}.get(m, m)
                parts.append(f"{nom} {sum(vals)}/{len(vals)} ({sum(vals)/len(vals):.0%})")
        print(f"palier {p} ({len(rs)} cas) : " + "   ".join(parts))

    if args.verbose and echecs:
        print("\n--- échecs détaillés ---")
        for cas, r in echecs:
            print(f"\n« {cas['q']} »\n  fiches attendues : {'/'.join(cas.get('gold') or ['—'])}"
                  f"\n  fiches obtenues  : {r['codes'] or '—'}   tier={r.get('tier')}"
                  + (f" (attendu {cas['tier_attendu']})" if cas.get('tier_attendu') else ""))
            if r.get("interdits"):
                print(f"  fragments interdits présents : {r['interdits']}")
            if r.get("manquants"):
                print(f"  fragments absents : {r['manquants']}")
            if r.get("non_couverts"):
                print(f"  fiches non citées : {r['non_couverts']}")
            if r.get("reponse"):
                print("  réponse :", r["reponse"][:400].replace("\n", " "))

    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(main())
