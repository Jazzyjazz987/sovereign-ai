<!-- confluence: SI / page 1769493 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/1769493 -->
<!-- parent_id: 1703958 · parent: 📦 Gestion du stock — cible -->

# PROC-STOCK-C03 — Retour de matériel

|  |  |
| --- | --- |
| **Code** | PROC-STOCK-C03 |
| **Domaine** | Gestion du stock |
| **Statut** | Cible à valider |
| **Criticité** | Moyenne |
| **Contrainte RGPD** | **Oui** |
| **Outils** | Tauturu, console Intune |

> **Règle invariante CPA** — Toute dotation, intervention ou action manuelle sur le parc fait l'objet d'un ticket Tauturu.

## Objet

Gérer le retour d'un équipement à la cellule, en assurant la protection des données de l'agent, la mise à jour de l'inventaire et l'orientation du matériel vers le stock ou vers la réforme.

## Déclencheur

Départ d'un agent, mutation, fin de contrat, remplacement de matériel ou restitution volontaire. Un ticket de récupération de poste est créé au départ de l'agent.

## Acteurs

| Rôle | Responsabilité |
| --- | --- |
| Agent de proximité terrain | Récupère le matériel sur site |
| Agent atelier | Inspecte et oriente : remise en stock ou réforme |
| Agent CPA | Met à jour Tauturu et la console Intune |

## Étapes

| # | Action | Qui | Résultat attendu |
| --- | --- | --- | --- |
| 1 | Créer ou reprendre le ticket Tauturu de récupération | Agent de proximité | Ticket ouvert |
| 2 | Récupérer le matériel chez l'agent ou au guichet | Agent de proximité | Matériel en transit |
| 3 | Inspecter l'état physique à l'atelier | Agent atelier | État documenté au ticket |
| 4 | Placer le matériel en zone de conservation | Agent atelier | Matériel isolé du stock neuf |
| 5 | Passer le statut Tauturu à « Retourné / En attente » | Agent CPA | Inventaire à jour |
| 6 | **Vérifier si un compte rattaché au poste est encore actif ; le cas échéant, le désactiver** | Agent CPA | Compte orphelin traité |
| 7 | À l'issue de la période de conservation : réinitialiser le poste via Intune et le remettre en stock, ou déclencher PROC-STOCK-C04 | Agent atelier | Poste réintégré ou orienté réforme |

## Points de contrôle RGPD

- Le matériel retourné contient des données de l'agent. Il reste **physiquement séparé du stock neuf** jusqu'à réinitialisation.
- La durée de conservation avant réinitialisation est régie par la politique d'archivage de la DSI. **Cette politique reste à établir** — écart de priorité 1 identifié en audit, non résolu par la migration.
- La réinitialisation via Intune doit être tracée dans le ticket : date, agent, appareil.

## Points de vigilance

- L'étape 6 est le filet de sécurité du dispositif d'identités : la réaffectation d'un poste fait remonter des comptes que le circuit de départ a laissés passer.
- Un poste retourné sans ticket est un poste perdu pour l'inventaire. Aucune récupération ne se fait de la main à la main.

## Procédures liées

- PROC-STOCK-C04 — Réforme et destruction des données
- PROC-INT-C05 — Retrait et désinscription d'un appareil
- PROC-ID-C01 — Vérification et suivi des comptes provisionnés
