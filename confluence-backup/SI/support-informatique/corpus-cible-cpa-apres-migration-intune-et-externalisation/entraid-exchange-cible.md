<!-- confluence: SI / page 1736726 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/1736726 -->
<!-- parent_id: 1703937 · parent: 🎯 Corpus cible CPA — après migration Intune et externalisation -->

# EntraID / Exchange — cible

**Statut : cible à valider**

Le domaine change de nature. **La CPA ne crée plus les comptes des agents.** IdentityDSI les provisionne depuis le SIRH de la DRH. La cellule devient gestionnaire des exceptions et des ressources hors contrat.

## Ce qui change

| Avant | Cible |
| --- | --- |
| Création manuelle dans LDAP puis EntraID | Provisionnement automatique par IdentityDSI |
| Deux annuaires non synchronisés, cohérence manuelle | EntraID annuaire unique — LDAP abandonné |
| Création sur ticket | Création sur contrat, sans ticket |
| Suppression au cas par cas | Suppression au départ comme à la mutation, procédure validée par la DPO |

## Le périmètre qui reste à la CPA

Rien de ce qui suit ne passe par IdentityDSI. Ces cas conservent le circuit manuel sur ticket et constituent désormais le cœur du domaine :

- comptes de prestataires externes
- comptes de service et comptes techniques
- boîtes aux lettres partagées
- ressources Exchange — salles et équipements
- groupes de sécurité M365
- déblocages et réinitialisations d'authentification multifacteur

## Procédures du domaine

- **PROC-ID-C01** — Vérification et suivi des comptes provisionnés
- **PROC-ID-C02** — Création d'un compte hors SIRH
- **PROC-ID-C03** — Gestion des boîtes aux lettres partagées et ressources Exchange
- **PROC-ID-C04** — Déblocage et réinitialisation MFA
- **PROC-ID-C05** — Attribution et suivi des licences M365

## Points d'attention

**La mutation efface les données.** Un agent muté voit son compte supprimé puis recréé : boîte aux lettres et OneDrive sont perdus. C'est la règle validée par la DPO. Elle doit être connue des services avant la date de mutation.

**Désynchronisation compte / matériel.** Le compte naît du contrat, la dotation naît du ticket. Les deux peuvent arriver dans le désordre. La procédure de dotation prévoit le contrôle d'existence du compte avant remise du poste.

Deux écarts relevés en audit restent ouverts : l'absence d'audit périodique des comptes inactifs de plus de 90 jours, et l'absence d'inventaire centralisé des boîtes aux lettres partagées.
