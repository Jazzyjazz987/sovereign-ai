---
name: veille-nocturne
description: Routine nocturne automatique (cron, 1h du matin, non-interactive) — vérifie que le synoptique d'architecture publié colle encore au code réel, fait une veille technique bornée (comment d'autres construisent des systèmes comparables, nouveaux skills/plugins Claude Code exploitables pour ce projet), écrit un rapport daté. Ne modifie JAMAIS le corpus, la config de production, ou docker-compose. Ne commit que sur une branche dédiée, jamais sur master, jamais de push.
---

# veille-nocturne

Tourne seule, sans opérateur présent, via `scripts/nightly_veille.sh` (cron, 1h du matin,
`claude -p`). Aucune supervision humaine pendant l'exécution — donc portée volontairement
étroite : **observer et rapporter, ne jamais modifier le système en production.**

## Garde-fous absolus

- **Jamais** de modification de `corpus/`, `config/`, `api/`, `docker-compose.yml`, `.env`.
- **Jamais** de `docker compose build/up/down/restart` — lecture seule (`ps`, `logs`, `curl`
  sur les endpoints `/health`/`/metrics` locaux).
- **Jamais** de `git push`. Commit uniquement sur une branche `veille/AAAA-MM-JJ` créée
  depuis `master` à jour ; ne jamais commit sur `master` directement.
- Si une vérification révèle un vrai problème (schéma qui ment, service down, régression) :
  l'écrire clairement dans le rapport, ne pas essayer de le corriger soi-même.
- Un rapport vide/sans anomalie est un bon résultat — ne pas inventer un problème pour
  justifier la nuit de travail.

## 1. Vérifier la cohérence du schéma d'architecture

Lire `docs/ARCHITECTURE_DIAGRAM.md` pour l'URL de l'Artifact publié. Le relire
(`Artifact` tool, `action: "read"`) et comparer son contenu à l'état réel :

- `docker compose ps` — les services listés dans le schéma existent-ils encore, avec les
  mêmes bindings de port (loopback vs LAN) ? Vérifier en particulier que `langgraph` reste
  le seul service en `0.0.0.0` et que les autres restent en `127.0.0.1`.
- `curl -s http://localhost:8888/health` — la cascade décrite (`sauvegarde → disambiguation
  → parcours → RAG → local → T5`) correspond-elle au champ `cascade` retourné ?
- Lire l'ordre réel dans `api/main.py::_query_cascade` (grep les commentaires « Étape N »)
  et comparer à l'ordre des 8 étapes dessinées dans le schéma.
- Si tout colle : le noter dans le rapport en une ligne, ne pas toucher à l'Artifact.
- Si ça a dérivé (nouveau service, port changé, étape ajoutée/retirée) : décrire précisément
  la différence dans le rapport. Ne republier le schéma corrigé que si la dérive est
  factuelle et sans ambiguïté (ex. un port qui a changé) — dans le doute, laisser à
  l'opérateur et le signaler seulement.

## 2. Veille technique (bornée)

Deux axes seulement, pas plus :
- **Comment d'autres construisent des systèmes comparables** — copilote de support interne
  RAG + garde-fous déterministes + escalade vers un LLM cloud avec anonymisation PII,
  pour une administration ou un contexte souveraineté/air-gap. Chercher des retours
  d'expérience publics (articles, docs techniques, projets open source), pas des
  généralités marketing. Comparer à nos choix documentés (`docs/DESIGN_REVIEW.md`,
  `docs/RAG_ROADMAP.md`) : qu'est-ce qui converge, qu'est-ce qui diverge et pourquoi c'est
  peut-être justifié ici (contrainte air-gap, budget GPU 12 Go, équipe de 8 agents).
- **Nouveautés Claude Code** (skills, plugins, fonctionnalités) depuis la dernière veille —
  regarder `docs/veille/` pour la date du dernier rapport, chercher ce qui est sorti depuis.
  Ne proposer que ce qui a un lien concret avec ce projet (pas une liste exhaustive de
  toutes les nouveautés).

Écrire les trouvailles avec la source (URL) — jamais une affirmation non sourcée présentée
comme un fait. Une réflexion honnête ("rien de neuf ce soir, à revoir dans une semaine")
est un résultat valide.

## 3. Rapport

Un seul fichier : `docs/veille/AAAA-MM-JJ.md` (date du jour). Structure :

```markdown
# Veille — AAAA-MM-JJ

## Cohérence schéma
[une ligne si tout colle, sinon le détail de la dérive]

## Veille technique
[axe 1 — comparaison avec d'autres systèmes]
[axe 2 — nouveautés Claude Code pertinentes]

## Rien à signaler ?
[explicite si c'est le cas — ne pas remplir pour remplir]
```

Puis :
```bash
git checkout -b veille/$(date +%Y-%m-%d)
git add docs/veille/$(date +%Y-%m-%d).md
git commit -m "veille: rapport automatique $(date +%Y-%m-%d)"
```
Revenir sur `master` ensuite (`git checkout master`) pour laisser le dépôt de travail propre
pour l'opérateur le lendemain. Ne jamais `git push`.
