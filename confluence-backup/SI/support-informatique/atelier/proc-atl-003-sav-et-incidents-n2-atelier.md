<!-- confluence: SI / page 98378 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/98378 -->
<!-- parent_id: 98329 · parent: 🔧 Atelier -->

# PROC-ATL-003 — SAV et incidents N2 atelier

| Code | `PROC-ATL-003` |
| --- | --- |
| Domaine | Atelier |
| --- | --- |
| Rôles concernés | Agent atelier |
| --- | --- |
| Déclencheur | Ticket Tauturu escaladé depuis la téléassistance (N1 non résolu) ou dépôt physique par un service |
| --- | --- |
| Outil(s) | Tauturu (GLPI), Atelier physique, VNC, TeamViewer |
| --- | --- |
| SLA cible | Traitement sous 3 jours ouvrés |
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

Traiter les incidents matériels et logiciels de niveau N2 nécessitant une intervention physique en atelier, après échec de la résolution à distance.

## ⚡ Déclencheur

Ticket Tauturu escaladé depuis la téléassistance (N1 non résolu) ou dépôt physique par un service

## 👤 Acteurs

| Rôle | Responsabilité dans cette procédure |
| --- | --- |
| Agent atelier | Diagnostique et répare — décide seul du traitement N2 |
| Chef de cellule CPA | Arbitre si réforme ou remplacement nécessaire |
| Agent téléassistance | Escalade le ticket N1 vers l'atelier avec diagnostic initial |

## 📋 Étapes

| # | Action | Qui | Outil | Résultat attendu |
| --- | --- | --- | --- | --- |
| 1 | Prendre en charge le ticket Tauturu escaladé et vérifier le diagnostic N1 | Agent atelier | Tauturu (GLPI) | Contexte incident compris |
| 2 | Réceptionner physiquement le matériel au guichet atelier | Agent atelier | Atelier physique | Matériel en atelier |
| 3 | Reproduire et diagnostiquer l'incident | Agent atelier | Postes de test atelier | Cause identifiée |
| 4 | Tenter la résolution : réinstallation OS, remplacement composant, reconfiguration | Agent atelier | MDT / Intune / Outillage | Réparation tentée |
| 5 | Si irréparable : escalader au chef CPA pour décision de réforme | Agent atelier | Tauturu (GLPI) | Décision réforme documentée |
| 6 | Tester le bon fonctionnement après réparation | Agent atelier | Poste réparé | Fonctionnement confirmé |
| 7 | Restituer le matériel au service ou informer le terrain pour livraison, documenter le ticket | Agent atelier | Tauturu (GLPI) | Ticket clôturé |

## ⚠️ Points de vigilance

* L'agent atelier décide seul du traitement N2 — il peut appeler en renfort la téléassistance pour diagnostic complémentaire
* Les pièces de rechange ne sont pas stockées en atelier — anticiper les délais d'approvisionnement
* Toute décision de réforme doit passer par le chef CPA et déclencher PROC-STOCK-006

## 🔗 Procédures liées

* PROC-TERRAIN-004 — Téléassistance et escalade
* PROC-STOCK-006 — Réforme et destruction

## 📝 Historique des modifications

| Date | Version | Auteur | Nature de la modification |
| --- | --- | --- | --- |
| 2026-03-15 | 1.0 | Chef CPA | Création initiale — projet de formalisation documentaire |
