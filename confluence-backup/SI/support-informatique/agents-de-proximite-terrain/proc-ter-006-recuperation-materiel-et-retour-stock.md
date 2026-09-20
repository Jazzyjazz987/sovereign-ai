<!-- confluence: SI / page 66070 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/66070 -->
<!-- parent_id: 229575 · parent: 🚗 Agents de proximité terrain -->

# PROC-TER-006 — Récupération matériel et retour stock

| Code | `PROC-TER-006` |
| --- | --- |
| Domaine | Agents de proximité terrain |
| Rôles concernés | Agent de proximité terrain |
| Déclencheur | Départ agent, remplacement matériel, ou restitution suite à signalement |
| Outil(s) | Tauturu (GLPI), Fichier Excel SharePoint CPA, Véhicule |
| SLA cible | Récupération planifiée dans les 5 jours ouvrés |
| Version | 1.0 |
| Date de création | 2026-03-15 |
| Dernière MAJ | 2026-03-15 |
| Statut | Actif |
| Criticité | Moyenne |
| Contrainte RGPD | Oui |

**Règle invariante CPA :** Toute action doit être tracée par un ticket Tauturu (GLPI). Pas de ticket = pas d'action.

## 🎯 Objet

Récupérer le matériel informatique chez les utilisateurs ou services et le ramener à l'atelier CPA pour traitement.

## ⚡ Déclencheur

Départ agent, remplacement matériel, ou restitution suite à signalement

## 👤 Acteurs

| Rôle | Responsabilité dans cette procédure |
| --- | --- |
| Agent de proximité terrain | Récupère physiquement le matériel et le remet à l'atelier |
| Agent atelier | Contrôle le statut GLPI avant classement |
| Gestionnaire de stock (intérim Chef CPA) | Met à jour l'inventaire |

## 📋 Étapes

| # | Action | Qui | Outil | Résultat attendu |
| --- | --- | --- | --- | --- |
| 1 | Créer ou référencer le ticket Tauturu de récupération | Agent de proximité terrain | Tauturu (GLPI) | Ticket récupération ouvert |
| 2 | Planifier le passage chez l'utilisateur ou le service | Agent de proximité terrain | Téléphone / Email | RDV planifié |
| 3 | Récupérer le matériel (poste, écran, câbles, périphériques) | Agent de proximité terrain | Véhicule + sac | Matériel récupéré |
| 4 | Rapporter le matériel à l'atelier et le déposer en zone reste (retours) | Agent de proximité terrain | Atelier CPA | Matériel en zone retour |
| 5 | Mettre à jour le ticket et le fichier Excel SharePoint (sortie bénéficiaire) | Agent de proximité terrain + Gestionnaire de stock (intérim Chef CPA) | Tauturu (GLPI), Fichier Excel SharePoint CPA | Inventaire mis à jour |
| 6 | L'atelier contrôle le statut GLPI avant classement définitif | Agent atelier | Tauturu (GLPI) | GLPI cohérent |

## ⚠️ Points de vigilance

* Le matériel récupéré avec données utilisateur entre en période de conservation 30 jours — cf. PROC-STOCK-005
* Récupérer systématiquement TOUS les périphériques : câbles, souris, clavier, écran
* Le véhicule est vidé à chaque retour d'intervention

## 🔴 Points de contrôle RGPD

* Le matériel récupéré contient potentiellement des données personnelles — appliquer obligatoirement PROC-STOCK-005 (conservation 30 jours)

## 🔗 Procédures liées

* PROC-STOCK-005 — Retour matériel
* PROC-STOCK-006 — Réforme et destruction

## 📝 Historique des modifications

| Date | Version | Auteur | Nature de la modification |
| --- | --- | --- | --- |
| 2026-03-15 | 1.0 | Chef CPA | Création initiale — projet de formalisation documentaire |
