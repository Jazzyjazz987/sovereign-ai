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
constraints, a synthesis agent ranks what to adopt and picks threads to go deeper on next round.
Per-round detail in `docs/design-review/round-NN.md`.

**Status:** 5 rounds complete (2026-09-05, ~2h20, 65 agents, ~3.4M tokens). 30 facets reviewed,
~113 proposals, ~110 survived adversarial critique. **Read the CONSOLIDATION section first** — its
two findings (unfunded human cost; ship v1 with no cloud tier + prove the bet with a pilot)
reframe everything below. 7 facets remain un-reviewed (listed in CONSOLIDATION) for a future
round 6.

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

---

# CONSOLIDATION — cross-round synthesis (5 rounds, ~2h20, 65 agents, ~3.4M tokens)

Full per-round detail in `docs/design-review/round-0N.md`. ~113 conceptual proposals generated,
~110 survived adversarial critique, distilled here.

## The two findings that reframe the whole project

**1. Nobody has totalled the recurring human cost of the adopted design.** Almost every
improvement adds standing load: an editorial/triage owner heading toward **~0.5 FTE**, three
functional escalation queues (**DPO / DGRH / DAF**), quarterly DR game-days, quarterly "secrets
days", safeguarding-lexicon + card upkeep, canonical-base curation, two rotating quality
reviewers. On a **2-3 person team** this is the top risk — most items silently degrade to "high
redirect rate" or "broken promise" if the roles aren't staffed. Round 5's answer: constitute the
whole compliance + resourcing effort as **`compliance/launch_dossier/`** with **one named
accountable owner — the PF DPO, *not* Jazzy** (a chef de cellule legally cannot authorise a
traitement for la Polynésie française; his role is "pilote technique") — carrying a **signed
low/expected/high FTE + euro cost range, each direction signing its own line**, presented to
leadership as a **funding decision, now, before the build**. `launch_authorization.yaml`
(fail-closed on session-minting only) is its code enforcement surface.

**2. The deliverable is a behaviour change, not an AI capability** — agents stop pasting citizen
data into public ChatGPT because a sanctioned tool exists. Nothing in the 4-round adopted set
de-risks that central bet: that ~5500 agents will accept a **slower (~3 tok/s), narrower** tool.
Round 5's recommendation: **ship v1 with NO cloud/T5 tier at all**, as a "substitution product" =
curated canonical FAQ + strong French search + a few constrained local lanes (Chercher / Rédiger
/ Traduire / Résumer + one local-only "poser une question"), and **prove the bet first with a
~15-25 person consent-based, pseudonymous, delete-by-default pilot** (~2-3 weeks of work vs. a
permanent commitment to 24 subsystems). Deferring T5 deletes the single largest coherent cost
cluster (`cloud_authorization.yaml` runtime, SCC+TIA shipping regime, workspace-key + hard cap,
durable `t5_ledger`, Article 9 lexicon gate, GLiNER-tuned-for-cloud + outbound re-scan, T5
fail-closed tests) — and since every T5 call is legally an Article 46 transfer, **if the
shadow-egress KPI moves without cloud, that surface never needs to exist.** The Article 46 / SCC
/ TIA / Anthropic-DPA legal groundwork still starts now in parallel (months of lead time, on the
critical path for any future cloud tier), owned by the dossier — only the *runtime machinery*
waits for a pre-committed v2 go/no-go gate.

**Realistic launch window: Q1-Q2 2027**, paced by the quarterly comité social / CTP calendar and
the arrêté en conseil des ministres — a fact the project must plan around, not around.

## What the review found is *actually* deployed (vs. CLAUDE.md)

- The "cascade figée" is **fiction**: `T2 = "Llama 3.3 8B"` — a model that only ever shipped at 70B.
  `api/main.py` really runs `mistral:7b` / `llama2:7b` / `neural-chat` / `dolphin-mixtral`.
- **`dolphin-mixtral` and `neural-chat` are uncensored community fine-tunes** — `dolphin-mixtral`
  is deliberately de-safety-trained — serving as the **legal/administratif and code tiers** for
  5500 agents, **with no system prompt at all** (`query_ollama` sends the user text raw). "The
  legal model" is literally "whatever dolphin-mixtral does raw". And it's Mixtral 8x7B (~26 GB) —
  it doesn't fit the VRAM budget and is unusable at 3 tok/s anyway.
- The orchestrator (`:8888`), LiteLLM (`:4000`, exposes `LITELLM_MASTER_KEY`), Ollama (`:11434`),
  Postgres (`:5432`) are **all host-published with no authentication**.
- `T5_MAX_CALLS` is an in-process counter that **resets on every restart** — a crash-loop or a
  second replica has **no cloud-spend ceiling**.
- `query_ollama_with_fallback` walks **down** to the weakest model on failure — the hardest
  question gets the worst answer, signalled only by a string glued onto the response.
- A T5 call is **legally always a GDPR Article 46 transfer** (DSI keeps the `pii_mapping`
  re-identification key), so "pseudonymised → US cloud" needs **SCCs + a Transfer Impact
  Assessment**, not a "c'est anonyme" flag. **No transfer basis is currently recorded anywhere.**
- No eval harness → every design change is unfalsifiable. No staging, no backup/restore, no DR.

## Sequenced roadmap (what the review says to build, in order)

### Phase 0 — decisions & near-free backstops (days; mostly not code)
1. **Answer the blocking operator questions** (§ below) — above all: is cloud T5 actually required
   by the *directions métier*? and who owns the ~0.5 FTE editorial role? These gate everything.
2. **Workspace-scoped Anthropic key with a server-side hard monthly cap** (~1h console + 1 compose
   line) — the only cloud-spend control that survives a restart, a wiped ledger, or the box being
   gone. Remove `ANTHROPIC_API_KEY` from the litellm service.
3. **Remove `dolphin-mixtral` + `neural-chat` now** from `ollama_init.sh` and `TIERS` (local
   cascade caps at T2 until the GPU). Correct the CLAUDE.md table (phantom Llama 3.3).
4. **`config/models.yaml`** with content-digest pinning; startup check fail-closed only on
   GLiNER / T4 mismatch.

### Phase 1 — safety & correctness floor (1-3 weeks; small code)
5. **Safeguarding lane** — a deterministic lexicon screen as the *very first* step of the request
   path (harcèlement / VSS / souffrance au travail / idées suicidaires / danger immédiat) → returns
   a Polynesia-localised help card, **calls no model, writes no ticket, touches no cache**, only an
   anonymous per-category counter. Non-negotiable, nearly free. + a safety system prompt on every
   local tier.
6. **Versioned fingerprinted prompt pack** (`config/prompts.yaml`) — closes the "no system prompt"
   hole; T1/T2 get disclaimer prompts (they're the fallback sink).
7. **Deterministic structured-PII layer** (regex+checksum NIR/IBAN/+689/M365/matricule) before
   GLiNER + **post-mask leak canary** + **outbound re-scan right before the Anthropic call**, all
   fail-closed to local.
8. **Fix the fallback**: escalate-or-degrade (never silent downgrade) + the **typed degradation
   response contract** (`service_level` enum, requested-vs-served tier, closed-enum reason with
   zero query text, UI banner, one Prometheus gauge) + per-dependency circuit breakers keyed on
   connrefused/5xx/liveness (never latency).
9. **Eval harness** (`api/eval/` + ~200-item pseudonymised/synthetic corpus) — gates every later
   change; routing/cost/cloud-rate slices run in CI CPU-only.

### Phase 2 — the perimeter & the client (weeks)
10. **Identity-terminating `oauth2-proxy`** (Entra OIDC, proxy-signed JWT with app *roles* not group
    claims) + **unpublish the data-plane host ports** + a **bounded no-identity lane** (clamped to
    T2, no T5/RAG/cache-write) so an Entra/satellite outage degrades gracefully instead of total
    outage.
11. **Decouple data residency from quality tier**: auto-cascade capped at **T4**; crossing the
    perimeter = a deliberate per-query human act (Entra-role sets "cloud autorisé" + justification
    → egress log) + an **Article 9 lexicon gate** (santé / disciplinaire / casier / syndical →
    on-prem-only, T5 structurally impossible).
12. **`cloud_authorization.yaml`** fail-closed startup gate (signed, expiring; `legal_basis:
    SCC+TIA|none`). Route T5 through LiteLLM, message logging off.
13. **Cited-fiche gate + accountability registry** — the legal/admin classifier *label* (not the
    complexity score) is the hard gate; for statutaire / RGPD-conseil / paie clusters the tier may
    return only verbatim-quoted + linked fiche text, else a hard "consultez [service]" card with
    zero model prose. `config/legal/content_owners.yaml` (service responsable, valideur nommé,
    date, péremption). Shrinks the Article 46 surface — these clusters stop going to T5.
14. **PWA "corbeille"** — identity-owned server-side ticket store + zero-JS progressive-enhancement
    client (**RGAA by architecture**). At 3 tok/s a synchronous chat UI is a lie; the ticket model
    makes latency a first-class fact. **The content-free notification** (plain M365 email) then
    falls entirely outside the CNIL boundary.
15. **Adoption front door** — onboarding as a property of login (4-min static walkthrough + charte
    acknowledgement), **three answer labels** ("référence validée DSI" / "générée localement — non
    vérifiée" / "réponse cloud"), the structured fiche de demande, a signaler→canonical loop.
    **North-star KPI = aggregate shadow-egress to chat.openai.com/claude.ai/gemini from DNS/proxy
    logs** (strictly aggregate, zero per-user, declared to CSE/CST) — this is the tool's real
    purpose.

### Phase 3 — capacity, cost, resilience (weeks; some gated on the RTX 3090)
16. **Metadata-only capacity request journal** (zero query text) + weekly arrival-rate fit →
    `config/capacity_profile.yaml`. The only way to get the load data every SLA/staffing/VM
    decision currently guesses at. **Publish no SLA number for 6-8 weeks.**
17. **Two-lane capacity**: bounded synchronous (cache/RAG + capped T1 reformulation) vs async
    "réponse différée". `OLLAMA_NUM_PARALLEL=1`; serialized queue. Reject any EWMA governor.
18. **Response cache "T0"** before the cascade — key `sha256(sensitivity_tier || normalized_query)`
    (3-4 coarse tiers, **not** identity); PII-screen every write; TTL + purge wired to RAG erasure.
19. **Curated canonical answer base** for the top ~30-50 helpdesk clusters — the single largest
    capacity multiplier; served ~10ms, keeps answering when inference is down.
20. **Durable Postgres `t5_ledger`** (post-pay check, spend gauge, 70/90/100% alerts) +
    `config/budget_envelopes.yaml` (one named holder; ops may alert, not raise a cap).
21. **DPIA-as-code**: `api/legal/data_manifest.yaml` (one entry per store: basis/purpose/location/
    `erasure_class` R|P|E/TTL/erasure) = Art. 30 register + nightly reaper config + CI gate.
    LiteLLM **metadata-only**. `erase_subject()` primitive over class-R stores; monthly scripted
    erasure drill (canary subject → erase → assert zero residual).
22. **Second-island CPU-only DR box** + **quarterly game-day** (the only thing that proves a
    restore works) + 3-class state split (legal/money core = ~1 MB/day append-only JSONL shipped
    off-box every 1-5 min; corbeille = nightly encrypted dump, RPO 24h; the rest = acceptable to
    lose). LUKS on both boxes.
23. **Secrets**: LUKS baseline + SOPS+age on the secrets file + migrate postgres/grafana/langgraph
    to Docker file-secrets. `docs/secrets_runbook.md` (per-secret rotation cadence; **any team
    departure → full rotation within 48h**).

### Phase 4 — deferred until the RTX 3090 / real load data
- Replace T3/T4 with **official vendor weights** (Qwen2.5-Coder-14B, Mistral-Small-24B class —
  never Ministral), IDs chosen by the admission harness. AWQ is GPU-only.
- Embedding-kNN categorical intent classifier replaces the scalar score (needs the corpus).
- vLLM continuous batching. Precise per-query ETA. RAG (`rag` service + pgvector) — but its
  per-chunk ACL needs the orchestrator auth (Phase 2) first.

## Round 5 additions to the roadmap (the 5 remaining facets, reviewed)
- **Breach-readiness = 4 composed artefacts**: a content-free **hash-chained scoping ledger**
  (the lint-enforced schema + prev-hash of the *already-shipped* request log — turns a maximal
  incident into "340 queries, 12 agents, 14:02-15:30, none Article-9, no T5") + **`breach_playbook.yaml`**
  (the CNIL-72h decision pre-adjudicated as code, one entry per store; auto-default applies *only*
  to the cheap reversible Art. 33 filing; Art. 34 always routes to a named alternate decider) +
  **~6 fail-loud tripwires on one out-of-band channel** (egress via a single forward proxy +
  ~5-entry allowlist, **not** host iptables default-deny; T5 alert = absolute ceiling primary) +
  **`sovereign-kill.sh`** (one idempotent script: egress-zero, stop, revoke key, freeze off-box
  ledger from the DR side, page, incident record; confirmation phrase + dry-run; runbook states
  the "blackout returns 5500 agents to public ChatGPT" tradeoff).
- **Structural log minimisation**: one `emit_event(type, **fields)` helper validated against
  frozen scalar/enum schemas + a CI AST-lint rule (no free text in logs, ever); **Agent Anone as
  a verdict-only black box** (never serialises `str(exc)` — it definitionally holds un-anonymised
  PII, and today `anone_api.py` leaks it into an outward-propagating reason string); unpublish
  Anone's `:8080`. **Follow the thread: if LiteLLM runs stateless too, nothing uses PostgreSQL →
  remove the container and close `:5432` entirely** — a bigger sovereignty win than any single
  logging fix.
- **JML = one idempotent daily reconciliation batch** (a leaver almost every working day at 5500
  — webhooks either rot or crush the team). Prefer a **DGRH roster CSV** so the box holds no
  tenant-wide Graph directory-read credential (a popped box would leak the whole government
  directory). Circuit breakers (roster-shrink >5% → abort; never straight-to-hard-erase).
  **De-identify derived data at *promotion*, not at erasure** — the editor accepting a signalement
  writes a fresh record with provenance = editor role-ID + date and drops the oid link, so the
  eval harness and canonical base are **class E by construction** and leave both the erasure drill
  and the JML lifecycle entirely (the highest-leverage sub-item).
- **Polynesian languages** — the safeguarding lexicon and PII gates are French-only, so a distress
  query or citizen PII in reo Mā'ohi / Marquesan / Pa'umotu **slips every gate**. Needs at minimum
  a language-ID gate that routes non-French input to a human, and an explicit written equity
  position (are Tahitian-comfortable agents disadvantaged by a French-only tool?).
- **`compliance/launch_dossier/`** (see finding #1 above) with templated drafts of every artefact
  (projet d'arrêté 6(1)(e), note DPO base légale, AIPD built on `data_manifest.yaml`,
  détermination Art. 36, inscription registre Art. 30, note Art. 13 + preuve de diffusion, saisine
  + PV d'avis du CTP, charte) + a reverse-planned Gantt from the next CTP session + `cost_estimate.md`.

## Facets still un-reviewed after 5 rounds (for a future round 6)
- **Initial content bootstrap** — who authors *and legally validates* the first 30-50 canonical
  fiches before launch (a large one-time project, distinct from the ongoing editorial owner; an
  empty base at launch = adoption collapse).
- **Helpdesk self-impact** — Parc & Assistance *is* the support desk; launching to 5500 agents
  generates a ticket surge onto the same 2-3 people.
- **Model licensing / provenance / AI-transparency** legal review for a government deployment;
  voluntary EU AI Act GPAI alignment.
- **Physical/environmental resilience** — where the box physically sits, UPS/cooling/access, RTX
  3090 procurement + spares lead time from Tahiti, dead-GPU runbook.
- **Formal RGAA audit + published déclaration d'accessibilité** (legal obligation; "RGAA-by-
  architecture" is a claim, not an audit).
- **Insider misuse / query-level purpose limitation** — an authenticated agent looking up a
  citizen they have no business reason to access (auth ≠ lawful purpose).
- **Software supply-chain / CVE watch** for LangGraph, LiteLLM, vLLM, oauth2-proxy, Ollama, base
  images — patching a security bug with no staging and no eval harness is itself a risk.

## Blocking operator decisions (nothing launches until these are answered)
The **45 questions** below. The 8 hard gates, in priority order:
1. **Has the PF DPO agreed IN WRITING** to own the compliance dossier and fund the recurring
   hours? If not — escalate now to the Secrétaire Général / cabinet du Président rather than let
   "no owner" persist silently. *(This is question #1 — everything else is downstream.)*
2. **Ship v1 with NO cloud/T5 tier?** — accepting that legal / RGPD / administrative-drafting
   questions get only a "consultez [service]" card for ~a year. Amends the frozen cascade.
3. **Replace the auto-cascade + kNN classifier with explicit user-chosen verbes + one local-only
   free-question lane; drop the open chat box?** Amends the frozen cascade.
4. **Run the ~15-25 person volunteer consent-based pilot** (accepting enthusiast selection bias)?
5. **Can the low/expected/high FTE funding actually be secured** across DGRH / DAF / DPO /
   editorial — or does this need a named political sponsor before any further build?
6. **Is Q1-Q2 2027 an acceptable launch window** (paced by the CTP calendar + arrêté en conseil
   des ministres), and is the project still worth doing on that timeline and cost?
7. **Fund a second-island DR box for v1**, or sign off on a 24h corbeille RPO + multi-day
   single-box outage risk (knowing corbeille tickets may carry safeguarding-relevant signalements)?
8. **Require DGRH to deliver a daily roster CSV** so the box holds no tenant-wide Graph
   directory-read credential (a popped box would leak the whole government directory)?

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
_(accumulated across rounds — 45 total; the 8 hard gates are in the CONSOLIDATION section above)_

### From round 5
36. **PF DPO written commitment** to own the compliance dossier + fund recurring hours — yes, or
    escalate to SG / cabinet du Président now?
37. **v1 with NO cloud/T5 tier** for ~a year — accepted? (amends the frozen cascade)
38. **Explicit verbes (Chercher/Rédiger/Traduire/Résumer) + one local-only question lane, no open
    chat box** — accepted? (amends the frozen cascade)
39. **~15-25 person volunteer consent-based pilot** — run it? (accept enthusiast bias)
40. **Fund a second-island DR box for v1**, or sign off on 24h corbeille RPO + multi-day outage?
41. **Q1-Q2 2027 launch window** — acceptable to you and leadership?
42. **Low/expected/high FTE funding** securable across DGRH/DAF/DPO/editorial, or needs a political
    sponsor first?
43. **Local (.pf) telco/SMS route** for out-of-band breach alerts so alerting metadata stays in PF?
44. **Who bootstraps + legally validates the initial 30-50 canonical fiches** — resourced as a
    distinct one-time project?
45. **Daily DGRH roster CSV** instead of a tenant-wide Graph directory-read credential on the box?

### From round 4
29. **Is the ~0.3-0.5 FTE editorial/triage owner a funded, named, standing role with a backup?**
    If it can't be funded at 0.5 FTE — which adopted items are cut?
30. Will **DPO, DGRH and DAF each formally commit** to staffing a functional escalation queue with
    a response SLA? If not, those domains get the redirect card with no callback promise.
31. Does the DSI have a **documented need to match a data subject against historical Article 46
    transfer-journal entries**, or is audit/proportionality the only purpose? (metadata-only journal
    vs. keyed digest + key custody)
32. **Launch strategy** — big-bang to 5500, or phased by direction? (drives onboarding gate,
    day-one capacity, required canonical-base coverage)
33. Will **DRH + secrétariat général co-sign the charte d'usage as a note de service** (disciplinary
    weight), not a standalone click-through?
34. Is the **interim CPU worker-VM's hosting itself sovereignty-compliant** for government personal
    data? (a rented hyperscaler VM running inference on agent queries is a sovereignty problem
    independent of cost)
35. Specific **decommissioned CPU box + rack space at a named second island** for DR — and can ops
    absorb ~½ day/quarter game-days + ~½ day/quarter secrets days?

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
