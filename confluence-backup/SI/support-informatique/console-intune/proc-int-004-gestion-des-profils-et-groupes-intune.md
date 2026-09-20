<!-- confluence: SI / page 66089 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/66089 -->
<!-- parent_id: 98345 · parent: 🖥️ Console Intune -->

# PROC-INT-004 — Gestion des profils et groupes Intune

| Code | `PROC-INT-004` |
| --- | --- |
| Domaine | Console Intune |
| --- | --- |
| Rôles concernés | Gestionnaire de comptes (ingénieur) + Chef de cellule CPA |
| --- | --- |
| Déclencheur | Nouveau service, nouveau type de poste, modification de politique de sécurité |
| --- | --- |
| Outil(s) | Console Intune (endpoint.microsoft.com) + Tauturu (GLPI) |
| --- | --- |
| SLA cible | Dans les 3 jours ouvrés |
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

Créer et maintenir les groupes de déploiement et profils de configuration Intune pour garantir l'application des politiques de sécurité sur le parc.

## ⚡ Déclencheur

Nouveau service, nouveau type de poste, modification de politique de sécurité

## 👤 Acteurs

| Rôle | Responsabilité dans cette procédure |
| --- | --- |
| Gestionnaire de comptes (ingénieur) | Crée et modifie les groupes et profils |
| Chef de cellule CPA | Valide toute modification de politique de sécurité (rôle audit) |

## 📋 Étapes

| # | Action | Qui | Outil | Résultat attendu |
| --- | --- | --- | --- | --- |
| 1 | Identifier le besoin (nouveau service, nouveau type d'appareil, modification politique) | Gestionnaire de comptes (ingénieur) | Tauturu (GLPI) | Besoin documenté |
| 2 | Créer ou modifier le groupe de déploiement dans Intune (nomenclature DSI) | Gestionnaire de comptes (ingénieur) | Console Intune (endpoint.microsoft.com) | Groupe disponible |
| 3 | Associer le profil de configuration ou la politique de conformité au groupe | Gestionnaire de comptes (ingénieur) | Console Intune (endpoint.microsoft.com) | Politique appliquée |
| 4 | Valider l'application sur un appareil de test | Gestionnaire de comptes (ingénieur) | Console Intune (endpoint.microsoft.com) | Profil validé |
| 5 | Documenter dans le ticket Tauturu | Gestionnaire de comptes (ingénieur) | Tauturu (GLPI) | Traçabilité |

## ⚠️ Points de vigilance

* Le chef CPA dispose d'un rôle audit Intune — toute modification de politique de sécurité doit lui être soumise
* Les politiques de conformité (Harfanglab, Defender, BitLocker, LAPS, Cloudflare Warp ZTNA) sont maintenues en coordination avec SecOps
* La nomenclature des groupes doit respecter les conventions DSI

## 🔗 Procédures liées

* PROC-INT-001 — Enrôlement Autopilot
* PROC-INT-002 — Enrôlement Android
* PROC-INT-006 — SecOps

## 📝 Historique des modifications

| Date | Version | Auteur | Nature de la modification |
| --- | --- | --- | --- |
| 2026-03-15 | 1.0 | Chef CPA | Création initiale — projet de formalisation documentaire |
