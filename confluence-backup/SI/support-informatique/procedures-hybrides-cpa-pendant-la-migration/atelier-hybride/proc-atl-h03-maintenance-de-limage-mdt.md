<!-- confluence: SI / page 1736947 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/1736947 -->
<!-- parent_id: 1736826 · parent: 🔧 Atelier — hybride -->

# PROC-ATL-H03 — Maintenance de l'image MDT

|  |  |
| --- | --- |
| **Code** | PROC-ATL-H03 |
| **Domaine** | Atelier |
| **Statut** | En vigueur pendant la migration — **procédure à durée de vie limitée** |
| **Discriminant** | Sans objet — ne concerne que le parc legacy |
| **Criticité** | Haute |
| **Outils** | Cluster, machine virtuelle MDT, poste de test |

> **Règle invariante CPA** — Toute dotation, intervention ou action manuelle sur le parc fait l'objet d'un ticket Tauturu.

## Objet

Maintenir l'image de déploiement à jour, afin que les postes encore préparés sous MDT intègrent les correctifs de sécurité et les pilotes récents.

**Cette procédure n'a pas de colonne 🔵.** Elle ne concerne que le parc legacy. Elle s'éteindra avec le dernier poste MDT et n'existe pas dans le corpus cible : sur un poste enrôlé, la configuration est appliquée par la console, sans image intermédiaire.

## Déclencheur

Publication mensuelle des correctifs de sécurité, nouveau pilote, ou modification de la séquence de déploiement.

## Étapes

| # | Action | Qui |
| --- | --- | --- |
| 1 | Identifier les correctifs applicables et les pilotes disponibles | Ingénieur |
| 2 | Modifier l'image et la séquence de déploiement | Ingénieur |
| 3 | Déployer l'image sur un poste de test en atelier | Ingénieur |
| 4 | Valider le déploiement : système, applications, pilotes, sécurité | Ingénieur et responsable de cellule |
| 5 | Mettre en production l'image validée | Ingénieur |
| 6 | **Effectuer une copie de sauvegarde de la machine virtuelle après modification** | Ingénieur |
| 7 | Documenter la modification dans un ticket | Ingénieur |

## Points de vigilance

- **L'étape 6 est la seule protection de l'infrastructure.** La machine virtuelle ne bénéficie d'aucune sauvegarde automatisée : la copie manuelle après chaque modification est ce qui sépare une reprise en quelques heures d'une reconstruction complète.
- **Une seule personne administre l'infrastructure.** Pendant toute la période hybride, son indisponibilité bloque la préparation de l'ensemble du parc non migré. L'identification et la formation d'un suppléant est un impératif de continuité, pas une amélioration.
- Tester systématiquement sur un poste physique avant mise en production : un déploiement défectueux se propage à tous les postes préparés ensuite.
- **Ne pas investir dans cette image au-delà du nécessaire.** Chaque évolution non indispensable porte sur un outil dont la date d'extinction est connue. Corriger la sécurité, oui ; enrichir, non.

## Extinction de la procédure

Cette procédure sera retirée du corpus lorsque le dernier poste legacy aura été remplacé ou enrôlé. À ce moment :

- l'infrastructure de déploiement pourra être décommissionnée ;
- la dépendance à une compétence unique disparaîtra ;
- PROC-ATL-H01 se réduira à sa colonne 🔵.

## Procédures liées

- PROC-ATL-H01 — Préparation ou contrôle d'un poste avant dotation
