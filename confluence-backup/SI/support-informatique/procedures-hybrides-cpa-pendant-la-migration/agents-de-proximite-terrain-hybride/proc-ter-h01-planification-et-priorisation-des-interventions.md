<!-- confluence: SI / page 1802437 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/1802437 -->
<!-- parent_id: 1736847 · parent: 🚗 Agents de proximité terrain — hybride -->

# PROC-TER-H01 — Planification et priorisation des interventions

|  |  |
| --- | --- |
| **Code** | PROC-TER-H01 |
| **Domaine** | Agents de proximité terrain |
| **Statut** | En vigueur pendant la migration |
| **Discriminant** | État des postes concernés par l'intervention |
| **Criticité** | Haute |

> **Règle invariante CPA** — Toute dotation, intervention ou action manuelle sur le parc fait l'objet d'un ticket Tauturu.

## Objet

Organiser et prioriser les interventions quotidiennes.

La matrice de priorité ne change pas. Ce qui change, c'est l'estimation de charge : une même intervention ne coûte pas le même temps selon l'état du poste.

## Matrice de priorité — commune

| Priorité | Périmètre | Traitement |
| --- | --- | --- |
| **VIP** | Présidence, Haut-commissariat, cabinets ministériels et fonctions stratégiques | Prise en charge immédiate |
| **Urgent** | Panne bloquante, service prioritaire, poste unique d'un service | Prise en charge dans la journée |
| **Standard** | Demande courante sans blocage | Planification selon la charge |

## Étapes communes

| # | Action | Qui |
| --- | --- | --- |
| 1 | Consulter la file de tickets en début de journée, au briefing | Agent de proximité |
| 2 | Trier par priorité : VIP, puis Urgent, puis Standard | Agent de proximité |
| 3 | Répartir géographiquement lorsque plusieurs agents sont disponibles | Agent de proximité |
| 4 | En cas d'urgence VIP simultanée, faire prendre le relais par un agent atelier ou le responsable | Responsable de cellule |
| 5 | Mettre à jour les tickets à chaque étape | Agent de proximité |

## Estimation de charge par intervention

| Type d'intervention | 🟠 Poste MDT | 🔵 Poste Intune |
| --- | --- | --- |
| Dotation sur site | ~45 min | ~15 min |
| Dépannage applicatif | Variable, diagnostic local | Souvent résolu à distance sans déplacement |
| Remplacement de poste | Préparation préalable de 2 h à prévoir | Poste disponible immédiatement |
| Réinstallation | 2 h en atelier | Quelques minutes, à distance |

## Points de vigilance

- **Vérifier l'état des postes concernés avant de bâtir la tournée.** Une journée planifiée sur l'hypothèse de postes migrés se transforme en demi-journée de retard si les postes sont legacy. C'est la première cause de dérive de planning de la période.
- Les horaires d'intervention encadrent la planification ; aucune intervention n'est programmée au-delà.
- Un agent sur site peut solliciter la télé-assistance en renfort sans quitter le lieu d'intervention.
- Le briefing quotidien reste le point de coordination central : l'avancement de la migration y est un sujet permanent, puisqu'il conditionne la charge.

| 🟠 Poste MDT | 🔵 Poste Intune |
| --- | --- |
| Prévoir systématiquement une marge : la reconfiguration sur site réserve des surprises | Un incident qui semble isolé peut relever d'un déploiement : vérifier avant de se déplacer |

**Une campagne de migration n'est pas une intervention de support.** Les postes migrés dans le cadre d'une vague planifiée relèvent du projet, pas de la file de tickets courante. Les mélanger fausse la mesure de la charge de support et retarde les demandes des services.

## Procédures liées

- PROC-TER-H02 — Dotation sur site
- PROC-TER-H03 — Dépannage de niveau 1 sur site
- PROC-TER-H04 — Télé-assistance et interventions aux îles
