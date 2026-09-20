<!-- confluence: SI / page 65975 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/65975 -->
<!-- parent_id: 98313 · parent: 📦 Gestion du stock -->

# PROC-STOCK-002 — Étiquetage et injection GLPI

| Code | `PROC-STOCK-002` |
| --- | --- |
| Domaine | Gestion du stock |
| --- | --- |
| Rôles concernés | Tous agents CPA |
| --- | --- |
| Déclencheur | Suite à la réception validée (PROC-STOCK-001) |
| --- | --- |
| Outil(s) | Tauturu (GLPI), Excel SharePoint, Étiqueteuse |
| --- | --- |
| SLA cible | Dans les 24h suivant la réception |
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

Enregistrer le matériel reçu dans Tauturu (GLPI) et apposer les étiquettes d'inventaire afin d'assurer la traçabilité complète du parc.

## ⚡ Déclencheur

Suite à la réception validée (PROC-STOCK-001)

## 👤 Acteurs

| Rôle | Responsabilité dans cette procédure |
| --- | --- |
| Gestionnaire de stock (intérim Chef CPA) | Pilote le processus d'étiquetage et l'injection GLPI |
| Agent atelier | Participe à l'étiquetage sur les gros volumes |

## 📋 Étapes

| # | Action | Qui | Outil | Résultat attendu |
| --- | --- | --- | --- | --- |
| 1 | Déballer les cartons et sortir le matériel sur les postes de travail atelier | Gestionnaire de stock (intérim Chef CPA) | Stock physique | Matériel accessible |
| 2 | Identifier le type d'étiquette applicable : étiquette pré-imprimée fournisseur (matériel acquis par d'autres services) OU étiquette DSI avec numéro SI = numéro de série (matériel DSI) | Gestionnaire de stock (intérim Chef CPA) | Bon de commande | Type d'étiquette déterminé |
| 3 | Imprimer ou coller les étiquettes sur le châssis de chaque unité, de manière visible et durable | Gestionnaire de stock (intérim Chef CPA) | Étiqueteuse | Matériel étiqueté |
| 4 | Télécharger le template GLPI vierge depuis SharePoint CPA | Gestionnaire de stock (intérim Chef CPA) | Fichier Excel SharePoint CPA | Template disponible |
| 5 | Remplir le fichier d'injection : numéro de série, référence, BC, BL, facture, valeur financière | Gestionnaire de stock (intérim Chef CPA) | Excel | Fichier d'injection complété |
| 6 | Stocker le fichier sur SharePoint CPA (dossier commun) | Gestionnaire de stock (intérim Chef CPA) | Fichier Excel SharePoint CPA | Fichier archivé |
| 7 | Injecter le fichier dans Tauturu | Gestionnaire de stock (intérim Chef CPA) | Tauturu (GLPI) | Matériel enregistré GLPI |
| 8 | Exécuter la requête de contrôle GLPI pour vérifier la conformité de l'injection | Gestionnaire de stock (intérim Chef CPA) | Tauturu (GLPI) | Injection vérifiée — statut 'En stock' |
| 9 | Mettre à jour le fichier Excel SharePoint de suivi (entrée en stock) | Gestionnaire de stock (intérim Chef CPA) | Fichier Excel SharePoint CPA | Suivi temps réel mis à jour |
| 10 | Ranger le matériel étiqueté dans le stock selon le plan de rangement en vigueur | Gestionnaire de stock (intérim Chef CPA) | Stock physique | Matériel rangé et prêt |

## ⚠️ Points de vigilance

* Toujours joindre les documents financiers (BC, BL, facture) au ticket GLPI via le plugin financier
* La double saisie GLPI + Excel SharePoint est obligatoire — l'Excel permet l'extraction de KPI non disponibles nativement dans GLPI
* Archivage des fichiers d'injection sur SharePoint : organiser par année/marché/BC pour faciliter les audits futurs
* Vérifier systématiquement par requête GLPI après injection — une erreur d'injection peut fausser l'inventaire

## 🔗 Procédures liées

* PROC-STOCK-001 — Réception et contrôle livraison
* PROC-STOCK-003 — Inventaire périodique

## 📝 Historique des modifications

| Date | Version | Auteur | Nature de la modification |
| --- | --- | --- | --- |
| 2026-03-15 | 1.0 | Chef CPA | Création initiale — projet de formalisation documentaire |
