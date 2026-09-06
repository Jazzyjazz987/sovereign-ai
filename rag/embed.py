"""Embeddings locaux — `intfloat/multilingual-e5-base` sur CPU.

e5 attend un préfixe : `query: ` pour une requête, `passage: ` pour un document.
Le chunker met déjà `passage: ` en tête de chaque chunk ; ici on ne préfixe que les requêtes.
"""
from __future__ import annotations

import os
import threading

_MODEL_NAME = os.getenv("RAG_EMBED_MODEL", "intfloat/multilingual-e5-base")
DIM = 768

_model = None
_lock = threading.Lock()


def _get_model():
    global _model
    if _model is None:
        with _lock:
            if _model is None:
                from sentence_transformers import SentenceTransformer
                _model = SentenceTransformer(_MODEL_NAME, device="cpu")
    return _model


def embed_passages(texts: list[str], batch_size: int = 16) -> list[list[float]]:
    m = _get_model()
    vecs = m.encode(texts, batch_size=batch_size, normalize_embeddings=True,
                    show_progress_bar=len(texts) > 64)
    return [v.tolist() for v in vecs]


def embed_query(text: str) -> list[float]:
    m = _get_model()
    v = m.encode(f"query: {text}", normalize_embeddings=True)
    return v.tolist()
