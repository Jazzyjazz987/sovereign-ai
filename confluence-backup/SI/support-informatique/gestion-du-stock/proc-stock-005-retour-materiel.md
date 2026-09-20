<!-- confluence: SI / page 65994 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/65994 -->
<!-- parent_id: 98313 · parent: 📦 Gestion du stock -->

# PROC-STOCK-005 — Retour matériel

| Code | `PROC-STOCK-005` |
| --- | --- |
| Domaine | Gestion du stock |
| --- | --- |
| Rôles concernés | Tous agents CPA |
| --- | --- |
| Déclencheur | Départ d'un agent, fin de contrat, remplacement matériel ou restitution volontaire |
| --- | --- |
| Outil(s) | Tauturu (GLPI), Fichier Excel SharePoint CPA |
| --- | --- |
| SLA cible | Traitement dans les 5 jours ouvrés suivant le retour physique |
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
| Contrainte RGPD | Oui |
| --- | --- |

**Règle invariante CPA :** Toute action doit être tracée par un ticket Tauturu (GLPI). Pas de ticket = pas d'action.

## 🎯 Objet

Gérer le retour de matériel informatique en assurant la préservation des données (30 jours), la mise à jour de l'inventaire et l'orientation vers le stock ou la réforme.

## ⚡ Déclencheur

Départ d'un agent, fin de contrat, remplacement matériel ou restitution volontaire

## 👤 Acteurs

| Rôle | Responsabilité dans cette procédure |
| --- | --- |
| Agent de proximité terrain | Récupère le matériel sur site et le ramène à l'atelier |
| Agent atelier | Inspecte le matériel et oriente : stock reste ou réforme |
| Gestionnaire de stock (intérim Chef CPA) | Met à jour GLPI et fichier Excel, gère la période de conservation |

## 📋 Étapes

| # | Action | Qui | Outil | Résultat attendu |
| --- | --- | --- | --- | --- |
| 1 | Créer ou mettre à jour le ticket Tauturu de retour | Agent de proximité terrain | Tauturu (GLPI) | Ticket retour ouvert |
| 2 | Récupérer le matériel chez l'utilisateur ou au guichet atelier | Agent de proximité terrain | Véhicule | Matériel en transit |
| 3 | Inspecter l'état physique du matériel à l'atelier | Agent atelier | Atelier physique | État documenté dans le ticket |
| 4 | Placer le matériel en zone 'Reste' (30 jours de conservation des données) | Agent atelier | Stock physique | Matériel en quarantaine données |
| 5 | Passer le statut GLPI à 'Retourné / En attente' | Gestionnaire de stock (intérim Chef CPA) | Tauturu (GLPI) | GLPI mis à jour |
| 6 | Mettre à jour le fichier Excel SharePoint (sortie bénéficiaire) | Gestionnaire de stock (intérim Chef CPA) | Fichier Excel SharePoint CPA | Suivi mis à jour |
| 7 | Après 30 jours : réinitialiser le poste et le placer en stock ou déclencher PROC-STOCK-006 si réforme | Agent atelier | MDT / Intune | Poste réintégré ou réformé |

## ⚠️ Points de vigilance

* Le délai de 30 jours de conservation des données est une règle RGPD — le bénéficiaire peut réclamer ses données dans ce délai
* Ce délai de 30 jours n'est pas encore formalisé dans une politique RGPD écrite — action prioritaire P1
* Tout matériel retourné avec données doit rester physiquement séparé du stock neuf

## 🔴 Points de contrôle RGPD

* Conservation des données 30 jours avant réinitialisation — non formalisé : créer une politique RGPD écrite (P1)
* Le bénéficiaire doit être informé du délai de conservation avant réinitialisation


## 🔗 Procédures liées

* PROC-STOCK-006 — Réforme et destruction
* PROC-TERRAIN-006 — Récupération matériel et retour stock

## 📝 Historique des modifications

| Date | Version | Auteur | Nature de la modification |
| --- | --- | --- | --- |
| 2026-03-15 | 1.0 | Chef CPA | Création initiale — projet de formalisation documentaire |
