<!-- confluence: SI / page 98361 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/98361 -->
<!-- parent_id: 98313 · parent: 📦 Gestion du stock -->

# PROC-STOCK-004 — Dotation matériel

| Code | `PROC-STOCK-004` |
| --- | --- |
| Domaine | Gestion du stock |
| --- | --- |
| Rôles concernés | Tous agents CPA |
| --- | --- |
| Déclencheur | Ticket de demande de dotation créé par un valideur dans Tauturu |
| --- | --- |
| Outil(s) | Tauturu (GLPI), Fichier Excel SharePoint CPA |
| --- | --- |
| SLA cible | 7 jours ouvrés (objectif SLA CPA) |
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

Attribuer un équipement informatique à un agent ou service suite à une demande validée, en garantissant la traçabilité complète dans Tauturu.

## ⚡ Déclencheur

Ticket de demande de dotation créé par un valideur dans Tauturu

## 👤 Acteurs

| Rôle | Responsabilité dans cette procédure |
| --- | --- |
| Chef de cellule CPA | Valide les dotations hors standard, arbitre en cas de litige |
| Agent atelier | Prépare le matériel (image MDT ou Intune) et le met 'En fonction' |
| Agent de proximité terrain | Livre et installe le matériel chez le bénéficiaire |
| Gestionnaire de stock (intérim Chef CPA) | Met à jour le stock et les fichiers de suivi |

## 📋 Étapes

| # | Action | Qui | Outil | Résultat attendu |
| --- | --- | --- | --- | --- |
| 1 | Vérifier la demande de dotation dans Tauturu (valideur identifié, justification, service) | Gestionnaire de stock (intérim Chef CPA) | Tauturu (GLPI) | Demande validée |
| 2 | Vérifier la disponibilité du stock tampon (100 UC / 50 portables) | Gestionnaire de stock (intérim Chef CPA) | Tauturu (GLPI), Fichier Excel SharePoint CPA | Disponibilité confirmée |
| 3 | Préparer le poste via MDT ou Intune/Autopilot selon le type de matériel | Agent atelier | MDT / Console Intune | Poste préparé, Windows installé |
| 4 | Passer le statut GLPI de 'En stock' à 'En fonction' et associer au bénéficiaire | Agent atelier | Tauturu (GLPI) | GLPI mis à jour |
| 5 | Organiser la livraison : soit dépôt à la DSI, soit intervention terrain | Agent de proximité terrain | Tauturu (GLPI), Véhicule | Livraison planifiée |
| 6 | Livrer le matériel dans le bureau du bénéficiaire et finaliser la session utilisateur (présence bénéficiaire obligatoire) | Agent de proximité terrain | Poste, Intune/MDT | Bénéficiaire opérationnel |
| 7 | Mettre à jour le ticket Tauturu et le fichier Excel SharePoint | Agent de proximité terrain / Gestionnaire de stock (intérim Chef CPA) | Tauturu (GLPI), Fichier Excel SharePoint CPA | Traçabilité complète |
| 8 | Clôturer le ticket — le demandeur valide ou la CPA clôture après délai | Gestionnaire de stock (intérim Chef CPA) | Tauturu (GLPI) | Ticket clôturé |

## ⚠️ Points de vigilance

* La finalisation de session (premier login) nécessite la présence physique du bénéficiaire
* Stock tampon minimal à maintenir : 100 UC + 50 portables prêts à doter pour tenir le SLA de 7 jours
* En cas de dotation VIP : priorité absolue, même traitement que les urgences
* Pour les îles : utiliser le coursier (délai moyen 2-3 jours ouvrés) + téléassistance pour finalisation

## 🔗 Procédures liées

* PROC-ATELIER-001 — Préparation poste MDT
* PROC-ATELIER-002 — Préparation poste Intune/Autopilot
* PROC-TERRAIN-002 — Dotation sur site

## 📝 Historique des modifications

| Date | Version | Auteur | Nature de la modification |
| --- | --- | --- | --- |
| 2026-03-15 | 1.0 | Chef CPA | Création initiale — projet de formalisation documentaire |
