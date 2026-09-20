<!-- confluence: SI / page 131270 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/131270 -->
<!-- parent_id: 229575 · parent: 🚗 Agents de proximité terrain -->

# PROC-TER-004 — Téléassistance et escalade atelier

| Code | `PROC-TER-004` |
| --- | --- |
| Domaine | Agents de proximité terrain |
| Rôles concernés | Agent téléassistance + Agent atelier |
| Déclencheur | Ticket Tauturu d'incident logiciel N1 ou appel utilisateur |
| Outil(s) | Tauturu (GLPI), VNC, TeamViewer, Kaspersky Console |
| SLA cible | N1 téléassistance : résolution dans la journée |
| Version | 1.0 |
| Date de création | 2026-03-15 |
| Dernière MAJ | 2026-03-15 |
| Statut | Actif |
| Criticité | Moyenne |
| Contrainte RGPD | Non |

**Règle invariante CPA :** Toute action doit être tracée par un ticket Tauturu (GLPI). Pas de ticket = pas d'action.

## 🎯 Objet

Résoudre les incidents logiciels N1 à distance via téléassistance, ou escalader vers l'atelier si non résolvable.

## ⚡ Déclencheur

Ticket Tauturu d'incident logiciel N1 ou appel utilisateur

## 👤 Acteurs

| Rôle | Responsabilité dans cette procédure |
| --- | --- |
| Agent téléassistance | Prend en charge et résout le ticket N1 à distance |
| Agent atelier | Prend en charge l'escalade N2 physique |

## 📋 Étapes

| # | Action | Qui | Outil | Résultat attendu |
| --- | --- | --- | --- | --- |
| 1 | Prendre en charge le ticket Tauturu (2-3 agents en rotation téléassistance) | Agent téléassistance | Tauturu (GLPI) | Ticket assigné |
| 2 | Obtenir l'accord verbal de l'utilisateur avant toute prise en main | Agent téléassistance | Téléphone | Accord utilisateur obtenu |
| 3 | Choisir l'outil de prise en main adapté : Kaspersky Console (tâches à distance), VNC (Linux), TeamViewer (ponctuel externe) | Agent téléassistance | Outils téléassistance | Connexion établie |
| 4 | Diagnostiquer et résoudre l'incident à distance | Agent téléassistance | Console téléassistance | Incident résolu ou non |
| 5 | Si non résolvable à distance : documenter le diagnostic dans le ticket et escalader à l'atelier | Agent téléassistance | Tauturu (GLPI) | Escalade N2 documentée |
| 6 | Clore la session de contrôle à distance | Agent téléassistance | Outils téléassistance | Session fermée |
| 7 | Documenter les actions dans le ticket et clôturer si résolu | Agent téléassistance | Tauturu (GLPI) | Ticket mis à jour / clôturé |

## ⚠️ Points de vigilance

* L'accord verbal de l'utilisateur est obligatoire avant toute prise en main à distance (charte informatique)
* Teamviewer est réservé au support ponctuel externe — VNC pour Linux, Kaspersky Console pour les tâches à distance standard
* Si 2-3 agents sont en téléassistance et qu'une urgence VIP terrain arrive : un agent bascule vers le terrain

## 🔗 Procédures liées

* PROC-TER-003 — Dépannage N1 sur site
* PROC-ATL-003 — SAV et incidents N2

## 📝 Historique des modifications

| Date | Version | Auteur | Nature de la modification |
| --- | --- | --- | --- |
| 2026-03-15 | 1.0 | Chef CPA | Création initiale — projet de formalisation documentaire |
