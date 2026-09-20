<!-- confluence: SI / page 98475 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/98475 -->
<!-- parent_id: 98345 · parent: 🖥️ Console Intune -->

# PROC-INT-006 — SecOps — Remontée et traitement des alertes

| Code | `PROC-INT-006` |
| --- | --- |
| Domaine | Console Intune |
| --- | --- |
| Rôles concernés | Chef de cellule CPA + Gestionnaire de comptes (ingénieur) |
| --- | --- |
| Déclencheur | Alerte Harfanglab EDR, Microsoft Defender, ou signal de sécurité Intune |
| --- | --- |
| Outil(s) | Console Intune (endpoint.microsoft.com), Console Harfanglab, Tauturu (GLPI) |
| --- | --- |
| SLA cible | Alerte critique : réponse dans l'heure \| Alerte standard : 4h |
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

Traiter les alertes de sécurité provenant des outils EDR et MDM, en coordination avec SecOps (RSSI/DSI).

## ⚡ Déclencheur

Alerte Harfanglab EDR, Microsoft Defender, ou signal de sécurité Intune

## 👤 Acteurs

| Rôle | Responsabilité dans cette procédure |
| --- | --- |
| Chef de cellule CPA | Rôle audit Intune — reçoit et valide les alertes critiques, remonte au RSSI |
| Gestionnaire de comptes (ingénieur) | Analyse technique et action de remédiation |

## 📋 Étapes

| # | Action | Qui | Outil | Résultat attendu |
| --- | --- | --- | --- | --- |
| 1 | Recevoir l'alerte (Harfanglab EDR, Defender, Intune non-conformité) | Chef de cellule CPA / Gestionnaire de comptes (ingénieur) | Console sécurité | Alerte identifiée |
| 2 | Qualifier la criticité de l'alerte | Gestionnaire de comptes (ingénieur) | Console Harfanglab / Defender | Niveau de criticité défini |
| 3 | Ouvrir un ticket Tauturu de sécurité | Gestionnaire de comptes (ingénieur) | Tauturu (GLPI) | Incident sécurité tracé |
| 4 | En cas d'alerte critique : isoler immédiatement l'appareil via Intune | Gestionnaire de comptes (ingénieur) | Console Intune (endpoint.microsoft.com) | Appareil isolé |
| 5 | Remonter au chef CPA et au RSSI (Directeur DSI) | Chef de cellule CPA | Email / Téléphone | Hiérarchie informée |
| 6 | Réaliser la remédiation après validation du chef CPA | Gestionnaire de comptes (ingénieur) | Intune / Harfanglab | Menace neutralisée |
| 7 | Documenter le post-mortem dans le ticket | Chef de cellule CPA | Tauturu (GLPI) | Retour d'expérience documenté |

## ⚠️ Points de vigilance

* Le chef CPA peut reporter directement au Directeur DSI (RSSI) pour les sujets de sécurité
* Cloudflare Warp ZTNA est actif — toute connexion hors politique doit déclencher une investigation
* Les logs Intune doivent être consultés de manière proactive (mensuelle) — actuellement jamais consultés : à corriger

## 🔗 Procédures liées

* PROC-INT-004 — Gestion profils et groupes
* PROC-INT-005 — Retrait appareil

## 📝 Historique des modifications

| Date | Version | Auteur | Nature de la modification |
| --- | --- | --- | --- |
| 2026-03-15 | 1.0 | Chef CPA | Création initiale — projet de formalisation documentaire |
