<!-- confluence: SI / page 66032 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/66032 -->
<!-- parent_id: 98329 · parent: 🔧 Atelier -->

# PROC-ATL-004 — Maintenance de l'image MDT

| Code | `PROC-ATL-004` |
| --- | --- |
| Domaine | Atelier |
| --- | --- |
| Rôles concernés | Gestionnaire de comptes (ingénieur) + Chef de cellule CPA |
| --- | --- |
| Déclencheur | Patch Tuesday mensuel, nouveau driver, modification de la task sequence |
| --- | --- |
| Outil(s) | Cluster Proxmox, VM MDT, Poste de test |
| --- | --- |
| SLA cible | Mise à jour mensuelle (correctifs sécurité) |
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

Maintenir les images MDT (Windows 10 et Windows 11) à jour pour garantir que les postes déployés intègrent les derniers correctifs de sécurité et drivers.

## ⚡ Déclencheur

Patch Tuesday mensuel, nouveau driver, modification de la task sequence

## 👤 Acteurs

| Rôle | Responsabilité dans cette procédure |
| --- | --- |
| Gestionnaire de comptes (ingénieur) | Réalise les modifications et maintient la VM MDT (ingénieur) |
| Chef de cellule CPA | Valide la mise en production et supervise |

## 📋 Étapes

| # | Action | Qui | Outil | Résultat attendu |
| --- | --- | --- | --- | --- |
| 1 | Identifier les correctifs du Patch Tuesday applicable et les nouveaux drivers disponibles | Gestionnaire de comptes (ingénieur) | Windows Update Catalog / Fabricants | Liste des mises à jour identifiées |
| 2 | Modifier l'image dans MDT (task sequence, intégration des correctifs) | Gestionnaire de comptes (ingénieur) | VM MDT / Proxmox | Image modifiée |
| 3 | Déployer l'image sur un poste de test en atelier | Gestionnaire de comptes (ingénieur) | Switch PXE, Poste test | Image testée |
| 4 | Valider le déploiement test (OS, apps, drivers, sécurité) | Gestionnaire de comptes (ingénieur) + Chef de cellule CPA | Poste test | Image validée |
| 5 | Mettre en production l'image validée | Gestionnaire de comptes (ingénieur) | VM MDT | Image production mise à jour |
| 6 | Effectuer une copie de sauvegarde de la VM après modification | Gestionnaire de comptes (ingénieur) | Proxmox | Sauvegarde réalisée |

## ⚠️ Points de vigilance

* La VM MDT n'a pas de sauvegarde automatisée — la copie manuelle post-modification est impérative
* L'ingénieur est le seul à administrer Proxmox — identifier un suppléant pour cette compétence critique
* Cette procédure sera obsolète post-migration Intune 2026 — Intune gère les mises à jour automatiquement
* Tester toujours sur un poste physique avant mise en production

## 🔗 Procédures liées

* PROC-ATL-001 — Préparation poste via MDT

## 📝 Historique des modifications

| Date | Version | Auteur | Nature de la modification |
| --- | --- | --- | --- |
| 2026-03-15 | 1.0 | Chef CPA | Création initiale — projet de formalisation documentaire |
