<!-- confluence: SI / page 65958 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/65958 -->
<!-- parent_id: 98313 · parent: 📦 Gestion du stock -->

# PROC-STOCK-001 — Réception et contrôle livraison

| Code | `PROC-STOCK-001` |
| --- | --- |
| Domaine | Gestion du stock |
| --- | --- |
| Rôles concernés | Tous agents CPA |
| --- | --- |
| Déclencheur | Le fournisseur notifie la DSI au moins 48h avant la livraison |
| --- | --- |
| Outil(s) | Tauturu (GLPI), Excel SharePoint, Bon de livraison |
| --- | --- |
| SLA cible | Traitement le jour de la livraison |
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

Décrire le processus de réception physique du matériel informatique, du contrôle de conformité jusqu'au rangement dans le stock sécurisé de la CPA.

## ⚡ Déclencheur

Le fournisseur notifie la DSI au moins 48h avant la livraison

## 👤 Acteurs

| Rôle | Responsabilité dans cette procédure |
| --- | --- |
| Chef de cellule CPA | Désigne l'agent réceptionnaire, informe la comptabilité en cas d'anomalie |
| Gestionnaire de stock (intérim Chef CPA) | Responsable de la réception, contrôle, signature du BL |
| Agent atelier | Renfort déballage et étiquetage pour les gros volumes |

## 📋 Étapes

| # | Action | Qui | Outil | Résultat attendu |
| --- | --- | --- | --- | --- |
| 1 | Réserver le parking au rez-de-chaussée via la logistique DSI | Chef de cellule CPA | Email / téléphone | Emplacement confirmé |
| 2 | Désigner l'agent réceptionnaire et communiquer le planning | Chef de cellule CPA | Briefing CPA | Agent identifié |
| 3 | Accueillir le livreur et compter les cartons | Gestionnaire de stock (intérim Chef CPA) | BL fournisseur | Nombre de colis vérifié |
| 4 | Contrôler l'intégrité des emballages et vérifier les numéros de série sur le BL | Gestionnaire de stock (intérim Chef CPA) | BL, scan douchette | Conformité validée |
| 5 | En cas d'anomalie : NE PAS signer le BL, consigner l'anomalie par écrit, alerter le chef CPA et la comptabilité | Gestionnaire de stock (intérim Chef CPA) | Email | Anomalie tracée |
| 6 | Signer le BL uniquement après vérification complète | Gestionnaire de stock (intérim Chef CPA) | BL papier | Livraison acceptée |
| 7 | Déplacer le matériel dans la zone de stockage temporaire (stock sécurisé badge) | Gestionnaire de stock (intérim Chef CPA) | Stock physique | Matériel sécurisé |
| 8 | Récupérer BC, BL, facture au format PDF auprès de la comptabilité | Gestionnaire de stock (intérim Chef CPA) | Email comptabilité | Documents financiers disponibles |
| 9 | Créer un ticket Tauturu de réception et y joindre les documents financiers | Gestionnaire de stock (intérim Chef CPA) | Tauturu (GLPI) | Ticket de réception ouvert |

## ⚠️ Points de vigilance

* Le BL ne doit JAMAIS être signé avant vérification complète — toute signature engage la DSI sur la conformité de la livraison
* En cas de grosse livraison (ex : 2 200 postes 2026), mobiliser toute l'équipe CPA + appui Section Production si disponible
* Le stock sécurisé est accessible à 2 personnes maximum habilitées (badge)
* Tout écart entre le BL et le matériel reçu doit être signalé immédiatement au chef CPA et à la comptabilité (risque de pénalités fournisseur)

## 🔗 Procédures liées

* PROC-STOCK-002 — Étiquetage et injection GLPI
* PROC-STOCK-007 — Marchés publics et achats

## 📝 Historique des modifications

| Date | Version | Auteur | Nature de la modification |
| --- | --- | --- | --- |
| 2026-03-15 | 1.0 | Chef CPA | Création initiale — projet de formalisation documentaire |
