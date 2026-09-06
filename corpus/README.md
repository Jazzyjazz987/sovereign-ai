# corpus/ — sources documentaires du RAG

⚠️ **Tout ce dossier est hors git** (sauf ce README). Les documents contiennent des données
nominatives (noms d'agents, adresses, matricules). Ne jamais committer, ne jamais sortir de la
machine autrement que par la clé USB sécurisée.

## Structure

| Dossier | Contenu | Ordre de fourniture |
|---------|---------|---------------------|
| `01-procedures-legacy/` | procédures « legacy » de traitement de la CPA (le périmètre du POC) | 1er |
| `02-mails-bal-partagee/` | mails de la boîte aux lettres partagée envoyés aux utilisateurs | 2e |
| `03-tickets/` | tickets résolus (question utilisateur + réponse agent) — pour l'éval et U2 | 3e |

## Formats acceptés

Markdown, PDF, DOCX, HTML, `.eml` / `.msg` (mails), `.txt`. Déposer les fichiers tels quels ;
l'ingestion s'occupe de l'extraction et du découpage.

## Périmètre POC (rappel — `docs/RAG_REQUIREMENTS.md`)

Procédures de traitement des agents CPA. Support informatique. **Pas** le juridique / statutaire PF
(cible ultérieure, derrière le gate fiche citée).
