<!-- confluence: SI / page 131248 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/131248 -->
<!-- parent_id: 229575 · parent: 🚗 Agents de proximité terrain -->

# PROC-TER-002 — Dotation sur site

| Code | `PROC-TER-002` |
| --- | --- |
| Domaine | Agents de proximité terrain |
| Rôles concernés | Agent de proximité terrain |
| Déclencheur | Ticket de dotation préparé par l'atelier (poste en statut 'En fonction') |
| Outil(s) | Tauturu (GLPI), Véhicule utilitaire |
| SLA cible | Livraison dans les 7 jours ouvrés |
| Version | 1.0 |
| Date de création | 2026-03-15 |
| Dernière MAJ | 2026-03-15 |
| Statut | Actif |
| Criticité | Haute |
| Contrainte RGPD | Non |

**Règle invariante CPA :** Toute action doit être tracée par un ticket Tauturu (GLPI). Pas de ticket = pas d'action.

## 🎯 Objet

Livrer et installer un poste de travail préparé par l'atelier sur le site du bénéficiaire, en finalisant la configuration avec l'utilisateur.

## ⚡ Déclencheur

Ticket de dotation préparé par l'atelier (poste en statut 'En fonction')

## 👤 Acteurs

| Rôle | Responsabilité dans cette procédure |
| --- | --- |
| Agent atelier | Prépare le poste et le met 'En fonction' dans GLPI |
| Agent de proximité terrain | Livre, installe et finalise avec le bénéficiaire |

## 📋 Étapes

| # | Action | Qui | Outil | Résultat attendu |
| --- | --- | --- | --- | --- |
| 1 | Récupérer le matériel préparé sur l'étagère 'Prêt à déployer' de l'atelier | Agent de proximité terrain | Stock atelier | Matériel embarqué |
| 2 | Charger le matériel dans le véhicule utilitaire avec les câbles et outils nécessaires | Agent de proximité terrain | Véhicule + sac d'intervention | Équipement de déplacement prêt |
| 3 | Se rendre sur le site du bénéficiaire | Agent de proximité terrain | Véhicule | Arrivée sur site |
| 4 | Installer physiquement le poste dans le bureau du bénéficiaire (connexions réseau, écran, périphériques) | Agent de proximité terrain | Outillage sac intervention | Poste installé |
| 5 | Finaliser la session utilisateur en présence du bénéficiaire (premier login Autopilot ou MDT) | Agent de proximité terrain | Poste + Intune/MDT | Session utilisateur active |
| 6 | Former brièvement le bénéficiaire aux nouvelles fonctionnalités si besoin | Agent de proximité terrain | Poste | Bénéficiaire autonome |
| 7 | Mettre à jour le ticket Tauturu au retour (non en cours d'intervention) | Agent de proximité terrain | Tauturu (GLPI) | Ticket mis à jour |

## ⚠️ Points de vigilance

* La présence physique du bénéficiaire est obligatoire pour le premier login — planifier le rendez-vous à l'avance
* Pour les gros déploiements (> 3 dotations sur un même site) : renfort de 1-2 agents atelier
* Le véhicule est vidé à chaque retour d'intervention
* Pour les îles : le matériel est envoyé par coursier (fréquence ~tous les 2-3 jours ouvrés) — la finalisation est assurée par la téléassistance

## 🔗 Procédures liées

* PROC-ATL-001 — Préparation poste MDT
* PROC-ATL-002 — Préparation poste Intune
* PROC-TER-005 — Interventions îles éloignées

## 📝 Historique des modifications

| Date | Version | Auteur | Nature de la modification |
| --- | --- | --- | --- |
| 2026-03-15 | 1.0 | Chef CPA | Création initiale — projet de formalisation documentaire |
