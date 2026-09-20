<!-- confluence: SI / page 1802321 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/1802321 -->
<!-- parent_id: 1802241 · parent: 🖥️ Console Intune — cible -->

# PROC-INT-C04 — Gestion des profils et groupes dynamiques

|  |  |
| --- | --- |
| **Code** | PROC-INT-C04 |
| **Domaine** | Console Intune |
| **Statut** | Cible à valider |
| **Criticité** | Haute |
| **Contrainte RGPD** | Non |
| **Outils** | Console Intune, EntraID |

> **Règle invariante CPA** — Toute dotation, intervention ou action manuelle sur le parc fait l'objet d'un ticket Tauturu.

## Objet

Maintenir les profils de déploiement et les groupes dynamiques EntraID qui déterminent la configuration et les applications reçues par chaque appareil.

C'est le mécanisme de ciblage de l'ensemble du parc : toute modification se propage automatiquement, sans intervention sur les postes.

## Déclencheur

Création d'un service, réorganisation, évolution d'un périmètre applicatif, ou demande de modification du ciblage.

## Étapes

| # | Action | Qui | Résultat attendu |
| --- | --- | --- | --- |
| 1 | Qualifier le besoin : quels appareils, quelle configuration, quel périmètre | Agent CPA | Besoin caractérisé |
| 2 | Identifier le groupe dynamique existant couvrant le besoin, ou en définir un nouveau | Agent CPA | Cible identifiée |
| 3 | Rédiger ou modifier la règle d'appartenance | Agent CPA | Règle formulée |
| 4 | **Évaluer la population concernée avant application** | Agent CPA | Volume et périmètre vérifiés |
| 5 | Appliquer la règle et attendre le recalcul des appartenances | Agent CPA | Groupe peuplé |
| 6 | Vérifier sur un échantillon d'appareils que le ciblage est correct | Agent CPA | Ciblage confirmé |
| 7 | Documenter la modification dans le ticket | Agent CPA | Traçabilité assurée |

## Points de vigilance

- **L'étape 4 n'est pas facultative.** Une règle d'appartenance mal formulée peut cibler une population bien plus large que prévu, et le déploiement associé part sans confirmation supplémentaire. Sur un parc de cette taille, une erreur se compte en milliers de postes.
- Le recalcul des appartenances est asynchrone : vérifier trop tôt donne une image incomplète.
- Une modification de profil de déploiement ne s'applique qu'aux appareils qui repassent par le processus d'inscription. Les appareils déjà en service conservent leur configuration.
- Les groupes servant au ciblage des licences relèvent de PROC-ID-C05.

## Procédures liées

- PROC-INT-C01 — Attribution d'un appareil enrôlé
- PROC-INT-C03 — Packaging et déploiement d'une application
- PROC-ID-C05 — Attribution et suivi des licences M365
