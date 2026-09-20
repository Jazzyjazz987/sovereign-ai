<!-- confluence: SI / page 66051 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/66051 -->
<!-- parent_id: 229575 · parent: 🚗 Agents de proximité terrain -->

# PROC-TER-001 — Planification et priorisation des interventions

| Code | `PROC-TER-001` |
| --- | --- |
| Domaine | Agents de proximité terrain |
| Rôles concernés | Agent de proximité terrain + Agent téléassistance |
| Déclencheur | Arrivée de tickets Tauturu ou demandes directes au briefing quotidien |
| Outil(s) | Tauturu (GLPI) |
| SLA cible | VIP : immédiat \| Urgent : dans la journée \| Standard : selon SLA GLPI |
| Version | 1.0 |
| Date de création | 2026-03-15 |
| Dernière MAJ | 2026-03-15 |
| Statut | Actif |
| Criticité | Haute |
| Contrainte RGPD | Non |

**Règle invariante CPA :** Toute action doit être tracée par un ticket Tauturu (GLPI). Pas de ticket = pas d'action.

## 🎯 Objet

Organiser et prioriser les interventions terrain quotidiennes selon la matrice de priorité CPA (VIP > Urgent > Standard).

## ⚡ Déclencheur

Arrivée de tickets Tauturu ou demandes directes au briefing quotidien

## 👤 Acteurs

| Rôle | Responsabilité dans cette procédure |
| --- | --- |
| Agent de proximité terrain | Traite les tickets par ordre de priorité |
| Chef de cellule CPA | Arbitre les conflits de priorité et affecte des renforts si besoin |
| Agent téléassistance | Filtre et oriente les tickets entrants |

## 📋 Étapes

| # | Action | Qui | Outil | Résultat attendu |
| --- | --- | --- | --- | --- |
| 1 | Consulter la file de tickets Tauturu en début de journée au briefing | Agent de proximité terrain | Tauturu (GLPI) | Vue consolidée de la charge |
| 2 | Trier les tickets par priorité : 1/ VIP (fonction de l'agent), 2/ Urgent, 3/ Standard | Agent de proximité terrain | Tauturu (GLPI) | File priorisée |
| 3 | Si 2 agents terrain disponibles : répartir les tickets géographiquement pour optimiser les déplacements | Agent de proximité terrain | Tauturu (GLPI) + Carte des sites | Tournées optimisées |
| 4 | En cas d'urgence VIP simultanée : l'agent en cours bascule, un agent atelier ou le chef CPA prend la relève | Chef de cellule CPA | Briefing | Couverture VIP assurée |
| 5 | Mettre à jour les tickets à chaque étape de l'intervention | Agent de proximité terrain | Tauturu (GLPI) | Traçabilité en temps réel |

## ⚠️ Points de vigilance

* Horaires d'intervention : 7h30–15h30 (lun–jeu) / 7h30–14h30 (ven) — aucune intervention après ces horaires
* La définition VIP est basée sur la fonction de l'agent (ministres, directeurs, fonctions stratégiques) — pas de liste nominative fixe
* Un agent terrain peut appeler la téléassistance en renfort pour diagnostic complémentaire sans quitter le site

## 🔗 Procédures liées

* PROC-TER-002 — Dotation sur site
* PROC-TER-003 — Dépannage N1 sur site

## 📝 Historique des modifications

| Date | Version | Auteur | Nature de la modification |
| --- | --- | --- | --- |
| 2026-03-15 | 1.0 | Chef CPA | Création initiale — projet de formalisation documentaire |
