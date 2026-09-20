<!-- confluence: SI / page 1704098 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/1704098 -->
<!-- parent_id: 1736726 · parent: 👤 EntraID / Exchange — cible -->

# PROC-ID-C02 — Création d'un compte hors SIRH

|  |  |
| --- | --- |
| **Code** | PROC-ID-C02 |
| **Domaine** | EntraID / Exchange |
| **Statut** | Cible à valider |
| **Criticité** | Haute |
| **Contrainte RGPD** | **Oui** |
| **Outils** | EntraID, Tauturu |

> **Règle invariante CPA** — Toute dotation, intervention ou action manuelle sur le parc fait l'objet d'un ticket Tauturu.

## Objet

Créer les comptes qui ne relèvent pas du SIRH et ne sont donc pas provisionnés par IdentityDSI.

Ces cas constituent désormais le cœur de l'activité de la cellule sur le domaine des identités.

## Périmètre

| Type de compte | Particularité |
| --- | --- |
| Prestataire externe | Durée limitée, validation hiérarchique obligatoire |
| Compte de service ou technique | Pas de titulaire personne physique |
| Stagiaire ou vacataire sans contrat au SIRH | Durée limitée |

## Déclencheur

Ticket créé par un valideur, avec justification du besoin et durée demandée.

## Étapes

| # | Action | Qui | Résultat attendu |
| --- | --- | --- | --- |
| 1 | Vérifier la présence du ticket, du valideur et de la justification | Agent CPA | Demande recevable |
| 2 | **Vérifier que le besoin ne relève pas du SIRH** | Agent CPA | Circuit correct confirmé |
| 3 | Vérifier la validation hiérarchique pour un compte de prestataire externe | Agent CPA | Validation obtenue |
| 4 | Créer le compte dans EntraID | Agent CPA | Compte créé |
| 5 | **Renseigner une date d'expiration correspondant à la durée demandée** | Agent CPA | Extinction programmée |
| 6 | Attribuer les groupes et la licence nécessaires, au plus juste | Agent CPA | Droits minimaux appliqués |
| 7 | Transmettre les accès au valideur, jamais directement à un tiers non identifié | Agent CPA | Remise tracée |
| 8 | Documenter et clôturer le ticket | Agent CPA | Traçabilité assurée |

## Points de contrôle RGPD

- Un compte de prestataire donne accès à des données de l'administration. Sa durée est limitée, son périmètre restreint au strict nécessaire, et sa création validée hiérarchiquement.
- **L'étape 5 est la protection principale du dispositif.** Un compte sans date d'expiration survit à la mission qui l'a justifié, et personne ne le remarque : c'est le mécanisme par lequel se constituent les comptes dormants.

## Points de vigilance

- L'étape 2 évite le contournement : un agent sous contrat dont le compte tarde à arriver relève d'un écart de provisionnement, non d'une création manuelle. Créer un compte en doublon crée deux identités pour une personne.
- Les comptes de service n'ont pas de titulaire physique : leur propriétaire fonctionnel doit être nommé dans le ticket, sans quoi personne n'en assume la revue.

## Procédures liées

- PROC-ID-C01 — Vérification et suivi des comptes provisionnés
- PROC-ID-C05 — Attribution et suivi des licences M365
