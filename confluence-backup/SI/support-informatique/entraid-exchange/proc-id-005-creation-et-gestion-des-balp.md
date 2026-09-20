<!-- confluence: SI / page 98516 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/98516 -->
<!-- parent_id: 65942 · parent: 👤 EntraID / Exchange -->

# PROC-ID-005 — Création et gestion des BALP

| Code | `PROC-ID-005` |
| --- | --- |
| Domaine | EntraID / Exchange |
| --- | --- |
| Rôles concernés | Gestionnaire de comptes (ingénieur) |
| --- | --- |
| Déclencheur | Ticket créé par un valideur de service pour une nouvelle boîte aux lettres partagée |
| --- | --- |
| Outil(s) | Centre d'admin EntraID / Exchange + Tauturu (GLPI) |
| --- | --- |
| SLA cible | Création dans les 48h |
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

Créer et gérer les boîtes aux lettres partagées (BALP) permettant la gestion collaborative des courriels sans compte utilisateur dédié.

## ⚡ Déclencheur

Ticket créé par un valideur de service pour une nouvelle boîte aux lettres partagée

## 👤 Acteurs

| Rôle | Responsabilité dans cette procédure |
| --- | --- |
| Gestionnaire de comptes (ingénieur) | Crée la BALP et configure le groupe de sécurité |

## 📋 Étapes

| # | Action | Qui | Outil | Résultat attendu |
| --- | --- | --- | --- | --- |
| 1 | Vérifier le ticket : valideur identifié, nom BALP, service, propriétaire obligatoire | Gestionnaire de comptes (ingénieur) | Tauturu (GLPI) | Ticket validé |
| 2 | Créer la BALP dans Exchange : Centre admin Exchange > Destinataires > Boîtes partagées | Gestionnaire de comptes (ingénieur) | Centre d'admin EntraID / Exchange | BALP créée (balp.service@domaine) |
| 3 | Vérifier la création automatique du groupe de sécurité M365 (nom.service.list@domaine) | Gestionnaire de comptes (ingénieur) | Centre d'admin EntraID / Exchange | Groupe créé avec délégation complète |
| 4 | Définir le propriétaire de la BALP et lui communiquer l'adresse + les instructions de gestion des membres via Outlook | Gestionnaire de comptes (ingénieur) | Tauturu (GLPI) | Propriétaire informé et autonome |
| 5 | Clôturer le ticket | Gestionnaire de comptes (ingénieur) | Tauturu (GLPI) | Ticket clôturé |

## ⚠️ Points de vigilance

* Le propriétaire gère lui-même les membres via Outlook (Accueil > Groupes) — pas besoin de ticket pour ajout/retrait membre
* La modification du nom d'une BALP nécessite suppression + recréation — prévenir le propriétaire
* Pas de limite au nombre de membres d'une BALP

## 🔗 Procédures liées

* PROC-ID-006 — Ressources Exchange
* PROC-ID-007 — Licences M365

## 📝 Historique des modifications

| Date | Version | Auteur | Nature de la modification |
| --- | --- | --- | --- |
| 2026-03-15 | 1.0 | Chef CPA | Création initiale — projet de formalisation documentaire |
