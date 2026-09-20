<!-- confluence: SI / page 98602 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/98602 -->
<!-- parent_id: 98567 · parent: 👁️ Vues par rôle -->

# Vue procédures — Gestionnaire de comptes

Cette vue liste toutes les procédures impliquant le rôle **Gestionnaire de comptes**. Elle est générée à partir des métadonnées des pages procédures.

| Code | Procédure | Domaine | SLA |
| --- | --- | --- | --- |
| PROC-ATL-001 | Préparation poste via MDT | Atelier | Durée de préparation : ~2h par poste (8 postes simultanément en standard) |
| PROC-ATL-002 | Préparation poste via Intune/Autopilot | Atelier | ~30 min (préprovisionnement simple) ou ~2h (avec reseal) |
| PROC-ATL-004 | Maintenance de l'image MDT | Atelier | Mise à jour mensuelle (correctifs sécurité) |
| PROC-INT-001 | Enrôlement Autopilot Windows 11 | Console Intune | 30 min à 2h selon mode de provisionnement |
| PROC-INT-002 | Enrôlement Android Enterprise | Console Intune | Dans la journée |
| PROC-INT-003 | Packaging et déploiement d'application | Console Intune | Déploiement test : 1 semaine \| Production : 2 semaines |
| PROC-INT-004 | Gestion des profils et groupes Intune | Console Intune | Dans les 3 jours ouvrés |
| PROC-INT-005 | Retrait et désinscription appareil Intune | Console Intune | Immédiat en cas de perte/vol \| Dans les 24h pour départ agent |
| PROC-INT-006 | SecOps — Remontée et traitement des alertes | Console Intune | Alerte critique : réponse dans l'heure \| Alerte standard : 4h |
| PROC-ID-001 | Création de compte utilisateur | EntraID / Exchange | Création dans les 24h suivant le ticket |
| PROC-ID-002 | Modification de compte utilisateur | EntraID / Exchange | Modification dans les 12h suivant le ticket |
| PROC-ID-003 | Désactivation et suppression de compte | EntraID / Exchange | Désactivation dans les 24h du ticket |
| PROC-ID-004 | Déblocage et réinitialisation MFA | EntraID / Exchange | Résolution dans les 2h (urgence pour les VIP) |
| PROC-ID-005 | Création et gestion des BALP | EntraID / Exchange | Création dans les 48h |
| PROC-ID-006 | Gestion des ressources Exchange (salles, équipements) | EntraID / Exchange | Création dans les 48h |
| PROC-ID-007 | Attribution et suivi des licences M365 | EntraID / Exchange | Attribution : lors de la création compte \| Revue : mensuelle |

*Mise à jour : cette vue se régénère automatiquement lors de la modification d'une procédure.*
