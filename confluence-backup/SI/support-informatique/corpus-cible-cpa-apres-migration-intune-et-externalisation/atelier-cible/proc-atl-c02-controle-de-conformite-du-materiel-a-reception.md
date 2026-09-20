<!-- confluence: SI / page 1736746 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/1736746 -->
<!-- parent_id: 1736705 · parent: 🔧 Atelier — cible -->

# PROC-ATL-C02 — Contrôle de conformité du matériel à réception

|  |  |
| --- | --- |
| **Code** | PROC-ATL-C02 |
| **Domaine** | Atelier |
| **Statut** | Cible à valider |
| **Criticité** | Haute |
| **Contrainte RGPD** | Non |
| **Outils** | Tauturu, console Intune |

> **Règle invariante CPA** — Toute dotation, intervention ou action manuelle sur le parc fait l'objet d'un ticket Tauturu.

## Objet

Vérifier, par échantillonnage, que le matériel livré est conforme à ce que le marché prévoit : étiquetage correct, hash Autopilot enregistré, tag de déploiement attendu, appareil visible dans la console Intune.

Cette procédure remplace la préparation de poste. Elle en est l'exact inverse : la cellule ne fabrique plus la conformité, elle la constate.

## Déclencheur

Réception d'un lot de matériel, après import du bon de livraison dans Tauturu.

## Acteurs

| Rôle | Responsabilité |
| --- | --- |
| Agent atelier | Réalise le contrôle et documente les écarts |
| Responsable de cellule | Décide de la suite en cas d'écart : acceptation, réserve, refus |

## Étapes

| # | Action | Qui | Résultat attendu |
| --- | --- | --- | --- |
| 1 | Déterminer la taille de l'échantillon selon le volume du lot | Agent atelier | Échantillon défini |
| 2 | Vérifier la présence et la lisibilité de l'étiquette sur chaque unité de l'échantillon | Agent atelier | Étiquetage conforme |
| 3 | Vérifier la présence de l'appareil dans la console Intune et la cohérence du tag de déploiement | Agent atelier | Enrôlement confirmé |
| 4 | Démarrer un poste de l'échantillon et vérifier l'application des profils | Agent atelier | Conformité fonctionnelle établie |
| 5 | Vérifier la remontée de la fiche par l'agent d'inventaire GLPI | Agent atelier | Inventaire enrichi |
| 6 | En cas d'écart : élargir le contrôle au lot entier, documenter dans le ticket de réception, alerter le responsable de cellule | Agent atelier | Écart caractérisé |
| 7 | Documenter le résultat du contrôle au ticket de réception | Agent atelier | Contrôle tracé |

## Points de vigilance

- **La procédure d'injection des hash en usine est certifiée.** Le contrôle porte sur la conformité de la livraison, non sur la validité du procédé fournisseur.
- Un écart constaté sur l'échantillon n'est jamais traité unité par unité : il justifie l'élargissement au lot, car une erreur d'usine est systématique par nature.
- Le contrôle intervient après l'import du bon de livraison : la fiche existe déjà dans Tauturu, l'écart s'y documente.
- Les tablettes Android suivent le même principe, avec vérification de l'inscription au programme Android Enterprise.

## Procédures liées

- PROC-STOCK-C01 — Réception et injection du matériel
- PROC-INT-C01 — Attribution d'un appareil enrôlé
- PROC-INT-C02 — Enrôlement et gestion des tablettes Android Enterprise
