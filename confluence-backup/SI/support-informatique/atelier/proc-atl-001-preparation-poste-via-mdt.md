<!-- confluence: SI / page 66015 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/66015 -->
<!-- parent_id: 98329 · parent: 🔧 Atelier -->

# PROC-ATL-001 — Préparation poste via MDT

| Code | `PROC-ATL-001` |
| --- | --- |
| Domaine | Atelier |
| --- | --- |
| Rôles concernés | Agent atelier + Gestionnaire de comptes (ingénieur) |
| --- | --- |
| Déclencheur | Demande de dotation nécessitant un poste préparé (image MDT) |
| --- | --- |
| Outil(s) | Cluster Proxmox, VM MDT, Switch PXE, Tauturu |
| --- | --- |
| SLA cible | Durée de préparation : \~2h par poste (8 postes simultanément en standard) |
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

Décrire le processus de préparation technique d'un poste de travail via Microsoft Deployment Toolkit (MDT) hébergé sur le cluster Proxmox CPA.

## ⚡ Déclencheur

Demande de dotation nécessitant un poste préparé (image MDT)

## 👤 Acteurs

| Rôle | Responsabilité dans cette procédure |
| --- | --- |
| Agent atelier | Réalise le déploiement MDT et le contrôle qualité |
| Gestionnaire de comptes (ingénieur) | Maintient et met à jour les images MDT (ingénieur) |

## 📋 Étapes

| # | Action | Qui | Outil | Résultat attendu |
| --- | --- | --- | --- | --- |
| 1 | Vérifier le ticket Tauturu de dotation et identifier le type de poste à préparer | Agent atelier | Tauturu (GLPI) | Besoin confirmé |
| 2 | Connecter le poste au réseau PXE dédié (switch atelier isolé) | Agent atelier | Switch PXE atelier | Poste connecté au réseau MDT |
| 3 | Démarrer le poste en mode PXE (F12 au boot) | Agent atelier | BIOS poste | Poste en démarrage PXE |
| 4 | Sélectionner l'image appropriée dans MDT (Windows 10 ou Windows 11) | Agent atelier | VM MDT / Proxmox | Image sélectionnée |
| 5 | Lancer le déploiement automatique MDT et attendre (\~2h) | Agent atelier | MDT | OS déployé avec applications et pilotes |
| 6 | Contrôle qualité post-installation : vérifier OS, applications, drivers, Harfanglab EDR, BitLocker | Agent atelier | Poste préparé | Poste conforme |
| 7 | Placer le poste sur l'étagère 'Prêt à déployer' du stock | Agent atelier | Stock physique | Poste disponible pour terrain |
| 8 | Mettre à jour le statut GLPI en 'En fonction' et le ticket de dotation | Agent atelier | Tauturu (GLPI) | Traçabilité mise à jour |

## ⚠️ Points de vigilance

* L'image MDT est maintenue mensuellement (correctifs Patch Tuesday) par l'ingénieur — vérifier la fraîcheur de l'image avant déploiement massif
* Le cluster Proxmox est administré uniquement par l'ingénieur CPA — escalader toute panne infrastructure
* MDT sera décommissionné post-migration Intune 2026 — cette procédure a une durée de vie limitée
* Pour les grosses migrations : ajouter un switch 48 ports pour préparer une batterie de postes simultanément

## 🔗 Procédures liées

* PROC-ATL-002 — Préparation poste Intune/Autopilot
* PROC-ATL-004 — Maintenance image MDT
* PROC-STOCK-004 — Dotation matériel

## 📝 Historique des modifications

| Date | Version | Auteur | Nature de la modification |
| --- | --- | --- | --- |
| 2026-03-15 | 1.0 | Chef CPA | Création initiale — projet de formalisation documentaire |
