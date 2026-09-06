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
        hits = _rr(query, hits, top_k=k)
    return hits[:k]
