<!-- confluence: SI / page 1736786 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/1736786 -->
<!-- parent_id: 1736726 · parent: 👤 EntraID / Exchange — cible -->

# PROC-ID-C04 — Déblocage et réinitialisation MFA

|  |  |
| --- | --- |
| **Code** | PROC-ID-C04 |
| **Domaine** | EntraID / Exchange |
| **Statut** | Cible à valider |
| **Criticité** | Moyenne |
| **Contrainte RGPD** | **Oui** |
| **Outils** | EntraID, Tauturu |

> **Règle invariante CPA** — Toute dotation, intervention ou action manuelle sur le parc fait l'objet d'un ticket Tauturu.

## Objet

Rétablir l'accès d'un agent à son compte après un blocage, ou réinitialiser sa méthode d'authentification multifacteur.

## Déclencheur

Appel ou ticket d'un agent ne pouvant plus s'authentifier : téléphone changé, perdu, application d'authentification réinstallée.

## Étapes

| # | Action | Qui | Résultat attendu |
| --- | --- | --- | --- |
| 1 | Créer ou reprendre le ticket | Agent CPA | Demande tracée |
| 2 | **Vérifier l'identité de l'agent par un moyen indépendant du compte bloqué** | Agent CPA | Identité établie |
| 3 | Consulter l'état du compte et la cause du blocage dans EntraID | Agent CPA | Cause identifiée |
| 4 | Si le blocage résulte d'une détection de risque, orienter vers la Cellule Sécurité Opérationnelle avant toute action | Agent CPA | Incident qualifié |
| 5 | Réinitialiser la méthode d'authentification | Agent CPA | Méthode effacée |
| 6 | Accompagner l'agent dans le réenregistrement de sa méthode | Agent CPA | Agent de nouveau autonome |
| 7 | Documenter et clôturer le ticket | Agent CPA | Traçabilité assurée |

## Points de contrôle RGPD et sécurité

- **L'étape 2 est la seule protection réelle de la procédure.** Réinitialiser l'authentification d'un compte sur simple demande téléphonique, sans vérification indépendante, c'est offrir un accès complet aux données de l'agent à qui se présente en son nom. La vérification ne passe jamais par le compte bloqué lui-même.
- **L'étape 4 n'est pas une formalité.** Un blocage consécutif à une détection de risque peut signaler une tentative d'accès illégitime : réinitialiser sans qualification revient à débloquer l'attaquant.
- Toute réinitialisation est tracée : date, agent demandeur, agent intervenant, moyen de vérification employé.

## Points de vigilance

- Un agent en déplacement ou aux îles ne peut pas se présenter physiquement : le moyen de vérification doit être prévu à l'avance, et non improvisé au moment de l'appel.
- Une multiplication des demandes de réinitialisation sur un même compte est un signal : elle se signale à la Cellule Sécurité Opérationnelle.

## Procédures liées

- PROC-ID-C01 — Vérification et suivi des comptes provisionnés
- PROC-TER-C04 — Télé-assistance et interventions aux îles
