<!-- confluence: SI / page 1704138 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/1704138 -->
<!-- parent_id: 1736806 · parent: 📦 Gestion du stock — hybride -->

# PROC-STOCK-H01 — Réception et enregistrement du matériel

|  |  |
| --- | --- |
| **Code** | PROC-STOCK-H01 |
| **Domaine** | Gestion du stock |
| **Statut** | En vigueur pendant la migration |
| **Discriminant** | Marché sur lequel le matériel a été commandé |
| **Criticité** | Haute |
| **Outils** | Tauturu, bon de livraison, étiqueteuse, Excel SharePoint |

> **Règle invariante CPA** — Toute dotation, intervention ou action manuelle sur le parc fait l'objet d'un ticket Tauturu.

## Objet

Réceptionner le matériel livré et l'enregistrer dans l'inventaire.

Deux flux coexistent : le matériel commandé sous l'ancien marché, qui arrive brut, et le matériel commandé sous le nouveau marché, qui arrive étiqueté, enrôlé et doté de son tag.

## Déterminer le flux

Le bon de commande indique le marché. En cas de doute, l'absence d'étiquette sur le carton ou sur le châssis signale un matériel de l'ancien flux.

## Étapes communes aux deux flux

| # | Action | Qui |
| --- | --- | --- |
| 1 | Réserver l'emplacement de livraison auprès de la logistique DSI | Responsable de cellule |
| 2 | Désigner l'agent réceptionnaire au briefing | Responsable de cellule |
| 3 | Accueillir le livreur et compter les colis | Agent réceptionnaire |
| 4 | Contrôler l'intégrité des emballages et la concordance des numéros de série avec le bon de livraison | Agent réceptionnaire |
| 5 | **En cas d'anomalie : ne pas signer.** Consigner l'écart, alerter le responsable de cellule et la comptabilité | Agent réceptionnaire |
| 6 | Signer le bon de livraison, uniquement après contrôle complet | Agent réceptionnaire |
| 7 | Créer le ticket Tauturu de réception | Agent réceptionnaire |

## Étapes propres au flux

| # | 🟠 Matériel ancien marché | 🔵 Matériel nouveau marché |
| --- | --- | --- |
| 8 | Déballer et sortir le matériel sur les postes de travail | Déballer et contrôler la présence des étiquettes usine |
| 9 | Identifier le type d'étiquette applicable et l'apposer sur le châssis | *Sans objet — étiquetage réalisé en usine* |
| 10 | Télécharger le template d'injection GLPI depuis SharePoint | *Sans objet* |
| 11 | Remplir le fichier d'injection : numéro de série, référence, bon de commande, bon de livraison, facture, valeur | *Sans objet* |
| 12 | Injecter le fichier dans Tauturu | Importer le bon de livraison fournisseur dans Tauturu |
| 13 | Exécuter la requête de contrôle pour vérifier l'injection | Vérifier la cohérence de l'import : nombre d'enregistrements, numéros de série |
| 14 | Mettre à jour le fichier Excel SharePoint de suivi | Vérifier la présence des appareils dans la console Intune |
| 15 | Ranger le matériel en **zone à préparer** | Ranger le matériel en **zone prêt à doter** |

## Étape finale commune

| # | Action | Qui |
| --- | --- | --- |
| 16 | Joindre bon de commande, bon de livraison et facture au ticket | Agent réceptionnaire |

## Points de vigilance

**Communs aux deux flux**

- Le bon de livraison ne doit jamais être signé avant contrôle complet : la signature engage la DSI et conditionne les pénalités de retard.
- Le stock sécurisé est accessible à deux personnes habilitées au maximum.

| 🟠 Flux ancien marché | 🔵 Flux nouveau marché |
| --- | --- |
| La double saisie GLPI et Excel reste obligatoire tant que le suivi Excel n'est pas arrêté | Le suivi Excel ne s'applique pas : Tauturu est la seule source |
| Archiver les fichiers d'injection par année et par marché, pour les audits futurs | Aucun fichier d'injection produit — la traçabilité repose sur le bon de livraison joint au ticket |
| Vérifier systématiquement l'injection par requête : une erreur fausse l'inventaire | Un écart d'étiquetage ou de tag relève du fournisseur : élargir le contrôle au lot et documenter |

**Le rangement est le point critique de la période.** Un poste enrôlé rangé en zone à préparer sera repréparé pour rien ; un poste legacy rangé en zone prêt à doter sera livré non configuré, et l'agent bénéficiaire découvrira un poste inutilisable.

## Procédures liées

- PROC-STOCK-H02 — Dotation de matériel
- PROC-ATL-H01 — Préparation ou contrôle d'un poste avant dotation
- PROC-INT-H01 — Enrôlement et attribution d'un appareil
