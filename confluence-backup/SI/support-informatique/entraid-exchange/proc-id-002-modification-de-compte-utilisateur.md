<!-- confluence: SI / page 98495 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/98495 -->
<!-- parent_id: 65942 · parent: 👤 EntraID / Exchange -->

# PROC-ID-002 — Modification de compte utilisateur

| Code | `PROC-ID-002` |
| --- | --- |
| Domaine | EntraID / Exchange |
| --- | --- |
| Rôles concernés | Gestionnaire de comptes (ingénieur) |
| --- | --- |
| Déclencheur | Ticket de modification créé par un valideur (mutation, changement de fonction, correction) |
| --- | --- |
| Outil(s) | Centre d'admin EntraID / Exchange + Tauturu (GLPI) |
| --- | --- |
| SLA cible | Modification dans les 12h suivant le ticket |
| --- | --- |
| Version | 1.0 |
| --- | --- |
| Date de création | 2026-03-15 |
| --- | --- |
| Dernière MAJ | 2026-03-15 |
| --- | --- |
| Statut | Actif |
| --- | --- |
| Criticité | Moyenne |
| --- | --- |
| Contrainte RGPD | Non |
| --- | --- |

**Règle invariante CPA :** Toute action doit être tracée par un ticket Tauturu (GLPI). Pas de ticket = pas d'action.

## 🎯 Objet

Modifier les attributs d'un compte utilisateur existant dans EntraID et LDAP suite à un changement de situation professionnelle.

## ⚡ Déclencheur

Ticket de modification créé par un valideur (mutation, changement de fonction, correction)

## 👤 Acteurs

| Rôle | Responsabilité dans cette procédure |
| --- | --- |
| Gestionnaire de comptes (ingénieur) | Exécute la modification dans LDAP et EntraID |

## 📋 Étapes

| # | Action | Qui | Outil | Résultat attendu |
| --- | --- | --- | --- | --- |
| 1 | Vérifier le ticket Tauturu et les modifications demandées | Gestionnaire de comptes (ingénieur) | Tauturu (GLPI) | Ticket validé |
| 2 | Modifier les attributs dans LDAP (OU, fonction, service) | Gestionnaire de comptes (ingénieur) | Console LDAP | LDAP mis à jour |
| 3 | Vérifier la synchronisation EntraID et mettre à jour si nécessaire | Gestionnaire de comptes (ingénieur) | Centre d'admin EntraID / Exchange | EntraID cohérent |
| 4 | En cas d'erreur UPN : supprimer et recréer le compte (PROC-ID-003 + PROC-ID-001) | Gestionnaire de comptes (ingénieur) | Centre d'admin EntraID / Exchange | Compte corrigé |
| 5 | Documenter et clôturer le ticket | Gestionnaire de comptes (ingénieur) | Tauturu (GLPI) | Ticket clôturé |

## ⚠️ Points de vigilance

* Toute correction doit passer par un ticket — même les corrections d'erreur
* Le nom patronymique est toujours conservé, même en cas de changement de nom suite à mariage
* Pas d'accents ni de caractères spéciaux dans les UPN

## 🔗 Procédures liées

* PROC-ID-001 — Création compte
* PROC-ID-003 — Désactivation et suppression

## 📝 Historique des modifications

| Date | Version | Auteur | Nature de la modification |
| --- | --- | --- | --- |
| 2026-03-15 | 1.0 | Chef CPA | Création initiale — projet de formalisation documentaire |
