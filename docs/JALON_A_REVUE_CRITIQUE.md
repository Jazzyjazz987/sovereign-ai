# Jalon A (portail à fiches citées) — revue critique

2026-09-06. Le Jalon A est **livré et en service** (service `rag:8090`, câblage `api/main.py`,
étiquettes de confiance, screening). Cette revue liste ce qui est fragile ou manquant, **par
gravité**.

> **Suivi — 18/20 traités (commits 598b8f6, à venir).**
> - **C4** `:8090`/`:8888` en loopback ; `/ingest` fermé (403) sauf jeton + chemin confiné à `/corpus`.
> - **C5** modèles bakés dans l'image ; `HF_HUB_OFFLINE=1` / `TRANSFORMERS_OFFLINE=1` par défaut.
> - **C6** `safeguarding.validated` → avertissement sur la carte + `/health`.
> - **C1** `RAG_SCORE_FLOOR` / `RAG_SCORE_HIGH` + confiance à 2 niveaux (champ `confidence`), *non validés*.
> - **C2** contrat JSON `{repond, reponse, fiches}` (Ollama `format=json`) au lieu du string-match.
> - **C3** rejet si une citation `PROC-*` est absente des extraits fournis.
> - **C8** gate hors-périmètre déplacé après le RAG.
> - **C9** expansion `related` : les « Procédures liées » du top des résultats sont ajoutées
>   en contexte (`via_related`) — multi-fiches.
> - **C10** `fiches[].score` = max des chunks ; voisines dans l'ordre RRF.
> - **C11** cache de réponses T0 : `sha256(requête normalisée)`, TTL `RAG_CACHE_TTL` (3600 s),
>   `POST /cache/clear`, seulement pour `tier ∈ {RAG, aucune-fiche, hors-perimetre}`. 2ᵉ appel : ~0 s.
> - **C12** empreinte `rag_prompt`. **C13** latence par tier.
> - **C14** `RAG_MAX_CONCURRENCY` (3) sur `/search` → `503` au-delà (`rag_search_busy_total`,
>   `rag_search_inflight`).
> - **C15/C16/C17** lifespan, `k` borné 1-20, `init_db` au démarrage.
> - **C18** un terme support annule le raccourci « smalltalk ». **C19** préfixe `passage:` retiré
>   avant le reranker.
> - **C20** deux tests d'intégration `/query` (chemin RAG, priorité sauvegarde).
> - **Bug corrigé au passage** : `_rrf` gardait la version non rerankée d'un chunk présent dans
>   deux listes → `rerank_score` perdu, confiance calculée sur le cosinus. Fusion des champs.
>
> - **C7** (commit 15568b0) : compteur `query_ungated_no_scope_total` (requête → cascade sans
>   fiche / sans vocab / sans motif hors-sujet). Aucun texte journalisé. La blocklist reste un
>   compromis assumé ; ce taux dit à l'opérateur s'il faut la compléter ou ajouter des fiches.
>
> **Reste (relève du Jalon C, pas du Jalon A) :**
> - **`comp-depart-agent`** — synthèse multi-hop inter-chaînes (`PROC-ID-003` n'est pas dans le
>   `related` de `PROC-STOCK-005`). L'extraction de codes depuis les pages 00-* a été essayée
>   puis écartée (dégradait le palier 4). → fine-tuning reranker + prompt de synthèse, ou un
>   graphe d'événements « départ agent / arrivée / mutation » explicite.
> - Palier 4 `attendu_ok` **varie 50-75 %** selon le tirage `qwen2.5:7b` (`lim-vip-iles`,
>   `lim-prestataire`) → même levier.

État mesuré : éval pipeline complet paliers 1/4/5 forts (recall@1 100 %, tier_ok 7/7),
3 cas résiduels (`docs/EVAL_BASELINE.md`).

---

## 🔴 Sérieux — à traiter avant un usage réel

### C1 — Le seuil `RAG_MIN_RERANK = 0.0` ne filtre presque rien
Dans l'éval, les bonnes réponses scorent de **0,01 à 1,0**, les mauvaises de **0,0 à 0,3**.
Le seuil à 0 laisse tout passer ; le vrai tri vient du filtre `proc_code`, du regroupement
par domaine et de **l'auto-déclaration du modèle** (« Je n'ai pas de fiche »). Conséquence :
la décision « fiche exploitable ou non » repose sur des signaux indirects, non calibrés.
→ Remplacer par une règle de **marge** (écart primaire vs bruit) ou un **percentile**, et
re-dériver après tout changement de reranker. Documenter la constante comme *non validée*.

### C2 — La détection « pas de fiche » est du string-matching sur la sortie du modèle
`text.lower().startswith("je n'ai pas de fiche") and len(t) < 130`. Fragile des deux côtés :
- « Je n'ai pas de fiche exhaustive, mais PROC-X impose… » (131 car.) → passe et **répond**
- une bonne réponse qui commence par cette tournure → **jetée à tort**

C'est un contrat implicite avec un modèle 7B non déterministe. → Il faut un signal
**structurel** : sortie JSON `{repond: bool, fiches: [...]}`, ou un mini-classifieur, ou
s'en tenir au seul gate de score (C1) sans demander au modèle de s'auto-évaluer.

### C3 — Aucune vérification que la réponse est fidèle à ses citations
Le prompt *demande* de ne citer que les extraits, rien ne le **vérifie**. Une étape inventée
au milieu d'une réponse par ailleurs sourcée passe (l'éval `citation_ok` ne teste que le
recouvrement avec le gold, pas la fidélité). → Post-contrôle : chaque code cité existe et est
dans `usable` ; idéalement un contrôle d'ancrage (NLI ou recouvrement lexical) des phrases.

### C4 — `rag:8090` publié sur `0.0.0.0`, `/ingest` non authentifié
`docker-compose.yml` mappe `8090:8090`. `POST /ingest {"path": "/quelconque"}` lit tout
`*.md` du chemin monté et l'indexe — endpoint d'admin **sans auth** sur un port exposé.
Même classe de problème que `:8888`/`:4000`/`:5432` (DESIGN_REVIEW Phase 2 : « unpublish
data-plane ports »). → `expose:` au lieu de `ports:` (accès interne seul), ou proxy
d'identité devant. `/ingest` derrière une clé ou retiré du service (ré-ingestion = script).

### C5 — Air-gap : modèles non embarqués dans l'image
Le `Dockerfile` du service `rag` **ne bundle pas** e5-base (~440 Mo) ni bge-reranker-base
(~1,1 Go) — ils se téléchargent au 1er démarrage dans le volume `rag_hf_cache`. Pour la
salle fermée : le volume doit être pré-rempli **ou** les modèles copiés dans l'image
(`docker save`). `HF_HUB_OFFLINE=1` n'est pas posé → risque d'appel réseau silencieux.
→ Étape de provisionnement à écrire ; poser `HF_HUB_OFFLINE=1` + `TRANSFORMERS_OFFLINE=1`.

### C6 — Carte de sauvegarde avec des numéros non validés
`screening.yaml` : « SOS Suicide Polynésie 40 44 47 48 » + « coordonnées à compléter par la
DSI ». Un numéro d'urgence **faux** est un préjudice direct. → Validation formelle DSI avant
mise en service ; ajouter un drapeau `validated: false` bloquant en attendant.

---

## 🟠 Modéré — dette à cadrer

### C7 — Gate hors-périmètre = liste noire, maintenance sans fin
`is_out_of_scope` matche `capitale de`, `recette`, `poème`… Toute formulation hors sujet
absente de la liste part en **génération libre T1**. L'éval ne teste que les motifs listés :
couverture réelle inconnue. → Soit assumer (et suivre les faux négatifs en prod via un log
des requêtes tier=T1 sans fiche), soit repasser à un **gate positif** (répondre seulement si
fiche trouvée OU vocabulaire support fort).

### C8 — Le gate hors-périmètre s'exécute AVANT le RAG
« quelle est la date de péremption d'un certificat de destruction ? » → `date de` matche la
blocklist. Sauvé ici par `scope_lexicon` (`destruction`), mais l'ordre est risqué. →
Déplacer le gate **après** le RAG : ne refuser que si le RAG n'a rien ET motif hors-sujet.

### C9 — `related` (graphe des procédures liées) calculé mais inutilisé
`chunker` extrait « Procédures liées », `store` le persiste, `/search` le renvoie —
`_rag_answer` ne s'en sert jamais. C'est exactement le levier du cas résiduel
`comp-depart-agent` (STOCK-005 → related STOCK-006, TER-006). → Expansion multi-fiches par
`related` quand la question est large.

### C10 — `fiches[].score` trompeur pour l'UI
C'est le `rerank_score` d'**un** chunk de la fiche (le premier de `usable`), pas le meilleur.
La fiche primaire peut afficher `0,08` (chunk §Points de vigilance) alors qu'un chunk
§Étapes scorait `0,9`. → `max` sur les chunks de la fiche, ou retirer le champ.

### C11 — Pas de cache de réponses (« T0 »)
Chaque « comment créer une BALP » refait embed + lexical + rerank + qwen (~4 s). Le
DESIGN_REVIEW nomme la base d'answers canoniques « le plus gros multiplicateur de capacité ».
→ Cache clé = `sha256(requête normalisée)` (pas d'identité), TTL, purge à la ré-ingestion.

### C12 — `prompt_set` renvoyé par la réponse RAG est faux
La réponse RAG porte `prompt_set: PROMPT_SET_FP` (empreinte du *prompt pack*), mais elle
utilise `RAG_SYSTEM` (chaîne en dur dans `main.py`). Les changements de `RAG_SYSTEM` ne sont
tracés par **aucune empreinte**. → Empreinte dédiée `rag_prompt` (comme `screening.config`).

### C13 — Observabilité : latence non ventilée par tier
`QUERY_LATENCY` mélange RAG (~4 s), `sauvegarde` (~1 ms), `aucune-fiche` (~2 s), cascade.
Pas de métrique « temps de recherche RAG » vs « temps de génération qwen ». → Histogramme
par `tier` ; le service `rag` expose déjà `rag_search_latency_seconds`, le relier au dashboard.

### C14 — Concurrence : `OLLAMA_NUM_PARALLEL=1` + reranker CPU bloquant
Le reranker (~1,8 s CPU) et qwen (RAG) se sérialisent avec toute la cascade. Pour ~8 agents
c'est probablement tenable, mais aucune file ni limite : une rafale empile les requêtes
(timeout `_rag_search` 30 s + `query_ollama` 120 s = requête à 150 s au pire, sans deadline
globale). → File bornée + une réponse « service occupé, réessayez » au-delà.

---

## 🟡 Mineur

- **C15** — `service.py` : `@app.on_event("startup")` déprécié (FastAPI lifespan).
- **C16** — `/search` ne borne pas `k` (accepte `k=10000`).
- **C17** — `service.py` n'appelle jamais `store.init_db()` : sur un volume Postgres vierge
  sans ingestion, `/search` renvoie 500 jusqu'au premier `/ingest`.
- **C18** — `_SMALLTALK` matche « merci … » : « merci, et pour le MFA ? » (< 60 car.) saute
  le RAG.
- **C19** — le texte des chunks est stocké avec le préfixe `passage:` (pour e5) ; le
  reranker le reçoit tel quel (bruit léger, bge n'attend pas ce préfixe).
- **C20** — pas de test d'intégration bout-en-bout du chemin `/query`→RAG (les 30 pytest
  sont unitaires + `_rag_answer` mocké). L'éval `run.py` joue ce rôle mais hors CI.

---

## Ce que le Jalon A fait bien

- Ordre déterministe clair : sauvegarde → hors-périmètre → RAG → cascade → aucune-fiche.
- Fail-open sur RAG indisponible (cascade), fail-closed sur « périmètre sans fiche »
  (pas de génération — E6).
- Étiquettes de confiance présentes (`Fondé sur fiches CPA` / `Généré localement — à
  vérifier` / `Aucune fiche` / `Voie de sauvegarde` / `Hors périmètre`).
- Lexiques screening éditables par l'opérateur, empreinte dans `/health`.
- Récupération hybride (vecteur + lexical + reranker RRF) — recall@1 100 % en récupération
  seule sur les paliers 1-4.
- Jeu d'éval reproductible (`eval/run.py`), 30 pytest verts.

---

## Priorisation proposée

| # | Item | Effort | Pourquoi maintenant |
|---|------|--------|---------------------|
| 1 | **C6** valider la carte de sauvegarde | S (opérateur) | préjudice direct |
| 2 | **C4** dé-publier `:8090` + garder `/ingest` | S | surface d'attaque |
| 3 | **C5** modèles hors-ligne (image + `*_OFFLINE=1`) | M | bloque l'air-gap |
| 4 | **C2 + C1** contrat « pas de fiche » structurel + seuil calibré | M | fiabilité du cœur |
| 5 | **C8** réordonner gate hors-périmètre après RAG | S | évite les refus à tort |
| 6 | **C3** post-contrôle des citations | M | responsabilité juridique |
| 7 | **C12 + C13** empreinte `rag_prompt` + latence par tier | S | traçabilité / pilotage |

C9 (expansion `related`) et C11 (cache) relèvent plutôt du Jalon C / de l'optimisation.

---

# Seconde revue — après les correctifs C1-C20 (2026-09-06)

Regard critique sur l'état *actuel* : ce que les correctifs ont introduit, et ce que la
première revue a manqué. Par gravité.

## 🔴 Sérieux

### D1 — C1 n'est corrigé qu'en façade
`RAG_SCORE_FLOOR = -1.0` : sur les 20 candidats rerankés, presque aucun ne descend sous
-1 → le plancher ne filtre quasiment rien, comme l'ancien `RAG_MIN_RERANK = 0.0`.
`RAG_SCORE_HIGH = 0.30` (seuil « à vérifier » vs « fondé sur fiches ») a été posé à l'œil
sur **6 points de données**. Le vrai correctif — calibration sur le jeu d'éval, ou règle
de **marge** (primaire vs médiane du bruit) — n'est pas fait. À traiter avec le
fine-tuning du reranker (les seuils devront de toute façon être re-dérivés).

### D2 — C3 ne couvre pas les citations en prose
Le post-contrôle vérifie `obj["fiches"]` (liste déclarée par le modèle), **pas** les
codes `PROC-*` glissés dans le texte de `reponse`. Un « … voir PROC-XX-999 » au fil de
la phrase passe. → Aussi passer `_PROC_RE.findall(answer)` au même filtre.

### D3 — Cache T0 : mémoire non bornée + pas d'invalidation à la ré-ingestion
- `_resp_cache` grandit d'une entrée par requête normalisée distincte, **sans plafond** ;
  le nettoyage TTL n'a lieu qu'à la lecture d'une clé → une entrée jamais re-posée reste
  en mémoire jusqu'au redémarrage. → cap LRU + purge périodique.
- Une fiche mise à jour dans Confluence → ré-ingérée → l'ancienne réponse est servie
  encore **1 h** (il faut appeler `/cache/clear` à la main). Aucun lien rag `/ingest` →
  langgraph. → au minimum, inclure l'empreinte du corpus (`rag /health.corpus`) dans la
  clé de cache, rafraîchie périodiquement.
- On met en cache les réponses **basse confiance** (« à vérifier ») et **négatives**
  (`aucune-fiche`) : si une fiche est ajoutée sur le sujet, la réponse « aucune fiche »
  persiste 1 h. Discutable.

### D4 — Aucune échéance globale sur `/query`
`_rag_search` 30 s + `_rag_answer`→`query_ollama` 120 s + repli cascade (T4→T1, 120 s
chacun) → une requête peut courir **~10 min** si Ollama se fige. Rien n'enveloppe
`_query_cascade` dans un `asyncio.wait_for`. Le sémaphore C14 ne borne que `/search`.

### D5 — Le contrat JSON n'a pas de sonde
Tous les tests mockent `query_ollama`. Si une MAJ de `qwen2.5:7b` casse la forme
`{repond, reponse, fiches}` (ex. renvoie `{"answer": …}`), **tout** tombe silencieusement
en « pas de fiche » / cascade, sans alerte. → un test d'éval « le modèle rend bien la
forme attendue » à faire tourner au démarrage ou en CI, + une alerte sur
`rag_answers_total{outcome="parse_error"}`.

## 🟠 Modéré

### D6 — RAG sans plafond de génération
`query_ollama` pour le RAG ne pose pas `num_predict` (Ollama) → une réponse verbeuse de
qwen n'est pas bornée (latence, lisibilité). Idem cascade.

### D7 — Sur-prompt du 7B
`RAG_SYSTEM` = ~8 règles distinctes (forme JSON, logique `repond`, contournement, pas
d'invention, signaler les contraintes, citer, être concis). C'est à la limite de ce
qu'un 7B tient — la variance du palier 4 (`attendu` 50-75 %) vient en partie de là. →
prompt plus court et plus net ; déplacer une partie de la logique en post-traitement.

### D8 — Parcours de cycle de vie (JML) = trou produit, pas bug
Départ / arrivée / mutation d'agent sont **les événements CPA les plus fréquents** (page
Onboarding, RACI, Registre RGPD les regroupent) et le RAG ne sait pas synthétiser
« départ → PROC-ID-003 + INT-005 + STOCK-005 + TER-006 ». Le DESIGN_REVIEW le nommait
« sous-item à plus fort levier ». → une **réponse canonique rédigée et validée** pour
ces 3-4 parcours (comme la « base de fiches canoniques » du DESIGN_REVIEW), pas du RAG.

### D9 — Métriques présentes, aucun tableau de bord
`rag_search_latency_seconds`, `query_latency_seconds{tier}`, `rag_answers_total{outcome}`,
`query_ungated_no_scope_total`, `query_cache_hits_total` : tout est scrapé, rien n'est
visualisé. « Jalon A fini » devrait inclure un dashboard Grafana (taux de réponse RAG,
taux hors-périmètre, taux in-scope-sans-fiche, cache hit, latence par tier).

### D10 — Incohérence `fiches` affichées vs grounding réel
`fiches` (rendu à l'UI) vient de la récupération (`usable`). La liste `cited` du modèle
(utilisée pour C3) peut différer. L'agent voit des fiches que le modèle n'a peut-être pas
utilisées, et ne voit pas lesquelles ont réellement porté la réponse.

## 🟡 Mineur

- **D11** — `_cache_key` ne normalise pas les accents (« creer » ≠ « créer ») → taux de
  hit réel faible.
- **D12** — « merci » (smalltalk) déclenche quand même une génération cascade (~4 s) pour
  rien ; une réponse figée suffirait.
- **D13** — pas de test d'intégration de l'**ordre** screening→RAG→hors-périmètre→cascade
  (un revert de C8 passerait les tests).
- **D14** — volume `rag_hf_cache` monté sur `/models/hf` masque les modèles bakés dans
  l'image (fonctionne, mais fragile sur un déploiement USB neuf). → monter en `:ro` ou
  supprimer le volume.
- **D15** — la voie de sauvegarde sert la carte **non validée** en entier ; pour une
  fonction de sécurité, un repli minimal « 15 / 17 / 18 » jusqu'à validation serait plus
  prudent (débat).

## Priorisation (seconde vague)

| # | Item | Effort |
|---|------|--------|
| 1 | **D4** échéance globale `/query` (`asyncio.wait_for`) | S |
| 2 | **D2** C3 étendu aux citations en prose | S |
| 3 | **D3** cache : cap LRU + empreinte corpus dans la clé + `/cache/clear` auto à l'ingest | M |
| 4 | **D5** sonde du contrat JSON (démarrage + alerte `parse_error`) | S |
| 5 | **D8** réponses canoniques « parcours agent » (départ / arrivée / mutation) | M — **fort levier** |
| 6 | **D9** dashboard Grafana RAG | M |
| 7 | **D1** calibrer les seuils (avec le fine-tuning) | — Jalon C |
| 8 | **D6/D7** plafond `num_predict` + prompt raccourci | S |
