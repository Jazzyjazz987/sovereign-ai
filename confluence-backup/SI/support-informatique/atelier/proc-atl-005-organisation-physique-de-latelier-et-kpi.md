<!-- confluence: SI / page 98395 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/98395 -->
<!-- parent_id: 98329 · parent: 🔧 Atelier -->

# PROC-ATL-005 — Organisation physique de l'atelier et KPI

| Code | `PROC-ATL-005` |
| --- | --- |
| Domaine | Atelier |
| --- | --- |
| Rôles concernés | Agent atelier + Chef de cellule CPA |
| --- | --- |
| Déclencheur | Continu — organisation quotidienne et revue périodique des indicateurs |
| --- | --- |
| Outil(s) | Fichier Excel SharePoint CPA, Tauturu (GLPI) |
| --- | --- |
| SLA cible | Revue KPI : mensuelle |
| --- | --- |
| Version | 1.0 |
| --- | --- |
| Date de création | 2026-03-15 |
| --- | --- |
| Dernière MAJ | 2026-03-15 |
| --- | --- |
| Statut | Actif |
| --- | --- |
| Criticité | Faible |
| --- | --- |
| Contrainte RGPD | Non |
| --- | --- |

**Règle invariante CPA :** Toute action doit être tracée par un ticket Tauturu (GLPI). Pas de ticket = pas d'action.

## 🎯 Objet

Définir les règles d'organisation physique de l'atelier CPA et les indicateurs de performance à suivre pour piloter l'activité de la cellule.

## ⚡ Déclencheur

Continu — organisation quotidienne et revue périodique des indicateurs

## 👤 Acteurs

| Rôle | Responsabilité dans cette procédure |
| --- | --- |
| Agent atelier | Maintient l'organisation physique et alimente les données KPI |
| Chef de cellule CPA | Pilote la revue KPI mensuelle et décide des ajustements |

## 📋 Étapes

| # | Action | Qui | Outil | Résultat attendu |
| --- | --- | --- | --- | --- |
| 1 | Maintenir la séparation physique : Zone stock neuf / Zone reste (retours) / Postes en préparation / Cage réforme | Agent atelier | Atelier physique | Zones clairement identifiées |
| 2 | À chaque mouvement de matériel : mettre à jour immédiatement le fichier Excel SharePoint | Agent atelier | Fichier Excel SharePoint CPA | Suivi temps réel |
| 3 | Extraire mensuellement les KPI depuis GLPI et Excel (délai dotation, taux de disponibilité stock, tickets traités) | Chef de cellule CPA | Tauturu (GLPI), Fichier Excel SharePoint CPA | KPI disponibles |
| 4 | Animer la revue KPI mensuelle au briefing — identifier les dérives | Chef de cellule CPA | Briefing CPA | Actions correctives définies |

## ⚠️ Points de vigilance

* Le briefing quotidien est l'outil central de communication CPA — toute information importante doit y passer
* Les KPI formalisés seront pleinement opérationnels post-migration Intune (un chef de projet dédié les pilotera)
* La cage de parking pour le matériel réformé doit être évacuée au moins semestriellement

## 🔗 Procédures liées

* PROC-STOCK-003 — Inventaire périodique

## 📝 Historique des modifications

| Date | Version | Auteur | Nature de la modification |
| --- | --- | --- | --- |
| 2026-03-15 | 1.0 | Chef CPA | Création initiale — projet de formalisation documentaire |
