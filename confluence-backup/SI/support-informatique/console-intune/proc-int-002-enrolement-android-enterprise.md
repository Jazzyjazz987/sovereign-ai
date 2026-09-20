<!-- confluence: SI / page 229626 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/229626 -->
<!-- parent_id: 98345 · parent: 🖥️ Console Intune -->

# PROC-INT-002 — Enrôlement Android Enterprise

| Code | `PROC-INT-002` |
| --- | --- |
| Domaine | Console Intune |
| --- | --- |
| Rôles concernés | Agent atelier + Gestionnaire de comptes (ingénieur) |
| --- | --- |
| Déclencheur | Nouveau terminal Android à intégrer dans le parc géré |
| --- | --- |
| Outil(s) | Console Intune (endpoint.microsoft.com) + Tauturu (GLPI) |
| --- | --- |
| SLA cible | Dans la journée |
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

Enregistrer et configurer un terminal Android dans Microsoft Intune via le profil Android Enterprise approprié.

## ⚡ Déclencheur

Nouveau terminal Android à intégrer dans le parc géré

## 👤 Acteurs

| Rôle | Responsabilité dans cette procédure |
| --- | --- |
| Agent atelier | Exécute l'enrôlement Android Enterprise |
| Gestionnaire de comptes (ingénieur) | Maintient les profils Android (DAC, SDT, DBS et autres) |

## 📋 Étapes

| # | Action | Qui | Outil | Résultat attendu |
| --- | --- | --- | --- | --- |
| 1 | Identifier le service destinataire et le profil Android applicable | Agent atelier | Console Intune (endpoint.microsoft.com) | Profil identifié |
| 2 | Enrôler le terminal Android via le QR code ou le compte géré | Agent atelier | Terminal + Intune | Terminal enrôlé |
| 3 | Vérifier l'application des politiques et applications du service | Agent atelier | Console Intune (endpoint.microsoft.com) | Configuration appliquée |
| 4 | Documenter dans le ticket Tauturu | Agent atelier | Tauturu (GLPI) | Traçabilité |

## ⚠️ Points de vigilance

* Les profils Android (DAC, SDT, DBS...) sont amenés à évoluer au fur et à mesure que d'autres services s'équipent
* Vérifier systématiquement les applications déployées sur le profil du service destinataire

## 🔗 Procédures liées

* PROC-INT-004 — Gestion profils et groupes Intune

## 📝 Historique des modifications

| Date | Version | Auteur | Nature de la modification |
| --- | --- | --- | --- |
| 2026-03-15 | 1.0 | Chef CPA | Création initiale — projet de formalisation documentaire |
