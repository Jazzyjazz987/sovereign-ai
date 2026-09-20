<!-- confluence: SI / page 1802478 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/1802478 -->
<!-- parent_id: 1736867 · parent: 🖥️ Console Intune — hybride -->

# PROC-INT-H02 — Packaging et déploiement d'une application

| Champ | Valeur |
| --- | --- |
| **Code** | PROC-INT-H02 |
| **Domaine** | Console Intune — hybride |
| **Statut** | Hybride — applicable pendant la migration |
| **Discriminant** | État du poste destinataire : 🟠 poste MDT / 🔵 poste Intune |
| **Criticité** | Haute |
| **Outils** | Tauturu (GLPI), console Intune, partage de déploiement MDT, dépôt de sources applicatives |

> **Règle invariante.** Une application n'est jamais déployée depuis les deux chaînes en même temps sur un même poste. Le poste appartient à une seule chaîne, et c'est cette chaîne qui porte l'application. Le packaging, lui, est réalisé une seule fois et produit deux formats tant que le parc est mixte.

## 1 — Objet

Cette procédure décrit le packaging d'une application métier et son déploiement, pendant la période où le parc comporte à la fois des postes déployés par MDT et des postes enrôlés dans Intune.

Le packaging est réalisé par la CPA ou par la CSO, selon l'affectation du ticket.

## 2 — Déterminer l'état du poste destinataire

Avant tout déploiement, identifier l'état de chaque poste destinataire :

1. Ouvrir la fiche du poste dans Tauturu.
2. Rechercher le poste dans la console Intune par son numéro de série.
3. Le poste présent dans la console Intune et rattaché à un utilisateur est un poste 🔵. Sinon, le poste est un poste 🟠.

En cas de doute, traiter le poste comme un poste 🟠.

## 3 — Étapes communes — qualification et packaging

| # | Action |
| --- | --- |
| 1 | Recevoir le ticket de demande d'application dans Tauturu et vérifier son affectation : CPA ou CSO. |
| 2 | Vérifier que l'application est homologuée et que la licence couvre le périmètre demandé. |
| 3 | Récupérer les sources auprès de l'éditeur ou du service demandeur, et en vérifier l'intégrité. |
| 4 | Identifier le mode d'installation silencieuse et les paramètres associés. |
| 5 | Recenser les postes destinataires et, pour chacun, appliquer le chapitre 2. |
| 6 | Tant que le parc comporte des postes 🟠, produire **les deux formats de package** à partir des mêmes sources et des mêmes paramètres silencieux. |

## 4 — Étapes propres à l'état du poste

| # | 🟠 Poste MDT | 🔵 Poste Intune |
| --- | --- | --- |
| 1 | Déposer le package sur le partage de déploiement et le référencer dans la séquence de tâches. | Empaqueter l'application au format Win32 et l'importer dans la console Intune. |
| 2 | Renseigner la ligne de commande d'installation silencieuse dans la séquence. | Renseigner les commandes d'installation et de désinstallation silencieuses. |
| 3 | *Sans objet — l'application est portée par l'image ou installée manuellement.* | Définir la règle de détection : présence de fichier, clé de registre ou version du produit. |
| 4 | Rattacher l'application au profil de déploiement correspondant au service demandeur. | Affecter l'application au groupe dynamique ou au groupe de déploiement correspondant. |
| 5 | Tester l'installation sur un poste de l'atelier redéployé depuis le partage. | Tester l'installation sur un poste pilote enrôlé, et vérifier le rapport d'installation dans la console. |
| 6 | Planifier l'installation à distance ou lors du prochain passage de l'agent de proximité. | Laisser le déploiement s'effectuer, puis contrôler l'état d'installation dans la console. |
| 7 | Consigner l'installation dans le ticket, poste par poste. | Consigner le résultat global du déploiement dans le ticket. |

## 5 — Étapes finales communes

| # | Action |
| --- | --- |
| 1 | Vérifier que le logiciel est correctement remonté dans l'inventaire Tauturu. |
| 2 | Documenter le package : version, source, paramètres, date, auteur, format produit. |
| 3 | Informer le service demandeur et clore le ticket. |

## 6 — Points de vigilance

Points valables dans les deux cas :

- Un package testé sur une seule chaîne n'est pas un package validé. Tant que le parc est mixte, les deux formats sont testés.
- Un écart entre les deux formats crée un écart de configuration entre agents d'un même service. Les paramètres doivent être strictement identiques.
- Toute application déployée est inscrite au catalogue applicatif, quelle que soit la chaîne utilisée.

| 🟠 Poste MDT | 🔵 Poste Intune |
| --- | --- |
| Le partage de déploiement est en fin de vie. N'y déposer que les applications réellement nécessaires aux postes restants. | Une règle de détection mal écrite fait réinstaller l'application en boucle. La tester avant affectation. |
| Aucune remontée automatique de l'état d'installation. Le contrôle est manuel, poste par poste. | L'affectation par groupe dynamique peut toucher plus de postes que prévu. Vérifier le périmètre avant validation. |

## 7 — Procédures liées

- PROC-INT-H01 — Enrôlement et attribution d'un appareil
- PROC-INT-H03 — Retrait et désinscription d'un appareil
- PROC-ATL-H01 — Préparation ou contrôle d'un poste avant dotation
- PROC-ATL-H03 — Maintenance de l'image MDT
