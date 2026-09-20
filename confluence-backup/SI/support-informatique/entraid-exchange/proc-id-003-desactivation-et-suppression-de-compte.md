<!-- confluence: SI / page 131350 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/131350 -->
<!-- parent_id: 65942 · parent: 👤 EntraID / Exchange -->

# PROC-ID-003 — Désactivation et suppression de compte

| Code | `PROC-ID-003` |
| --- | --- |
| Domaine | EntraID / Exchange |
| --- | --- |
| Rôles concernés | Gestionnaire de comptes (ingénieur) + Chef de cellule CPA |
| --- | --- |
| Déclencheur | Ticket de suppression créé par un valideur (départ, mutation, fin de contrat) |
| --- | --- |
| Outil(s) | Centre d'admin EntraID / Exchange + Tauturu (GLPI) |
| --- | --- |
| SLA cible | Désactivation dans les 24h du ticket |
| --- | --- |
| Version | 1.0 |
| --- | --- |
| Date de création | 2026-03-15 |
| --- | --- |
| Dernière MAJ | 2026-03-15 |
| --- | --- |
| Statut | Actif |
| --- | --- |
| Criticité | Haute |
| --- | --- |
| Contrainte RGPD | Oui |
| --- | --- |

**Règle invariante CPA :** Toute action doit être tracée par un ticket Tauturu (GLPI). Pas de ticket = pas d'action.

## 🎯 Objet

Désactiver et supprimer proprement un compte utilisateur d'EntraID et Exchange, en respectant les délais de rétention RGPD.

## ⚡ Déclencheur

Ticket de suppression créé par un valideur (départ, mutation, fin de contrat)

## 👤 Acteurs

| Rôle | Responsabilité dans cette procédure |
| --- | --- |
| Gestionnaire de comptes (ingénieur) | Exécute la désactivation et coordonne l'archivage |
| Chef de cellule CPA | Valide les suppressions définitives |

## 📋 Étapes

| # | Action | Qui | Outil | Résultat attendu |
| --- | --- | --- | --- | --- |
| 1 | Vérifier le ticket : valideur identifié, motif de suppression, date effective | Gestionnaire de comptes (ingénieur) | Tauturu (GLPI) | Ticket validé |
| 2 | Désactiver le compte dans LDAP (déplacer vers OU 'Comptes désactivés') | Gestionnaire de comptes (ingénieur) | Console LDAP | Compte LDAP désactivé |
| 3 | Bloquer la connexion dans EntraID et révoquer toutes les sessions actives | Gestionnaire de comptes (ingénieur) | Centre d'admin EntraID / Exchange | Accès bloqué immédiatement |
| 4 | Retirer la licence M365 | Gestionnaire de comptes (ingénieur) | Centre d'admin EntraID / Exchange | Licence libérée |
| 5 | CRITIQUE RGPD : Archiver la boîte aux lettres avant suppression (politique à définir — délai recommandé 6 mois) | Gestionnaire de comptes (ingénieur) | Exchange / M365 Rétention | Données archivées |
| 6 | Supprimer le compte dans EntraID → 1ère corbeille (30 jours de restauration possible) | Gestionnaire de comptes (ingénieur) | Centre d'admin EntraID / Exchange | Compte en corbeille 1 |
| 7 | Documenter dans le ticket toutes les actions et dates | Gestionnaire de comptes (ingénieur) | Tauturu (GLPI) | Traçabilité RGPD |

## ⚠️ Points de vigilance

* CRITIQUE RGPD P1 : Il n'existe actuellement AUCUNE procédure d'archivage des données avant suppression définitive — action immédiate requise
* Deux corbeilles : 1ère (30 jours, restauration possible) → 2ème (30 jours, suppression définitive ensuite)
* Coordonner avec PROC-INT-005 pour le retrait simultané du poste Intune
* Les logs EntraID ne sont jamais consultés — mettre en place un monitoring des suppressions

## 🔴 Points de contrôle RGPD

* Définir et appliquer une politique d'archivage des boîtes aux lettres avant suppression (délai recommandé : 6 mois minimum) — action P1
* Utiliser les stratégies de rétention Microsoft 365 pour automatiser l'archivage
* Tracer la date de suppression et l'identité de l'agent dans le ticket Tauturu
* Référence : RGPD Art. 5 — limitation de la conservation des données personnelles


## 🔗 Procédures liées

* PROC-ID-001 — Création compte
* PROC-INT-005 — Retrait appareil Intune
* PROC-ID-007 — Licences M365

## 📝 Historique des modifications

| Date | Version | Auteur | Nature de la modification |
| --- | --- | --- | --- |
| 2026-03-15 | 1.0 | Chef CPA | Création initiale — projet de formalisation documentaire |
