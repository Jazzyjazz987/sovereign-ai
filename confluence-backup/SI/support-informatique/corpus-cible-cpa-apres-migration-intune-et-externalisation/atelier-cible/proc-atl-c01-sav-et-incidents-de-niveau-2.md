<!-- confluence: SI / page 1802261 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/1802261 -->
<!-- parent_id: 1736705 · parent: 🔧 Atelier — cible -->

# PROC-ATL-C01 — SAV et incidents de niveau 2

|  |  |
| --- | --- |
| **Code** | PROC-ATL-C01 |
| **Domaine** | Atelier |
| **Statut** | Cible à valider |
| **Criticité** | Moyenne |
| **Contrainte RGPD** | Non |
| **Outils** | Tauturu, console Intune, AnyDesk |
| **SLA cible** | 3 jours ouvrés |

> **Règle invariante CPA** — Toute dotation, intervention ou action manuelle sur le parc fait l'objet d'un ticket Tauturu.

## Objet

Traiter les incidents matériels et logiciels nécessitant une intervention physique en atelier, après échec de la résolution à distance.

Le SAV devient l'activité principale de l'atelier : la préparation de poste ayant disparu, c'est désormais le matériel en panne qui justifie le lieu.

## Déclencheur

Ticket Tauturu escaladé depuis la télé-assistance, ou dépôt physique au guichet de l'atelier.

## Acteurs

| Rôle | Responsabilité |
| --- | --- |
| Agent atelier | Diagnostique, répare, décide du traitement de niveau 2 |
| Agent télé-assistance | Escalade avec le diagnostic initial |
| Responsable de cellule | Arbitre entre réparation, échange standard et réforme |

## Étapes

| # | Action | Qui | Résultat attendu |
| --- | --- | --- | --- |
| 1 | Prendre en charge le ticket et prendre connaissance du diagnostic de niveau 1 | Agent atelier | Contexte compris |
| 2 | Réceptionner le matériel au guichet | Agent atelier | Matériel en atelier |
| 3 | Reproduire l'incident et établir le diagnostic | Agent atelier | Cause identifiée |
| 4 | Vérifier la couverture de garantie constructeur dans Tauturu | Agent atelier | Éligibilité établie |
| 5 | Si sous garantie : engager l'échange standard auprès du fournisseur | Agent atelier | Demande d'échange ouverte |
| 6 | Sinon, tenter la résolution : réinitialisation via Intune, remplacement de composant, reconfiguration | Agent atelier | Réparation effectuée |
| 7 | Si irréparable : escalader au responsable de cellule pour décision de réforme | Agent atelier | Décision documentée |
| 8 | Tester le fonctionnement après intervention | Agent atelier | Fonctionnement confirmé |
| 9 | Restituer le matériel, documenter et clôturer le ticket | Agent atelier | Ticket clôturé |

## Points de vigilance

- **Le parc étant intégralement sous garantie constructeur, l'arbitrage réparation / échange standard change de nature.** L'étape 4 précède désormais toute tentative de réparation : intervenir sur un matériel sous garantie peut faire perdre le bénéfice de celle-ci.
- L'agent atelier décide seul du traitement de niveau 2. Il peut solliciter la télé-assistance en renfort de diagnostic.
- Les pièces de rechange ne sont pas stockées : anticiper les délais d'approvisionnement et informer le bénéficiaire.
- Toute décision de réforme déclenche PROC-STOCK-C04, y compris pour un matériel arrivé en panne dès la livraison.

## Procédures liées

- PROC-TER-C04 — Télé-assistance et interventions aux îles
- PROC-STOCK-C04 — Réforme et destruction des données
- PROC-ATL-C02 — Contrôle de conformité du matériel à réception
