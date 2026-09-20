<!-- confluence: SI / page 1703978 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/1703978 -->
<!-- parent_id: 1703958 · parent: 📦 Gestion du stock — cible -->

# PROC-STOCK-C01 — Réception et injection du matériel

|  |  |
| --- | --- |
| **Code** | PROC-STOCK-C01 |
| **Domaine** | Gestion du stock |
| **Statut** | Cible à valider |
| **Criticité** | Haute |
| **Contrainte RGPD** | Non |
| **Outils** | Tauturu, bon de livraison fournisseur |
| **Version** | 1.0 |

> **Règle invariante CPA** — Toute dotation, intervention ou action manuelle sur le parc fait l'objet d'un ticket Tauturu.

## Objet

Décrire la réception physique du matériel informatique livré par le fournisseur et son enregistrement dans Tauturu par import du bon de livraison.

Le matériel arrive **préparé en usine** : étiqueté, hash Autopilot injecté, tag de déploiement défini, appareil enrôlé. La cellule ne prépare plus, elle contrôle et enregistre.

## Déclencheur

Notification de livraison par le fournisseur, au moins 48 heures avant.

## Acteurs

| Rôle | Responsabilité |
| --- | --- |
| Responsable de cellule | Désigne l'agent réceptionnaire, informe la comptabilité en cas d'anomalie |
| Agent CPA réceptionnaire | Réception, contrôle, signature du bon de livraison, import dans Tauturu |
| Renfort atelier | Manutention sur les volumes importants |

## Étapes

| # | Action | Qui | Résultat attendu |
| --- | --- | --- | --- |
| 1 | Réserver l'emplacement de livraison auprès de la logistique DSI | Responsable de cellule | Emplacement confirmé |
| 2 | Désigner l'agent réceptionnaire au briefing | Responsable de cellule | Agent identifié |
| 3 | Accueillir le livreur et compter les colis | Agent réceptionnaire | Nombre de colis vérifié |
| 4 | Contrôler l'intégrité des emballages et la concordance des numéros de série avec le bon de livraison | Agent réceptionnaire | Conformité établie |
| 5 | **En cas d'anomalie : ne pas signer.** Consigner l'écart par écrit, alerter le responsable de cellule et la comptabilité | Agent réceptionnaire | Anomalie tracée |
| 6 | Signer le bon de livraison, uniquement après contrôle complet | Agent réceptionnaire | Livraison acceptée |
| 7 | Déplacer le matériel dans la zone de stockage sécurisée | Agent réceptionnaire | Matériel sécurisé |
| 8 | Créer le ticket Tauturu de réception | Agent réceptionnaire | Ticket ouvert |
| 9 | Importer le bon de livraison dans Tauturu | Agent réceptionnaire | Matériel enregistré, statut « En stock » |
| 10 | Vérifier la cohérence de l'import : nombre d'enregistrements, numéros de série | Agent réceptionnaire | Import validé |
| 11 | Joindre bon de commande, bon de livraison et facture au ticket | Agent réceptionnaire | Dossier financier complet |

## Points de vigilance

- **Le bon de livraison ne doit jamais être signé avant contrôle complet.** La signature engage la DSI sur la conformité de la livraison et conditionne les pénalités de retard gérées par la comptabilité.
- **La qualité du bon de livraison conditionne la fiabilité de tout l'inventaire.** Un numéro de série erroné produit une fiche fantôme dans Tauturu et un poste réel non tracé. Le contrôle de l'étape 4 est la seule barrière : il n'y a plus de ressaisie manuelle pour rattraper l'erreur.
- L'agent d'inventaire GLPI enrichit la fiche au premier démarrage du poste chez l'agent bénéficiaire. Entre la réception et cette remontée, la fiche existe mais reste partielle : c'est normal.
- Le stock sécurisé est accessible à deux personnes habilitées au maximum.
- Sur une livraison de volume important, mobiliser l'ensemble de la cellule et solliciter un appui de la section Production.

## Procédures liées

- PROC-STOCK-C02 — Dotation de matériel
- PROC-ATL-C02 — Contrôle de conformité du matériel à réception

## Évolution anticipée

Le marché envisagé imposant le stockage chez le titulaire supprimerait les étapes 1, 3 et 7 et déplacerait le contrôle de l'étape 4 vers le service demandeur. Cette procédure serait alors entièrement reprise.
