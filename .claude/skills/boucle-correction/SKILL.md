---
name: boucle-correction
description: Teste un cas concret d'agent CPA sur le système en prod (via /query, pas juste /search), diagnostique la cause si la réponse est mauvaise ou surprenante, corrige au plus court (prompt, routeur, config, fiche corpus), redéploie/réingère, puis rejoue le même cas et le jeu d'éval complet pour confirmer avant de déclarer que c'est corrigé. Opérationnalise la boucle Jalon C de docs/RAG_ROADMAP.md ("test → diagnostic → correction → re-test"). À utiliser quand l'opérateur donne une question réaliste à vérifier, signale un comportement bizarre, ou après une correction pour confirmer qu'elle tient sans rien casser ailleurs.
---

# boucle-correction

Opérationnalise `docs/RAG_ROADMAP.md § Jalon C` : « test → diagnostic → correction → re-test ».
Ne clame jamais une correction sans l'avoir rejouée. Ne clame jamais « aucune régression » sans
avoir relancé l'éval.

## Entrée

`args` = une ou plusieurs questions réalistes, telles qu'un agent CPA les taperait (pas la
formulation exacte d'un cas de `eval/dataset.yaml` — le but est de débusquer ce que l'éval ne
couvre pas). Si `args` est vide, demander à l'opérateur quel(s) cas tester.

## 1. Tester en conditions réelles

Toujours via le pipeline complet, jamais `/search` seul en premier — c'est `/query` que
l'agent CPA voit :

```bash
curl -s -X POST http://localhost:8888/query -H "Content-Type: application/json" \
  -d '{"query": "<question telle que tapée par un agent>"}' | python3 -m json.tool
```

Tester 2-3 reformulations proches (sans le jargon exact « PROC-XXX », avec des fautes de
frappe plausibles) — un seul essai littéral cache les biais de sur-généralisation du LLM.
Si la première réponse semble bonne, la considérer suspecte tant qu'elle n'a pas survécu à
une reformulation.

## 2. Lire la réponse en esprit critique

Chercher, dans l'ordre de gravité :
- **Contenu inventé** : référence, code PROC, étape, adresse — qui n'est pas dans les fiches
  citées.
- **Mauvais tier/routage** : `tier` dans la réponse (`parcours`, `RAG`, `clarification`,
  `aucune-fiche`, `hors-perimetre`, `sauvegarde`, `T1`-`T5`) cohérent avec l'intention réelle ?
- **Artefact de prompt** : préfixe, ton, ou structure qui ne colle pas à la question posée
  (ex. le « Non, » qui s'appliquait à toute question évoquant une contrainte, pas seulement
  aux vraies questions « peut-on... sans... »).
- **Ambiguïté tranchée en silence** : un mot à double sens (type « poste ») qui aurait dû
  déclencher une clarification plutôt qu'un choix arbitraire.
- **Fond correct mais fiche source obsolète/incomplète** : la réponse est fidèle aux extraits,
  mais les extraits eux-mêmes ont un trou (cf. le cas `PROC-ID-001` — pas de vérification de
  compte existant avant création).

Si tout est bon, s'arrêter là et le dire — ne pas chercher un problème qui n'existe pas.

## 3. Diagnostiquer — décider OÙ est la cause avant de toucher au code

| Symptôme | Cause probable | Fichier |
|---|---|---|
| Mauvais tier choisi par collision de mot-clé | `config/parcours.yaml` (patterns/anti trop larges) | `api/parcours.py` |
| Terme à double sens tranché sans poser la question | Pas de garde dans `config/disambiguation.yaml` | `api/disambiguation.py` |
| Ton/structure de réponse qui déborde sur des cas non voulus | Prompt système trop permissif | `api/main.py` (`RAG_SYSTEM`, `RAG_SYSTEM_REDACTION`, ou `config/prompts.yaml` par tier) |
| Bonne fiche récupérée mais réponse incomplète/dangereuse | Trou dans le contenu de la fiche source | `corpus/01-procedures-legacy/PROC-*.md` |
| Mauvaise fiche récupérée alors que la bonne existe | Retrieval/reranking (`rag/retriever.py`, `rag/rerank.py`) — vérifier avec `/search` en direct avant de toucher au reranker |
| Filtre légitime bloque une vraie question | `config/screening.yaml` (blocklist trop large) | `api/screening.py` |

Ne pas corriger dans deux fichiers à la fois « au cas où » — isoler la cause, corriger UN
endroit, suivre le patron déjà en place (`screening.py`/`parcours.py`/`disambiguation.py` sont
le même patron : YAML fail-soft, sous-chaînes normalisées, aucun modèle appelé quand c'est
déterministe). Correction chirurgicale seulement — ne pas refactorer ce qui marche déjà à côté.

## 4. Corriger, puis redéployer ce qui a changé

- Code Python (`api/*.py`) : si le `Dockerfile.langgraph`/`Dockerfile.anone` copie les fichiers
  par nom explicite, ajouter le nouveau fichier à la liste `COPY`. Puis :
  ```bash
  docker compose build <service> && docker compose up -d <service>
  sleep 6 && curl -s http://localhost:8888/health | python3 -m json.tool   # vérifier le fingerprint config a changé
  ```
- Config YAML seule (`config/*.yaml`) monté en volume : redémarrer suffit, pas de rebuild.
- Contenu corpus (`corpus/01-procedures-legacy/*.md`) : ré-ingérer (pas de rebuild/restart —
  le service RAG lit la base live) :
  ```bash
  export $(grep POSTGRES_PASSWORD .env | xargs)
  export RAG_PG_DSN="postgresql://claude:${POSTGRES_PASSWORD}@localhost:5432/langgraph_db"
  .venv-rag/bin/python rag/ingest.py corpus/01-procedures-legacy --corpus procedures-legacy
  ```
  Un edit de fiche corpus est **local** (`corpus/` est hors git) — dire explicitement à
  l'opérateur qu'il faudra la reporter sur Confluence, et proposer de le faire directement via
  le connecteur Atlassian (`getConfluencePage` puis `updateConfluencePage`) — jamais silencieux,
  jamais sans confirmation (ça modifie un document de référence réel).

## 5. Rejouer — même cas, plusieurs essais, cache vidé

```bash
curl -s -X POST http://localhost:8888/cache/clear >/dev/null
```
puis rejouer les 2-3 reformulations de l'étape 1. Si identique sur 3 essais alors qu'on vient
de vider le cache, c'est suspect (vérifier `"cached"` dans la réponse) — sinon la variance de
génération du LLM local est normale et fait partie de la preuve (un fix qui ne marche qu'une
fois sur trois n'est pas un fix).

## 6. Vérifier l'absence de régression

```bash
.venv-rag/bin/python eval/run.py --full   # tous paliers, passe par /query — pas juste --search
```
Lire chaque palier. Un score qui baisse n'est pas automatiquement une régression : creuser
avec `--palier N -v`, regarder si le cas en échec a un rapport avec ce qui vient de changer.
Un cas isolé sans rapport (ex. `attendu_ok` qui varie de 50% à 75% selon l'essai sur un cas
totalement étranger au changement) est de la variance de génération LLM normale — le confirmer
en le rejouant 2-3 fois et en vérifiant que le score oscille sans tendance, pas en l'ignorant
silencieusement. Si le doute persiste, tester le cas suspect via `/query` (chemin réel) plutôt
que `/search` seul — un score `/search` isolé peut rater ce qu'un parcours canonique intercepte
correctement en amont.

## 7. Rapporter

Un résumé court : le cas testé, ce qui n'allait pas, où était la vraie cause (pas juste le
symptôme), ce qui a changé, la preuve que ça marche maintenant (avant/après), le résultat de
l'éval complet. Si quelque chose reste à faire côté opérateur (sync Confluence, décision de
commit git, arbitrage sur un trou de contenu qui dépasse le RAG) — le dire explicitement,
ne pas le faire à sa place sans demander.

**Ne jamais commit git ni pousser Confluence sans confirmation explicite** — même à la fin
d'une boucle de correction réussie. Rapporter que le fix est vérifié et prêt, proposer le
commit, attendre la réponse.
