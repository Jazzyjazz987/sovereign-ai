# Synoptique d'architecture — Sovereign AI CPA

**Artifact publié :** https://claude.ai/code/artifact/37176f6b-6b96-40ea-af18-105696866107

Diagramme (Claude Design) montrant le flux d'une requête chat en 8 étapes, la frontière
réseau LAN/air-gap/internet, et à quelles étapes un modèle est réellement appelé.
Créé le 2026-09-17 à partir de l'état vérifié en session (pas de la doc historique).

**Contenu à garder synchronisé avec le code** (voir `.claude/skills/veille-nocturne/`) :
- ordre de la cascade dans `api/main.py::_query_cascade` (sauvegarde → disambiguation →
  parcours → RAG → gate hors-périmètre → T1-T4 → T5)
- ports/bindings de `docker-compose.yml` (lequel est exposé LAN vs loopback)
- le fait que T5 est la seule sortie réseau, après anonymisation Agent Anone
