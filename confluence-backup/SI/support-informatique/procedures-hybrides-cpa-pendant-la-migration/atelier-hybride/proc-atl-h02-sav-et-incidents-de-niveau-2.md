<!-- confluence: SI / page 1736927 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/1736927 -->
<!-- parent_id: 1736826 · parent: 🔧 Atelier — hybride -->

# PROC-ATL-H02 — SAV et incidents de niveau 2

|  |  |
| --- | --- |
| **Code** | PROC-ATL-H02 |
| **Domaine** | Atelier |
| **Statut** | En vigueur pendant la migration |
| **Discriminant** | État du poste en panne |
| **Criticité** | Moyenne |
| **SLA cible** | 3 jours ouvrés |

> **Règle invariante CPA** — Toute dotation, intervention ou action manuelle sur le parc fait l'objet d'un ticket Tauturu.

## Objet

Traiter les incidents nécessitant une intervention physique en atelier, après échec de la résolution à distance.

## Étapes communes

| # | Action | Qui |
| --- | --- | --- |
| 1 | Prendre en charge le ticket et prendre connaissance du diagnostic de niveau 1 | Agent atelier |
| 2 | Réceptionner le matériel au guichet | Agent atelier |
| 3 | Reproduire l'incident | Agent atelier |

## Étapes propres à l'état du poste

| # | 🟠 Poste MDT | 🔵 Poste Intune |
| --- | --- | --- |
| 4 | Diagnostiquer localement : journaux système, état des applications, pilotes | Consulter d'abord l'état de conformité et l'historique de déploiement dans la console |
| 5 | Vérifier la couverture de garantie dans Tauturu | Vérifier la couverture de garantie dans Tauturu |
| 6 | Si sous garantie : engager l'échange standard | Si sous garantie : engager l'échange standard |
| 7 | Sinon : réinstallation MDT complète, remplacement de composant, ou reconfiguration | Sinon : réinitialisation depuis la console, remplacement de composant, ou redéploiement d'application |
| 8 | Après réinstallation, reconfigurer manuellement applications, imprimantes et accès | Après réinitialisation, les profils se réappliquent automatiquement |
| 9 | Si le poste est éligible, proposer son enrôlement plutôt qu'une réinstallation MDT | *Sans objet* |

## Étapes finales communes

| # | Action | Qui |
| --- | --- | --- |
| 10 | Si irréparable : escalader au responsable de cellule pour décision de réforme | Agent atelier |
| 11 | Tester le fonctionnement après intervention | Agent atelier |
| 12 | Restituer le matériel, documenter et clôturer le ticket | Agent atelier |

## Points de vigilance

**Communs**

- Le parc étant progressivement placé sous garantie constructeur, vérifier la couverture **avant** toute intervention : ouvrir un poste sous garantie peut en faire perdre le bénéfice.
- Les pièces de rechange ne sont pas stockées : anticiper les délais et informer le bénéficiaire.
- Toute décision de réforme déclenche PROC-STOCK-H04.

| 🟠 Poste MDT | 🔵 Poste Intune |
| --- | --- |
| Le diagnostic repose entièrement sur l'examen local : aucun historique centralisé n'est disponible | La console donne l'historique des déploiements et des écarts de conformité : commencer par là fait gagner du temps |
| Une réinstallation coûte environ 2 h, plus la reconfiguration : l'arbitrage réparation / remplacement en tient compte | Une réinitialisation coûte quelques minutes : elle devient une option de diagnostic, pas un dernier recours |
| Un incident applicatif se traite poste par poste | Un incident applicatif peut concerner tout un groupe de déploiement : vérifier s'il est isolé avant d'intervenir sur le poste |

**Le même symptôme n'a pas la même cause selon la colonne.** Une application manquante sur un poste MDT est un défaut d'installation ; sur un poste Intune, c'est un problème de ciblage qui affecte probablement d'autres postes. Traiter le second comme le premier revient à corriger un cas et à laisser le reste du groupe en panne.

## Procédures liées

- PROC-TER-H04 — Télé-assistance et interventions aux îles
- PROC-STOCK-H04 — Réforme et destruction des données
- PROC-INT-H02 — Packaging et déploiement d'une application
