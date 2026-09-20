<!-- confluence: SI / page 1704058 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/1704058 -->
<!-- parent_id: 1802241 · parent: 🖥️ Console Intune — cible -->

# PROC-INT-C05 — Retrait et désinscription d'un appareil

|  |  |
| --- | --- |
| **Code** | PROC-INT-C05 |
| **Domaine** | Console Intune |
| **Statut** | Cible à valider |
| **Criticité** | Haute |
| **Contrainte RGPD** | **Oui** |
| **Outils** | Console Intune, Tauturu |

> **Règle invariante CPA** — Toute dotation, intervention ou action manuelle sur le parc fait l'objet d'un ticket Tauturu.

## Objet

Retirer un appareil de la gestion Intune, avec effacement des données lorsque la situation l'exige.

## Déclencheur

Retour de matériel, réforme, réaffectation, perte ou vol.

## Étapes

| # | Action | Qui | Résultat attendu |
| --- | --- | --- | --- |
| 1 | Identifier l'appareil dans la console et confirmer le ticket de rattachement | Agent CPA | Appareil identifié |
| 2 | Déterminer l'action adaptée selon le cas | Agent CPA | Action choisie |
| 3 | Pour une réaffectation : réinitialiser l'appareil en conservant l'inscription | Agent CPA | Appareil remis à neuf, toujours géré |
| 4 | Pour une réforme : désinscrire l'appareil de la console | Agent CPA | Appareil retiré de la gestion |
| 5 | **Pour une perte ou un vol : déclencher l'effacement à distance et déclarer l'incident à la CSO** | Agent CPA | Données protégées, incident déclaré |
| 6 | **Tracer l'effacement dans le ticket : date, appareil, agent, nature de l'action** | Agent CPA | Opération tracée |
| 7 | Mettre à jour le statut dans Tauturu | Agent CPA | Inventaire cohérent |

## Points de contrôle RGPD

- Tout effacement de données doit être tracé dans le ticket : c'est la preuve que la donnée de l'agent a été traitée conformément.
- **La désinscription seule n'efface pas les données.** Sur un appareil réformé, elle ne dispense pas de la destruction physique des supports prévue par PROC-STOCK-C04.
- Une perte ou un vol est un incident de sécurité : la déclaration à la Cellule Sécurité Opérationnelle est immédiate et ne dépend pas de l'issue de la recherche du matériel.

## Points de vigilance

- Réinitialiser en conservant l'inscription évite de repasser par un enrôlement : c'est l'action normale pour une réaffectation.
- Un appareil désinscrit par erreur devra être réenrôlé manuellement, sans le bénéfice du tag usine.

## Procédures liées

- PROC-STOCK-C03 — Retour de matériel
- PROC-STOCK-C04 — Réforme et destruction des données
- PROC-INT-C02 — Enrôlement et gestion des tablettes Android Enterprise
