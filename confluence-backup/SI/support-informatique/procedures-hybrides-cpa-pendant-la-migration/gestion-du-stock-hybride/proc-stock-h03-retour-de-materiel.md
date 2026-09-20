<!-- confluence: SI / page 1802416 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/1802416 -->
<!-- parent_id: 1736806 · parent: 📦 Gestion du stock — hybride -->

# PROC-STOCK-H03 — Retour de matériel

|  |  |
| --- | --- |
| **Code** | PROC-STOCK-H03 |
| **Domaine** | Gestion du stock |
| **Statut** | En vigueur pendant la migration |
| **Discriminant** | État du poste retourné |
| **Criticité** | Moyenne |
| **Contrainte RGPD** | **Oui** |

> **Règle invariante CPA** — Toute dotation, intervention ou action manuelle sur le parc fait l'objet d'un ticket Tauturu.

## Objet

Gérer le retour d'un équipement, en protégeant les données de l'agent et en orientant le matériel vers le stock ou vers la réforme.

## Déclencheur

Départ d'un agent, mutation, fin de contrat, remplacement ou restitution volontaire. Un ticket de récupération de poste est créé au départ.

## Étapes communes

| # | Action | Qui |
| --- | --- | --- |
| 1 | Créer ou reprendre le ticket Tauturu de récupération | Agent de proximité |
| 2 | Récupérer le matériel chez l'agent ou au guichet | Agent de proximité |
| 3 | Inspecter l'état physique à l'atelier et le documenter au ticket | Agent atelier |
| 4 | Placer le matériel en zone de conservation, isolé du stock neuf | Agent atelier |
| 5 | Passer le statut Tauturu à « Retourné / En attente » | Agent CPA |
| 6 | Vérifier si un compte rattaché au poste est encore actif ; le cas échéant, le désactiver | Agent CPA |

## Étapes propres à l'état du poste

| # | 🟠 Poste MDT | 🔵 Poste Intune |
| --- | --- | --- |
| 7 | Vérifier si des données locales subsistent sur le poste, y compris hors profil utilisateur | Les données de l'agent résident sur SharePoint ; vérifier néanmoins le cache local |
| 8 | Mettre à jour le fichier Excel SharePoint de suivi | *Sans objet* |
| 9 | Effacer le poste par réinstallation MDT complète | Réinitialiser le poste depuis la console, en conservant l'inscription |
| 10 | Le poste réinstallé retourne en **zone à préparer** — il reste un poste legacy | Le poste réinitialisé retourne en **zone prêt à doter** |
| 11 | *Si le poste est éligible : étudier son enrôlement Intune plutôt que sa réinstallation MDT* | *Sans objet* |

## Étape finale commune

| # | Action | Qui |
| --- | --- | --- |
| 12 | À l'issue de la période de conservation : remise en stock, ou déclenchement de PROC-STOCK-H04 | Agent atelier |

## Points de contrôle RGPD

Identiques dans les deux cas :

- Le matériel retourné reste physiquement séparé du stock neuf jusqu'à effacement.
- La durée de conservation avant effacement est régie par la politique d'archivage de la DSI. **Cette politique reste à établir** — écart de priorité 1.
- L'effacement est tracé dans le ticket : date, agent, appareil, méthode employée.

| 🟠 Poste MDT | 🔵 Poste Intune |
| --- | --- |
| L'effacement repose sur la réinstallation complète : vérifier qu'elle a bien abouti avant remise en stock | La réinitialisation est tracée dans la console ; en conserver la référence au ticket |

## Point de vigilance propre à la période

**L'étape 11 est une opportunité, pas une obligation.** Un poste legacy qui revient est un candidat naturel à la migration : le réinstaller sous MDT prolonge la dette d'une génération de dotation. Si le matériel est éligible, l'orienter vers l'enrôlement fait avancer la migration sans effort supplémentaire.

## Procédures liées

- PROC-STOCK-H04 — Réforme et destruction des données
- PROC-INT-H03 — Retrait et désinscription d'un appareil
- PROC-ID-H01 — Cycle de vie d'un compte d'agent
