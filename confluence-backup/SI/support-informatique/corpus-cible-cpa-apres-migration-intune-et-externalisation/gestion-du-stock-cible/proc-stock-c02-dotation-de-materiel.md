<!-- confluence: SI / page 1703998 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/1703998 -->
<!-- parent_id: 1703958 · parent: 📦 Gestion du stock — cible -->

# PROC-STOCK-C02 — Dotation de matériel

|  |  |
| --- | --- |
| **Code** | PROC-STOCK-C02 |
| **Domaine** | Gestion du stock |
| **Statut** | Cible à valider |
| **Criticité** | Haute |
| **Contrainte RGPD** | Non |
| **Outils** | Tauturu, console Intune |
| **SLA cible** | 7 jours ouvrés |

> **Règle invariante CPA** — Toute dotation, intervention ou action manuelle sur le parc fait l'objet d'un ticket Tauturu.

## Objet

Attribuer un équipement informatique à un agent ou à un service, à partir d'une demande validée, en garantissant la traçabilité dans Tauturu et la cohérence avec le compte de l'agent.

Le poste arrivant enrôlé d'usine, la dotation ne comporte plus de phase de préparation technique.

## Déclencheur

Ticket de demande de dotation créé dans Tauturu **par le demandeur de matériel**, à l'arrivée d'un agent ou pour un remplacement.

## Acteurs

| Rôle | Responsabilité |
| --- | --- |
| Demandeur du service | Crée le ticket de dotation |
| Valideur hiérarchique | Valide la demande |
| Responsable de cellule | Arbitre les dotations hors standard |
| Agent CPA | Attribue le matériel, met à jour Tauturu et Intune |
| Agent de proximité terrain | Livre et installe |

## Étapes

| # | Action | Qui | Résultat attendu |
| --- | --- | --- | --- |
| 1 | Vérifier la demande : valideur identifié, justification, service | Agent CPA | Demande recevable |
| 2 | Vérifier la conformité à la politique de gestion du parc et à la charte informatique | Agent CPA | Éligibilité confirmée |
| 3 | **Contrôler l'existence du compte de l'agent bénéficiaire dans EntraID** | Agent CPA | Compte présent, ou cas traité à l'étape 4 |
| 4 | Si le compte est absent : clôturer le ticket, ou le mettre en attente du compte selon que l'arrivée est confirmée ou non | Agent CPA | Décision tracée dans le ticket |
| 5 | Vérifier la disponibilité du stock | Agent CPA | Matériel identifié |
| 6 | Attribuer l'appareil au bénéficiaire dans Tauturu — statut « En fonction » | Agent CPA | Inventaire à jour |
| 7 | Vérifier l'affectation du profil de déploiement dans la console Intune | Agent CPA | Poste rattaché au bon profil |
| 8 | Organiser la remise : retrait à la DSI, ou intervention terrain | Agent de proximité | Remise planifiée |
| 9 | Remettre le poste et accompagner le premier démarrage en présence du bénéficiaire | Agent de proximité | Session utilisateur active |
| 10 | Mettre à jour et clôturer le ticket | Agent CPA | Traçabilité complète |

## Points de vigilance

- **La présence du bénéficiaire est requise au premier démarrage** : c'est lui qui ouvre la session et déclenche l'application des profils.
- Le compte naît du contrat via IdentityDSI, la dotation naît du ticket. Les deux peuvent arriver dans le désordre — d'où le contrôle de l'étape 3.
- Une dotation VIP est traitée en priorité absolue, au même titre qu'une urgence.
- Pour les îles, le matériel est acheminé par transporteur : voir PROC-TER-C04.
- La règle de non-double-dotation issue de la charte informatique reste applicable.

## Procédures liées

- PROC-STOCK-C01 — Réception et injection du matériel
- PROC-TER-C02 — Dotation sur site
- PROC-INT-C01 — Attribution d'un appareil enrôlé
- PROC-ID-C01 — Vérification et suivi des comptes provisionnés
