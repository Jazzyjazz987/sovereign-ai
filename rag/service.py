"""Service RAG — port 8090.

Endpoints :
  POST /search   {query, k?, rerank?, audience?, domaine?, rgpd_only?} -> {hits:[...]}
  POST /ingest   {path, corpus?}  -> stats  (admin : ré-ingestion d'un dossier monté)
  GET  /health
  GET  /metrics  (Prometheus)

Les modèles (e5-base + bge-reranker-base) sont chargés au démarrage (warm-up).
"""
from __future__ import annotations

import contextlib
import os
import threading
import time
from pathlib import Path

from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel, Field
from prometheus_client import Counter, Gauge, Histogram, CONTENT_TYPE_LATEST, generate_latest

import audiences
import store
from retriever import retrieve

RAG_RERANK_DEFAULT = os.getenv("RAG_RERANK", "on").lower() in ("1", "true", "on", "yes")
# /ingest désactivé sauf si un jeton est configuré (C4). Vide => endpoint fermé.
RAG_ADMIN_TOKEN = os.getenv("RAG_ADMIN_TOKEN", "").strip()
# C14 : le reranker + les embeddings sont CPU-bound. On borne les recherches simultanées ;
# au-delà, 503 « occupé » plutôt qu'une file qui gonfle sans limite.
RAG_MAX_CONCURRENCY = int(os.getenv("RAG_MAX_CONCURRENCY", "3"))
_slots = threading.BoundedSemaphore(RAG_MAX_CONCURRENCY)

SEARCH_REQUESTS = Counter("rag_search_total", "Requêtes /search", ["status", "rerank"])
SEARCH_LATENCY = Histogram("rag_search_latency_seconds", "Latence /search")
SEARCH_BUSY = Counter("rag_search_busy_total", "Recherches refusées (concurrence max)")
SEARCH_INFLIGHT = Gauge("rag_search_inflight", "Recherches en cours")
NO_HIT = Counter("rag_search_no_hit_total", "Recherches sans résultat exploitable")


@contextlib.asynccontextmanager
async def _lifespan(app: FastAPI):
    with contextlib.suppress(Exception):
        store.init_db()                  # C17 : schéma en place même sur volume vierge
    from embed import embed_query
    embed_query("préchauffage")
    if RAG_RERANK_DEFAULT:
        from rerank import rerank as _rr
        _rr("préchauffage", [{"text": "préchauffage"}], top_k=1)
    print("[rag] modèles chargés", flush=True)
    yield


app = FastAPI(title="RAG CPA", version="1.0", lifespan=_lifespan)


class SearchIn(BaseModel):
    query: str = Field(min_length=1, max_length=2000)
    k: int = Field(5, ge=1, le=20)       # C16 : k borné
    rerank: bool | None = None
    audience: str | None = None          # 'atelier' (défaut, tout) | 'teleassistance' (liste blanche)
    domaine: str | None = None
    rgpd_only: bool = False


class IngestIn(BaseModel):
    path: str
    corpus: str = "procedures-legacy"


@app.post("/search")
def search(inp: SearchIn):
    rr = RAG_RERANK_DEFAULT if inp.rerank is None else inp.rerank
    if not _slots.acquire(timeout=2):                       # C14
        SEARCH_BUSY.inc()
        raise HTTPException(status_code=503, detail="service occupé, réessayez")
    SEARCH_INFLIGHT.inc()
    t0 = time.perf_counter()
    try:
        hits = retrieve(inp.query, k=inp.k, rerank=rr, domaine=inp.domaine,
                        rgpd_only=inp.rgpd_only, audience=inp.audience)
    except Exception as e:  # noqa: BLE001
        SEARCH_REQUESTS.labels(status="error", rerank=str(rr)).inc()
        raise HTTPException(status_code=500, detail=f"recherche KO: {e}")
    finally:
        SEARCH_INFLIGHT.dec()
        _slots.release()
    SEARCH_LATENCY.observe(time.perf_counter() - t0)
    SEARCH_REQUESTS.labels(status="ok", rerank=str(rr)).inc()
    if not hits:
        NO_HIT.inc()
    # D-B3 : profil téléassistance -> on ne renvoie pas le lien Confluence interne.
    hide_src = (audiences.normalize(inp.audience) == "teleassistance"
                and audiences.TELEASSISTANCE_HIDE_SOURCE)
    fields = ("chunk_id", "doc_id", "proc_code", "titre", "domaine", "section",
              "sla", "criticite", "contrainte_rgpd", "source_url", "source_file",
              "related", "text", "score", "vector_score", "rerank_score")
    return {
        "query": inp.query,
        "audience": audiences.normalize(inp.audience),
        "count": len(hits),
        "hits": [
            {k: (None if (k == "source_url" and hide_src) else h.get(k)) for k in fields}
            for h in hits
        ],
    }


@app.post("/ingest")
def ingest_dir(inp: IngestIn, x_admin_token: str | None = Header(default=None)):
    if not RAG_ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="/ingest désactivé (RAG_ADMIN_TOKEN non configuré)")
    if x_admin_token != RAG_ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="jeton admin invalide")
    p = Path(inp.path).resolve()
    # Confiné aux dossiers montés prévus pour l'ingestion.
    if not (str(p) == "/corpus" or str(p).startswith("/corpus/")):
        raise HTTPException(status_code=400, detail="chemin hors de /corpus")
    if not p.is_dir():
        raise HTTPException(status_code=400, detail=f"dossier introuvable: {p}")
    from ingest import run
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
        "audiences": {
            "config": audiences.FINGERPRINT,
            "validated": audiences.VALIDATED,
            "teleassistance_fiches": sorted(audiences.TELEASSISTANCE_FICHES),
        },
    }


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8090)
