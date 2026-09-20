<!-- confluence: SI / page 1737027 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/1737027 -->
<!-- parent_id: 1802396 · parent: 👤 EntraID / Exchange — hybride -->

# PROC-ID-H03 — Déblocage MFA et gestion des licences

| Champ | Valeur |
| --- | --- |
| **Code** | PROC-ID-H03 |
| **Domaine** | EntraID / Exchange — hybride |
| **Statut** | Hybride — applicable pendant la migration |
| **Discriminant** | Service de rattachement de l'agent : 🟠 hors IdentityDSI / 🔵 raccordé à IdentityDSI |
| **Criticité** | Haute |
| **Outils** | Tauturu (GLPI), IdentityDSI, console EntraID, Exchange Online |

> **Règle invariante.** Un déblocage d'authentification multifacteur n'est réalisé qu'après vérification de l'identité de l'agent par un canal distinct de celui de la demande. Aucune exception, quelle que soit l'urgence invoquée ou la colonne applicable.

> **Attention — le discriminant n'est pas le poste.** Les deux colonnes distinguent l'avant et l'après mise en service d'IdentityDSI pour le service de l'agent. Le déblocage MFA lui-même est identique dans les deux colonnes : c'est la gestion des licences qui diffère.

## 1 — Objet

Cette procédure traite deux demandes courantes du domaine identité :

- le déblocage ou la réinitialisation de l'authentification multifacteur d'un agent ;
- l'attribution, le changement et la libération des licences.

## 2 — Déterminer l'état du service

1. Identifier le service de rattachement de l'agent.
2. Consulter la liste des services raccordés à IdentityDSI.
3. Service raccordé : colonne 🔵. Service non raccordé : colonne 🟠.

Ce chapitre ne concerne que la partie licences. Le déblocage MFA suit le chapitre 3, commun aux deux colonnes.

## 3 — Déblocage MFA — commun aux deux colonnes

| # | Action |
| --- | --- |
| 1 | Recevoir la demande dans Tauturu. Une demande arrivée par un autre canal est d'abord transformée en ticket. |
| 2 | Vérifier l'identité de l'agent par un canal distinct : rappel sur la ligne du service, confirmation du responsable hiérarchique, ou identification en présence. |
| 3 | Vérifier que le compte de l'agent est actif et qu'aucune procédure de départ n'est en cours. |
| 4 | Consulter les journaux de connexion pour écarter une tentative d'usurpation. |
| 5 | Réinitialiser les méthodes d'authentification de l'agent depuis la console. |
| 6 | Demander à l'agent de réinscrire immédiatement une méthode d'authentification. |
| 7 | Contrôler la réinscription effective avant de clore. |
| 8 | Consigner dans le ticket le canal de vérification d'identité utilisé, puis clore. |

> Le motif du blocage est consigné. Un agent débloqué plusieurs fois dans une même période signale un besoin d'accompagnement ou un incident de sécurité.

## 4 — Gestion des licences

| # | 🟠 Service hors IdentityDSI | 🔵 Service raccordé à IdentityDSI |
| --- | --- | --- |
| 1 | Recevoir le ticket de demande ou de changement de licence. | Recevoir le ticket, ou constater le changement provisionné depuis le SIRH. |
| 2 | Vérifier que le profil demandé correspond à la fonction de l'agent. | Vérifier la fonction remontée du SIRH, qui détermine l'appartenance au groupe. |
| 3 | Affecter ou retirer la licence manuellement sur le compte. | Ajuster l'appartenance de l'agent au groupe dynamique, jamais la licence directement. |
| 4 | Vérifier le stock de licences disponibles avant affectation. | Vérifier le stock de licences disponibles avant tout élargissement de groupe. |
| 5 | Libérer explicitement la licence au départ ou à la mutation de l'agent. | Vérifier que la sortie du groupe a bien libéré la licence. |
| 6 | Tenir à jour le suivi manuel des licences affectées. | Contrôler l'écart entre le nombre de licences consommées et l'effectif provisionné. |

## 5 — Étapes finales communes

| # | Action |
| --- | --- |
| 1 | Vérifier l'effet réel de l'action : connexion possible pour un déblocage, service accessible pour une licence. |
| 2 | Informer l'agent ou le service demandeur. |
| 3 | Consigner l'action et la colonne appliquée dans le ticket, puis clore. |

## 6 — Points de vigilance

Points valables dans les deux cas :

- Une demande de déblocage MFA est un vecteur d'attaque connu. La vérification d'identité n'est jamais allégée, y compris pour un membre de la direction.
- Une licence libérée au départ d'un agent et non réaffectée est un coût inutile. Le suivi du stock est mensuel.
- Le déblocage MFA ne donne aucun droit supplémentaire. Toute demande d'élévation de droits présentée comme un déblocage est refusée et signalée.

| 🟠 Service hors IdentityDSI | 🔵 Service raccordé à IdentityDSI |
| --- | --- |
| L'absence de suivi automatique fait dériver le nombre de licences consommées. Le rapprochement avec l'effectif est manuel. | Une licence affectée directement sur un compte, hors groupe dynamique, sera retirée au prochain cycle. Passer par le groupe. |
| Le retrait de licence doit être explicite. Il est oublié dans la majorité des départs non tracés. | Un écart entre licences consommées et effectif provisionné signale un groupe dynamique mal défini. Le traiter à la source. |

## 7 — Procédures liées

- PROC-ID-H01 — Cycle de vie d'un compte d'agent
- PROC-ID-H02 — Comptes hors SIRH, boîtes partagées et ressources
