<!-- confluence: SI / page 131367 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/131367 -->
<!-- parent_id: 65942 · parent: 👤 EntraID / Exchange -->

# PROC-ID-004 — Déblocage et réinitialisation MFA

| Code | `PROC-ID-004` |
| --- | --- |
| Domaine | EntraID / Exchange |
| --- | --- |
| Rôles concernés | Gestionnaire de comptes (ingénieur) |
| --- | --- |
| Déclencheur | Ticket de déblocage ou appel utilisateur (mot de passe oublié, compte verrouillé) |
| --- | --- |
| Outil(s) | Centre d'admin EntraID / Exchange + Tauturu (GLPI) |
| --- | --- |
| SLA cible | Résolution dans les 2h (urgence pour les VIP) |
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

Débloquer un compte utilisateur verrouillé ou réinitialiser les méthodes MFA configurées dans EntraID.

## ⚡ Déclencheur

Ticket de déblocage ou appel utilisateur (mot de passe oublié, compte verrouillé)

## 👤 Acteurs

| Rôle | Responsabilité dans cette procédure |
| --- | --- |
| Gestionnaire de comptes (ingénieur) | Débloque le compte ou réinitialise le MFA |
| Agent téléassistance | Oriente l'utilisateur vers le self-service MFA en premier recours |

## 📋 Étapes

| # | Action | Qui | Outil | Résultat attendu |
| --- | --- | --- | --- | --- |
| 1 | Vérifier si l'utilisateur peut utiliser le self-service MFA (numéro de téléphone configuré) | Agent téléassistance | Portail self-service M365 | Self-service utilisé si possible |
| 2 | Si self-service impossible : créer un ticket Tauturu de déblocage | Gestionnaire de comptes (ingénieur) | Tauturu (GLPI) | Ticket ouvert |
| 3 | Cas mot de passe oublié : fournir un mot de passe temporaire via le ticket | Gestionnaire de comptes (ingénieur) | Centre d'admin EntraID / Exchange | Mot de passe temporaire communiqué |
| 4 | Cas compte verrouillé : déverrouiller dans EntraID et/ou LDAP | Gestionnaire de comptes (ingénieur) | Centre d'admin EntraID / Exchange | Compte déverrouillé |
| 5 | Cas réinitialisation MFA : supprimer les méthodes MFA dans EntraID, l'utilisateur reconfigure | Gestionnaire de comptes (ingénieur) | Centre d'admin EntraID / Exchange | MFA réinitialisé |
| 6 | Clôturer le ticket | Gestionnaire de comptes (ingénieur) | Tauturu (GLPI) | Ticket clôturé |

## ⚠️ Points de vigilance

* Promouvoir le self-service MFA en premier recours — réduit la charge CPA
* Ne jamais communiquer un mot de passe par téléphone — uniquement via le ticket Tauturu sécurisé
* VIP bloqué = urgence — traitement prioritaire

## 🔗 Procédures liées

* PROC-ID-001 — Création compte

## 📝 Historique des modifications

| Date | Version | Auteur | Nature de la modification |
| --- | --- | --- | --- |
| 2026-03-15 | 1.0 | Chef CPA | Création initiale — projet de formalisation documentaire |
