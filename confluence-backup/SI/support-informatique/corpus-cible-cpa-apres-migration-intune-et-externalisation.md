<!-- confluence: SI / page 1703937 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/1703937 -->
<!-- parent_id: 65813 · parent: Support informatique -->

# Corpus cible de la Cellule Parc et Assistance

**Statut : cible à valider** — Version 1.0 — Septembre 2026

Ce corpus décrit l'organisation de la CPA **après** la migration complète du parc sous Microsoft Intune et l'externalisation partielle du datacenter. Il ne décrit pas le fonctionnement actuel. Il est soumis à arbitrage avant bascule.

> Le corpus opérationnel en vigueur reste celui de la branche « Procédures CPA ». Les deux coexistent jusqu'à la bascule.

## Décisions structurantes de la cible

### Parc et déploiement

| Décision | Conséquence |
| --- | --- |
| Parc à 100 % sous Intune | Plus aucune préparation de poste en interne |
| MDT décommissionné | Les procédures de préparation et de maintenance d'image disparaissent |
| Cluster Proxmox décommissionné | La dépendance à une compétence unique disparaît |
| Postes livrés étiquetés, hash Autopilot injecté et tag défini en usine | La CPA contrôle et attribue, elle ne fabrique plus |
| Postes enrôlés par le fournisseur | Le déploiement vers les îles ne dépend plus de la connexion au premier démarrage |
| Tablettes Android maintenues sous MDM Intune | Périmètre inchangé |

### Infrastructure et outillage

| Décision | Conséquence |
| --- | --- |
| Tauturu (GLPI) reste hébergé en local | Le ticketing et l'inventaire survivent à une rupture de liaison |
| LDAP abandonné | EntraID devient l'annuaire unique, fin de la réconciliation manuelle |
| Serveurs de fichiers migrés sur SharePoint | Tenant M365 en région Europe |
| Proxy SQUID arrêté | Le filtrage des flux sortants ne relève plus de la CPA |
| VNC et Kaspersky abandonnés au profit d'AnyDesk | AnyDesk est géré par la Cellule Sécurité Opérationnelle |
| Harfanglab et Defender maintenus | Socle de sécurité inchangé |

### Gestion du stock

| Décision | Conséquence |
| --- | --- |
| Injection dans GLPI par import du bon de livraison fournisseur | Le matériel est tracé dès la réception, carton fermé compris |
| Inventaire assuré par l'agent d'inventaire GLPI | Fin de la saisie manuelle des entrées et sorties |
| Fin du suivi Excel SharePoint | Tauturu devient la source unique |
| Stockage maintenu à la DSI | Voir « Évolutions anticipées » ci-dessous |

### Identités

| Décision | Conséquence |
| --- | --- |
| IdentityDSI lie le SIRH de la DRH à M365 | La CPA ne crée plus les comptes des agents |
| Compte créé à la création du contrat, supprimé à sa fin | Le cycle de vie suit le contrat, non le ticket |
| Suppression au départ comme à la mutation, recréation si nécessaire | Procédure validée par la DPO |
| Le ticket reste à la charge du demandeur pour la dotation matérielle | La règle de traçabilité est préservée |

## La règle invariante, reformulée

> **Toute dotation, intervention ou action manuelle sur le parc fait l'objet d'un ticket Tauturu.**

Le provisionnement des identités par IdentityDSI est automatique et sans ticket : il est tracé par les journaux de l'application. La règle reste donc vraie sur l'intégralité du périmètre de la cellule, puisque la CPA n'intervient plus dans la création des comptes.

## Périmètre de responsabilité

| Acteur | Rôle dans la cible |
| --- | --- |
| **CPA** | Cycle de vie du poste, dotation, support, stock, réforme, comptes hors SIRH |
| **CSO** — Cellule Sécurité Opérationnelle | Politiques de sécurité, AnyDesk, applications stratégiques, packaging partagé |
| **IdentityDSI** | Provisionnement et suppression des comptes des agents sous contrat |
| **Fournisseur** | Étiquetage, hash Autopilot, tag, enrôlement |
| **DRH** | Gestion du SIRH, source du cycle de vie des identités |

## Évolutions anticipées

Deux évolutions sont connues mais non actées. Elles ne sont pas intégrées au corpus, qui décrirait sinon un fonctionnement inapplicable.

**Marché avec stockage chez le titulaire.** Un nouveau marché est envisagé, imposant le stockage du matériel chez le titulaire, le service demandeur venant le récupérer sur son lieu de stockage. Le jour de sa notification, quatre procédures seront à reprendre : réception, contrôle du bon de livraison, dotation, et gestion du stock tampon.

**Nouvelles tâches de la cellule.** Le temps libéré par la migration sera réaffecté à de nouvelles missions, principalement sur les consoles Intune, EntraID et Exchange. Elles restent à définir et viendront s'ajouter aux procédures existantes sans refonte du corpus.

## Structure du corpus

- 📦 Gestion du stock
- 🔧 Atelier
- 🚗 Agents de proximité terrain
- 🖥️ Console Intune
- 👤 EntraID / Exchange
- 🎯 Matrice RACI cible
- 🔄 Correspondance ancien / nouveau corpus

## Références réglementaires

- Arrêté n° 2388 CM du 28 novembre 2025 portant modification de l'organisation de la DSI
- Circulaire n° 7726 PR du 1er octobre 2021 relative à la charte informatique
- Circulaire n° 4748/PR du 15 juillet 2025 relative à la protection des données personnelles
- Circulaire n° 979/PR du 14 février 2025 relative à l'exécution des achats informatiques
- Règlement général sur la protection des données
