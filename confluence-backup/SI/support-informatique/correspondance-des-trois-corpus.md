<!-- confluence: SI / page 1802341 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/1802341 -->
<!-- parent_id: 65813 · parent: Support informatique -->

# Correspondance des trois corpus

**Statut : la colonne hybride est en vigueur, la colonne cible reste à valider**

Cette page est la table de passage entre les trois corpus de procédures de la cellule. Pour chaque procédure historique : ce qu'elle est devenue pendant la migration, ce qu'elle deviendra après, et pourquoi.

C'est le seul document qui se lit horizontalement. Les trois corpus se lisent verticalement, chacun dans sa branche.

| Corpus | Décrit | Statut |
| --- | --- | --- |
| Procédures CPA | Avant migration | Historique, sauf les 4 procédures non hybridées |
| Procédures hybrides | Pendant la migration | **En vigueur** |
| Corpus cible | Après migration | Cible à valider |

## Synthèse

|  | Historique | Hybride | Cible |
| --- | --- | --- | --- |
| **Procédures** | **31** | **17** | **20** |
| Domaine stock | 7 | 4 | 4 |
| Domaine atelier | 5 | 3 | 2 |
| Domaine terrain | 6 | 4 | 4 |
| Domaine Intune | 6 | 3 | 5 |
| Domaine identités | 7 | 3 | 5 |

Le corpus hybride est le plus court des trois, et c'est normal : il ne reprend que les procédures dont la migration change l'exécution. Les quatre autres restent applicables dans leur version historique.

Du début à la fin du mouvement, **onze procédures disparaissent**. La migration supprime davantage qu'elle ne crée : le travail de préparation et de saisie s'efface au profit du contrôle et du pilotage.

## Comment lire les tableaux

- **→ H..** : la procédure est reprise dans le corpus hybride sous ce code. C'est la version à appliquer aujourd'hui.
- **—** : la procédure n'est pas hybridée. Sa version historique reste applicable en l'état.
- **à produire** : lacune identifiée. La procédure existe en historique et en cible, mais pas encore en hybride ; appliquer la version historique en attendant.

## 📦 Gestion du stock

| Procédure historique | Pendant la migration | Après migration | Motif |
| --- | --- | --- | --- |
| STOCK-001 — Réception et contrôle livraison | → STOCK-H01 | **Fusionnée** → STOCK-C01 | Réception et injection ne font plus qu'une étape |
| STOCK-002 — Étiquetage et injection GLPI | → STOCK-H01 | **Fusionnée** → STOCK-C01 | Étiquetage réalisé en usine, injection par import du bon de livraison |
| STOCK-003 — Inventaire périodique | — | **Supprimée** | Aucun discriminant pendant la migration ; assuré ensuite par l'agent d'inventaire GLPI |
| STOCK-004 — Dotation matériel | → STOCK-H02 | **Maintenue** → STOCK-C02 | Allégée de la phase de préparation, enrichie du contrôle de compte |
| STOCK-005 — Retour matériel | → STOCK-H03 | **Maintenue** → STOCK-C03 | Enrichie de la détection des comptes orphelins |
| STOCK-006 — Réforme et destruction | → STOCK-H04 | **Maintenue** → STOCK-C04 | Inchangée sur le fond — écart RGPD de priorité 1 non résolu |
| STOCK-007 — Marchés publics et achats | — | **Sortie du corpus** | Relève du pilotage de la cellule, non de l'opérationnel courant |

## 🔧 Atelier

| Procédure historique | Pendant la migration | Après migration | Motif |
| --- | --- | --- | --- |
| ATL-001 — Préparation poste MDT | → ATL-H01, colonne 🟠 | **Supprimée** | MDT décommissionné |
| ATL-002 — Préparation poste Intune/Autopilot | → ATL-H01, colonne 🔵 | **Remplacée** → ATL-C02 | Devient un contrôle de conformité : le poste arrive enrôlé |
| ATL-003 — SAV et incidents N2 | → ATL-H02 | **Maintenue** → ATL-C01 | Enrichie de l'arbitrage garantie constructeur |
| ATL-004 — Maintenance image MDT | → ATL-H03 | **Supprimée** | Plus d'image maintenue en interne |
| ATL-005 — Organisation physique et KPI | — | **Sortie du corpus** | Relève du pilotage de la cellule |

> ATL-H01 est la seule procédure hybride qui fusionne deux procédures historiques en deux colonnes : la colonne 🟠 est ATL-001, la colonne 🔵 est ATL-002. C'est la lecture la plus directe du principe du corpus hybride.

> ATL-H03 n'a pas de colonne 🔵 et pas de successeur cible : la maintenance de l'image MDT disparaît avec MDT. Elle s'éteint avec le dernier poste 🟠.

## 🚗 Agents de proximité terrain

| Procédure historique | Pendant la migration | Après migration | Motif |
| --- | --- | --- | --- |
| TER-001 — Planification et priorisation | → TER-H01 | **Maintenue** → TER-C01 | Inchangée |
| TER-002 — Dotation sur site | → TER-H02 | **Maintenue** → TER-C02 | Allégée : plus de finalisation d'enrôlement |
| TER-003 — Dépannage N1 sur site | → TER-H03 | **Maintenue** → TER-C03 | Enrichie du contrôle de conformité Intune |
| TER-004 — Téléassistance et escalade | → TER-H04 | **Fusionnée** → TER-C04 | Outil changé : AnyDesk remplace VNC et TeamViewer |
| TER-005 — Interventions îles éloignées | → TER-H04 | **Fusionnée** → TER-C04 | Simplifiée : les postes arrivent enrôlés |
| TER-006 — Récupération matériel | → STOCK-H03 | **Fusionnée** → STOCK-C03 | Le retour relève du cycle de vie du matériel |

## 🖥️ Console Intune

| Procédure historique | Pendant la migration | Après migration | Motif |
| --- | --- | --- | --- |
| INT-001 — Enrôlement Autopilot Windows 11 | → INT-H01 | **Remplacée** → INT-C01 | L'enrôlement est réalisé par le fournisseur ; reste l'attribution |
| INT-002 — Enrôlement Android Enterprise | **à produire** | **Maintenue** → INT-C02 | Périmètre conservé — lacune du corpus hybride |
| INT-003 — Packaging et déploiement | → INT-H02 | **Maintenue** → INT-C03 | Enrichie du partage CPA/CSO selon affectation du ticket |
| INT-004 — Gestion profils et groupes | **à produire** | **Maintenue** → INT-C04 | Inchangée — lacune du corpus hybride |
| INT-005 — Retrait et désinscription | → INT-H03 | **Maintenue** → INT-C05 | Inchangée |
| INT-006 — SecOps, alertes EDR et antivirus | — | **Transférée à la CSO** | Relève du périmètre de la Cellule Sécurité Opérationnelle |

## 👤 EntraID / Exchange

Le discriminant de ce domaine n'est pas le poste mais la mise en service d'IdentityDSI pour le service de l'agent. Les trois procédures hybrides regroupent donc davantage que leurs homologues.

| Procédure historique | Pendant la migration | Après migration | Motif |
| --- | --- | --- | --- |
| ID-001 — Création compte utilisateur | → ID-H01 | **Remplacée** → ID-C01 | IdentityDSI provisionne ; la cellule vérifie |
| ID-002 — Modification compte | → ID-H01 | **Supprimée** | Le modèle de poste est appliqué par IdentityDSI |
| ID-003 — Désactivation et suppression | → ID-H01 | **Remplacée** → ID-C01 | Pilotée par IdentityDSI ; la cellule désactive les comptes orphelins |
| ID-004 — Déblocage et réinitialisation MFA | → ID-H03 | **Maintenue** → ID-C04 | Enrichie de la qualification sécurité |
| ID-005 — Création et gestion BALP | → ID-H02 | **Fusionnée** → ID-C03 | Regroupée avec les ressources Exchange |
| ID-006 — Gestion ressources Exchange | → ID-H02 | **Fusionnée** → ID-C03 | Même circuit, même logique de propriétaire fonctionnel |
| ID-007 — Attribution et suivi licences M365 | → ID-H03 | **Maintenue** → ID-C05 | Inchangée — écart de suivi non résolu |

## Procédures créées

| Code | Procédure | Apparaît en | Raison d'être |
| --- | --- | --- | --- |
| **ID-C02** | Création d'un compte hors SIRH | Cible ; traitée dès aujourd'hui dans ID-H02 | Le périmètre hors contrat devient le cœur du domaine identités, alors qu'il n'était traité qu'incidemment |

## Lacunes du corpus hybride

Deux procédures existent en historique et en cible, mais pas encore en hybride. Tant qu'elles ne sont pas produites, l'agent applique la version historique.

| Manque | Source historique | Équivalent cible |
| --- | --- | --- |
| Enrôlement et gestion des tablettes Android Enterprise | INT-002 | INT-C02 |
| Gestion des profils et groupes dynamiques | INT-004 | INT-C04 |

## Écarts d'audit non résolus par la migration

Sept constats subsistent. Ils ne relèvent pas de la bascule technique mais de l'organisation, et devront être portés par les nouvelles missions de la cellule.

| Écart | Domaine | Priorité |
| --- | --- | --- |
| Absence de registre de traçabilité des destructions | Stock | **1** |
| Absence de certificats de destruction du prestataire | Stock | **1** |
| Absence de suivi de consommation des licences M365 | Identités | **1** |
| Absence d'audit périodique des comptes inactifs | Identités | 2 |
| Absence d'inventaire centralisé des BALP | Identités | 2 |
| Absence de versioning et de revue des scripts PowerShell | Intune | 2 |
| Absence de veille sur les mises à jour applicatives | Intune | 3 |

## Politiques à établir

Deux politiques conditionnent l'applicabilité de procédures cibles :

- **Politique d'archivage et de rétention des données** — conditionne la durée de conservation avant réinitialisation dans STOCK-C03.
- **Registre RGPD des destructions** — conditionne l'exécutabilité de STOCK-C04, dont deux étapes sont inapplicables sans lui.
