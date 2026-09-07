# Jalon A (portail à fiches citées) — revue critique

2026-09-06. Le Jalon A est **livré et en service** (service `rag:8090`, câblage `api/main.py`,
étiquettes de confiance, screening). Cette revue liste ce qui est fragile ou manquant, **par
gravité**.

> **Suivi (commit à venir)** — traités : **C4** (`:8090`/`:8888` en loopback, `/ingest`
> fermé sauf jeton), **C5** (modèles embarqués dans l'image + `*_OFFLINE=1` par défaut),
> **C6** (drapeau `safeguarding.validated` + avertissement sur la carte + `/health`),
> **C1** (seuils `RAG_SCORE_FLOOR`/`RAG_SCORE_HIGH` + confiance à 2 niveaux, documentés
> *non validés*), **C2** (contrat JSON `{repond, reponse, fiches}` au lieu du string-match),
> **C3** (post-contrôle : toute citation `PROC-*` doit être une fiche fournie, sinon rejet),
> **C8** (gate hors-périmètre déplacé après le RAG), **C10** (`fiches[].score` = max ;
> voisines dans l'ordre RRF), **C12** (empreinte `rag_prompt`), **C13** (latence par tier),
> **C15/C16/C17** (lifespan, `k` borné, `init_db` au démarrage).
> Restent : **C7** (blocklist), **C9** (`related` inutilisé), **C11** (cache), **C14**
> (concurrence), **C18/C19/C20**.

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
