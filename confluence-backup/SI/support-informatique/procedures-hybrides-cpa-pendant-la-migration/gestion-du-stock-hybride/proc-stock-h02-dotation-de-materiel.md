<!-- confluence: SI / page 1736887 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/1736887 -->
<!-- parent_id: 1736806 · parent: 📦 Gestion du stock — hybride -->

# PROC-STOCK-H02 — Dotation de matériel

|  |  |
| --- | --- |
| **Code** | PROC-STOCK-H02 |
| **Domaine** | Gestion du stock |
| **Statut** | En vigueur pendant la migration |
| **Discriminant** | État du poste attribué |
| **Criticité** | Haute |
| **SLA cible** | 7 jours ouvrés |

> **Règle invariante CPA** — Toute dotation, intervention ou action manuelle sur le parc fait l'objet d'un ticket Tauturu.

## Objet

Attribuer un équipement à un agent ou à un service, à partir d'une demande validée.

## Déclencheur

Ticket de dotation créé dans Tauturu par le demandeur de matériel. Identique dans les deux cas.

## Étapes communes

| # | Action | Qui |
| --- | --- | --- |
| 1 | Vérifier la demande : valideur identifié, justification, service | Agent CPA |
| 2 | Vérifier la conformité à la politique de gestion du parc et à la charte informatique | Agent CPA |
| 3 | Vérifier l'existence du compte du bénéficiaire ; si absent, clôturer le ticket ou le mettre en attente | Agent CPA |
| 4 | Vérifier la disponibilité du stock et choisir le matériel | Agent CPA |

## Étapes propres à l'état du poste

| # | 🟠 Poste MDT | 🔵 Poste Intune |
| --- | --- | --- |
| 5 | Vérifier que le poste a été préparé — voir PROC-ATL-H01 | Vérifier que le poste a été contrôlé conforme — voir PROC-ATL-H01 |
| 6 | Passer le statut Tauturu de « En stock » à « En fonction » et associer le bénéficiaire | Idem, et vérifier l'affectation du profil de déploiement dans la console Intune |
| 7 | Mettre à jour le fichier Excel SharePoint de suivi | *Sans objet — Tauturu est la seule source* |
| 8 | Prévoir un temps d'installation d'environ 45 min sur site : session, profils, imprimantes, accès réseau | Prévoir environ 15 min : ouverture de session et vérification des accès |
| 9 | Vérifier la présence des applications métier après première ouverture de session | Vérifier l'application des profils et l'état de conformité |
| 10 | Reprendre les données depuis les serveurs de fichiers si l'agent en disposait | Vérifier l'accès aux bibliothèques SharePoint |

## Étapes finales communes

| # | Action | Qui |
| --- | --- | --- |
| 11 | Organiser la remise : retrait à la DSI, intervention terrain, ou acheminement vers les îles | Agent de proximité |
| 12 | Remettre le poste en présence du bénéficiaire | Agent de proximité |
| 13 | Mettre à jour et clôturer le ticket | Agent CPA |

## Points de vigilance

**Communs**

- La présence du bénéficiaire est requise au premier démarrage, dans les deux cas.
- Une dotation VIP est traitée en priorité absolue.
- La règle de non-double-dotation issue de la charte informatique reste applicable.

| 🟠 Poste MDT | 🔵 Poste Intune |
| --- | --- |
| Le délai de mise à disposition intègre environ 2 h de préparation en atelier | Aucun délai de préparation : le poste est disponible dès réception |
| La configuration des imprimantes et des accès réseau se fait sur site | Ces éléments sont déployés par la console |
| Le poste n'apparaîtra pas dans la console Intune : ne pas le chercher | Le poste doit y apparaître ; son absence est une anomalie à traiter avant remise |

**Ne jamais annoncer un délai sans avoir vérifié l'état du poste attribué.** Sur un même ticket, selon le matériel affecté, l'écart va de quelques minutes à plus d'une demi-journée de travail. C'est la principale source d'engagement non tenu de la période.

## Procédures liées

- PROC-STOCK-H01 — Réception et enregistrement du matériel
- PROC-ATL-H01 — Préparation ou contrôle d'un poste avant dotation
- PROC-TER-H02 — Dotation sur site
- PROC-ID-H01 — Cycle de vie d'un compte d'agent
