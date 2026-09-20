<!-- confluence: SI / page 1704038 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/1704038 -->
<!-- parent_id: 1769473 · parent: 🚗 Agents de proximité terrain — cible -->

# PROC-TER-C02 — Dotation sur site

|  |  |
| --- | --- |
| **Code** | PROC-TER-C02 |
| **Domaine** | Agents de proximité terrain |
| **Statut** | Cible à valider |
| **Criticité** | Haute |
| **Contrainte RGPD** | Non |
| **Outils** | Tauturu, véhicule de service |
| **SLA cible** | 7 jours ouvrés |

> **Règle invariante CPA** — Toute dotation, intervention ou action manuelle sur le parc fait l'objet d'un ticket Tauturu.

## Objet

Livrer et installer un poste de travail chez le bénéficiaire, et accompagner son premier démarrage.

Le poste arrivant enrôlé, l'intervention se limite à l'installation physique et à l'ouverture de session.

## Déclencheur

Ticket de dotation attribué et matériel disponible — voir PROC-STOCK-C02.

## Étapes

| # | Action | Qui | Résultat attendu |
| --- | --- | --- | --- |
| 1 | Récupérer le matériel attribué | Agent de proximité | Matériel embarqué |
| 2 | Charger le véhicule avec les câbles et l'outillage nécessaires | Agent de proximité | Équipement prêt |
| 3 | Se rendre sur le site, au rendez-vous convenu avec le bénéficiaire | Agent de proximité | Arrivée sur site |
| 4 | Installer le poste : connexions réseau, écran, périphériques | Agent de proximité | Poste installé |
| 5 | Accompagner le premier démarrage en présence du bénéficiaire | Agent de proximité | Session active, profils appliqués |
| 6 | Vérifier l'accès aux ressources : messagerie, bibliothèques SharePoint | Agent de proximité | Bénéficiaire opérationnel |
| 7 | Présenter brièvement les nouveautés au bénéficiaire si nécessaire | Agent de proximité | Bénéficiaire autonome |
| 8 | Mettre à jour le ticket au retour d'intervention | Agent de proximité | Ticket documenté |

## Points de vigilance

- **La présence du bénéficiaire est obligatoire** : le premier démarrage passe par son authentification. Le rendez-vous se planifie à l'avance.
- Au-delà de trois dotations sur un même site, demander le renfort d'un agent atelier.
- Le véhicule est vidé à chaque retour d'intervention.
- Les fichiers de l'agent résident sur SharePoint : aucune reprise de données locales n'est à prévoir, contrairement à l'ancien fonctionnement sur serveurs de fichiers.
- Pour les îles, la remise n'est pas assurée sur site : voir PROC-TER-C04.

## Procédures liées

- PROC-STOCK-C02 — Dotation de matériel
- PROC-TER-C04 — Télé-assistance et interventions aux îles
- PROC-ID-C01 — Vérification et suivi des comptes provisionnés
