# DESIGN REVIEW — Sovereign AI stack (conception)

Continuous multi-agent review of the **global design** of the sovereign AI system for
DSI Polynésie française. Not bug-hunting — architecture-level improvements: different
structure, different boundary, a capability that changes what's possible, a simplification
that removes a whole class of problem.

**Started:** 2026-09-05 12:52 (session_0146Gw93oyAzeQRMBQienYB2), operator request:
"refais une passe sur la conception globale … en faisant travailler des agents … orchestre
… tourne en boucle pendant au moins deux heures".

**Method:** each round, a Workflow decomposes the design into ~6 facets, one agent per facet
proposes conceptual improvements, a critic agent per facet stress-tests them against the hard
constraints, a synthesis agent ranks what to adopt and picks threads to go deeper on next
round. Per-round detail in `docs/design-review/round-NN.md`; this file holds the running
summary.

## Hard constraints every proposal must respect
- CPU-only today (~3 tok/s); single NVIDIA RTX 3090 24 GB later. No multi-GPU.
- RGPD / CNIL — personal data of *natural persons*; no un-anonymised nominative data to any cloud.
- Sovereignty — cloud (T5, Anthropic API) only via Agent Anone anonymisation, and it's conditional.
- French-first (comments, logs, user-facing).
- ~5 500 agents, ~3 500 postes, multi-île, satellite connectivity, Microsoft 365 F3.
- Small ops team. Docker Compose today. Secrets in `.env`.
- The CLAUDE.md model-cascade table is "figée" (T1 Mistral 7B · T2 Llama 3.3 8B · T3 Qwen 3 14B ·
  T4 Mistral Small 22B · T5 Claude Sonnet) — proposals may argue to amend it but must say so.

## Current architecture (as built)
- **LangGraph orchestrator** (`api/main.py`, :8888) — keyword-based complexity score → tier;
  `TIERS` list T1–T5; `query_ollama_with_fallback` walks down on failure; T5 path =
  Anone `/anonymize` → Claude → `/deanonymize`, fail-closed, `T5_MODERATION` human gate,
  `T5_MAX_TOKENS`/`T5_MAX_CALLS` cost caps.
- **Agent Anone** (`api/anone_api.py`, :8080) — GLiNER `urchade/gliner_multi_pii-v1`,
  unique tokens + `pii_mapping`, HTTP 503 on failure, 6 PII labels (no `organization` —
  masking public bodies broke question meaning).
- **LiteLLM** gateway (:4000), **Ollama** T1–T4 (:11434), **PostgreSQL**, **Prometheus** +
  **Grafana**, **/metrics** on langgraph + anone.
- **RAG** — planned (B18): `rag` service :8090 + pgvector in PostgreSQL + local embeddings
  `intfloat/multilingual-e5-base`; `/ingest`, `/search`, `DELETE /doc/{id}`; LangGraph
  `use_rag` step; retrieved chunks → Anone before T5; ACL by Entra group.
- Vast majority of the codebase is CPU-mode; no working GPU driver yet.

## Known conceptual weak points (seeds for the review)
- Complexity scoring is keyword-bag heuristics — brittle, gameable, no semantic understanding.
- T5 is auto-unreachable in practice (hard to score ≥4.5); T5 is really only forced or high-override.
- Anonymisation is lossy for the *subject* of a question, and pseudonymised text sent to cloud is
  arguably still "processing" under RGPD — the legal basis for T5 needs scrutiny.
- Single-GPU ceiling vs 5 500 agents — no queueing / batching / caching design.
- Fail-closed everywhere is safe but silently degrades quality; no user signal, no SLO.
- The stack has no eval harness — model/prompt changes are unmeasured.
- Docker adds GPU-passthrough friction; hybrid-native was floated.

---

## Running summary of adopted improvements
_(updated after each round)_

### Round 01 — <pending>

---

## Open design questions for the operator
_(accumulated across rounds)_
