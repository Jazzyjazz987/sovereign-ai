<!-- confluence: SI / page 98455 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/98455 -->
<!-- parent_id: 98345 · parent: 🖥️ Console Intune -->

# PROC-INT-003 — Packaging et déploiement d'application

| Code | `PROC-INT-003` |
| --- | --- |
| Domaine | Console Intune |
| --- | --- |
| Rôles concernés | Gestionnaire de comptes (ingénieur) + Agent atelier |
| --- | --- |
| Déclencheur | Demande de déploiement d'une nouvelle application ou mise à jour |
| --- | --- |
| Outil(s) | Console Intune (endpoint.microsoft.com) + Tauturu (GLPI) |
| --- | --- |
| SLA cible | Déploiement test : 1 semaine \| Production : 2 semaines |
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

Packager et déployer une application métier via Intune en suivant une procédure de test progressif en production réelle.

## ⚡ Déclencheur

Demande de déploiement d'une nouvelle application ou mise à jour

## 👤 Acteurs

| Rôle | Responsabilité dans cette procédure |
| --- | --- |
| Gestionnaire de comptes (ingénieur) | Réalise le packaging et le déploiement Intune |
| Chef de cellule CPA | Valide le passage en production |
| Agent atelier | Teste l'application sur poste physique |

## 📋 Étapes

| # | Action | Qui | Outil | Résultat attendu |
| --- | --- | --- | --- | --- |
| 1 | Récupérer le package de l'application (MSI, MSIX, ou conversion Win32) | Gestionnaire de comptes (ingénieur) | Éditeur / DL officiel | Package disponible |
| 2 | Créer l'application dans Intune avec les paramètres de déploiement | Gestionnaire de comptes (ingénieur) | Console Intune (endpoint.microsoft.com) | Application créée dans Intune |
| 3 | Déployer en test sur un groupe restreint (1-3 postes avec consentement utilisateur) | Gestionnaire de comptes (ingénieur) | Console Intune (endpoint.microsoft.com) | Test en cours |
| 4 | Valider le bon fonctionnement sur les postes de test | Agent atelier | Postes test | Application validée |
| 5 | Déployer en production sur le groupe cible après validation chef CPA | Gestionnaire de comptes (ingénieur) | Console Intune (endpoint.microsoft.com) | Application déployée en production |
| 6 | Documenter le déploiement dans le ticket Tauturu | Gestionnaire de comptes (ingénieur) | Tauturu (GLPI) | Traçabilité |

## ⚠️ Points de vigilance

* Le test en production réelle avec consentement utilisateur est la pratique CPA — pas d'environnement de test isolé
* Les scripts PowerShell de packaging doivent faire l'objet d'une revue de code (peer review) avant déploiement
* Surveiller les mises à jour des applications déployées — veille mensuelle recommandée

## 🔗 Procédures liées

* PROC-INT-004 — Gestion profils et groupes Intune

## 📝 Historique des modifications

| Date | Version | Auteur | Nature de la modification |
| --- | --- | --- | --- |
| 2026-03-15 | 1.0 | Chef CPA | Création initiale — projet de formalisation documentaire |
