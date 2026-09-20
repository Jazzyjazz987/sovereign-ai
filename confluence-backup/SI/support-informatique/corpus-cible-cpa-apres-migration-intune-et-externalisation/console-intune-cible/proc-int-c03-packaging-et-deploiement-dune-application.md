<!-- confluence: SI / page 1769553 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/1769553 -->
<!-- parent_id: 1802241 · parent: 🖥️ Console Intune — cible -->

# PROC-INT-C03 — Packaging et déploiement d'une application

|  |  |
| --- | --- |
| **Code** | PROC-INT-C03 |
| **Domaine** | Console Intune |
| **Statut** | Cible à valider |
| **Criticité** | Haute |
| **Contrainte RGPD** | Non |
| **Outils** | Console Intune, Tauturu, outil de packaging Win32 |

> **Règle invariante CPA** — Toute dotation, intervention ou action manuelle sur le parc fait l'objet d'un ticket Tauturu.

## Objet

Empaqueter une application métier et la déployer sur le parc via Intune.

Le packaging est réalisé indifféremment par un agent de la CPA ou de la Cellule Sécurité Opérationnelle, **selon l'affectation du ticket**. Les applications stratégiques détenues par la CSO sont ajoutées pendant la phase de tests.

## Déclencheur

Ticket de demande de déploiement applicatif émanant d'un service, ou mise à jour d'une application déjà déployée.

## Acteurs

| Rôle | Responsabilité |
| --- | --- |
| Responsable de cellule | Affecte le ticket à la CPA ou à la CSO selon la charge et la nature de l'application |
| Agent CPA ou CSO affecté | Réalise le packaging, les tests et le déploiement |
| Cellule Sécurité Opérationnelle | Fournit et intègre les applications stratégiques en phase de tests |

## Étapes

| # | Action | Qui | Résultat attendu |
| --- | --- | --- | --- |
| 1 | Qualifier la demande : application, périmètre de déploiement, service demandeur | Agent affecté | Besoin caractérisé |
| 2 | **Affecter le ticket à la CPA ou à la CSO** | Responsable de cellule | Responsable identifié |
| 3 | Récupérer les sources et la documentation d'installation | Agent affecté | Sources disponibles |
| 4 | Empaqueter l'application au format Win32 | Agent affecté | Paquet constitué |
| 5 | Écrire le script de détection et les règles d'exigence | Agent affecté | Détection fiable |
| 6 | Déployer sur le groupe de test | Agent affecté | Déploiement pilote en cours |
| 7 | **Intégrer les applications stratégiques fournies par la CSO** | CSO | Périmètre de test complet |
| 8 | Valider le comportement : installation, détection, désinstallation | Agent affecté | Paquet validé |
| 9 | Élargir le déploiement au périmètre cible | Agent affecté | Application déployée |
| 10 | Documenter et clôturer le ticket | Agent affecté | Traçabilité assurée |

## Points de vigilance

- **L'affectation du ticket désigne le responsable, et elle seule.** Sans règle d'affectation explicite, les tickets de packaging rebondissent entre les deux cellules. L'étape 2 nomme l'arbitre : le responsable de cellule, sur critère de charge et de nature applicative.
- Le script de détection conditionne le comportement d'Intune : une détection imprécise provoque des réinstallations en boucle sur l'ensemble du périmètre.
- Toujours tester la désinstallation, pas seulement l'installation : c'est elle qui sert lors d'un retrait ou d'une migration.

## Écarts non résolus par la migration

Deux constats d'audit restent ouverts et ne sont pas traités par cette procédure :

- **Absence de versioning et de revue par les pairs des scripts PowerShell.** Aucun historique, aucun second regard avant déploiement sur le parc.
- **Absence de veille sur les mises à jour applicatives.** La détection des nouvelles versions reste réactive, par remontée des utilisateurs.

Ces deux points relèvent des nouvelles missions à définir pour la cellule.

## Procédures liées

- PROC-INT-C04 — Gestion des profils et groupes dynamiques
