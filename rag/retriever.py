"""Récupération hybride : vecteur + lexical + reranker, fusionnés par RRF (E2).

Le reranker seul se laisse piéger par la forme (table « Étapes », motif « délai … »).
On le traite comme UN classement parmi trois et on fusionne : l'exact-match lexical
(« BALP », « E3 », « PROC-ID-007 », noms d'îles) garde alors du poids.

Expansion `related` (C9) : les procédures citées en « Procédures liées » par le top des
résultats sont ajoutées en queue (marquées `via_related`) — utile aux questions larges
multi-domaine (« un agent part : compte ET matériel »).
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
            if cid not in keep:
                keep[cid] = h
            else:
                # fusionne les champs présents (ex. rerank_score posé par une seule des listes)
                for kk, vv in h.items():
                    if vv is not None and keep[cid].get(kk) is None:
                        keep[cid][kk] = vv
    fused = sorted(keep.values(), key=lambda h: score[h["chunk_id"]], reverse=True)
    for h in fused:
        h["rrf_score"] = round(score[h["chunk_id"]], 5)
    return fused


def _expand_related(hits: list[dict], k: int, query: str, rerank: bool,
                    audience: str | None) -> list[dict]:
    """Ajoute en contexte les procédures citées en « Procédures liées » par les
    meilleures fiches du résultat (champ `related`)."""
    present = {h.get("proc_code") for h in hits if h.get("proc_code")}
    wanted: list[str] = []
    for h in hits[:max(2, k)]:
        for code in (h.get("related") or []):
            if code and code not in present and code not in wanted:
                wanted.append(code)
    if not wanted:
        return hits
    extra = store.chunks_for_codes(wanted[:4], audience=audience)
    if not extra:
        return hits
    if rerank:
        from rerank import rerank as _rr
        extra = _rr(query, extra, top_k=len(extra))
    for e in extra:
        e["via_related"] = True
    return hits + extra


def retrieve(query: str, k: int = 5, *, rerank: bool = True, hybrid: bool = True,
             expand_related: bool = True, domaine: str | None = None,
             rgpd_only: bool = False, audience: str | None = None,
             corpora: tuple[str, ...] = store.DEFAULT_CORPORA) -> list[dict]:
    vec = store.search(embed_query(query), k=POOL, domaine=domaine,
                       rgpd_only=rgpd_only, audience=audience, corpora=corpora)
    lex = (store.search_lexical(query, k=POOL, domaine=domaine, audience=audience,
                                corpora=corpora)
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
    top = fused[:k]
    if expand_related:
        top = _expand_related(top, k, query, rerank, audience)
    return top
