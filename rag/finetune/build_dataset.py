"""Construit le jeu d'entraînement du reranker à partir des questions synthétiques
(queries.jsonl). Négatifs durs = chunks bien classés par le reranker ACTUEL mais
d'une autre procédure que la fiche cible.

eval/dataset.yaml est volontairement EXCLU : il reste le held-out de mesure.

Sortie : rag/finetune/train.jsonl / val.jsonl  — {query, passage, label}
À lancer avec .venv-rag (récupération CPU).
"""
from __future__ import annotations

import json
import random
import sys
from pathlib import Path

sys.path.insert(0, "rag")
from embed import embed_query          # noqa: E402
import store                            # noqa: E402
from rerank import rerank as _rerank    # noqa: E402

FT = Path("rag/finetune")
random.seed(13)

NEG_PER_Q = 4
POS_PER_Q = 3
CAND = 20


def _load_queries() -> list[dict]:
    # UNIQUEMENT les questions synthétiques : eval/dataset.yaml reste un held-out honnête
    # (constat 5 — « éval itérée contre elle-même »). Le fine-tune ne doit jamais voir
    # les formulations d'opérateur qui servent à le mesurer.
    rows = [json.loads(l) for l in (FT / "queries.jsonl").read_text().splitlines() if l.strip()]
    random.shuffle(rows)
    return rows


def _passage(h: dict) -> str:
    t = h.get("text") or ""
    return t.split("\n", 1)[-1] if t.startswith("passage:") else t


def main():
    rows = _load_queries()
    print(f"{len(rows)} (q, proc_code)")
    examples: list[dict] = []
    for i, r in enumerate(rows, 1):
        q, gold = r["q"], r["proc_code"]
        vec = store.search(embed_query(q), k=CAND)
        lex = store.search_lexical(q, k=CAND)
        union = list({h["chunk_id"]: h for h in vec + lex}.values())
        if not union:
            continue
        ranked = _rerank(q, union, top_k=len(union))
        pos = [h for h in ranked if h.get("proc_code") == gold][:POS_PER_Q]
        neg = [h for h in ranked if h.get("proc_code") and h.get("proc_code") != gold][:NEG_PER_Q]
        if not pos:  # la fiche cible n'a rien été récupéré — on prend son meilleur chunk direct
            direct = store.chunks_for_codes([gold])
            pos = direct[:1]
        for h in pos:
            examples.append({"query": q, "passage": _passage(h), "label": 1.0})
        for h in neg:
            examples.append({"query": q, "passage": _passage(h), "label": 0.0})
        if i % 50 == 0:
            print(f"  {i}/{len(rows)}  ({len(examples)} exemples)", flush=True)

    random.shuffle(examples)
    n_val = max(40, len(examples) // 10)
    val, train = examples[:n_val], examples[n_val:]
    (FT / "train.jsonl").write_text("\n".join(json.dumps(e, ensure_ascii=False) for e in train))
    (FT / "val.jsonl").write_text("\n".join(json.dumps(e, ensure_ascii=False) for e in val))
    pos_n = sum(1 for e in train if e["label"] == 1.0)
    print(f"\ntrain {len(train)} ({pos_n} pos / {len(train)-pos_n} neg) · val {len(val)}")


if __name__ == "__main__":
    main()
