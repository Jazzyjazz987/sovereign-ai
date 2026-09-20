<!-- confluence: SI / page 229602 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/229602 -->
<!-- parent_id: 98313 · parent: 📦 Gestion du stock -->

# PROC-STOCK-003 — Inventaire périodique

| Code | `PROC-STOCK-003` |
| --- | --- |
| Domaine | Gestion du stock |
| --- | --- |
| Rôles concernés | Tous agents CPA |
| --- | --- |
| Déclencheur | À la demande du chef CPA, après mouvement important, ou idéalement trimestriel |
| --- | --- |
| Outil(s) | Tauturu (GLPI), Fichier Excel SharePoint CPA, Douchette code-barres |
| --- | --- |
| SLA cible | À planifier — objectif : inventaire trimestriel |
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

Vérifier la cohérence entre le stock physique et les données Tauturu (GLPI), et traiter les écarts identifiés.

## ⚡ Déclencheur

À la demande du chef CPA, après mouvement important, ou idéalement trimestriel

## 👤 Acteurs

| Rôle | Responsabilité dans cette procédure |
| --- | --- |
| Gestionnaire de stock (intérim Chef CPA) | Pilote et déclenche l'inventaire |
| Chef de cellule CPA | Autorise et valide les corrections d'écart |
| Agent atelier | Participe au comptage physique |

## 📋 Étapes

| # | Action | Qui | Outil | Résultat attendu |
| --- | --- | --- | --- | --- |
| 1 | Décider et planifier l'inventaire (date, équipe mobilisée) | Chef de cellule CPA | Briefing CPA | Inventaire planifié |
| 2 | Exporter la liste de stock attendue depuis GLPI | Gestionnaire de stock (intérim Chef CPA) | Tauturu (GLPI) | Liste de référence disponible |
| 3 | Scanner chaque unité physique avec la douchette | Gestionnaire de stock (intérim Chef CPA) + Agent atelier | Douchette → GLPI | Présence physique vérifiée |
| 4 | Vérifier la cohérence statut GLPI / emplacement physique | Gestionnaire de stock (intérim Chef CPA) | Tauturu (GLPI) | Écarts identifiés |
| 5 | Pour chaque écart : contacter le service destinataire, recouper les tickets de dotation, investiguer | Gestionnaire de stock (intérim Chef CPA) | Tauturu (GLPI), Email | Écarts documentés |
| 6 | Corriger les statuts GLPI après validation chef CPA | Gestionnaire de stock (intérim Chef CPA) | Tauturu (GLPI) | GLPI mis à jour |
| 7 | Mettre à jour le fichier Excel SharePoint | Gestionnaire de stock (intérim Chef CPA) | Fichier Excel SharePoint CPA | Suivi cohérent |

## ⚠️ Points de vigilance

* Objectif cible : inventaire trimestriel programmé — actuellement au fil de l'eau (à corriger)
* Le matériel doté 'oublié' dans les services reste 'En fonction' dans GLPI — sensibiliser les services à l'obligation de retour (charte informatique circulaire 7726 PR)
* Toute correction GLPI doit être validée par le chef CPA avant application

## 🔗 Procédures liées

* PROC-STOCK-004 — Dotation matériel
* PROC-STOCK-005 — Retour matériel

## 📝 Historique des modifications

| Date | Version | Auteur | Nature de la modification |
| --- | --- | --- | --- |
| 2026-03-15 | 1.0 | Chef CPA | Création initiale — projet de formalisation documentaire |
