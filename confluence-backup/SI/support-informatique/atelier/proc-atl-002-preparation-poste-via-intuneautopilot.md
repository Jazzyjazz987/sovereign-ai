<!-- confluence: SI / page 131226 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/131226 -->
<!-- parent_id: 98329 · parent: 🔧 Atelier -->

# PROC-ATL-002 — Préparation poste via Intune/Autopilot

| Code | `PROC-ATL-002` |
| --- | --- |
| Domaine | Atelier |
| --- | --- |
| Rôles concernés | Agent atelier + Gestionnaire de comptes (ingénieur) |
| --- | --- |
| Déclencheur | Dotation d'un poste Windows 11 compatible TPM 2.0 |
| --- | --- |
| Outil(s) | Console Intune (endpoint.microsoft.com), Tauturu (GLPI) |
| --- | --- |
| SLA cible | \~30 min (préprovisionnement simple) ou \~2h (avec reseal) |
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

Préparer un poste Windows 11 via Microsoft Intune et Windows Autopilot, technologie cible de déploiement pour le parc 2026.

## ⚡ Déclencheur

Dotation d'un poste Windows 11 compatible TPM 2.0

## 👤 Acteurs

| Rôle | Responsabilité dans cette procédure |
| --- | --- |
| Agent atelier | Exécute l'enrôlement Autopilot et le préprovisionnement |
| Gestionnaire de comptes (ingénieur) | Maintient la configuration Intune et les profils Autopilot |

## 📋 Étapes

| # | Action | Qui | Outil | Résultat attendu |
| --- | --- | --- | --- | --- |
| 1 | Vérifier la compatibilité du poste : Windows 11, TPM 2.0 | Agent atelier | Poste physique | Compatibilité confirmée |
| 2 | Extraire le hash matériel (hardware hash) du poste | Agent atelier | PowerShell / Script extraction hash | Hash matériel disponible |
| 3 | Enregistrer le hash dans la console Intune (Appareils > Enrôlement Windows > Appareils) | Agent atelier | Console Intune (endpoint.microsoft.com) | Appareil enregistré dans Intune |
| 4 | Attribuer le tag de groupe de déploiement approprié | Agent atelier | Console Intune (endpoint.microsoft.com) | Poste affecté au bon profil Autopilot |
| 5 | Lancer le préprovisionnement avec le compte DEM (Device Enrollment Manager) | Agent atelier | Console Intune (endpoint.microsoft.com) + Connexion réseau DSI ou Internet | Préprovisionnement en cours |
| 6 | Si reseal nécessaire : réinitialisation OOBE puis retour à l'expérience Autopilot (selon performance réseau service destinataire) | Agent atelier | Poste + Intune | Poste en état OOBE Autopilot |
| 7 | Contrôle qualité : vérifier profils Intune appliqués, Harfanglab EDR, BitLocker, LAPS | Agent atelier | Console Intune (endpoint.microsoft.com) | Poste conforme aux politiques |
| 8 | Mettre à jour le statut GLPI et le ticket de dotation | Agent atelier | Tauturu (GLPI) | Traçabilité complète |

## ⚠️ Points de vigilance

* La connexion Internet est obligatoire pour le préprovisionnement Autopilot — vérifier disponibilité réseau
* Le choix entre préprovisionnement simple et reseal dépend de la qualité réseau du service destinataire
* Technologie cible 2026 : 100% des 2 200 nouveaux postes seront pré-provisionnés (hash enregistré avant livraison)
* Post-migration Intune : MDT sera éteint — former tous les agents à cette procédure en priorité

## 🔗 Procédures liées

* PROC-ATL-001 — Préparation poste MDT
* PROC-INT-001 — Enrôlement Autopilot Windows 11

## 📝 Historique des modifications

| Date | Version | Auteur | Nature de la modification |
| --- | --- | --- | --- |
| 2026-03-15 | 1.0 | Chef CPA | Création initiale — projet de formalisation documentaire |
