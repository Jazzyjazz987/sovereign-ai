"""Récupération hybride : vecteur + lexical + reranker, fusionnés par RRF (E2).

Le reranker seul se laisse piéger par la forme (table « Étapes », motif « délai … »).
On le traite comme UN classement parmi trois et on fusionne : l'exact-match lexical
(« BALP », « E3 », « PROC-ID-007 », noms d'îles) garde alors du poids.
"""
from __future__ import annotations

from embed import embed_query
import store

RRF_K = 60
POOL = 20           # profondeur de chaque classement avant fusion


def _rrf(*ranked_lists: list[dict]) -> list[dict]:
    score: dict[str, float] = {}
    keep: dict[str, dict] = {}
    for lst in ranked_lists:
        for rank, h in enumerate(lst):
            cid = h["chunk_id"]
            score[cid] = score.get(cid, 0.0) + 1.0 / (RRF_K + rank)
            keep.setdefault(cid, h)
    fused = sorted(keep.values(), key=lambda h: score[h["chunk_id"]], reverse=True)
    for h in fused:
        h["rrf_score"] = round(score[h["chunk_id"]], 5)
    return fused


def retrieve(query: str, k: int = 5, *, rerank: bool = True, hybrid: bool = True,
             domaine: str | None = None, rgpd_only: bool = False,
             corpora: tuple[str, ...] = store.DEFAULT_CORPORA) -> list[dict]:
    vec = store.search(embed_query(query), k=POOL, domaine=domaine,
                       rgpd_only=rgpd_only, corpora=corpora)
    lex = (store.search_lexical(query, k=POOL, domaine=domaine, corpora=corpora)
           if hybrid and not rgpd_only else [])

    lists = [vec] + ([lex] if lex else [])
    if rerank:
        union = list({h["chunk_id"]: h for lst in lists for h in lst}.values())
        if union:
            from rerank import rerank as _rr
            lists.append(_rr(query, union, top_k=len(union)))

    fused = _rrf(*lists) if len(lists) > 1 else (lists[0] if lists else [])
    # Pages sans proc_code (00-*, RACI, registre) = contexte, pas fiche citable (E1).
    fused.sort(key=lambda h: 0 if h.get("proc_code") else 1)
    return fused[:k]
