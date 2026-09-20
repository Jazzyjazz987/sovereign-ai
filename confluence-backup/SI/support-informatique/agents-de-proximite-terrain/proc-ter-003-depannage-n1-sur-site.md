<!-- confluence: SI / page 98415 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/98415 -->
<!-- parent_id: 229575 · parent: 🚗 Agents de proximité terrain -->

# PROC-TER-003 — Dépannage N1 sur site

| Code | `PROC-TER-003` |
| --- | --- |
| Domaine | Agents de proximité terrain |
| Rôles concernés | Agent de proximité terrain |
| Déclencheur | Ticket Tauturu d'incident N1 nécessitant déplacement |
| Outil(s) | Tauturu (GLPI), VNC, TeamViewer, Sac d'intervention |
| SLA cible | Selon priorité : VIP immédiat, Urgent dans la journée, Standard 3 jours |
| Version | 1.0 |
| Date de création | 2026-03-15 |
| Dernière MAJ | 2026-03-15 |
| Statut | Actif |
| Criticité | Moyenne |
| Contrainte RGPD | Non |

**Règle invariante CPA :** Toute action doit être tracée par un ticket Tauturu (GLPI). Pas de ticket = pas d'action.

## 🎯 Objet

Résoudre les incidents informatiques de niveau N1 sur site utilisateur, ou escalader vers l'atelier si non résolvable sur place.

## ⚡ Déclencheur

Ticket Tauturu d'incident N1 nécessitant déplacement

## 👤 Acteurs

| Rôle | Responsabilité dans cette procédure |
| --- | --- |
| Agent de proximité terrain | Résout l'incident sur site ou décide de l'escalade |
| Agent téléassistance | Renfort téléassistance si besoin depuis le terrain |
| Agent atelier | Prend en charge l'escalade N2 |

## 📋 Étapes

| # | Action | Qui | Outil | Résultat attendu |
| --- | --- | --- | --- | --- |
| 1 | Consulter le ticket et le diagnostic initial avant départ | Agent de proximité terrain | Tauturu (GLPI) | Contexte compris |
| 2 | Se rendre sur site avec le sac d'intervention (outils + câbles spare) | Agent de proximité terrain | Véhicule + sac | Arrivée sur site |
| 3 | Reproduire et diagnostiquer l'incident sur place | Agent de proximité terrain | Poste utilisateur | Cause identifiée ou supposée |
| 4 | Si besoin de renfort diagnostic : appeler la téléassistance pour prise en main à distance simultanée | Agent de proximité terrain | Téléphone + VNC/TeamViewer | Diagnostic complémentaire |
| 5 | Résoudre l'incident sur place si possible | Agent de proximité terrain | Poste + outils | Incident résolu |
| 6 | Si non résolvable : laisser le matériel en l'état, prévenir le bénéficiaire, escalader à l'atelier dans Tauturu | Agent de proximité terrain | Tauturu (GLPI) | Escalade N2 documentée |
| 7 | Mettre à jour le ticket au retour (jamais pendant l'intervention) | Agent de proximité terrain | Tauturu (GLPI) | Ticket mis à jour |

## ⚠️ Points de vigilance

* L'agent terrain résout ce qu'il peut sur place — il n'y a pas de limite formelle à ses actions tant que l'incident peut être résolu
* La mise à jour du ticket se fait au retour, pas pendant l'intervention
* Ne jamais accéder aux données personnelles de l'utilisateur sans demander son accord verbal préalable
* Le mot de passe est saisi par l'utilisateur lui-même — l'agent demande à l'utilisateur de le retaper si besoin

## 🔗 Procédures liées

* PROC-TER-004 — Téléassistance et escalade
* PROC-ATL-003 — SAV et incidents N2

## 📝 Historique des modifications

| Date | Version | Auteur | Nature de la modification |
| --- | --- | --- | --- |
| 2026-03-15 | 1.0 | Chef CPA | Création initiale — projet de formalisation documentaire |
