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

### Round 02 — orchestrator-auth-identity · eval-and-prompt-governance · cloud-legal-basis · capacity-model-and-latency · data-lifecycle-dpia · client-ux-and-continuity
23 proposals, all 23 survived. **Highest-leverage:** *unpublish the data-plane ports + one
identity-terminating proxy*. A 4-line `docker-compose.yml` edit removes host mappings for
`:8888` (auth-free FastAPI that calls the cloud), `:4000` (exposes `LITELLM_MASTER_KEY`),
`:11434` (raw Ollama), `:5432` (Postgres). Then one `oauth2-proxy` container + one Entra app
registration + a ~30-line JWT dependency in `main.py`. Unblocks ~half the roadmap (Round 1
named "no auth on :8888" as the blocker for all ACL/quota/RAG-ACL/cache work).

**Top 6 to adopt:**
1. **Identity-terminating proxy + unpublish data-plane ports + bounded no-identity lane** —
   `oauth2-proxy` (Entra OIDC, self-hosted since M365 F3 has no App Proxy / Conditional Access /
   P1) injecting a proxy-signed JWT (oid, roles, tenant). **Must ship bundled** with a no-identity
   lane (unauth-passthrough through the same proxy, clamped to T2, cannot reach T5/RAG/cache-write,
   one global rate bucket) so a satellite/Entra outage degrades to local Q&A instead of total
   outage. Use Entra **app roles**, not raw group claims (group-overage cap). Define a
   client-credentials path for service-to-service + RAG `/ingest`.
2. **Curated canonical answer base** for the recurring core — the single largest capacity multiplier;
   50-60% of helpdesk load is ~30-50 clusters (reset MDP, VPN satellite, MFA, F3 licences, congés).
   Human-reviewed answers served at ~10ms with zero inference, and they keep answering when
   inference is down. Needs the pgvector/embeddings layer first, a named editorial owner (~0.3 FTE),
   fail-toward-live-cascade below a confidence threshold, review-by dates, one-click unpublish.
3. **DPIA-as-code** — one checked-in `api/legal/data_manifest.yaml` enumerating every store that can
   hold nominative/pseudonymised data (lawful basis, purpose, location, reversible?, TTL, erasure
   procedure) = simultaneously the CNIL Art. 30 register, a nightly reaper's config, and a CI gate
   (no new store without a manifest entry). **LiteLLM runs metadata-only** (`turn_off_message_logging`)
   — removes an entire pseudonymised-PII store for a one-liner. Scripted erasure drill (seed a
   canary subject across all stores → fire erasure → assert zero residual) monthly.
4. **Extract every behaviour-defining prompt into a versioned fingerprinted prompt pack** —
   code-confirmed: `query_ollama` sends the user prompt **raw with no system field**, so T1-T4
   answer with zero French enforcement, no "réponse indicative non juridique" framing, no Article-9
   refusal, no defence against "ignore les consignes". "The legal model" is literally "whatever
   dolphin-mixtral does raw". `config/prompts.yaml` per-tier (version, owner, body), fail-fast load,
   fingerprint stamped into `/query` response. T1/T2 get disclaimer prompts (they're the T5/T4
   failure sink). Lands now, no dependency on the corpus.
5. **`cloud_authorization.yaml` + `api/legal/` + fail-closed startup gate** — `route_t5_with_anonymization`
   calls the Anthropic API with **no recorded transfer basis**. A machine-readable signed+expiring
   YAML `{t5_enabled, legal_basis: SCC+TIA|none, dpia_ref, tia_ref, signed_by, review_due}` that
   `main.py` reads at startup, hard-failing T5 closed to local if basis is `none` or review is
   overdue. Ship **only Regime B (SCCs + TIA)** as operative — because `main.py` keeps the
   `pii_mapping` key, the transfer stays in GDPR Chapter V scope regardless of what Anthropic can do
   (EDPB Jan-2025 pseudonymisation guidance). Route T5 through LiteLLM so the key + spend log live
   in one place, message logging OFF.
6. **Honest two-lane capacity model** — bounded synchronous product (cache/RAG hits + a hard-capped
   ~40-token T1 reformulation) vs asynchronous "réponse différée" product (all T2-T5, answered by
   notification). `OLLAMA_NUM_PARALLEL=1` (currently 2 — on CPU, two concurrent generations just
   make both miss their deadline). Serialized queue → latency becomes deterministic
   (`wait = queue_depth × mean_answer_time`) = one Grafana gauge. **Reject the EWMA closed-loop
   governor** (a stateful control loop a 2-3 person team can't debug at 2am). Publish the SLA as
   "heures ouvrées, best effort" with **no number** until drain capacity is measured.

**Cross-cutting R2 findings:**
- `LITELLM_MASTER_KEY` on `:4000`, Postgres on `:5432`, Ollama on `:11434` — all host-published, no
  ingress control.
- The `pii_mapping` key retention (DSI holds the re-identification key) means **a T5 call is always
  a GDPR Article 46 transfer** — a code switch labelled "effectivement anonyme" would encode a legal
  bet a regulator is likely to reject.
- **`dolphin-mixtral` and `neural-chat` are uncensored community fine-tunes** being used as the code
  and legal tiers with no stated vetting.
- Anone at write-time should apply **only** to artifacts that can feed T5 / cross the perimeter — not
  every local queue job (GLiNER-at-0.5 mangles text, competes for CPU, adds a 503-prone SPOF to work
  that never leaves the building).
- Cache key must be `sha256(sensitivity_tier || normalized_query)` with 3-4 coarse sensitivity tiers
  — **not** caller identity (per-user group sets → near-zero cross-user hit rate).
- Teams as a transport puts every query in M365 Purview/eDiscovery scope → primary client must be an
  Entra-auth PWA served from the box; Teams only for the approver-side T5 gate (anonymised payload).

---

### Round 03 — model-supply-chain-vetting · production-answer-quality-loop · acceptable-use-safety-incident · measured-capacity-harness · pwa-client-and-notification · tco-budget-governance
23 proposals, 21 survived. **Highest-leverage:** a *metadata-only capacity request journal* — one
JSONL line per query (token counts, tier, cold/warm, queue depth, per-phase wall-times; **zero
query text, no client id**), async fire-and-forget, ~50-line weekly pandas fit. ~1.5 days, no RGPD
downside (strengthens the CNIL story with verifiable volume figures), and it's the only way to get
the arrival-rate data that **every** capacity / staffing / SLA / interim-VM decision currently
guesses at.

**Top 6:**
1. **Metadata-only capacity request journal + weekly arrival-rate fit** — `api/obs/journal.py`,
   wired into the existing metrics wrapper; reaper + manifest entry; `api/bench/fit_arrival.py`
   writes an "observed" block into `config/capacity_profile.yaml`.
2. **Remove the uncensored community weights NOW; add `config/models.yaml` scoped fail-closed
   admission control** — `dolphin-mixtral` (deliberately de-safety-trained "uncensored" fine-tune)
   is the legal/administratif tier answering RGPD & HR questions for 5500 agents *with no system
   prompt*, and it's Mixtral 8x7B (~26 GB — doesn't fit the budget, unusable at 3 tok/s). Delete it
   + `neural-chat` from `ollama_init.sh` and `TIERS` now (local cascade caps at T2 until the GPU).
   `config/models.yaml`: one entry per resident weight with an immutable content digest; startup
   check fails-closed **only** on GLiNER or T4 mismatch (T1-T3 log + banner + serve — a stack that
   won't boot at 2am is its own hazard); never auto-write the CLAUDE.md table.
3. **Minimal cloud-egress substrate** — re-run the R1.2 deterministic PII detector over the
   *outbound anonymised text* right before the Anthropic call (fail-closed to local on any hit) +
   an **append-only transfer journal** (HMAC of the payload, gliner_version, rescan_result,
   request/approval id, token count, 3-year retention). Turns "did subject X's data leave in clear?"
   from a worst-case assumption into a hash lookup.
4. **PWA as an identity-owned server-side ticket store ("corbeille") + zero-JS
   progressive-enhancement client** — at 3 tok/s a synchronous chat UI is a lie; the ticket model
   makes latency a first-class fact. **Decisive property:** if the answer is only ever pulled over
   the authenticated on-prem channel, the notification never carries content → its transport (plain
   M365 email) falls entirely outside the CNIL/sovereignty boundary. Zero-JS server-rendered
   semantic HTML makes **RGAA 4.1** an architectural property, not a bug backlog, and runs on the
   oldest workstations over satellite. **The only round-3 proposal that dissolves a hard constraint
   instead of working around it.** ~2-3 weeks, gated on the R2.1 proxy.
5. **Consolidated AI TCO line + durable Postgres spend/transfer ledger + two-tier overrun
   authority** — `_t5_calls` is an in-process counter that resets on every restart, so a crash-loop
   or a second replica has **no ceiling**; overspend is found on the monthly invoice. One
   `t5_ledger` table on the existing Postgres: post-pay check before each call (over → local; ledger
   unreachable → fail-closed to local); Prometheus spend gauge + 70/90/100% alerts;
   `config/budget_envelopes.yaml` in git, one named holder, ops may alert but not raise a ceiling.
6. **Hardware-fingerprinted `config/capacity_profile.yaml`** — `main.py` hardcodes `timeout=120`
   with no basis; every latency constant is silently invalidated the day the 3090 arrives. Split
   into a "measured" block (only the harness writes it) + a hand-owned "policy" block; startup
   fingerprint mismatch → **concrete conservative static profile** (serial, worker pool 1, hard
   queue cap, reject-over-capacity with a typed reason — NOT "no deadline", which is fail-open).

**Cross-cutting R3 findings:**
- CPU-era UX = coarse "réponse différée, ~N min" only, measured at concurrency 1; precise per-query
  ETA + tokenizer-in-hot-path deferred to post-3090. "Never multi-GPU" (hardware) ≠ request
  concurrency (unrelated) — don't cap request concurrency at 2 post-3090, it kills vLLM batching.
- **One access-control policy for ALL identity-linked query data** (corbeille, transfer journal, any
  abuse dataset): named access only, logged reason, retention cap, RoPA entry, **CSE/CST
  consultation before go-live**. Do NOT build a standalone per-agent query log.
- Abuse detection: **drop** "near-duplicate burst" / "templated fan-out" signals (they collide with
  the canonical-answer + templated-workflow direction); keep only a structured-citizen-identifier
  -count tripwire (throttle-and-review, never auto-block, tuned so a benefits clerk clearing 200
  dossiers isn't flagged). Ship only a user-facing charte-reminder banner + anonymous weekly
  aggregate counter — **no per-identity risk tagging** without CSE sign-off + an eval-proven FP rate.
- Field-failure corpus **augments but never merges into** the hand-built offline eval set;
  field entries are reviewer-paraphrased to synthetic wording before any git commit (pseudonymised
  user text in git history is permanent and un-erasable).

---

## Open design questions for the operator
_(accumulated across rounds)_

### From round 3
20. **Chapter V transfer basis** — does the marché public with the (EU-)Claude provider carry signed
    SCCs + a documented TIA (or DPF), DPO-signed, **before any production T5 call**? Until yes, T5
    stays disabled — the egress journal is forensics, not a lawful basis.
21. **French labour law** — is prior **CSE/CST consultation + formal information des agents**
    required before the authenticated PWA can launch with per-agent logging? Who runs it, what
    timeline? This may gate the whole identity-bound design.
22. **Interim CPU worker-VM hosting** — contractually/legally acceptable for government-agent
    personal data (SecNumCloud / EU sovereignty)? If not, inference stays on the on-prem box at
    ~3 tok/s until the 3090.
23. **Approve the frozen-cascade amendment**: `neural-chat` + `dolphin-mixtral` removed now; T3/T4
    become named official vendor weights when the 3090 lands. Changes the CLAUDE.md table — needs
    Jazzy's signature.
24. **Named holder of the consolidated AI TCO line** + concrete euro caps (T5/day, T5/month, total
    stack/month) + monthly kWh assumption.
25. **reo Tahiti UI-chrome locale** (not model output) — committed v1+ deliverable with a named
    translation owner + Fare Vāna'a review cadence, or explicitly out of scope? (Build the
    string-pack seam either way.)
26. **Named-people capacity check on a 3-person team**: confirm or descope the 2 rotating quality
    reviewers (~0.2 FTE), the canonical-answer editorial owner (~0.3 FTE), the 2 dual-control
    unseal authorities. Permanent commitments, not project tasks.
27. **SLA posture** — prepared to publish "heures ouvrées, best effort, no number" to 5500 agents
    until 6-8 weeks of request-journal data exist, and defend that to leadership?
28. **Access-control + retention for identity-linked query data** — who may read the corbeille /
    transfer journal / abuse dataset, under what logged justification, for how long, and **who can
    compel disclosure** (a manager, a court order, a future administration)?

### From round 2
11. **Is cloud T5 actually required by the directions métier**, or is "T4 is the ceiling, fully
    local" acceptable? This one decision determines whether the whole cloud-legal workstream (DPIA,
    TIA, SCCs, EU-hosting) is needed now or shelved.
12. **Named DPO / RGPD sign-off owner** — do they have real bandwidth for DPIA ownership + a
    quarterly human review of legal-category answers? If the role is fiction, the `api/legal/`
    artifacts and human-review tiers are fiction.
13. **Comité social (works council)** consulted + DPIA filed for the new processing purposes over
    5500 civil servants: per-identity usage metering/quota, query-log mining for the FAQ base, the
    operational query-text store? Cannot go live without it.
14. **Async "answer delivered later by notification" as the PRIMARY UX** — acceptable, or must it
    stay an exception?
15. **Sign-off on the frozen-cascade amendments** already implied: auto-cascade capped at T4, T5 =
    deliberate escalation-only, CLAUDE.md table corrected to match `api/main.py` reality (+ phantom
    Llama 3.3 fixed). Needs explicit written approval.
16. **Budget / procurement appetite** — money + marché public willingness for EU-hosted Claude
    (Bedrock/Vertex EU) and/or interim sovereign CPU worker VMs (OVH / Scaleway / Outscale — **not**
    AWS/Azure/GCP for personal data)? Or strictly single-box, no external compute?
17. **Retention period** for the operational query store + deferred queue (24-48h proposed) — and is
    losing multi-day conversation memory acceptable as a product decision?
18. **Funded named owners** for the canonical answer base (~0.3 FTE editorial) and the prompt pack /
    `GOVERNANCE.md`?
19. **Are `dolphin-mixtral` and `neural-chat` (uncensored community fine-tunes) acceptable** as the
    deployed code and legal tiers, or must the cascade move to the vetted CLAUDE.md models before
    go-live?

### From round 1

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
