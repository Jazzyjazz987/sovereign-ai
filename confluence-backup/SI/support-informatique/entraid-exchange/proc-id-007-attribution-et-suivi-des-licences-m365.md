<!-- confluence: SI / page 98550 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/98550 -->
<!-- parent_id: 65942 · parent: 👤 EntraID / Exchange -->

# PROC-ID-007 — Attribution et suivi des licences M365

| Code | `PROC-ID-007` |
| --- | --- |
| Domaine | EntraID / Exchange |
| --- | --- |
| Rôles concernés | Gestionnaire de comptes (ingénieur) + Chef de cellule CPA |
| --- | --- |
| Déclencheur | Création compte, demande de changement de licence, ou revue mensuelle |
| --- | --- |
| Outil(s) | Centre d'admin EntraID / Exchange + Tauturu (GLPI) + PowerShell |
| --- | --- |
| SLA cible | Attribution : lors de la création compte \| Revue : mensuelle |
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
| Contrainte RGPD | Non |
| --- | --- |

**Règle invariante CPA :** Toute action doit être tracée par un ticket Tauturu (GLPI). Pas de ticket = pas d'action.

## 🎯 Objet

Gérer l'attribution des licences Microsoft 365 (F3, E1, E3) et assurer un suivi mensuel pour optimiser les coûts et éviter les dépassements.

## ⚡ Déclencheur

Création compte, demande de changement de licence, ou revue mensuelle

## 👤 Acteurs

| Rôle | Responsabilité dans cette procédure |
| --- | --- |
| Gestionnaire de comptes (ingénieur) | Attribue et modifie les licences |
| Chef de cellule CPA | Pilote la revue mensuelle et le tableau de bord licences |

## 📋 Étapes

| # | Action | Qui | Outil | Résultat attendu |
| --- | --- | --- | --- | --- |
| 1 | Attribution par défaut : licence F3 attribuée automatiquement à la création du compte | Gestionnaire de comptes (ingénieur) | Centre d'admin EntraID / Exchange | Licence F3 active |
| 2 | Demande de changement (E1 ou E3) : vérifier le ticket et le droit (E3 = ministères uniquement) | Gestionnaire de comptes (ingénieur) | Tauturu (GLPI) | Demande validée |
| 3 | Modifier la licence dans le centre d'administration M365 | Gestionnaire de comptes (ingénieur) | Centre d'admin EntraID / Exchange | Licence modifiée |
| 4 | Revue mensuelle : extraire le tableau de bord licences via PowerShell (F3/E1/E3 utilisées, disponibles, sur comptes désactivés) | Chef de cellule CPA | PowerShell / Power BI | Tableau de bord disponible |
| 5 | Libérer les licences sur les comptes désactivés identifiés lors de la revue | Gestionnaire de comptes (ingénieur) | Centre d'admin EntraID / Exchange | Licences optimisées |
| 6 | Documenter dans le ticket Tauturu | Gestionnaire de comptes (ingénieur) | Tauturu (GLPI) | Traçabilité |

## ⚠️ Points de vigilance

* CRITIQUE P1 : Il n'existe actuellement AUCUN suivi des licences M365 — créer le tableau de bord PowerShell/Power BI en priorité
* Les licences sur comptes désactivés représentent un surcoût direct — les détecter et libérer mensuellement
* Alerte à configurer : 80% et 90% de saturation du pool de licences
* Licence E3 : réservée aux ministères — ne pas déroger sans validation chef CPA

## 🔗 Procédures liées

* PROC-ID-001 — Création compte
* PROC-ID-003 — Désactivation compte

## 📝 Historique des modifications

| Date | Version | Auteur | Nature de la modification |
| --- | --- | --- | --- |
| 2026-03-15 | 1.0 | Chef CPA | Création initiale — projet de formalisation documentaire |
