<!-- confluence: SI / page 1736987 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/1736987 -->
<!-- parent_id: 1736847 · parent: 🚗 Agents de proximité terrain — hybride -->

# PROC-TER-H04 — Télé-assistance et interventions aux îles

|  |  |
| --- | --- |
| **Code** | PROC-TER-H04 |
| **Domaine** | Agents de proximité terrain |
| **Statut** | En vigueur pendant la migration |
| **Discriminant** | État du poste, et outil de prise en main en service |
| **Criticité** | Moyenne |
| **Contrainte RGPD** | **Oui** |

> **Règle invariante CPA** — Toute dotation, intervention ou action manuelle sur le parc fait l'objet d'un ticket Tauturu.

## Objet

Assurer le support à distance, et traiter les demandes des îles éloignées où aucun déplacement n'est réalisé.

## Étapes communes de télé-assistance

| # | Action | Qui |
| --- | --- | --- |
| 1 | Créer ou reprendre le ticket Tauturu | Agent télé-assistance |
| 2 | Qualifier la demande : périmètre, impact, priorité | Agent télé-assistance |
| 3 | Identifier l'état du poste concerné | Agent télé-assistance |
| 4 | **Obtenir l'accord explicite de l'agent avant toute prise en main** | Agent télé-assistance |

## Étapes propres à l'état du poste

| # | 🟠 Poste MDT | 🔵 Poste Intune |
| --- | --- | --- |
| 5 | Prendre la main avec l'outil de prise en main en service | Consulter d'abord la console : l'incident peut se résoudre sans prise en main |
| 6 | Diagnostiquer localement, sur le poste | Vérifier conformité, déploiements et politiques appliquées |
| 7 | Résoudre à distance, ou escalader vers une intervention sur site | Résoudre par la console lorsque possible, sinon prise en main |
| 8 | Une réinstallation impose le retour du poste à l'atelier | Une réinitialisation se déclenche à distance, sans déplacer le poste |

## Étape finale commune

| # | Action | Qui |
| --- | --- | --- |
| 9 | Documenter la session dans le ticket : durée, actions réalisées, consentement obtenu | Agent télé-assistance |

## Interventions aux îles

| # | 🟠 Poste MDT | 🔵 Poste Intune |
| --- | --- | --- |
| 1 | Préparer le poste en atelier **avant** expédition — environ 2 h | Aucune préparation : le poste part tel qu'il est reçu |
| 2 | Expédier le matériel par transporteur | Expédier le matériel par transporteur |
| 3 | Informer le référent local de l'arrivée et du mode opératoire | Informer le référent local de l'arrivée et du mode opératoire |
| 4 | Accompagner la finalisation par télé-assistance : session, applications, imprimantes | Accompagner le premier démarrage : l'agent s'authentifie, tout s'applique |
| 5 | Prévoir une session d'accompagnement d'environ 45 min | Prévoir environ 15 min |
| 6 | Pour un retour : organiser l'acheminement inverse | Pour un retour : organiser l'acheminement inverse |

**Le gain est le plus net aux îles.** Un poste enrôlé par le fournisseur supprime à la fois la préparation en atelier et la dépendance à une session de télé-assistance longue avec un référent local peu outillé.

## Points de contrôle RGPD

Identiques dans les deux colonnes :

- Le consentement préalable à la prise en main est obligatoire et tracé au ticket.
- L'accès non surveillé, s'il est activé, doit être justifié, encadré et connu de l'agent.
- La session est documentée : durée et actions réalisées.

## Point de vigilance sur l'outil

L'outil de prise en main à distance évolue pendant la période. Selon l'état du déploiement, deux outils peuvent coexister sur le parc.

| Situation | Conduite à tenir |
| --- | --- |
| L'ancien outil est encore installé sur le poste | L'utiliser, sans chercher à installer le nouveau dans l'urgence |
| Le nouvel outil est déployé | L'utiliser exclusivement |
| Les deux sont présents | Utiliser le nouvel outil et signaler le doublon : un outil de prise en main résiduel est une surface d'exposition |

L'outil cible est administré par la Cellule Sécurité Opérationnelle : toute demande de configuration lui est adressée.

## Procédures liées

- PROC-TER-H03 — Dépannage de niveau 1 sur site
- PROC-ATL-H02 — SAV et incidents de niveau 2
- PROC-STOCK-H02 — Dotation de matériel
