<!-- confluence: SI / page 98432 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/98432 -->
<!-- parent_id: 229575 · parent: 🚗 Agents de proximité terrain -->

# PROC-TER-005 — Interventions dans les îles éloignées

| Code | `PROC-TER-005` |
| --- | --- |
| Domaine | Agents de proximité terrain |
| Rôles concernés | Agent téléassistance + Gestionnaire de stock (intérim Chef CPA) |
| Déclencheur | Ticket de dotation ou d'incident pour un service hors Tahiti |
| Outil(s) | Tauturu (GLPI), Coursier fret, Téléassistance |
| SLA cible | Délai coursier : ~2-3 jours ouvrés + délai de finalisation |
| Version | 1.0 |
| Date de création | 2026-03-15 |
| Dernière MAJ | 2026-03-15 |
| Statut | Actif |
| Criticité | Moyenne |
| Contrainte RGPD | Non |

**Règle invariante CPA :** Toute action doit être tracée par un ticket Tauturu (GLPI). Pas de ticket = pas d'action.

## 🎯 Objet

Gérer les interventions informatiques (dotations et incidents) pour les agents des îles éloignées de la Polynésie française, via un système combinant envoi par coursier et téléassistance.

## ⚡ Déclencheur

Ticket de dotation ou d'incident pour un service hors Tahiti

## 👤 Acteurs

| Rôle | Responsabilité dans cette procédure |
| --- | --- |
| Gestionnaire de stock (intérim Chef CPA) | Prépare et expédie le matériel via coursier |
| Agent téléassistance | Finalise l'installation à distance avec le bénéficiaire |
| Agent de proximité terrain | Coordonne et suit les expéditions dans le ticket |

## 📋 Étapes

| # | Action | Qui | Outil | Résultat attendu |
| --- | --- | --- | --- | --- |
| 1 | Créer et qualifier le ticket Tauturu (type d'intervention, service destinataire, île concernée) | Agent téléassistance | Tauturu (GLPI) | Ticket qualifié |
| 2 | Pour une dotation : préparer le matériel à l'atelier (MDT ou Intune) | Agent atelier | MDT / Intune | Matériel préparé |
| 3 | Emballer et étiqueter le colis pour expédition fret | Gestionnaire de stock (intérim Chef CPA) | Stock + emballage | Colis prêt |
| 4 | Remettre le colis au coursier pour envoi fret (fréquence ~tous les 2-3 jours ouvrés) | Gestionnaire de stock (intérim Chef CPA) | Service coursier | Colis expédié |
| 5 | Informer le service destinataire via le ticket : numéro de suivi, instructions de récupération | Agent téléassistance | Tauturu (GLPI) | Service destinataire informé |
| 6 | Le bénéficiaire récupère le matériel et contacte la téléassistance pour finalisation | Agent téléassistance | Téléphone + TeamViewer/VNC | Installation finalisée à distance |
| 7 | Mettre à jour le ticket et clôturer | Agent téléassistance | Tauturu (GLPI) | Ticket clôturé |

## ⚠️ Points de vigilance

* Le service destinataire est responsable de la récupération du colis au fret — le prévenir impérativement dans le ticket
* La finalisation de session (premier login) se fait par téléassistance — vérifier que le bénéficiaire a une connexion internet fonctionnelle
* Le suivi coursier doit être documenté dans le ticket Tauturu

## 🔗 Procédures liées

* PROC-TER-002 — Dotation sur site
* PROC-TER-004 — Téléassistance et escalade

## 📝 Historique des modifications

| Date | Version | Auteur | Nature de la modification |
| --- | --- | --- | --- |
| 2026-03-15 | 1.0 | Chef CPA | Création initiale — projet de formalisation documentaire |
