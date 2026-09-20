<!-- confluence: SI / page 1769573 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/1769573 -->
<!-- parent_id: 1736726 · parent: 👤 EntraID / Exchange — cible -->

# PROC-ID-C05 — Attribution et suivi des licences M365

|  |  |
| --- | --- |
| **Code** | PROC-ID-C05 |
| **Domaine** | EntraID / Exchange |
| **Statut** | Cible à valider |
| **Criticité** | Haute |
| **Contrainte RGPD** | Non |
| **Outils** | EntraID, centre d'administration M365, Tauturu |

> **Règle invariante CPA** — Toute dotation, intervention ou action manuelle sur le parc fait l'objet d'un ticket Tauturu.

## Objet

Attribuer les licences Microsoft 365 selon le besoin réel des agents, et suivre la consommation du parc de licences.

Le périmètre comprend plusieurs types de licences, du plus léger au plus complet. Le principe est l'adéquation au besoin, non l'attribution par défaut du niveau le plus élevé.

## Déclencheur

Provisionnement d'un compte par IdentityDSI, création d'un compte hors SIRH, ou demande d'évolution du besoin d'un agent.

## Étapes

| # | Action | Qui | Résultat attendu |
| --- | --- | --- | --- |
| 1 | Identifier le besoin réel de l'agent selon sa fonction | Agent CPA | Niveau de licence déterminé |
| 2 | Vérifier la disponibilité de licences du type requis | Agent CPA | Disponibilité confirmée |
| 3 | Attribuer la licence, de préférence par groupe plutôt qu'individuellement | Agent CPA | Licence appliquée |
| 4 | Vérifier l'activation effective des services attendus | Agent CPA | Services disponibles |
| 5 | Documenter l'attribution dans le ticket | Agent CPA | Traçabilité assurée |
| 6 | **Lors d'une suppression de compte, vérifier la libération de la licence** | Agent CPA | Licence rendue au pool |

## Suivi de la consommation

| # | Action | Périodicité | Résultat attendu |
| --- | --- | --- | --- |
| 1 | Extraire l'état de consommation par type de licence | Périodique | Volume attribué connu |
| 2 | Comparer au volume souscrit | Périodique | Marge ou dépassement identifié |
| 3 | Identifier les licences attribuées à des comptes inactifs | Périodique | Gisement de récupération |
| 4 | Alerter le responsable de cellule en cas d'approche du plafond | Périodique | Anticipation du renouvellement |

## Points de vigilance

- **L'attribution par groupe est préférable à l'attribution individuelle.** Elle rend la licence conditionnelle à l'appartenance, donc automatiquement libérée quand l'agent quitte le périmètre. Une licence attribuée à la main y reste jusqu'à ce que quelqu'un la retire.
- Une licence non libérée après suppression d'un compte est une dépense sans contrepartie. L'étape 6 est le seul point de récupération.
- Le niveau de licence conditionne l'accès aux services : attribuer en dessous du besoin génère des tickets, au-dessus génère des coûts.

## Écart non résolu

Aucun suivi formalisé de la consommation de licences n'est en place. En l'absence de ce suivi, ni les surcoûts ni les dépassements ne sont détectables. Cet écart a été classé en priorité 1 lors de l'audit du domaine, et relève des nouvelles missions à définir pour la cellule.

## Procédures liées

- PROC-ID-C01 — Vérification et suivi des comptes provisionnés
- PROC-ID-C02 — Création d'un compte hors SIRH
- PROC-INT-C04 — Gestion des profils et groupes dynamiques
