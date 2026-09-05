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
_(updated after each round; full detail in `docs/design-review/round-NN.md`)_

### Round 01 — cascade-routing · anonymisation-rgpd · sovereignty-boundary · retrieval-rag · resilience-failure-modes · scaling-throughput
25 proposals, 24 survived critique. **Highest-leverage:** a *typed degradation response contract* —
`service_level` enum (nominal/degraded/deferred/unavailable), requested-vs-served tier, closed-enum
`degradation_reason` (carrying zero query text), a UI banner, one Prometheus `served_below_requested`
gauge. Size S, no GPU, no RGPD risk; it dissolves the stack's worst pathology ("fail-closed silently
lowers answer quality, no signal, no SLO") and is the precondition that makes every other change
measurable in production.

**Top 6 to adopt (ranked):**
1. **Eval harness first, gating everything** — `api/eval/` + ~200-item labelled corpus (query, gold
   category, gold tier, reference answer). Routing-accuracy / cloud-call-rate / cost slices run in CI
   CPU-only today; gives Jazzy a defensible CNIL number. Corpus must be pseudonymised (through Anone)
   or synthetic, with an owner + purpose + retention. **Blocks proposals 4 & 6.**
2. **Deterministic structured-PII layer before GLiNER + post-mask leak canary** — regex+checksum for
   NIR (clé de contrôle, 987/988), IBAN mod-97, +689 phones, M365 emails, DSI matricule; run before
   GLiNER, interval-merge spans, re-run detectors after masking, fail-closed to local on any residual
   match. Highest value-per-effort; cheapest cut of the tail risk that makes the cloud path
   indefensible. Hidden work: span-merge with overlap resolution (current right-to-left substitution
   assumes non-overlapping spans).
3. **Fix the fallback path** — `query_ollama_with_fallback` currently walks T4→T1, handing the hardest
   question to the weakest model. Replace with **escalate-or-degrade** (never silent downgrade) +
   the typed degradation contract (the highest-leverage item) + per-dependency **circuit breakers**
   keyed on connection-refused/5xx/liveness (never on generation latency — a healthy T4 answer
   already exceeds the 120s httpx timeout). Also raise the real-call timeout to fit CPU inference.
4. **Decouple data residency from quality tier** — cap the *auto* cascade at T4 (fully local);
   crossing the perimeter becomes a separate deliberate per-query act: Entra-role-restricted human
   sets "cloud autorisé" + free-text justification → egress log → still enforces Anone + moderation +
   caps. Bundle an **Article 9 lexicon gate**: santé / arrêt maladie / disciplinaire / sanctions /
   casier / appartenance syndicale → on-prem-only, T5 structurally impossible. Kills the un-tunable
   ≥4.5 threshold and the "scored 4.6 → US cloud" failure class. **Amends the frozen cascade —
   needs sign-off.**
5. **Response cache "T0" before the cascade** — helpdesk traffic is a few hundred recurring questions
   (reset MDP, Outlook F3, VPN, congés). Cache hit ≈ 100-300ms vs 150s+ generation → 40-70% hit rate
   is the single biggest concurrency lever on one box. Phase 1 exact-match hash; phase 2 semantic
   (conservative cosine threshold + mandatory "ce n'est pas ma question" feedback). ACL-namespaced
   default-deny key; PII-screen every write (Anone becomes a hard dep of the write path); TTL +
   purge endpoint wired to RAG `/ingest` and `DELETE /doc/{id}` so erasure isn't defeated.
6. **Replace scalar complexity with embedding-kNN categorical intent classifier** — a 1.0-5.0 scalar
   forces a false total order onto tiers that are *domains* (T3 Qwen=code, T4 Mistral Small=legal,
   not harder/easier). Fixed category→tier map (salutation/reformulation/code/analyse/juridique) is
   inspectable and gives an auditable reason. Implement as kNN over the proposal-1 corpus (one
   e5-base forward pass, ~100-300ms CPU) — **never** a per-query LLM classifier (doubles trivial-query
   latency at 3 tok/s). Classifier **never** emits "besoin-cloud". Fix the phantom `TIERS` list in the
   same change.

**Cross-cutting findings the facets surfaced:**
- The **frozen cascade is already not what's deployed**: "Llama 3.3 8B" is a phantom (Llama 3.3 only
  shipped at 70B); `main.py` `TIERS` points at `neural-chat` / `dolphin-mixtral` / `llama2:7b`.
- **The orchestrator (:8888) has no authentication** — yet every routing/ACL/cache-namespace/approval
  /egress-ledger proposal assumes a known caller identity. Stack-wide prerequisite.
- **No eval harness** = every proposal here is currently unfalsifiable.
- Durable queue + async job model + response cache + eval corpus all want to **persist query text** —
  must run Anone at enqueue/write time and store only anonymised text.

---

## Open design questions for the operator
_(accumulated across rounds — round 1)_

1. **Amend the frozen cascade?** Sign off on: (a) T5 no longer auto-reachable; (b) collapse T1+T2
   into one entry model; (c) "small / medium / cloud" framing; (d) juridique/RGPD advice on Qwen 14B
   instead of Mistral Small 22B — or keep 22B as a cold-swap low-volume legal tier?
2. **Cloud legal basis** — Anthropic direct US API (DPA + SCCs + a Schrems II Transfer Impact
   Assessment vs FISA 702) / EU-hosted Claude (Bedrock/Vertex EU) / zero-cloud & delete T5? Who owns
   the sign-off, by when? **No cloud traffic until this is documented.**
3. May the cloud tier **ever** be reached by automatic routing, or only by explicit per-query human
   authorization with written justification?
4. Which **Entra roles** may approve a cloud call, and which may set the "cloud autorisé" flag?
5. Acceptable **latency per tier** given CPU-only (~3 tok/s → 130-270s/answer today)? Is deferred
   answering ("répondre bien, réponse par mail") acceptable, or will agents just re-ask "maintenant"?
6. **Eval/kNN corpus** — is the one-time annotation of ~200 real DSI queries funded, who owns it,
   what retention/pseudonymisation applies?
7. **GPU timeline** — when is the NVIDIA 570 driver install scheduled? Budget for CPU worker VMs
   meanwhile?
8. **RAG in scope this cycle?** Who classifies each SharePoint site / file share as cloud-eligible
   vs restricted at onboarding?
9. **Retention periods** (DPO mandate) for: LiteLLM logs, LangGraph state, response cache, job queue,
   cloud egress ledger, pseudonymisation register?
10. **Polynesian languages** (reo Mā'ohi and others) — in scope as input/output, or French-only?
