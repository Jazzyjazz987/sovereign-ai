<!-- confluence: SI / page 1704118 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/1704118 -->
<!-- parent_id: 1736726 · parent: 👤 EntraID / Exchange — cible -->

# PROC-ID-C03 — Gestion des boîtes aux lettres partagées et ressources Exchange

|  |  |
| --- | --- |
| **Code** | PROC-ID-C03 |
| **Domaine** | EntraID / Exchange |
| **Statut** | Cible à valider |
| **Criticité** | Moyenne |
| **Contrainte RGPD** | **Oui** |
| **Outils** | Centre d'administration Exchange, Tauturu |

> **Règle invariante CPA** — Toute dotation, intervention ou action manuelle sur le parc fait l'objet d'un ticket Tauturu.

## Objet

Créer et administrer les boîtes aux lettres partagées, ainsi que les ressources Exchange — salles de réunion et équipements.

Ces objets n'ont pas de titulaire au SIRH : ils restent intégralement à la charge de la cellule.

## Déclencheur

Ticket créé par un valideur, avec justification du besoin et liste des accès demandés.

## Étapes — boîte aux lettres partagée

| # | Action | Qui | Résultat attendu |
| --- | --- | --- | --- |
| 1 | Vérifier la justification du besoin et l'identité du valideur | Agent CPA | Demande recevable |
| 2 | Vérifier qu'une boîte équivalente n'existe pas déjà | Agent CPA | Doublon écarté |
| 3 | Créer la boîte partagée et lui affecter un nom explicite | Agent CPA | Boîte créée |
| 4 | **Désigner un propriétaire fonctionnel, nommé dans le ticket** | Agent CPA | Responsabilité établie |
| 5 | Attribuer les droits d'accès total et d'envoi en tant que, aux seuls agents autorisés | Agent CPA | Accès conformes à la demande |
| 6 | Documenter et clôturer le ticket | Agent CPA | Traçabilité assurée |

## Étapes — modification ou suppression

| # | Action | Qui | Résultat attendu |
| --- | --- | --- | --- |
| 1 | Vérifier le ticket et la validation du propriétaire fonctionnel | Agent CPA | Demande légitime |
| 2 | Pour un retrait d'accès : supprimer les droits de l'agent concerné | Agent CPA | Accès révoqué |
| 3 | Pour une suppression : confirmer l'absence de besoin auprès du propriétaire | Agent CPA | Suppression confirmée |
| 4 | Documenter l'action dans le ticket | Agent CPA | Traçabilité assurée |

## Points de contrôle RGPD

- Une boîte partagée contient de la correspondance professionnelle susceptible de comporter des données personnelles. **L'attribution d'un accès doit être justifiée et tracée** : c'est la seule preuve que l'accès était légitime.
- Le retrait d'accès à la sortie d'un agent du périmètre fonctionnel n'est pas automatique : il relève de la vigilance du propriétaire fonctionnel et du ticket de sortie.
- La suppression d'une boîte partagée emporte son contenu. La confirmation du propriétaire fonctionnel est un prérequis.

## Points de vigilance

- **L'étape 4 est le point faible historique du dispositif.** Une boîte sans propriétaire nommé n'est jamais revue : ses accès s'accumulent au fil des années, bien après le départ des agents qui les ont obtenus.
- Les ressources Exchange suivent le même circuit, avec une attention particulière aux options de réservation automatique.

## Écart non résolu

Aucun inventaire centralisé des boîtes aux lettres partagées n'existe. Sans lui, aucune revue périodique des accès n'est possible. Ce point relève des nouvelles missions à définir pour la cellule.

## Procédures liées

- PROC-ID-C01 — Vérification et suivi des comptes provisionnés
- PROC-ID-C02 — Création d'un compte hors SIRH
