<!-- confluence: SI / page 131206 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/131206 -->
<!-- parent_id: 98313 · parent: 📦 Gestion du stock -->

# PROC-STOCK-007 — Marchés publics et achats informatiques

| Code | `PROC-STOCK-007` |
| --- | --- |
| Domaine | Gestion du stock |
| Rôles concernés | Chef de cellule CPA |
| Déclencheur | Identification d'un besoin de renouvellement ou d'acquisition de matériel |
| Outil(s) | Tauturu (GLPI), Marchés coordonnés DSI, Comptabilité |
| SLA cible | Selon les délais réglementaires des marchés publics |
| Version | 1.0 |
| Date de création | 2026-03-15 |
| Dernière MAJ | 2026-03-15 |
| Statut | Actif |
| Criticité | Haute |
| Contrainte RGPD | Non |

**Règle invariante CPA :** Toute action doit être tracée par un ticket Tauturu (GLPI). Pas de ticket = pas d'action.

## 🎯 Objet

Encadrer le processus d'achat de matériel informatique conformément à la circulaire n°979/PR du 14 février 2025 relative à l'exécution des achats informatiques de la DSI.

## ⚡ Déclencheur

Identification d'un besoin de renouvellement ou d'acquisition de matériel

## 👤 Acteurs

| Rôle | Responsabilité dans cette procédure |
| --- | --- |
| Chef de cellule CPA | Identifie le besoin, consulte les marchés, pilote la commande |
| Gestionnaire de stock (intérim Chef CPA) | Assure le suivi de la commande et la réception |

## 📋 Étapes

| # | Action | Qui | Outil | Résultat attendu |
| --- | --- | --- | --- | --- |
| 1 | Identifier et documenter le besoin (type matériel, quantité, justification) | Chef de cellule CPA | Document expression de besoin | Besoin formalisé |
| 2 | Consulter le marché coordonné DSI applicable à la catégorie de matériel | Chef de cellule CPA | Marchés DSI | Marché identifié ou absence confirmée |
| 3 | Si marché coordonné couvre le besoin : passer commande directe | Chef de cellule CPA | Bon de commande | BC émis |
| 4 | Si pas de marché applicable : réaliser une analyse des offres selon le code des marchés publics de la Polynésie française | Chef de cellule CPA | Code des marchés publics | Offre sélectionnée |
| 5 | Établir le bon de commande avec référence, quantité, délai, pénalités de retard | Chef de cellule CPA | Système comptable DSI | BC validé |
| 6 | Informer le gestionnaire de stock du planning de livraison pour coordination réception | Chef de cellule CPA | Briefing / Email | Réception planifiée |

## ⚠️ Points de vigilance

* Référence réglementaire : Circulaire n°979/PR du 14 février 2025 — respecter impérativement les seuils et procédures applicables
* Les pénalités de retard sur livraison sont gérées par la comptabilité sur la base du BL signé fourni par la CPA
* Pour la commande 2026 (~2 200 postes Intune) : anticiper les contraintes de stockage (capacité actuelle maximale)

## 🔗 Procédures liées

* PROC-STOCK-001 — Réception et contrôle livraison

## 📝 Historique des modifications

| Date | Version | Auteur | Nature de la modification |
| --- | --- | --- | --- |
| 2026-03-15 | 1.0 | Chef CPA | Création initiale — projet de formalisation documentaire |
