"""Reranker cross-encoder — `BAAI/bge-reranker-v2-m3` sur CPU.

Le bi-encodeur (e5) récupère un large top-N vite mais tasse les scores. Le cross-encodeur
lit (requête, passage) ensemble et sépare bien le pertinent du bruit. On l'applique en
2e passe : top-N vecteur → rerank → top-k.
"""
from __future__ import annotations

import os
import threading

# bge-reranker-base (278M, multilingue FR) : ~1,8 s pour 12 candidats sur CPU 16 threads,
# 6/6 sur le jeu difficile. bge-reranker-v2-m3 (568M) est ~1 pt meilleur mais ~12 s/req
# sur CPU — à réserver à une variante ONNX-INT8 ou GPU. Surchargeable via RAG_RERANK_MODEL.
_MODEL_NAME = os.getenv("RAG_RERANK_MODEL", "BAAI/bge-reranker-base")
_THREADS = int(os.getenv("RAG_TORCH_THREADS", "0")) or None
_model = None
_lock = threading.Lock()


def _get_model():
    global _model
    if _model is None:
        with _lock:
            if _model is None:
                if _THREADS:
                    import torch
                    torch.set_num_threads(_THREADS)
                from sentence_transformers import CrossEncoder
                _model = CrossEncoder(_MODEL_NAME, device="cpu", max_length=512)
    return _model


def rerank(query: str, hits: list[dict], top_k: int = 5, text_key: str = "text") -> list[dict]:
    """Trie `hits` par pertinence (query, hit[text_key]) et renvoie les `top_k` meilleurs.

    Chaque hit reçoit `rerank_score` ; `score` (cosinus e5) est conservé sous `vector_score`.
    """
    if not hits:
        return []
    model = _get_model()
    # C19 : le préfixe « passage: » (pour e5) n'a rien à faire dans une paire cross-encoder.
    pairs = [(query, h[text_key].split("\n", 1)[-1] if h[text_key].startswith("passage:")
              else h[text_key]) for h in hits]
    scores = model.predict(pairs, batch_size=16, show_progress_bar=False)
    for h, s in zip(hits, scores):
        h["vector_score"] = h.get("score")
        h["rerank_score"] = float(s)
    hits.sort(key=lambda h: h["rerank_score"], reverse=True)
    return hits[:top_k]
