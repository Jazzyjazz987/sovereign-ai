"""Stockage vectoriel — pgvector dans le PostgreSQL de la stack.

Schéma minimal : une table `rag.chunks`. Recherche par distance cosinus (`<=>`).
"""
from __future__ import annotations

import json
import os

import psycopg2
import psycopg2.extras

from embed import DIM

DSN = os.getenv(
    "RAG_PG_DSN",
    os.getenv("POSTGRES_DSN", "postgresql://claude:claude@localhost:5432/langgraph_db"),
)

DDL = f"""
CREATE EXTENSION IF NOT EXISTS vector;
CREATE SCHEMA IF NOT EXISTS rag;
CREATE TABLE IF NOT EXISTS rag.chunks (
    chunk_id        TEXT PRIMARY KEY,
    doc_id          TEXT NOT NULL,
    proc_code       TEXT,
    titre           TEXT,
    domaine         TEXT,
    section         TEXT,
    criticite       TEXT,
    contrainte_rgpd BOOLEAN DEFAULT FALSE,
    sla             TEXT,
    roles           JSONB DEFAULT '[]',
    related         JSONB DEFAULT '[]',
    source_url      TEXT,
    source_file     TEXT,
    text            TEXT NOT NULL,
    corpus          TEXT DEFAULT 'procedures-legacy',
    embedding       vector({DIM}),
    ingested_at     TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX IF NOT EXISTS chunks_domaine_idx  ON rag.chunks (domaine);
CREATE INDEX IF NOT EXISTS chunks_proc_idx     ON rag.chunks (proc_code);
CREATE INDEX IF NOT EXISTS chunks_embed_idx    ON rag.chunks
    USING hnsw (embedding vector_cosine_ops);
"""


def connect():
    return psycopg2.connect(DSN)


def init_db():
    with connect() as c, c.cursor() as cur:
        cur.execute(DDL)
        c.commit()


def replace_corpora(rows: list[dict], embeddings: list[list[float]]):
    """Remplace tous les corpus présents dans `rows` (champ `corpus` par ligne)."""
    corpora = sorted({r["corpus"] for r in rows})
    with connect() as c, c.cursor() as cur:
        cur.execute("DELETE FROM rag.chunks WHERE corpus = ANY(%s)", (corpora,))
        psycopg2.extras.execute_values(
            cur,
            """INSERT INTO rag.chunks
               (chunk_id, doc_id, proc_code, titre, domaine, section, criticite,
                contrainte_rgpd, sla, roles, related, source_url, source_file, text,
                corpus, embedding)
               VALUES %s
               ON CONFLICT (chunk_id) DO UPDATE SET
                 text=EXCLUDED.text, embedding=EXCLUDED.embedding, section=EXCLUDED.section,
                 domaine=EXCLUDED.domaine, related=EXCLUDED.related,
                 corpus=EXCLUDED.corpus, ingested_at=now()""",
            [
                (r["chunk_id"], r["doc_id"], r["proc_code"], r["titre"], r["domaine"],
                 r["section"], r["criticite"], r["contrainte_rgpd"], r["sla"],
                 json.dumps(r["roles"]), json.dumps(r["related"]), r["source_url"],
                 r["source_file"], r["text"], r["corpus"], _vec(e))
                for r, e in zip(rows, embeddings)
            ],
        )
        c.commit()


def _vec(v: list[float]) -> str:
    return "[" + ",".join(f"{x:.6f}" for x in v) + "]"


DEFAULT_CORPORA = ("procedures-legacy",)


def search(query_vec: list[float], k: int = 5, domaine: str | None = None,
           rgpd_only: bool = False, corpora: tuple[str, ...] = DEFAULT_CORPORA) -> list[dict]:
    where, params = ["corpus = ANY(%s)"], [list(corpora)]
    if domaine:
        where.append("domaine = %s")
        params.append(domaine)
    if rgpd_only:
        where.append("contrainte_rgpd = TRUE")
    clause = "WHERE " + " AND ".join(where)
    sql = f"""
        SELECT chunk_id, doc_id, proc_code, titre, domaine, section, sla, criticite,
               contrainte_rgpd, source_url, source_file, related, text,
               1 - (embedding <=> %s) AS score
        FROM rag.chunks
        {clause}
        ORDER BY embedding <=> %s
        LIMIT %s
    """
    params = [_vec(query_vec), *params, _vec(query_vec), k]
    with connect() as c, c.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(sql, params)
        return [dict(r) for r in cur.fetchall()]


def stats() -> dict:
    with connect() as c, c.cursor() as cur:
        cur.execute("SELECT corpus, count(*), count(distinct doc_id) FROM rag.chunks GROUP BY corpus")
        return {row[0]: {"chunks": row[1], "docs": row[2]} for row in cur.fetchall()}
