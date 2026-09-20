<!-- confluence: SI / page 131289 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/131289 -->
<!-- parent_id: 98345 · parent: 🖥️ Console Intune -->

# PROC-INT-001 — Enrôlement Autopilot Windows 11

| Code | `PROC-INT-001` |
| --- | --- |
| Domaine | Console Intune |
| --- | --- |
| Rôles concernés | Agent atelier + Gestionnaire de comptes (ingénieur) |
| --- | --- |
| Déclencheur | Nouveau poste Windows 11 TPM 2.0 à intégrer dans le parc géré |
| --- | --- |
| Outil(s) | Console Intune (endpoint.microsoft.com) + Tauturu (GLPI) |
| --- | --- |
| SLA cible | 30 min à 2h selon mode de provisionnement |
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

Enregistrer et provisionner un poste Windows 11 dans Microsoft Intune via le processus Autopilot, pour un déploiement Zero Touch.

## ⚡ Déclencheur

Nouveau poste Windows 11 TPM 2.0 à intégrer dans le parc géré

## 👤 Acteurs

| Rôle | Responsabilité dans cette procédure |
| --- | --- |
| Agent atelier | Exécute l'enrôlement Autopilot |
| Gestionnaire de comptes (ingénieur) | Maintient la configuration Intune, les profils et groupes |

## 📋 Étapes

| # | Action | Qui | Outil | Résultat attendu |
| --- | --- | --- | --- | --- |
| 1 | Vérifier les prérequis : Windows 11, TPM 2.0, connexion Internet | Agent atelier | Poste physique | Prérequis validés |
| 2 | Extraire le hardware hash via script PowerShell | Agent atelier | PowerShell | Hash disponible |
| 3 | Importer le hash dans Intune : Appareils > Enrôlement Windows > Appareils > Importer | Agent atelier | Console Intune (endpoint.microsoft.com) | Appareil enregistré |
| 4 | Assigner le tag de groupe (profil Autopilot) | Agent atelier | Console Intune (endpoint.microsoft.com) | Profil attribué |
| 5 | Lancer le préprovisionnement avec compte DEM | Agent atelier | Console Intune (endpoint.microsoft.com) | Provisionnement en cours |
| 6 | Vérifier l'application des politiques : conformité, sécurité, applications | Agent atelier | Console Intune (endpoint.microsoft.com) | Poste conforme |
| 7 | Documenter dans le ticket Tauturu | Agent atelier | Tauturu (GLPI) | Traçabilité |

## ⚠️ Points de vigilance

* Voir aussi PROC-ATL-002 pour le processus complet de préparation poste Intune
* Pour les 2 200 postes 2026 : les hash seront pré-enregistrés par le fournisseur avant livraison
* Harfanglab EDR, Defender, BitLocker et LAPS doivent être vérifiés post-enrôlement

## 🔗 Procédures liées

* PROC-ATL-002 — Préparation poste Intune/Autopilot
* PROC-INT-004 — Gestion profils et groupes

## 📝 Historique des modifications

| Date | Version | Auteur | Nature de la modification |
| --- | --- | --- | --- |
| 2026-03-15 | 1.0 | Chef CPA | Création initiale — projet de formalisation documentaire |
