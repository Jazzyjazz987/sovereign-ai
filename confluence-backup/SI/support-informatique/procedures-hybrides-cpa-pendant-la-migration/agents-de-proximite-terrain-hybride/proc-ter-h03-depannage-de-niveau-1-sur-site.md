<!-- confluence: SI / page 1736967 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/1736967 -->
<!-- parent_id: 1736847 · parent: 🚗 Agents de proximité terrain — hybride -->

# PROC-TER-H03 — Dépannage de niveau 1 sur site

|  |  |
| --- | --- |
| **Code** | PROC-TER-H03 |
| **Domaine** | Agents de proximité terrain |
| **Statut** | En vigueur pendant la migration |
| **Discriminant** | État du poste concerné |
| **Criticité** | Moyenne |

> **Règle invariante CPA** — Toute dotation, intervention ou action manuelle sur le parc fait l'objet d'un ticket Tauturu.

## Objet

Résoudre sur site les incidents ne pouvant être traités à distance, ou décider de leur escalade.

## Étapes communes

| # | Action | Qui |
| --- | --- | --- |
| 1 | Consulter le ticket et le diagnostic initial avant le départ | Agent de proximité |
| 2 | **Identifier l'état du poste concerné** dans la console Intune | Agent de proximité |
| 3 | Se rendre sur site avec le sac d'intervention | Agent de proximité |
| 4 | Reproduire l'incident | Agent de proximité |

## Étapes propres à l'état du poste

| # | 🟠 Poste MDT | 🔵 Poste Intune |
| --- | --- | --- |
| 5 | Diagnostiquer localement : journaux, services, applications | Consulter l'état de conformité et l'historique de déploiement avant tout examen local |
| 6 | *Sans objet* | Vérifier si d'autres postes du même groupe présentent le symptôme : si oui, l'incident est un déploiement, pas un poste |
| 7 | Résoudre sur place : réinstallation d'application, correction de configuration, remplacement de périphérique | Résoudre par la console lorsque c'est possible : redéploiement d'application, réapplication de politique |
| 8 | Si non résolvable : escalader à l'atelier, le poste part en réinstallation | Si non résolvable : réinitialisation depuis la console, souvent sans déplacer le poste |

## Étapes finales communes

| # | Action | Qui |
| --- | --- | --- |
| 9 | Informer le bénéficiaire de la suite donnée | Agent de proximité |
| 10 | Mettre à jour le ticket au retour d'intervention | Agent de proximité |

## Points de vigilance

**Communs**

- Un incident relevant du réseau, de la messagerie ou d'une application métier sort du périmètre de la cellule : l'escalader sans traitement intermédiaire.
- Le filtrage des flux sortants ne relève plus de la cellule depuis l'arrêt du proxy : un accès bloqué s'oriente vers le Bureau de la sécurité.

| 🟠 Poste MDT | 🔵 Poste Intune |
| --- | --- |
| Une correction locale tient jusqu'à la prochaine réinstallation, puis disparaît : le noter au ticket | Une correction locale sera écrasée au prochain cycle de conformité : corriger dans la console, pas sur le poste |
| Le poste n'apparaît pas dans la console : ne pas conclure à un défaut d'enrôlement | Un poste absent de la console alors qu'il devrait y figurer est lui-même un incident à traiter |

**Le réflexe à acquérir pendant la période : regarder la console avant de se déplacer.** Sur un poste Intune, une part importante des incidents se diagnostique et se résout sans quitter le bureau. Se déplacer d'abord, comme sur un poste MDT, c'est dépenser une intervention pour une action de trois minutes.

## Procédures liées

- PROC-ATL-H02 — SAV et incidents de niveau 2
- PROC-TER-H04 — Télé-assistance et interventions aux îles
- PROC-INT-H02 — Packaging et déploiement d'une application
