<!-- confluence: SI / page 131189 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/131189 -->
<!-- parent_id: 98313 · parent: 📦 Gestion du stock -->

# PROC-STOCK-006 — Réforme et destruction de données

| Code | `PROC-STOCK-006` |
| --- | --- |
| Domaine | Gestion du stock |
| --- | --- |
| Rôles concernés | Chef de cellule CPA + Gestionnaire de stock (intérim Chef CPA) |
| --- | --- |
| Déclencheur | Décision de réforme du matériel (obsolescence, panne irréparable, fin de vie) |
| --- | --- |
| Outil(s) | Tauturu (GLPI), Destructeur de disques, Registre RGPD |
| --- | --- |
| SLA cible | Destruction dans les 30 jours suivant la décision de réforme |
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

Gérer la sortie définitive du matériel informatique du parc DSI en assurant la destruction sécurisée des données conformément au RGPD, et la réforme physique via le prestataire agréé.

## ⚡ Déclencheur

Décision de réforme du matériel (obsolescence, panne irréparable, fin de vie)

## 👤 Acteurs

| Rôle | Responsabilité dans cette procédure |
| --- | --- |
| Chef de cellule CPA | Prend la décision de réforme et valide la procédure |
| Gestionnaire de stock (intérim Chef CPA) | Exécute la destruction, tient le registre, collecte le certificat |

## 📋 Étapes

| # | Action | Qui | Outil | Résultat attendu |
| --- | --- | --- | --- | --- |
| 1 | Créer un ticket Tauturu de réforme et y documenter la décision (motif, liste des équipements) | Chef de cellule CPA | Tauturu (GLPI) | Ticket réforme ouvert |
| 2 | Physiquement extraire les disques durs (HDD et SSD) des équipements à réformer | Gestionnaire de stock (intérim Chef CPA) | Atelier — outillage | Disques extraits |
| 3 | Détruire chaque disque avec le destructeur physique de la CPA | Gestionnaire de stock (intérim Chef CPA) | Destructeur de disques (HDD + SSD) | Disques physiquement détruits |
| 4 | Enregistrer chaque destruction dans le registre RGPD de traçabilité (numéro de série, date, agent, méthode) | Gestionnaire de stock (intérim Chef CPA) | Registre RGPD CPA | Destruction tracée — CONFORME RGPD |
| 5 | Déposer les carcasses à la cage parking pour évacuation semestrielle par le prestataire de réforme | Gestionnaire de stock (intérim Chef CPA) | Cage parking DSI | Carcasses en attente évacuation |
| 6 | Récupérer le certificat de destruction auprès du prestataire lors de l'évacuation | Gestionnaire de stock (intérim Chef CPA) | Prestataire réforme | Certificat de destruction obtenu |
| 7 | Archiver le certificat dans le ticket Tauturu et dans le registre RGPD | Gestionnaire de stock (intérim Chef CPA) | Tauturu (GLPI), Registre RGPD | Archive conforme RGPD |
| 8 | Passer le statut GLPI à 'Réformé' et mettre à jour Excel SharePoint | Gestionnaire de stock (intérim Chef CPA) | Tauturu (GLPI), Fichier Excel SharePoint CPA | Inventaire mis à jour |

## ⚠️ Points de vigilance

* CRITIQUE RGPD : L'absence de registre de traçabilité des destructions et de certificats du prestataire est la non-conformité RGPD la plus grave identifiée — action P1 immédiate
* Le destructeur de disques physique (HDD + SSD) de la CPA est l'outil de destruction obligatoire — jamais de simple formatage
* Le registre RGPD de destruction doit contenir a minima : numéro de série, type de support, date de destruction, identité de l'agent, méthode
* L'évacuation semestrielle des carcasses doit impérativement donner lieu à un certificat de destruction — l'exiger contractuellement auprès du prestataire

## 🔴 Points de contrôle RGPD

* Créer et tenir à jour un registre RGPD de traçabilité des destructions (action P1 — délai : immédiat)
* Exiger un certificat de destruction à chaque évacuation du prestataire (action P1)
* Formaliser une politique de destruction des données dans la gouvernance DSI
* Référence : RGPD Art. 5(1)(f) — intégrité et confidentialité des données personnelles


## 🔗 Procédures liées

* PROC-STOCK-005 — Retour matériel

## 📝 Historique des modifications

| Date | Version | Auteur | Nature de la modification |
| --- | --- | --- | --- |
| 2026-03-15 | 1.0 | Chef CPA | Création initiale — projet de formalisation documentaire |
