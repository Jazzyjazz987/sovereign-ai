<!-- confluence: SI / page 131309 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/131309 -->
<!-- parent_id: 98345 · parent: 🖥️ Console Intune -->

# PROC-INT-005 — Retrait et désinscription appareil Intune

| Code | `PROC-INT-005` |
| --- | --- |
| Domaine | Console Intune |
| --- | --- |
| Rôles concernés | Agent atelier + Gestionnaire de comptes (ingénieur) |
| --- | --- |
| Déclencheur | Départ agent, réforme, perte ou vol d'appareil |
| --- | --- |
| Outil(s) | Console Intune (endpoint.microsoft.com) + Tauturu (GLPI) |
| --- | --- |
| SLA cible | Immédiat en cas de perte/vol \| Dans les 24h pour départ agent |
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
| Contrainte RGPD | Oui |
| --- | --- |

**Règle invariante CPA :** Toute action doit être tracée par un ticket Tauturu (GLPI). Pas de ticket = pas d'action.

## 🎯 Objet

Retirer proprement un appareil du parc Intune en effaçant les données professionnelles conformément au RGPD.

## ⚡ Déclencheur

Départ agent, réforme, perte ou vol d'appareil

## 👤 Acteurs

| Rôle | Responsabilité dans cette procédure |
| --- | --- |
| Agent atelier | Exécute la désinscription dans Intune |
| Chef de cellule CPA | Valide et supervise en cas de perte/vol |

## 📋 Étapes

| # | Action | Qui | Outil | Résultat attendu |
| --- | --- | --- | --- | --- |
| 1 | Créer un ticket Tauturu de retrait (motif : départ, réforme, perte, vol) | Agent atelier | Tauturu (GLPI) | Ticket retrait ouvert |
| 2 | En cas de perte/vol : effectuer un effacement distant immédiat via Intune | Agent atelier | Console Intune (endpoint.microsoft.com) | Données professionnelles effacées |
| 3 | Retirer l'appareil du groupe de déploiement | Agent atelier | Console Intune (endpoint.microsoft.com) | Appareil retiré des groupes |
| 4 | Déconnecter l'appareil de Intune (Retirer ou Réinitialiser selon cas) | Agent atelier | Console Intune (endpoint.microsoft.com) | Appareil désinscrit |
| 5 | Documenter les actions dans le ticket Tauturu | Agent atelier | Tauturu (GLPI) | Traçabilité RGPD |

## ⚠️ Points de vigilance

* Perte ou vol : effacement distant immédiat — ne pas attendre
* L'action 'Réinitialiser' efface tout (données personnelles et pro) — l'action 'Retirer' efface uniquement les données pro
* Coordonner avec PROC-ID-003 pour la désactivation simultanée du compte EntraID

## 🔴 Points de contrôle RGPD

* Tracer l'effacement des données dans le ticket Tauturu (date, agent, méthode)
* En cas de perte/vol : obligation de signalement RGPD potentielle — alerter le chef CPA et le RSSI


## 🔗 Procédures liées

* PROC-INT-004 — Gestion profils et groupes
* PROC-ID-003 — Désactivation compte EntraID
* PROC-STOCK-006 — Réforme et destruction

## 📝 Historique des modifications

| Date | Version | Auteur | Nature de la modification |
| --- | --- | --- | --- |
| 2026-03-15 | 1.0 | Chef CPA | Création initiale — projet de formalisation documentaire |
