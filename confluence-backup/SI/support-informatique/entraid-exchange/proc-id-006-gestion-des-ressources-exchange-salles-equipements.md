<!-- confluence: SI / page 98533 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/98533 -->
<!-- parent_id: 65942 · parent: 👤 EntraID / Exchange -->

# PROC-ID-006 — Gestion des ressources Exchange (salles, équipements)

| Code | `PROC-ID-006` |
| --- | --- |
| Domaine | EntraID / Exchange |
| --- | --- |
| Rôles concernés | Gestionnaire de comptes (ingénieur) |
| --- | --- |
| Déclencheur | Ticket créé par un valideur pour une nouvelle salle ou ressource à réserver |
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
| Criticité | Faible |
| --- | --- |
| Contrainte RGPD | Non |
| --- | --- |

**Règle invariante CPA :** Toute action doit être tracée par un ticket Tauturu (GLPI). Pas de ticket = pas d'action.

## 🎯 Objet

Créer et gérer les ressources Exchange (salles de réunion, véhicules, équipements) permettant la réservation via le calendrier.

## ⚡ Déclencheur

Ticket créé par un valideur pour une nouvelle salle ou ressource à réserver

## 👤 Acteurs

| Rôle | Responsabilité dans cette procédure |
| --- | --- |
| Gestionnaire de comptes (ingénieur) | Crée et configure la ressource Exchange |

## 📋 Étapes

| # | Action | Qui | Outil | Résultat attendu |
| --- | --- | --- | --- | --- |
| 1 | Vérifier le ticket : type de ressource (salle/équipement), service, propriétaire | Gestionnaire de comptes (ingénieur) | Tauturu (GLPI) | Ticket validé |
| 2 | Créer la ressource dans Exchange (Centre admin > Ressources) | Gestionnaire de comptes (ingénieur) | Centre d'admin EntraID / Exchange | Ressource créée |
| 3 | Configurer les paramètres de réservation (auto-acceptation, capacité, horaires) | Gestionnaire de comptes (ingénieur) | Centre d'admin EntraID / Exchange | Ressource configurée |
| 4 | Informer le propriétaire et clôturer le ticket | Gestionnaire de comptes (ingénieur) | Tauturu (GLPI) | Ticket clôturé |

## ⚠️ Points de vigilance

* La suppression d'une ressource suit la même procédure que la suppression d'une BALP
* Documenter le propriétaire de chaque ressource pour les audits annuels

## 🔗 Procédures liées

* PROC-ID-005 — BALP

## 📝 Historique des modifications

| Date | Version | Auteur | Nature de la modification |
| --- | --- | --- | --- |
| 2026-03-15 | 1.0 | Chef CPA | Création initiale — projet de formalisation documentaire |
