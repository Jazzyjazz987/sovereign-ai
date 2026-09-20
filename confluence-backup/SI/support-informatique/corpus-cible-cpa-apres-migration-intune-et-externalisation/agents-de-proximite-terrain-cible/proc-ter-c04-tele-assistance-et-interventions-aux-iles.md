<!-- confluence: SI / page 1802301 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/1802301 -->
<!-- parent_id: 1769473 · parent: 🚗 Agents de proximité terrain — cible -->

# PROC-TER-C04 — Télé-assistance et interventions aux îles

|  |  |
| --- | --- |
| **Code** | PROC-TER-C04 |
| **Domaine** | Agents de proximité terrain |
| **Statut** | Cible à valider |
| **Criticité** | Moyenne |
| **Contrainte RGPD** | **Oui** |
| **Outils** | Tauturu, AnyDesk, transporteur |

> **Règle invariante CPA** — Toute dotation, intervention ou action manuelle sur le parc fait l'objet d'un ticket Tauturu.

## Objet

Assurer le support à distance des agents, et traiter les demandes des îles éloignées où aucun déplacement n'est réalisé.

## Déclencheur

Appel, courriel ou ticket d'un agent, quel que soit son lieu d'affectation.

## Télé-assistance — étapes

| # | Action | Qui | Résultat attendu |
| --- | --- | --- | --- |
| 1 | Créer ou reprendre le ticket Tauturu | Agent télé-assistance | Ticket ouvert |
| 2 | Qualifier la demande : périmètre, impact, priorité | Agent télé-assistance | Priorité établie |
| 3 | **Obtenir l'accord explicite de l'agent avant toute prise en main** | Agent télé-assistance | Consentement obtenu et tracé |
| 4 | Prendre la main via AnyDesk et diagnostiquer | Agent télé-assistance | Cause identifiée |
| 5 | Résoudre à distance lorsque c'est possible | Agent télé-assistance | Incident résolu |
| 6 | Sinon, escalader : intervention sur site, atelier, ou cellule compétente | Agent télé-assistance | Escalade documentée |
| 7 | Documenter la session dans le ticket : durée, actions réalisées | Agent télé-assistance | Traçabilité complète |

## Interventions aux îles — spécificités

Aucun déplacement physique n'est réalisé vers les îles éloignées.

| # | Action | Qui | Résultat attendu |
| --- | --- | --- | --- |
| 1 | Expédier le matériel par transporteur | Agent CPA | Matériel en acheminement |
| 2 | Informer le référent local de l'arrivée et du mode opératoire | Agent CPA | Référent prévenu |
| 3 | Accompagner le premier démarrage par télé-assistance | Agent télé-assistance | Poste opérationnel |
| 4 | Pour un retour : organiser l'acheminement inverse | Agent CPA | Matériel récupéré |

**Le poste arrive enrôlé par le fournisseur.** La contrainte de connexion au premier démarrage, qui rendait l'enrôlement à distance délicat, n'existe plus : l'agent ouvre simplement sa session.

## Points de contrôle RGPD

- La prise en main à distance donne accès aux données personnelles présentes sur le poste de l'agent. **Le consentement préalable est obligatoire**, et la session doit être tracée dans le ticket.
- L'accès non surveillé, s'il est activé sur certains postes, doit être justifié, encadré et connu de l'agent concerné.
- L'outil de prise en main est administré par la Cellule Sécurité Opérationnelle : toute demande d'évolution de sa configuration lui est adressée.

## Procédures liées

- PROC-TER-C03 — Dépannage de niveau 1 sur site
- PROC-ATL-C01 — SAV et incidents de niveau 2
- PROC-STOCK-C02 — Dotation de matériel
