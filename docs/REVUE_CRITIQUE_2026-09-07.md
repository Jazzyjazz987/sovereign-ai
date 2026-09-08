# Revue critique globale — 2026-09-07

Troisième passe critique, cette fois sur **l'ensemble du système tel qu'il tourne
aujourd'hui**, après le travail Jalon A / Jalon B / C1-C20 / D1-D15. Elle regarde ce que
les deux revues précédentes n'ont pas couvert (elles portaient sur le RAG) et ce que le
travail récent a laissé de côté ou introduit.

Méthode : lecture du code réellement embarqué dans les images, de `docker-compose.yml`,
de l'état runtime (`/health`, cibles Prometheus, volumes, images), croisement avec
`docs/DESIGN_REVIEW.md` (5 rounds) et la POC SHORTLIST.

---

## Résumé exécutif — la vérité désagréable

Le **portail à fiches citées fonctionne bien** (paliers d'éval 1/3/4/5 solides, screening,
parcours, audiences). Mais **autour** de ce portail, la « stack sovereign AI T1→T5 »
décrite dans `CLAUDE.md` et `/health` **n'existe pas** telle qu'affichée :

- la **cascade T1-T4 est un seul modèle** (`qwen2.5:7b`) appelé avec l'un de 4 prompts
  quasi identiques ; le routeur par « score de complexité » ne choisit rien d'utile ;
- **T5** (Claude) est le chemin **le moins fiable** (aucune fiche, aucun contexte CPA,
  prompt générique) — il **invente** — le plus cher, le seul qui franchit la frontière de
  souveraineté, et il est **actif** avec un garde-fou de budget qui se remet à zéro à
  chaque redémarrage ;
- **Agent Anone** — le point sur lequel repose toute la promesse « rien de nominatif vers
  le cloud » — est **un seul modèle ML à seuil 0,5**, sans la couche déterministe
  (regex NIR / IBAN / +689 / e-mail M365) que la revue de conception classait *n°1 en
  valeur/effort* ;
- **LiteLLM tourne pour rien** (le code l'ignore) mais détient la clé Anthropic ;
  **vLLM T3/T4** (65 Go d'images) sont abandonnés ; **~1000 lignes** de code `api/` sont
  mortes ;
- **l'air-gap est troué** : le modèle `qwen2.5:7b` est tiré par `ollama pull` au démarrage
  (besoin d'internet) et n'est **sauvegardé nulle part** — perte du volume `ollama_data`
  dans le local fermé = système mort, non récupérable ;
- **aucune procédure de sauvegarde/restauration**, aucun test de restauration ;
- **la supervision 24/7 est à ~80 % morte** : les règles d'alerte visent des métriques
  (`node_*`, `pg_up`, `nvidia_smi_*`, `vllm_*`) qu'**aucun exporter ne produit** ;
- **Jalon B (audiences) n'est pas appliqué** — sans authentification sur `:8888`, le profil
  se passe dans le corps de requête : n'importe qui sur la boîte lit la base atelier en
  écrivant `{"audience":"atelier"}` ;
- **l'UI de démo** (`static/index.html`, juin) n'affiche **aucune** des étiquettes de
  confiance / sources / bannières que l'API renvoie ;
- **la voie « rédiger la réponse au ticket »** (2ᵉ usage cœur de la POC SHORTLIST) **n'a
  pas été construite** ;
- **le corpus des 34 procédures a été généré par IA** (projet « Rédacteur de procédure »)
  et **personne ne l'a vérifié opérationnellement** — l'éval mesure la fidélité à un
  document d'exactitude inconnue.

Rien de tout cela n'empêche une démo. Tout cela empêche de dire « c'est prêt ».

---

## Constat 1 — La cascade derrière le RAG est un décor

`api/main.py` :
```
TIERS = [("T1","qwen2.5:7b"), ("T2","qwen2.5:7b"), ("T3","qwen2.5:7b"),
         ("T4","qwen2.5:7b"), ("T5","claude-sonnet")]
```
- **T1 à T4 = le même modèle.** Le `CascadeRouter` calcule un score 1,0-5,0 par sac de
  mots-clés et choisit un tier — qui ne change que le *prompt système* (`prompts.yaml`),
  pas le modèle. « Routé en T3 » vs « routé en T4 » = zéro différence de capacité.
- `"claude-sonnet"` dans `TIERS[4]` est une **chaîne morte** : le vrai modèle vient de
  `T5_MODEL` (`claude-sonnet-5`). `list_models()` et le repli s'appuient quand même dessus.
- Le sac de mots-clés est **buggé** : `"quoi"` est dans `simple_keywords` → `"pourquoi le
  poste ne démarre pas"` matche (sous-chaîne) et baisse la complexité ; `code_keywords`
  contient `"error"`/`"bug"` (anglais) — inopérant sur « erreur » ; `"test"`, `"api"` sur-
  déclenchent.
- La revue de conception (R1.6, adoptée) demandait : **remplacer le scalaire par un
  classifieur d'intention kNN** (ou des verbes explicites) — *« un scalaire force un faux
  ordre total sur des tiers qui sont des domaines »*. **Non fait.** Le scalaire est
  toujours là, et il ne sert désormais quasiment à rien.

**Architecture honnête aujourd'hui :** `portail RAG` → (repli) *un* appel `qwen2.5:7b` avec
1 prompt sur 4 → (rare) *un* appel Claude sans ancrage. Le « T1→T5 » de `/health` et de
`CLAUDE.md` est une fiction entretenue dans le code, la doc, les métriques et l'éval.

→ **Correction :** assumer 2 tiers — `local` (qwen) et `central` (T5, quand il aura un
sens) — supprimer `CascadeRouter`, router par intention (question / rédaction / hors
sujet), aligner `CLAUDE.md` et `/health`.

---

## Constat 2 — T5 : le maillon le plus faible, le plus cher, et il est actif

`route_t5_with_anonymization` :
- **Prompt système générique**, **aucune fiche**, **aucun contexte CPA** :
  `"Assistant IA francophone pour la DSI… précise, officielle et concise."` Sur une
  question support qui atteint T5, Claude répond **de mémoire paramétrique** → invente une
  procédure plausible et fausse. C'est l'**inverse** du design « fiche citée = confiance » :
  le tier d'escalade est le **seul sans ancrage**.
- **`requests.post` (synchrone) + SDK Anthropic (synchrone) dans une coroutine `async`** →
  pendant un appel T5, **tout le serveur langgraph est gelé** pour les autres requêtes. Le
  garde-fou D4 (`asyncio.wait_for`) **ne peut pas** annuler un appel bloquant.
- **`_t5_calls` = compteur en mémoire, remis à zéro à chaque redémarrage** (R3.5 :
  *« un crash-loop n'a aucun plafond de dépense cloud »*). La revue demandait un
  **`t5_ledger` durable en Postgres**. **Non fait.**
- **`T5_MODERATION` par défaut = `off`** dans `docker-compose.yml` (`.env` le force à `on`).
  Défaut *fail-open* pour un garde-fou budget + souveraineté : si `.env` est régénéré ou
  perdu, T5 part sans modération.
- **Aucune base de transfert** (SCC / TIA) enregistrée. La revue : *« chaque appel T5 est
  juridiquement un transfert Article 46 »* (la DSI garde `pii_mapping`, la clé de
  ré-identification). L'opérateur a sorti la gouvernance des données du périmètre — mais
  la conclusion de la revue était justement : **c'est pour ça que la voie la plus propre
  est « v1 sans T5 »** (hard-gate n°2, question ouverte).
- **Quand T5 se déclenche-t-il réellement ?** Presque jamais : il faut score ≥ 4,5 ET RAG
  rien ET pas hors-sujet ET pas smalltalk ET (`RAG_STRICT` on) pas de vocabulaire support
  — sinon `_no_fiche_response` intercepte avant le routage. Donc T5 = un chemin quasi mort
  qui invente quand il vit, avec une clé API facturable branchée dessus.

→ **Correction :** décider (hard-gate n°2). Si T5 reste : (a) lui donner les extraits RAG
en contexte comme le portail local, (b) `httpx` async + `anthropic.AsyncAnthropic`, (c)
`t5_ledger` durable, (d) `T5_MODERATION` défaut `on`. Si T5 sort : supprimer le chemin, la
clé du service `litellm`, `_await_t5_approval`, `T5_PRICES` — ~200 lignes et une clé
facturable en moins.

---

## Constat 3 — Agent Anone : la souveraineté tient à un modèle ML au seuil 0,5

`anone_api.py` : `ner.predict_entities(text, PII_LABELS, threshold=0.5)` — c'est tout.

- **Pas de couche déterministe.** La revue R1.2 (*« meilleure valeur par effort ; la coupe
  la moins chère du risque de queue qui rend le chemin cloud indéfendable »*) demandait :
  **regex + checksum pour NIR (clé de contrôle 987/988), IBAN (mod-97), téléphones +689,
  e-mails M365, matricule DSI**, *avant* GLiNER, + **canari post-masquage** (re-scanner le
  texte masqué), + **re-scan juste avant l'appel Anthropic**, tout *fail-closed*.
  **Rien de cela n'existe.**
- **GLiNER a un rappel < 100 %** par nature. Un NIR, un téléphone, une adresse e-mail
  ratés → **fuite propre et silencieuse vers Anthropic.**
- **Seuil 0,5 non validé.** Pour du *fail-closed*, on veut un seuil **bas** (sur-masquer) —
  quitte à dégrader la réponse, c'est la direction sûre.
- **Labels manquants** : matricule agent, date de naissance.
- Image `anone` = **13,2 Go** sur base `nvidia/cuda` alors que GLiNER **tourne sur CPU**
  (par conception, `CLAUDE.md`). Poids mort sur une boîte à sauvegarde USB.
- La revue R5 note aussi : *« Anone comme boîte noire verdict-only — ne jamais sérialiser
  `str(exc)` : par définition il détient de la PII non anonymisée »*. Or `anone_api.py`
  renvoie `detail=f"erreur anonymisation: {exc}"` dans une 503 qui remonte vers
  `main.py` → potentiellement dans un log ou une réponse.

**C'est la seule vraie faille de la promesse « souveraineté ».** Et elle ne compte que
parce que T5 existe (constat 2). Sans T5, Anone ne sert plus qu'à… rien (aucun autre
chemin ne quitte la boîte).

---

## Constat 4 — Code mort et services morts

| Élément | État |
|---|---|
| `api/main_flask.py`, `main_fastapi.py`, `chat_app.py` | **0 référence** — ~480 lignes mortes |
| `api/cascade_router.py`, `ollama_client.py`, `vllm_client.py` | référencés seulement entre eux / vieux tests ; `main.py` a tout ré-implémenté en interne — ~500 lignes en double |
| `docker-compose-core.yml` | 2ᵉ fichier compose, périmé (juin) |
| **service `litellm`** | **tourne** (port 4000, image 1,35 Go, hack d'entrypoint) mais `main.py` l'**ignore totalement** : `litellm_api_key` est lu puis jamais utilisé. Il détient quand même `ANTHROPIC_API_KEY` dans son env. La revue : soit *router T5 à travers lui* (clé + dépense au même endroit), soit *le supprimer*. Actuellement : le pire des deux. |
| images `sovereign-ai-vllm-t3/t4` | **65 Go**, jamais démarrées, abandonnées (RAG-only) ; `.env` garde `VLLM_API_KEY`, `VLLM_T3_PORT`, `VLLM_T4_PORT` |
| tables `langgraph.graph_state`, `litellm_logs` | créées par `postgres_init.sql`, **rien n'écrit dedans** |
| build cache Docker | **90 Go** ; images totales **115 Go** ; `docker system prune` en retard |

→ **Correction :** `git rm` les 6 fichiers morts + `docker-compose-core.yml` ; retirer le
service `litellm` (ou l'utiliser) ; `docker image rm` vllm-t3/t4 ; nettoyer `.env` ;
`docker builder prune`. ~1 h, et le dépôt cesse de mentir sur ce qu'il est.

---

## Constat 5 — L'éval mesure un système réglé sur elle, sur un corpus non vérifié

- **44 cas, itérés en boucle contre le code toute la session.** Les 100 % de recall@1 aux
  paliers 1/3/4 sont réels mais obtenus en partie en **déplaçant des `gold`**, en
  **ajustant des `interdit`**, en **ajoutant `parcours.yaml`** qui satisfait *directement*
  le palier 3, en calant `RAG_SCORE_HIGH` à l'œil. Une part est légitime (mauvais labels),
  une part est du **sur-apprentissage sur le jeu de test**.
- **Pas de jeu tenu à l'écart (held-out).** Pas de séparation dev/test.
- **L'éval n'est pas en CI** (R1.1 : *« gate tout changement ultérieur, tourne en CI »*).
  Elle se lance à la main.
- **Palier 4 `attendu_ok` oscille 25-100 % d'un run à l'autre** — l'éval mesure en partie
  le tirage de dé de `qwen2.5:7b`.
- **Le corpus des 34 procédures a été rédigé par l'opérateur avec Claude** (« 2025
  Rédacteur de procédure »). **Personne n'a vérifié qu'elles sont opérationnellement
  exactes.** Les réponses « gold » de l'éval sont dérivées de ce corpus. On mesure la
  fidélité à un document d'exactitude inconnue. C'est le **bootstrap de contenu** que la
  revue R5 listait comme *facette non revue* : *« qui rédige ET valide juridiquement les
  30-50 premières fiches — un chantier ponctuel, distinct de l'éditeur permanent ; base
  vide au lancement = effondrement de l'adoption »*.

→ **Correction :** faire relire les 34 procédures par le chef CPA (marquer chaque fiche
`valide_le` / `valideur`), figer un jeu d'éval tenu à l'écart, mettre `eval/run.py` en CI
(mode récupération seule, CPU, rapide), accepter que le palier 4 (`attendu`) restera
bruité tant que le modèle de rédaction est un 7B non fine-tuné.

---

## Constat 6 — La confiance RAG est cosmétique (D1, redit fort)

- `RAG_SCORE_FLOOR = -1.0` ne filtre **quasiment rien** (bge-reranker-base descend
  rarement sous -1 sur des candidats déjà récupérés).
- `RAG_SCORE_HIGH = 0.30` (seuil « Fondé sur fiches CPA » vs « à vérifier ») a été posé en
  **regardant 6 points de données**.
- Donc l'étiquette de confiance à 2 niveaux — celle qui est censée calibrer la confiance
  de l'agent — repose sur un nombre non validé.
- Après un fine-tuning du reranker (Jalon C), **tous ces seuils changent** et doivent être
  re-dérivés. La confiance actuelle est un placeholder en costume.

→ **Correction :** dériver les seuils du jeu d'éval (courbe précision/rappel du reranker
sur les paires requête↔fiche), ou passer à une **règle de marge** (score primaire − médiane
du reste). À faire **avec** le fine-tuning, pas avant.

---

## Constat 7 — Boîte unique, GPU unique, aucune sauvegarde — et l'air-gap est troué

- **1 boîte, 1 RTX 3080 Ti.** 7 services + tous les modèles dessus.
- **Aucun script de sauvegarde/restauration.** `scripts/` a des utilitaires GPU / santé /
  mode, **rien pour l'état**. `CLAUDE.md` dit « sauvegarde USB manuelle » — mais **quoi**
  exactement ? Pas de `backup.sh`, pas de doc, pas de test de restauration.
- **Le trou air-gap : `qwen2.5:7b`.** `scripts/ollama_init.sh` fait `ollama pull qwen2.5:7b`
  au démarrage → **besoin d'internet**. Le modèle n'est **baké nulle part** et n'entre dans
  **aucune** procédure de snapshot. **Perte du volume `ollama_data` dans le local fermé =
  système mort, non récupérable** (impossible de re-tirer le modèle sans réseau). J'ai
  corrigé ce point pour les modèles du RAG (bakés dans l'image) — **pas pour Ollama.**
- État à sauvegarder et sa criticité :
  | Volume | Contenu | Perte = |
  |---|---|---|
  | `ollama_data` | `qwen2.5:7b` (~4,7 Go) | **système mort en air-gap** |
  | `postgres_data` | chunks RAG + embeddings 768-dim + état langgraph | ré-ingestion depuis `corpus/` (récupérable, non testé) |
  | `rag_hf_cache` | e5-base + reranker | re-copié depuis l'image (OK) |
  | `grafana_data` | dashboards custom + users | mineur |
- **Aucun onduleur / refroidissement / runbook GPU mort** documenté (facette non revue R5).

→ **Correction (prioritaire) :** `scripts/backup.sh` qui `docker run --rm -v <vol>:/v -v
$USB:/b alpine tar czf /b/<vol>.tgz -C /v .` pour `ollama_data` + `postgres_data` (+
`config/`, `corpus/`, `.env`) ; `restore.sh` symétrique ; **un test de restauration** sur
une 2ᵉ machine ou un `docker compose -p test` ; documenter la fréquence.

---

## Constat 8 — L'UI n'a pas suivi le back-end

`api/static/index.html` (11 juin) est **antérieure** au RAG, au screening, aux parcours,
aux audiences, aux étiquettes, à la confiance. L'API renvoie `label`, `fiches` (avec
`source_url`), `confidence`, `tier`, `audience`, `cached` — **l'UI n'en affiche aucun.**
La POC SHORTLIST B8 : *« ajouter les étiquettes + la bannière de dégradation »*. **Non
fait.**

Conséquence : **la démo, en l'état, montre une boîte de chat banale** qui ne communique
pas la calibration de confiance qui est *tout l'intérêt* du produit. « Fiche validée CPA »
vs « à vérifier » vs « aucune fiche » vs « voie de sauvegarde » vs « hors périmètre » —
l'agent ne voit rien de cette distinction.

→ **Correction :** réécrire `index.html` (~1 jour) : afficher le `tier`/`label` en bandeau
coloré, les `fiches` cliquables (lien Confluence si `source_url`), la `confidence`, un état
« RAG indisponible → réponse cascade » quand `tier` ∈ {T1…T5}.

---

## Constat 9 — La pile de « validated: false »

| Fichier | En attente de | Impact si démo tel quel |
|---|---|---|
| `config/screening.yaml` | numéros d'urgence PF validés DSI | carte de détresse avec un numéro potentiellement faux |
| `config/parcours.yaml` | 3 parcours relus par le chef CPA | réponses canoniques « départ/arrivée/mutation » non vérifiées |
| `config/rag/audiences.yaml` | périmètre prestataire arrêté (D-B2/D-B3) | séparation atelier/téléassistance sur une liste blanche devinée |
| `config/models.yaml` | pinning par digest (A4 partiel) | « quels poids tournent » pas verrouillé |

Le motif « `validated: false` → avertissement sur la réponse + `/health` » est **bon**.
Mais **rien n'est planifié** pour la validation, et si la POC est présentée avec 3 configs
non validées, **c'est ça la POC**.

→ **Correction :** une réunion de 2 h avec le chef CPA sur les 3 fichiers. C'est le
chemin critique de la crédibilité, pas du code.

---

## Constat 10 — Sécurité : 2 ports fermés sur 6, Jalon B non appliqué

- `:8090` et `:8888` → loopback (C4). **Restent publiés `0.0.0.0` :** `anone:8080`,
  `litellm:4000` (avec la clé Anthropic dans l'env), `ollama:11434` (Ollama brut),
  `postgres:5432`, `grafana:3000`, `prometheus:9090`. La revue R2, item n°1 : *« dé-publier
  les ports du plan de données »*. **2 sur ~6.**
- **Jalon B est consultatif, pas appliqué.** Sans authentification sur `:8888`, le profil
  passe dans `QueryRequest.audience`. N'importe qui sur la boîte lit la base atelier en
  écrivant `{"audience":"atelier"}`. J'ai **construit le mécanisme** ; il ne **protège
  rien** tant qu'un jeton ne lie pas le profil au demandeur (Phase 2 / proxy d'identité).
- `git remote origin` : PAT GitHub en clair (connu, l'opérateur est au courant).
- Menace réelle sur une boîte mono-utilisateur en local badgé : « quelqu'un sur la boîte »
  — surface limitée. Mais alors **à quoi sert Jalon B** aujourd'hui ? À rien
  d'exécutoire. C'est une préparation, à assumer comme telle.

→ **Correction :** passer les 6 ports restants en `127.0.0.1:` (5 lignes) — les services
se parlent par le réseau Docker. L'auth sur `:8888` reste Phase 2, mais sans elle Jalon B
ne doit pas être présenté comme une garantie.

---

## Constat 11 — La voie « rédiger la réponse au ticket » n'existe pas

POC SHORTLIST B6 : *« le 2ᵉ usage cœur : coller le problème de l'utilisateur → le modèle
local rédige une réponse française claire que l'agent édite et envoie. Contraint, local,
pas de cloud. »*

**Non construit.** Tout le système répond à « comment fait-on X ». Personne ne fait
« écris l'e-mail à l'utilisateur qui explique le reset MFA ». Pour un desk de support,
c'est sans doute l'usage **le plus rentable** (gain de temps de rédaction, ton homogène).

Et le cadrage de fond de la revue (finding #2) : *« le livrable est un changement de
comportement — les agents arrêtent de coller des données citoyennes dans ChatGPT public »*.
**Rien ici ne mesure ni ne pilote ça.** Le KPI « shadow-egress » (trafic vers
chat.openai.com / claude.ai depuis les logs proxy) n'est pas câblé.

→ **Correction :** une voie `POST /redige` (ou un champ `mode: "redaction"`) : RAG sur le
sujet → prompt « rédige une réponse d'e-mail à l'utilisateur, à partir de ces fiches, ton
courtois DSI, l'agent relira » → étiquette « brouillon à relire ». ~1 jour, réutilise tout
le RAG.

---

## Constat 12 — La supervision 24/7 est majoritairement morte

`config/prometheus_alerts.yml` : ~30 règles. **Aucun exporter installé.**
- `node_*` (CPU/RAM/disque) → **pas de node_exporter**
- `pg_up`, `pg_stat_*` → **pas de postgres_exporter**
- `nvidia_smi_*`, `ollama_gpu_memory_*`, `vllm_gpu_memory_*` → **pas de dcgm/nvidia exporter**
- `up{job="docker"}` → **pas de cAdvisor**
- `langgraph_query_duration_seconds` / `langgraph_tier_timeout_total` → **noms périmés**
  (les vraies métriques sont `query_latency_seconds{tier}`, etc. — corrigées seulement
  dans le nouveau groupe `sovereign_ai_rag`)
- `ollama_model_load_errors_total{model="mistral:7b-q4"}` → **modèle qui n'existe plus**

Cibles Prometheus réellement UP : `anone`, `langgraph`, `rag`, `prometheus`. `litellm` et
`ollama` = `down` (ils n'exposent pas `/metrics`).

Donc « garder la stack en santé 24/7, monitoring actif » (**priorité n°2 du projet**)
repose sur : 4 cibles scrappées, 6 nouvelles alertes RAG valides, et **~24 règles mortes**.
Une panne disque, une pression VRAM, un Postgres à genoux → **aucune alerte**.

→ **Correction :** ajouter `node_exporter` + `postgres_exporter` + (si voulu) `cadvisor`
au compose (3 images, ~5 lignes chacune, config prometheus.yml), supprimer les règles
vLLM / mistral périmées, corriger les noms de métriques langgraph. Un dashboard Grafana
« stack » (le `grafana_dashboard_cascade.json` existant est au mauvais format —
`{"dashboard": …}` d'import, pas de provisioning).

---

## Ce qui va bien (pour l'équilibre)

- Le **portail à fiches citées** : récupération hybride (vecteur + lexical + reranker RRF),
  recall@1 100 % (paliers 1/3/4) en récupération seule, contrat JSON, post-contrôle des
  citations, étiquettes, 38 tests unitaires.
- **Ordre déterministe** clair et défendable : sauvegarde → parcours → RAG → hors-périmètre
  → aucune-fiche → cascade. Fail-open sur RAG KO, fail-closed sur « périmètre sans fiche ».
- **Screening** (détresse + hors-sujet) déterministe, éditable, empreinte dans `/health`,
  couverture E5 corrigée (7/7).
- **Parcours canoniques** (D8) — bon patron (réponse rédigée, tracée aux fiches, servie
  avant le modèle), a résolu le palier 3.
- **Jalon B** — mécanisme propre (colonne `audience`, liste blanche, fuite inter-audience
  vérifiée = 0), même s'il n'est pas encore *exécutoire*.
- **Cache T0** (LRU borné, empreinte corpus dans la clé, sélectif), **échéance globale**
  (D4), **sonde du contrat** (D5), **num_predict** (D6) — la 2ᵉ vague a vraiment durci.
- Modèles du RAG **bakés dans l'image** (air-gap OK pour le RAG).
- `docs/` : la traçabilité est bonne (DESIGN_REVIEW, EVAL_BASELINE, les 2 revues Jalon A,
  ce document).

---

## Priorisation — ce qui compte vraiment

### 🔴 Bloquant pour dire « prêt à démontrer sérieusement »

| # | Action | Effort | Pourquoi |
|---|--------|--------|----------|
| 1 | **`scripts/backup.sh` + baker `qwen2.5:7b` (ou snapshot `ollama_data`) + 1 test de restauration** | M | perte du volume Ollama en air-gap = mort définitive |
| 2 | **Valider les 3 configs** (`screening` / `parcours` / `audiences`) avec le chef CPA | réunion 2 h | un numéro d'urgence faux = préjudice ; sinon la démo = 3 fichiers non validés |
| 3 | **Faire relire les 34 procédures** par le chef CPA (elles sont générées par IA, non vérifiées) | M (chef CPA) | tout le RAG et l'éval en dépendent |
| 4 | **UI** — afficher étiquettes / fiches / confiance / bannière | ~1 j | la démo actuelle ne montre pas la calibration de confiance = le produit |
| 5 | **Décider T5** (hard-gate n°2 : v1 sans cloud ?) | décision | T5 invente, coûte, franchit la frontière, et ne répond à quasi rien |

### 🟠 Important, pas bloquant démo

| # | Action | Effort |
|---|--------|--------|
| 6 | Couche PII déterministe (regex NIR/IBAN/+689/e-mail) + canari post-masque **si T5 reste** | M |
| 7 | 6 ports restants → `127.0.0.1:` | S |
| 8 | Supprimer le code mort + `litellm` + images vLLM + nettoyer `.env` | ~1 h |
| 9 | Exporters Prometheus (node/pg) + purge des règles mortes + dashboard stack | M |
| 10 | Voie « rédiger la réponse au ticket » (B6) | ~1 j |
| 11 | `eval/run.py` en CI + jeu tenu à l'écart | S |

### 🟡 À faire avec le Jalon C (fine-tuning)

- Calibrer `RAG_SCORE_HIGH` / `FLOOR` (constat 6 / D1).
- Remplacer `CascadeRouter` par un routage par intention ; aligner `CLAUDE.md` et `/health`
  sur « 2 tiers » (constat 1).
- Prompt de rédaction plus court (D7) sous le filet du fine-tuning.

---

## La question de fond

Le projet a **deux blocages de fond qui ne sont pas techniques** et que trois passes
critiques ne feront pas disparaître :

1. **Le contenu.** 34 procédures générées par IA, non validées. Une base de fiches
   canoniques *validées* est *le produit* (POC SHORTLIST B5, revue R2.2). Sans un chef CPA
   qui relit et signe, on a un moteur de recherche sur un document incertain.

2. **La décision T5 / cloud** (hard-gate n°2, question ouverte depuis 5 rounds de revue).
   Tant qu'elle n'est pas prise, on maintient un chemin cloud qui invente, coûte, et
   engage juridiquement — pour un bénéfice quasi nul aujourd'hui.

Le reste — la cascade-décor, le code mort, les ports, la supervision morte, l'UI en
retard, l'air-gap troué — est **du nettoyage sérieux mais bornable** (une à deux
semaines). Il est faisable **maintenant, sans décision opérateur**, et il devrait l'être
avant toute présentation, parce que chacun de ces points est une question qu'un
interlocuteur DSI un peu attentif posera.
