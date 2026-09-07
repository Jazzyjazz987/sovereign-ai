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
-- Recherche lexicale (BM25-like) pour l'hybride — E2. Colonne générée : maintenue seule.
-- Le nom du code de procédure est ajouté au texte indexé pour matcher « PROC-ID-007 ».
ALTER TABLE rag.chunks ADD COLUMN IF NOT EXISTS tsv tsvector
    GENERATED ALWAYS AS (
        to_tsvector('french', coalesce(proc_code,'') || ' ' || coalesce(titre,'') || ' ' || text)
    ) STORED;
CREATE INDEX IF NOT EXISTS chunks_tsv_idx ON rag.chunks USING gin (tsv);
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


def _or_tsquery(cur, query: str):
    """Transforme la requête en tsquery OR (récupération large) ; None si vide."""
    cur.execute("SELECT plainto_tsquery('french', %s)::text AS q", (query,))
    plain = (cur.fetchone()["q"] or "").strip()
    if not plain:
        return None
    return plain.replace(" & ", " | ")


def search_lexical(query: str, k: int = 20, domaine: str | None = None,
                   corpora: tuple[str, ...] = DEFAULT_CORPORA) -> list[dict]:
    """Recherche plein-texte français (BM25-like), termes en OR — volet lexical (E2)."""
    with connect() as c, c.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        tsq = _or_tsquery(cur, query)
        if tsq is None:
            return []
        where = ["corpus = ANY(%s)", "tsv @@ to_tsquery('french', %s)"]
        params: list = [tsq, list(corpora), tsq]
        if domaine:
            where.append("domaine = %s")
            params.append(domaine)
        params.append(k)
        cur.execute(f"""
            SELECT chunk_id, doc_id, proc_code, titre, domaine, section, sla, criticite,
                   contrainte_rgpd, source_url, source_file, related, text,
                   ts_rank_cd(tsv, to_tsquery('french', %s)) AS score
            FROM rag.chunks
            WHERE {' AND '.join(where)}
            ORDER BY score DESC
            LIMIT %s
        """, params)
        return [dict(r) for r in cur.fetchall()]


def chunks_for_codes(codes: list[str], sections_pref=("Étapes", "Objet", "Fiche"),
                     corpora: tuple[str, ...] = DEFAULT_CORPORA) -> list[dict]:
    """Un chunk représentatif par code de procédure (pour l'expansion `related` — C9)."""
    if not codes:
        return []
    with connect() as c, c.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("""
            SELECT DISTINCT ON (proc_code)
                   chunk_id, doc_id, proc_code, titre, domaine, section, sla, criticite,
                   contrainte_rgpd, source_url, source_file, related, text
            FROM rag.chunks
            WHERE proc_code = ANY(%s) AND corpus = ANY(%s)
            ORDER BY proc_code,
                     CASE WHEN section ILIKE 'Étapes%%' THEN 0
                          WHEN section ILIKE 'Objet%%'  THEN 1
                          WHEN section ILIKE 'Fiche%%'  THEN 2 ELSE 3 END
        """, (list(codes), list(corpora)))
        return [dict(r) for r in cur.fetchall()]


def stats() -> dict:
    with connect() as c, c.cursor() as cur:
        cur.execute("SELECT corpus, count(*), count(distinct doc_id) FROM rag.chunks GROUP BY corpus")
        return {row[0]: {"chunks": row[1], "docs": row[2]} for row in cur.fetchall()}
