<!-- confluence: SI / page 66162 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/66162 -->
<!-- parent_id: 65813 · parent: Support informatique -->

# Synthèse du projet de formalisation documentaire CPA

**Direction du Système d'Information — Gouvernement de la Polynésie française**
Cellule Parc et Assistance (CPA) · Section Production
_Version 1.0 — Mars 2026 — Première formalisation documentaire complète de la CPA_

## Contexte de départ

La CPA gère environ **3 500 postes de travail** pour **5 500 agents** à travers la Polynésie française, avec une équipe de **8 agents polyvalents** (1 chef de cellule + 7 agents catégorie B). Au lancement du projet, la totalité des pratiques opérationnelles reposait sur une **transmission orale exclusive** — aucune procédure écrite n'existait.

## Objectifs du projet

| Objectif | Description |
| --- | --- |
| Continuité opérationnelle | Garantir le fonctionnement de la CPA en cas d'absence ou de départ d'un agent |
| Onboarding | Fournir un support de formation structuré pour les nouveaux recrutés |
| Conformité RGPD | Identifier et corriger les écarts de conformité sur les traitements de données |
| Marchés publics | Définir les lots de service pour le déploiement 2026 (~2 200 postes) |
| Migration Intune 2026 | Préparer la bascule complète du parc sous Microsoft Intune/Autopilot |

## Méthode appliquée

Pour chaque domaine opérationnel : **audit complet en questions-réponses en premier**, puis rédaction des procédures uniquement après validation des constats. Chaque domaine produit deux livrables appariés : un document de procédures opérationnelles et un rapport d'audit Q&R détaillé avec analyse des risques et plan d'action.

**Principe fondateur :** les procédures ne sont jamais rédigées avant que l'audit soit approuvé. Cela garantit que le contenu reflète la réalité opérationnelle et non une version idéalisée des pratiques.

## Domaines audités et livrables produits

| Domaine | Procédures | Rapport audit Q&R | Nb procédures |
| --- | --- | --- | --- |
| 📦 Gestion du stock | ✅ Produit | ✅ Produit | 7 |
| 🔧 Atelier | ✅ Produit | ✅ Produit | 5 |
| 🚗 Agents de proximité terrain | ✅ Produit | ✅ Produit | 6 |
| 🖥️ Console Microsoft Intune | ✅ Produit | ✅ Produit | 6 |
| 👤 EntraID / Exchange | ✅ Produit | ✅ Produit | 7 |
| **TOTAL** |  |  | **31 procédures** |

## Principes fondateurs de la CPA

| Principe | Description |
| --- | --- |
| Polyvalence totale | Tous les agents ont les mêmes droits et habilitations — interchangeabilité complète |
| No ticket, no action | Tauturu (GLPI) est l'unique outil de traçabilité — toute action sans ticket est interdite |
| Résilience au turnover | L'organisation garantit la continuité de service quelle que soit la composition de l'équipe |
| Briefing quotidien | Outil central de communication, priorisation et remontée d'information |

## Risques critiques identifiés — Priorité P1

Ces 5 points constituent les non-conformités les plus graves identifiées lors des audits. Ils nécessitent une action immédiate, indépendamment du reste du projet.

| # | Risque | Domaine | Délai cible |
| --- | --- | --- | --- |
| P1 | Absence de registre RGPD de traçabilité des destructions de disques durs | Stock | 0–1 mois |
| P1 | Aucun certificat de destruction fourni par le prestataire de réforme | Stock | 0–1 mois |
| P1 | Aucune politique d'archivage des boîtes Exchange avant suppression définitive | EntraID/Exchange | 0–2 mois |
| P1 | Aucun suivi ni inventaire des licences M365 — surcoûts et dépassements impossibles à détecter | EntraID/Exchange | 0–2 mois |
| P1 | SLA non définis dans Tauturu — aucun engagement de service formalisé | Transversal | 0–3 mois |

## Horizon stratégique 2026

| Jalon | Description | Impact |
| --- | --- | --- |
| Migration Intune/Autopilot | Bascule complète du parc sous Microsoft Intune — ~2 200 nouveaux postes commandés | Décommissionnement du cluster Proxmox et de MDT |
| Définition des lots de service | Les procédures formalisées servent de base à la rédaction des lots pour les marchés de déploiement | Clarification contractuelle et juridique |
| KPI et satisfaction utilisateur | Formulaires de satisfaction en développement dans Tauturu — pilotage post-migration par chef de projet dédié | Pilotage qualité de service |
| Onboarding structuré | Les procédures Confluence remplacent la transmission orale pour les nouveaux agents | Réduction du temps d'intégration |

## Ce que ce projet a accompli

La CPA est passée de **zéro documentation écrite** à un corpus procédural complet : **31 procédures opérationnelles** structurées, référencées aux textes réglementaires (arrêté 1733 CM, arrêté 2388 CM, circulaire 7726 PR, circulaire 979/PR, RGPD), organisées par domaine et par rôle dans cet espace Confluence, et prêtes à évoluer à mesure que les pratiques changent.

**Pour mettre à jour une procédure :** modifier directement la page Confluence concernée. Les vues par rôle, la matrice RACI et les pages d'index s'appuient sur les métadonnées structurées (macro Page Properties).
