"""Ingestion d'un dossier de corpus dans pgvector.

Usage :  python ingest.py corpus/01-procedures-legacy [--corpus procedures-legacy]
"""
from __future__ import annotations

import argparse
import time
from pathlib import Path

from chunker import chunk_corpus
from embed import embed_passages
import store

# Pages purement navigationnelles : indexées à part (corpus 'procedures-nav'),
# exclues de la recherche par défaut — elles citent plein de PROC-xxx et polluent
# les résultats sur les requêtes larges. RACI + Registre RGPD restent dans le corpus
# principal (ils répondent à de vraies questions « qui fait quoi / contraintes »).
NAV_FILES = {
    "00-accueil-cpa-dsi-polynesie-francaise.md",
    "00-synthese-du-projet-de-formalisation-cpa.md",
    "00-onboarding-parcours-nouvel-agent-cpa.md",
    "00-atelier.md", "00-console-intune.md", "00-entraid-exchange.md",
    "00-gestion-du-stock.md", "00-agents-de-proximite-terrain.md",
}


def _corpus_for(row: dict, base: str) -> str:
    return "procedures-nav" if row["source_file"] in NAV_FILES else base


def run(root: Path, corpus: str) -> dict:
    t0 = time.time()
    chunks = chunk_corpus(root)
    rows = [c.as_row() for c in chunks]
    for r in rows:
        r["corpus"] = _corpus_for(r, corpus)
    texts = [r["text"] for r in rows]
    vecs = embed_passages(texts)
    store.init_db()
    store.replace_corpora(rows, vecs)
    from collections import Counter
    by = Counter(r["corpus"] for r in rows)
    return {"docs": len({r["doc_id"] for r in rows}), "chunks": len(rows),
            "par_corpus": dict(by), "seconds": round(time.time() - t0, 1)}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("root", type=Path)
    ap.add_argument("--corpus", default="procedures-legacy")
    args = ap.parse_args()
    print(run(args.root, args.corpus))
    print(store.stats())
