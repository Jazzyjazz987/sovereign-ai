"""Point d'entrée récupération : embed requête → recherche vecteur → rerank optionnel."""
from __future__ import annotations

from embed import embed_query
import store


def retrieve(query: str, k: int = 5, *, rerank: bool = True, candidates: int = 12,
             domaine: str | None = None, rgpd_only: bool = False,
             corpora: tuple[str, ...] = store.DEFAULT_CORPORA) -> list[dict]:
    n = max(k, candidates) if rerank else k
    hits = store.search(embed_query(query), k=n, domaine=domaine,
                        rgpd_only=rgpd_only, corpora=corpora)
    if rerank and hits:
        from rerank import rerank as _rr
        hits = _rr(query, hits, top_k=n)  # rerank tout le pool, on tronque après
    # Les pages sans proc_code (index 00-*, RACI, registre) sont du contexte, pas des
    # fiches citables : on les place APRÈS les procédures (tri stable, E1).
    hits.sort(key=lambda h: 0 if h.get("proc_code") else 1)
    return hits[:k]
