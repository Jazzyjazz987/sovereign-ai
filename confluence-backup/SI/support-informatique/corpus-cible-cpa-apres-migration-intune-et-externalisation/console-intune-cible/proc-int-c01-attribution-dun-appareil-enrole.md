<!-- confluence: SI / page 1769533 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/1769533 -->
<!-- parent_id: 1802241 · parent: 🖥️ Console Intune — cible -->

# PROC-INT-C01 — Attribution d'un appareil enrôlé

|  |  |
| --- | --- |
| **Code** | PROC-INT-C01 |
| **Domaine** | Console Intune |
| **Statut** | Cible à valider |
| **Criticité** | Haute |
| **Contrainte RGPD** | Non |
| **Outils** | Console Intune, Tauturu |

> **Règle invariante CPA** — Toute dotation, intervention ou action manuelle sur le parc fait l'objet d'un ticket Tauturu.

## Objet

Rattacher un appareil, enrôlé en usine par le fournisseur, au bon profil de déploiement et au bon bénéficiaire.

Cette procédure remplace l'enrôlement Autopilot réalisé autrefois en atelier : extraction du hash, enregistrement dans la console et affectation du tag sont désormais faits par le fournisseur.

## Déclencheur

Attribution d'un appareil à un bénéficiaire, dans le cadre d'une dotation.

## Étapes

| # | Action | Qui | Résultat attendu |
| --- | --- | --- | --- |
| 1 | Identifier l'appareil dans la console Intune par son numéro de série | Agent CPA | Appareil localisé |
| 2 | Vérifier le tag de déploiement affecté en usine | Agent CPA | Profil correct confirmé |
| 3 | Corriger le tag si le profil attendu diffère du profil affecté | Agent CPA | Profil aligné sur le besoin |
| 4 | Vérifier l'appartenance aux groupes dynamiques attendus | Agent CPA | Ciblage applicatif confirmé |
| 5 | Documenter l'attribution dans le ticket de dotation | Agent CPA | Traçabilité assurée |
| 6 | Après premier démarrage, vérifier l'état de conformité de l'appareil | Agent CPA | Conformité constatée |

## Points de vigilance

- **Le tag de déploiement conditionne tout le reste** : profil Autopilot, groupes dynamiques, applications déployées. Une erreur de tag se traduit par un poste qui démarre avec la mauvaise configuration, et le bénéficiaire la découvre à l'ouverture de session.
- Les politiques de conformité et de configuration sont figées et identiques pour l'ensemble du parc : il n'y a pas de paramétrage par poste.
- Un appareil absent de la console alors qu'il figure au bon de livraison relève d'un écart de livraison — voir PROC-ATL-C02.
- Les appartenances aux groupes dynamiques se recalculent avec un délai : une vérification immédiate après attribution peut donner un résultat incomplet.

## Procédures liées

- PROC-STOCK-C02 — Dotation de matériel
- PROC-ATL-C02 — Contrôle de conformité du matériel à réception
- PROC-INT-C04 — Gestion des profils et groupes dynamiques
