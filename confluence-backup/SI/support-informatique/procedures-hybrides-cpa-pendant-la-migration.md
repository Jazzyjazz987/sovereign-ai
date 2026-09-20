<!-- confluence: SI / page 1802375 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/1802375 -->
<!-- parent_id: 65813 · parent: Support informatique -->

# Procédures hybrides de la Cellule Parc et Assistance

**Statut : applicable — c'est le corpus en vigueur pendant la migration**

Ce corpus décrit le fonctionnement **actuel** de la cellule, pendant la période où le parc est dans deux états simultanés : des postes encore préparés sous MDT, et des postes enrôlés sous Intune.

Il n'est ni l'ancien corpus ni la cible. Il couvre la transition entre les deux.

## Comment lire ces procédures

**Chaque chapitre est présenté en deux colonnes.**

| 🟠 Poste MDT | 🔵 Poste Intune |
| --- | --- |
| Ce que l'agent fait sur un poste encore géré par l'ancienne chaîne | Ce que l'agent fait sur un poste enrôlé |

L'agent identifie d'abord le poste qu'il a devant lui, puis lit **une seule colonne**. Lorsque les deux colonnes portent le même contenu, le chapitre est présenté en texte simple : la migration ne change rien sur ce point.

## Comment déterminer l'état d'un poste

| Question | Réponse | Colonne à lire |
| --- | --- | --- |
| L'appareil figure-t-il dans la console Intune ? | Oui | 🔵 Poste Intune |
|  | Non | 🟠 Poste MDT |

Le statut dans Tauturu confirme, mais la console Intune fait foi : un appareil qui y figure est géré par la nouvelle chaîne, quelles que soient les informations d'inventaire.

**En cas de doute, lire la colonne 🟠.** Appliquer l'ancienne procédure à un poste migré produit une action sans effet ; appliquer la nouvelle à un poste legacy produit une action impossible, et l'agent perd du temps à chercher ce qui n'existe pas.

## Deux discriminants, jamais une date

Une procédure hybride ne se lit jamais en fonction du calendrier de migration. Elle se lit en fonction d'un fait observable, et il n'en existe que deux dans ce corpus :

| Discriminant | Ce qu'il distingue | Chapitres concernés |
| --- | --- | --- |
| **Par poste** | L'appareil figure ou non dans la console Intune | Préparation, enrôlement, dotation, conformité, packaging, retrait |
| **Par bascule** | Une évolution acquise une fois pour toute la cellule, ou pour un service entier | Provisionnement des identités par IdentityDSI ; abandon de LDAP ; arrêt du proxy ; fin du suivi Excel ; passage à AnyDesk ; fichiers sur SharePoint |

Chaque procédure précise le discriminant qui lui est applicable dans son tableau de métadonnées, à la ligne **Discriminant**. Dans le domaine EntraID / Exchange, le discriminant n'est pas le poste : les colonnes y distinguent l'avant et l'après mise en service d'IdentityDSI.

Ce corpus reste donc valable quel que soit l'avancement de la migration. Il ne se périme pas, il se vide : à mesure que les postes basculent, la colonne 🟠 cesse simplement d'être lue.

## Pourquoi 17 procédures et non 31

Une procédure n'est hybridée que si la migration change la manière de l'exécuter. Celles que la migration ne touche pas ne sont pas recopiées ici : elles restent applicables dans la branche **Procédures CPA**, sans modification.

Procédures volontairement non hybridées :

| Procédure restée en vigueur dans la branche historique | Motif |
| --- | --- |
| PROC-STOCK-003 — Inventaire périodique | Aucun discriminant : l'inventaire porte sur les mêmes biens, par le même outil |
| PROC-STOCK-007 — Marchés publics et achats informatiques | Relève du cadre d'achat, indépendant de la chaîne de déploiement |
| PROC-ATL-005 — Organisation physique de l'atelier et KPI | Organisation de l'espace de travail, sans lien avec l'état des postes |
| PROC-INT-006 — SecOps, remontée et traitement des alertes | Relève de la Cellule Sécurité Opérationnelle |

Les regroupements effectués sont les suivants : STOCK-001 et STOCK-002 forment STOCK-H01 ; STOCK-005 et TER-006 forment STOCK-H03 ; ATL-001 et ATL-002 forment ATL-H01 ; TER-004 et TER-005 forment TER-H04 ; ID-001, ID-002 et ID-003 forment ID-H01 ; ID-005 et ID-006 forment ID-H02 ; ID-004 et ID-007 forment ID-H03.

**Procédures restant à hybrider** — elles existent dans la branche historique et dans le corpus cible, mais pas encore ici :

| Manque | Source historique | Équivalent cible |
| --- | --- | --- |
| Enrôlement et gestion des tablettes Android Enterprise | PROC-INT-002 | PROC-INT-C02 |
| Gestion des profils et groupes dynamiques | PROC-INT-004 | PROC-INT-C04 |

Tant que ces deux procédures ne sont pas produites, l'agent applique la version historique.

## Structure du corpus hybride

- 📦 Gestion du stock — hybride
- 🔧 Atelier — hybride
- 🚗 Agents de proximité terrain — hybride
- 🖥️ Console Intune — hybride
- 👤 EntraID / Exchange — hybride

## Les trois corpus

| Corpus | Décrit | Statut |
| --- | --- | --- |
| Procédures CPA | L'organisation avant migration | Historique, sauf les 4 procédures non hybridées ci-dessus, qui restent applicables |
| **Procédures hybrides** | **L'organisation pendant la migration** | **En vigueur** |
| Corpus cible | L'organisation après migration | Cible à valider |

Le corpus hybride s'éteint à l'achèvement de la migration : chaque procédure devient alors sa colonne 🔵, et le corpus cible prend le relais.

## La règle invariante

> **Toute dotation, intervention ou action manuelle sur le parc fait l'objet d'un ticket Tauturu.**

Elle vaut dans les deux colonnes, sans exception. C'est le seul point que la migration ne modifie nulle part.

## Références réglementaires

- Arrêté n° 2388 CM du 28 novembre 2025 portant modification de l'organisation de la DSI
- Circulaire n° 7726 PR du 1er octobre 2021 relative à la charte informatique
- Circulaire n° 4748/PR du 15 juillet 2025 relative à la protection des données personnelles
- Circulaire n° 979/PR du 14 février 2025 relative à l'exécution des achats informatiques
- Règlement général sur la protection des données
