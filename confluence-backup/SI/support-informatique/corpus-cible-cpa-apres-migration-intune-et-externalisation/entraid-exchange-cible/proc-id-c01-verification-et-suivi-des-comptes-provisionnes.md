<!-- confluence: SI / page 1704078 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/1704078 -->
<!-- parent_id: 1736726 · parent: 👤 EntraID / Exchange — cible -->

# PROC-ID-C01 — Vérification et suivi des comptes provisionnés

|  |  |
| --- | --- |
| **Code** | PROC-ID-C01 |
| **Domaine** | EntraID / Exchange |
| **Statut** | Cible à valider |
| **Criticité** | Haute |
| **Contrainte RGPD** | **Oui** |
| **Outils** | EntraID, Tauturu, IdentityDSI |

> **Règle invariante CPA** — Toute dotation, intervention ou action manuelle sur le parc fait l'objet d'un ticket Tauturu.

## Objet

Décrire le rôle de la cellule dans le cycle de vie des comptes des agents sous contrat, désormais provisionnés automatiquement.

**La CPA ne crée plus ces comptes.** Elle vérifie leur existence au moment de la dotation, traite les écarts, et désactive les comptes orphelins qu'elle rencontre.

## Le cycle de vie, en cible

| Événement | Acteur | Effet |
| --- | --- | --- |
| Création du contrat | IdentityDSI, depuis le SIRH | Compte créé, modèle de poste appliqué |
| Dotation de matériel | CPA, sur ticket du demandeur | Poste attribué au bénéficiaire |
| Départ ou mutation | IdentityDSI, ticket de sortie côté CPA | **Compte supprimé**, matériel récupéré |
| Réaffectation d'un poste | CPA | Compte orphelin éventuel détecté et désactivé |
| Fin de contrat | IdentityDSI | Compte supprimé |

La suppression au départ comme à la mutation, suivie d'une recréation si l'agent rejoint un autre service, est la **procédure validée par la DPO**.

## Étapes — vérification à la dotation

| # | Action | Qui | Résultat attendu |
| --- | --- | --- | --- |
| 1 | Rechercher le compte du bénéficiaire dans EntraID | Agent CPA | Compte présent ou absent |
| 2 | Si présent : vérifier la cohérence du modèle de poste appliqué | Agent CPA | Droits cohérents avec la fonction |
| 3 | Si absent : clôturer le ticket, ou le mettre en attente du compte | Agent CPA | Décision tracée |
| 4 | Signaler tout écart de provisionnement au gestionnaire d'IdentityDSI | Agent CPA | Écart remonté |

## Étapes — détection d'un compte orphelin

| # | Action | Qui | Résultat attendu |
| --- | --- | --- | --- |
| 1 | Lors d'un retour ou d'une réaffectation de poste, identifier le compte rattaché | Agent CPA | Compte identifié |
| 2 | Vérifier auprès du service si l'agent est toujours en poste | Agent CPA | Situation établie |
| 3 | Si l'agent a quitté ses fonctions : désactiver le compte et ouvrir un ticket | Agent CPA | Compte neutralisé, trace conservée |
| 4 | Informer le gestionnaire d'IdentityDSI pour traitement définitif | Agent CPA | Circuit de suppression engagé |

## Points de contrôle RGPD

- La suppression du compte emporte la boîte aux lettres et l'espace OneDrive de l'agent. **Cette conséquence est connue et validée par la DPO** ; elle s'applique aussi en cas de mutation interne.
- La désactivation préserve les données, la suppression non. La désactivation est le geste de la cellule ; la suppression relève d'IdentityDSI.
- Toute action manuelle sur un compte est tracée par un ticket : c'est ce qui distingue une intervention légitime d'un accès non justifié à des données personnelles.

## Points de vigilance

- **Le compte naît du contrat, la dotation naît du ticket.** Les deux circuits sont indépendants et peuvent se désynchroniser. La vérification à la dotation est le point de rattrapage.
- Un compte présent mais doté du mauvais modèle de poste est un écart de provisionnement, non un incident à corriger à la main : le corriger localement masquerait la cause.

## Écart non résolu

Aucun audit périodique des comptes inactifs de plus de 90 jours n'est en place. Ce contrôle relève des nouvelles missions à définir pour la cellule.

## Procédures liées

- PROC-STOCK-C02 — Dotation de matériel
- PROC-STOCK-C03 — Retour de matériel
- PROC-ID-C02 — Création d'un compte hors SIRH
