"""Service RAG — port 8090.

Endpoints :
  POST /search   {query, k?, rerank?, audience?, domaine?, rgpd_only?} -> {hits:[...]}
  POST /ingest   {path, corpus?}  -> stats  (admin : ré-ingestion d'un dossier monté)
  GET  /health
  GET  /metrics  (Prometheus)

Les modèles (e5-base + bge-reranker-base) sont chargés au démarrage (warm-up).
"""
from __future__ import annotations

import os
import time
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
from prometheus_client import Counter, Histogram, CONTENT_TYPE_LATEST, generate_latest

import store
from retriever import retrieve

app = FastAPI(title="RAG CPA", version="1.0")

RAG_RERANK_DEFAULT = os.getenv("RAG_RERANK", "on").lower() in ("1", "true", "on", "yes")

SEARCH_REQUESTS = Counter("rag_search_total", "Requêtes /search", ["status", "rerank"])
SEARCH_LATENCY = Histogram("rag_search_latency_seconds", "Latence /search")
NO_HIT = Counter("rag_search_no_hit_total", "Recherches sans résultat exploitable")


class SearchIn(BaseModel):
    query: str
    k: int = 5
    rerank: bool | None = None
    audience: str | None = None          # 'atelier' | 'teleassistance' (Jalon B — pas encore filtré)
    domaine: str | None = None
    rgpd_only: bool = False


class IngestIn(BaseModel):
    path: str
    corpus: str = "procedures-legacy"


@app.on_event("startup")
def _warm() -> None:
    from embed import embed_query
    embed_query("préchauffage")
    if RAG_RERANK_DEFAULT:
        from rerank import rerank as _rr
        _rr("préchauffage", [{"text": "préchauffage"}], top_k=1)
    print("[rag] modèles chargés", flush=True)


@app.post("/search")
def search(inp: SearchIn):
    rr = RAG_RERANK_DEFAULT if inp.rerank is None else inp.rerank
    t0 = time.perf_counter()
    try:
        hits = retrieve(inp.query, k=inp.k, rerank=rr, domaine=inp.domaine,
                        rgpd_only=inp.rgpd_only)
    except Exception as e:  # noqa: BLE001
        SEARCH_REQUESTS.labels(status="error", rerank=str(rr)).inc()
        raise HTTPException(status_code=500, detail=f"recherche KO: {e}")
    SEARCH_LATENCY.observe(time.perf_counter() - t0)
    SEARCH_REQUESTS.labels(status="ok", rerank=str(rr)).inc()
    if not hits:
        NO_HIT.inc()
    return {
        "query": inp.query,
        "count": len(hits),
        "hits": [
            {k: h.get(k) for k in (
                "chunk_id", "doc_id", "proc_code", "titre", "domaine", "section",
                "sla", "criticite", "contrainte_rgpd", "source_url", "source_file",
                "related", "text", "score", "vector_score", "rerank_score")}
            for h in hits
        ],
    }


@app.post("/ingest")
def ingest_dir(inp: IngestIn):
    from ingest import run
    p = Path(inp.path)
    if not p.is_dir():
        raise HTTPException(status_code=400, detail=f"dossier introuvable: {p}")
    return run(p, inp.corpus)


@app.get("/health")
def health():
    try:
        st = store.stats()
        db_ok = True
    except Exception as e:  # noqa: BLE001
        st, db_ok = {"error": str(e)}, False
    return {
        "status": "healthy" if db_ok else "degraded",
        "service": "rag",
        "db": db_ok,
        "corpus": st,
        "models": {
            "embed": os.getenv("RAG_EMBED_MODEL", "intfloat/multilingual-e5-base"),
            "rerank": os.getenv("RAG_RERANK_MODEL", "BAAI/bge-reranker-base"),
            "rerank_default": RAG_RERANK_DEFAULT,
        },
    }


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8090)
