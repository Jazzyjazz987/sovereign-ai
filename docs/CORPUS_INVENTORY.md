# Inventaire du corpus RAG

Suivi de ce qui a été ingéré. Les documents eux-mêmes sont dans `corpus/` (**hors git** — données
internes CPA). Ce fichier ne contient que la structure.

## Source 1 — Procédures legacy CPA (Confluence espace « SI »)

- **Origine** : Confluence Cloud `williamsjosiah.atlassian.net`, espace `Support informatique` (clé SI)
- **Récupéré** : 2026-09-06, via connecteur Atlassian, converti en Markdown
- **Emplacement** : `corpus/01-procedures-legacy/`
- **Volume** : 41 fichiers, ~133 Ko
- **Licence / propriété** : DSI PF — production interne CPA (projet de formalisation, mars 2026)

### Contenu

| Type | Fichiers | Détail |
|------|----------|--------|
| Procédures opérationnelles | 34 | `PROC-ATL-001..005`, `PROC-INT-001..006`, `PROC-ID-001..007`, `PROC-STOCK-001..007`, `PROC-TER-001..006` |
| Pages transverses | 7 | Accueil CPA, Synthèse projet, Matrice RACI, Registre RGPD, Onboarding nouvel agent, + 5 index de domaine |

### Gabarit d'une procédure (constant — base du chunking structuré)

`Table méta` (Code, Domaine, Rôles, Déclencheur, Outils, SLA, Version, Criticité, **Contrainte RGPD**)
→ `🎯 Objet` → `⚡ Déclencheur` → `👤 Acteurs` (table) → `📋 Étapes` (table numérotée)
→ `⚠️ Points de vigilance` → `🔴 Points de contrôle RGPD` (si applicable) → `🔗 Procédures liées`
→ `📝 Historique` (écarté à l'ingestion).

### Faits saillants pour le RAG

- **Outil ITSM = « Tauturu » (GLPI)**. Règle invariante répétée partout : « pas de ticket = pas d'action ».
- Contexte : ~3 500 postes / 5 500 agents, équipe **8 agents polyvalents** (1 chef + 7 cat. B),
  multi-îles, migration Intune/Autopilot 2026 (~2 200 postes), MDT en fin de vie.
- 5 procédures portent une **contrainte RGPD** : `PROC-ID-003`, `PROC-INT-005`, `PROC-STOCK-005`,
  `PROC-STOCK-006`, `PROC-TER-006` → ces chunks reçoivent `contrainte_rgpd: true` en métadonnée.
- Références réglementaires PF citées : arrêté 1733 CM, arrêté 2388 CM, circulaire 7726 PR,
  circulaire 979/PR (achats), charte informatique.
- La **Matrice RACI** donne le mapping rôle → procédure (6 rôles) : utilisable pour filtrer/router.

## Source 2 — Mails de la BAL partagée (à venir)

- Emplacement prévu : `corpus/02-mails-bal-partagee/`
- Mails envoyés aux utilisateurs finaux depuis la boîte partagée du support.
- Chunking : 1 mail ≈ 1 chunk ; métadonnées objet / date / thème / type de destinataire.

## Source 3 — Tickets résolus (à venir, pour l'éval + U2)

- Emplacement prévu : `corpus/03-tickets/`
