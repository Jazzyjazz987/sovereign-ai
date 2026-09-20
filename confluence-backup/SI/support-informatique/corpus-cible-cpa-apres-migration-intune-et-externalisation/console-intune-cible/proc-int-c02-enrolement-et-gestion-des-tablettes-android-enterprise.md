<!-- confluence: SI / page 1736766 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/1736766 -->
<!-- parent_id: 1802241 · parent: 🖥️ Console Intune — cible -->

# PROC-INT-C02 — Enrôlement et gestion des tablettes Android Enterprise

|  |  |
| --- | --- |
| **Code** | PROC-INT-C02 |
| **Domaine** | Console Intune |
| **Statut** | Cible à valider |
| **Criticité** | Moyenne |
| **Contrainte RGPD** | Non |
| **Outils** | Console Intune, Tauturu |

> **Règle invariante CPA** — Toute dotation, intervention ou action manuelle sur le parc fait l'objet d'un ticket Tauturu.

## Objet

Enrôler et gérer les tablettes Android sous Android Enterprise, pour les services qui en sont dotés.

Le volume reste marginal au regard du parc de postes de travail, mais le périmètre est maintenu dans la cible.

## Déclencheur

Ticket de dotation portant sur une tablette, ou incident sur une tablette déjà déployée.

## Étapes

| # | Action | Qui | Résultat attendu |
| --- | --- | --- | --- |
| 1 | Vérifier l'éligibilité de la demande et le service concerné | Agent CPA | Demande recevable |
| 2 | Enrôler la tablette selon le mode d'inscription retenu pour le service | Agent CPA | Tablette inscrite |
| 3 | Rattacher l'appareil au profil de configuration Android Enterprise | Agent CPA | Profil appliqué |
| 4 | Vérifier le déploiement des applications ciblées | Agent CPA | Applications présentes |
| 5 | Enregistrer l'appareil et son bénéficiaire dans Tauturu | Agent CPA | Inventaire à jour |
| 6 | Remettre la tablette au bénéficiaire et documenter le ticket | Agent CPA | Ticket clôturé |

## Points de vigilance

- **Le support des tablettes ne repose pas sur la prise en main à distance.** La couverture d'AnyDesk sur Android est limitée selon les modèles : le diagnostic s'effectue par téléphone, appuyé sur les informations remontées par la console.
- Une tablette perdue ou volée se traite par effacement à distance depuis la console, avec déclaration à la Cellule Sécurité Opérationnelle et création d'un ticket.
- Le retrait d'une tablette suit PROC-INT-C05 au même titre qu'un poste de travail.

## Procédures liées

- PROC-INT-C05 — Retrait et désinscription d'un appareil
- PROC-ATL-C02 — Contrôle de conformité du matériel à réception
