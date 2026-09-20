<!-- confluence: SI / page 131333 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/131333 -->
<!-- parent_id: 65942 · parent: 👤 EntraID / Exchange -->

# PROC-ID-001 — Création de compte utilisateur

| Code | `PROC-ID-001` |
| --- | --- |
| Domaine | EntraID / Exchange |
| --- | --- |
| Rôles concernés | Gestionnaire de comptes (ingénieur) |
| --- | --- |
| Déclencheur | Ticket de création créé par un valideur dans Tauturu |
| --- | --- |
| Outil(s) | Centre d'admin EntraID / Exchange + Tauturu (GLPI) |
| --- | --- |
| SLA cible | Création dans les 24h suivant le ticket |
| --- | --- |
| Version | 1.1 |
| --- | --- |
| Date de création | 2026-03-15 |
| --- | --- |
| Dernière MAJ | 2026-09-14 |
| --- | --- |
| Statut | Actif |
| --- | --- |
| Criticité | Haute |
| --- | --- |
| Contrainte RGPD | Non |
| --- | --- |

**Règle invariante CPA :** Toute action doit être tracée par un ticket Tauturu (GLPI). Pas de ticket = pas d'action.

## 🎯 Objet

Créer un compte utilisateur dans EntraID (LDAP + cloud) et Exchange Online, avec attribution de la licence M365 F3 par défaut.

## ⚡ Déclencheur

Ticket de création créé par un valideur dans Tauturu

## 👤 Acteurs

| Rôle | Responsabilité dans cette procédure |
| --- | --- |
| Gestionnaire de comptes (ingénieur) | Crée le compte dans LDAP et EntraID |

## 📋 Étapes

| # | Action | Qui | Outil | Résultat attendu |
| --- | --- | --- | --- | --- |
| 1 | Vérifier le ticket Tauturu : valideur identifié, informations complètes (nom, prénom, service, fonction) | Gestionnaire de comptes (ingénieur) | Tauturu (GLPI) | Ticket validé |
| 2 | Vérifier dans LDAP/EntraID qu'aucun compte n'existe déjà pour cet agent (mutation depuis un autre service PF, réintégration) — si un compte existe déjà, arrêter ici et traiter via PROC-ID-002 (Modification de compte) au lieu de créer un doublon | Gestionnaire de comptes (ingénieur) | Console LDAP / EntraID | Absence de compte existant confirmée |
| 3 | Créer le compte dans l'annuaire LDAP avec les attributs du service | Gestionnaire de comptes (ingénieur) | Console LDAP / EntraID | Compte LDAP créé |
| 4 | Vérifier la synchronisation automatique avec EntraID | Gestionnaire de comptes (ingénieur) | Centre d'admin EntraID / Exchange | Compte EntraID disponible |
| 5 | Attribuer la licence M365 F3 (par défaut) — ou E1/E3 si spécifié dans le ticket | Gestionnaire de comptes (ingénieur) | Centre d'admin EntraID / Exchange | Licence attribuée |
| 6 | Configurer le MFA (téléphone de l'agent) — l'agent configure son self-service via son numéro | Gestionnaire de comptes (ingénieur) | Centre d'admin EntraID / Exchange | MFA activé |
| 7 | Communiquer les identifiants provisoires au demandeur via le ticket Tauturu | Gestionnaire de comptes (ingénieur) | Tauturu (GLPI) | Agent informé |
| 8 | Clôturer le ticket | Gestionnaire de comptes (ingénieur) | Tauturu (GLPI) | Ticket clôturé |

## ⚠️ Points de vigilance

* Règle absolue : PAS DE CRÉATION SANS TICKET — aucune exception
* « Agent qui arrive » ne veut pas toujours dire compte à créer : une mutation interne depuis un autre service PF peut avoir déjà un compte — d'où l'étape 2 (vérification avant création, pour éviter un doublon LDAP)
* La nomenclature UPN doit respecter les conventions DSI (sans accents, nom patronymique conservé même en cas de changement de nom)
* La licence F3 donne accès à Exchange, Teams, Office Online, OneDrive, SharePoint
* Licence E3 : réservée aux ministères — validation renforcée requise

## 🔗 Procédures liées

* PROC-ID-002 — Modification compte
* PROC-ID-007 — Licences M365

## 📝 Historique des modifications

| Date | Version | Auteur | Nature de la modification |
| --- | --- | --- | --- |
| 2026-03-15 | 1.0 | Chef CPA | Création initiale — projet de formalisation documentaire |
| 2026-09-14 | 1.1 | Chef CPA (via copilote) | Ajout étape 2 — vérification qu'aucun compte n'existe déjà (mutation interne) avant création, pour éviter un doublon LDAP. MAJ locale, à reporter sur Confluence. |
