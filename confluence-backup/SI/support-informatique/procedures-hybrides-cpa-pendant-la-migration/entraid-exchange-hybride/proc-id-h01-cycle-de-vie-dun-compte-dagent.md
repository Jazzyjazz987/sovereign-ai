<!-- confluence: SI / page 1704178 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/1704178 -->
<!-- parent_id: 1802396 · parent: 👤 EntraID / Exchange — hybride -->

# PROC-ID-H01 — Cycle de vie d'un compte d'agent

| Champ | Valeur |
| --- | --- |
| **Code** | PROC-ID-H01 |
| **Domaine** | EntraID / Exchange — hybride |
| **Statut** | Hybride — applicable pendant la migration |
| **Discriminant** | Service de rattachement de l'agent : 🟠 hors IdentityDSI / 🔵 raccordé à IdentityDSI |
| **Criticité** | Haute |
| **Outils** | Tauturu (GLPI), IdentityDSI, console EntraID, Exchange Online, annuaire local |

> **Règle invariante.** Le compte suit l'agent, pas le poste. Au départ ou à la mutation d'un agent, son compte est **supprimé**, avant d'être recréé si nécessaire pour un autre service. Cette règle est validée par la déléguée à la protection des données et s'applique dans les deux colonnes, sans exception.

> **Attention — le discriminant n'est pas le poste.** Les deux colonnes ne distinguent pas un poste MDT d'un poste Intune : elles distinguent l'**avant** et l'**après** mise en service d'IdentityDSI pour le service auquel l'agent est rattaché.

## 1 — Objet

Cette procédure décrit l'arrivée, la mutation et le départ d'un agent du point de vue de son compte et de sa boîte aux lettres, pendant la période où certains services sont déjà provisionnés par IdentityDSI depuis le SIRH et d'autres ne le sont pas encore.

## 2 — Déterminer l'état du service

1. Identifier le service de rattachement de l'agent dans le ticket.
2. Consulter la liste des services raccordés à IdentityDSI, tenue à jour par la CPA.
3. Service figurant dans cette liste : colonne 🔵. Service absent de la liste : colonne 🟠.
4. Vérifier également si l'agent possède déjà un compte, quel que soit le service : un agent muté depuis un service 🔵 arrive avec un historique de provisionnement.

En cas de doute, traiter le cas selon la colonne 🟠 et signaler l'écart au responsable de cellule.

## 3 — Arrivée d'un agent

### 3.1 — Étapes communes

| # | Action |
| --- | --- |
| 1 | Recevoir le ticket d'arrivée dans Tauturu. Le ticket reste à la charge du service demandeur. |
| 2 | Vérifier la présence des éléments requis : identité de l'agent, service, date d'entrée, fonction, matériel demandé. |
| 3 | Vérifier qu'aucun compte existant n'est déjà rattaché à cet agent. |

### 3.2 — Étapes propres à l'état du service

| # | 🟠 Service hors IdentityDSI | 🔵 Service raccordé à IdentityDSI |
| --- | --- | --- |
| 1 | Créer le compte manuellement dans la console EntraID à partir des informations du ticket. | Vérifier que la fiche de l'agent a été créée dans le SIRH par la DRH. |
| 2 | Appliquer la convention de nommage en vigueur et contrôler l'unicité de l'identifiant. | Attendre le provisionnement du compte par IdentityDSI, puis en contrôler le résultat. |
| 3 | Renseigner manuellement le service, la fonction et le rattachement hiérarchique. | Vérifier que le service et la fonction remontés du SIRH sont exacts. Toute correction se fait dans le SIRH, jamais dans la console. |
| 4 | Affecter manuellement la licence correspondant au profil de l'agent. | Vérifier que la licence a été affectée par l'appartenance au groupe dynamique. |
| 5 | Créer la boîte aux lettres et l'adresse de messagerie selon la convention. | Vérifier la création automatique de la boîte aux lettres et de l'adresse. |
| 6 | Transmettre les éléments de première connexion au responsable du service. | Transmettre les éléments de première connexion au responsable du service. |

### 3.3 — Étapes finales communes

| # | Action |
| --- | --- |
| 1 | Vérifier l'inscription de l'agent à l'authentification multifacteur. |
| 2 | Poursuivre la dotation du matériel selon PROC-STOCK-H02, PROC-ATL-H01 et PROC-TER-H02. |
| 3 | Consigner dans le ticket la colonne appliquée et l'identifiant créé, puis clore le ticket. |

## 4 — Absence de compte au moment de l'intervention

Ce cas se produit dans les deux colonnes, pour des raisons différentes : fiche SIRH non créée côté 🔵, ticket incomplet côté 🟠.

L'agent de la CPA applique l'une des deux issues, et une seule :

- **Clôture du ticket**, si le service demandeur ne peut pas fournir les éléments manquants. Le service recréera un ticket.
- **Mise en attente du ticket**, si le compte est en cours de création et que le délai est connu.

Le motif de l'issue retenue est écrit dans le ticket. L'intervention n'est jamais réalisée « en attendant le compte ».

## 5 — Mutation d'un agent

| # | 🟠 Service hors IdentityDSI | 🔵 Service raccordé à IdentityDSI |
| --- | --- | --- |
| 1 | Recevoir le ticket de mutation et vérifier la date d'effet. | Recevoir le ticket de mutation et vérifier la date d'effet. |
| 2 | Supprimer le compte de l'agent conformément à la règle invariante. | Vérifier que la mutation a été saisie dans le SIRH, ce qui déclenche la suppression du compte. |
| 3 | Créer le nouveau compte du service d'accueil selon le chapitre 3.2, colonne applicable **au service d'accueil**. | Contrôler le provisionnement du nouveau compte, ou basculer sur la colonne 🟠 si le service d'accueil n'est pas raccordé. |
| 4 | Traiter le sort du poste : retour en stock selon PROC-STOCK-H03, ou réaffectation sur site selon PROC-TER-H02. | Traiter le sort du poste : retour en stock selon PROC-STOCK-H03, ou réaffectation sur site selon PROC-TER-H02. |

> Un agent muté d'un service 🔵 vers un service 🟠 change de colonne. La colonne est déterminée par le service d'accueil, pas par celui d'origine.

## 6 — Départ d'un agent

### 6.1 — Étapes propres à l'état du service

| # | 🟠 Service hors IdentityDSI | 🔵 Service raccordé à IdentityDSI |
| --- | --- | --- |
| 1 | Recevoir le ticket de départ, émis par le service. | Recevoir le ticket de départ, ou constater la sortie provisionnée depuis le SIRH. |
| 2 | Supprimer le compte à la date d'effet. | Vérifier que la sortie a été saisie dans le SIRH, puis contrôler la suppression du compte. |
| 3 | Traiter les délégations, redirections et boîtes partagées avant la suppression. | Traiter les délégations, redirections et boîtes partagées avant la suppression. |
| 4 | Émettre ou rattacher le ticket de récupération du poste. | Émettre ou rattacher le ticket de récupération du poste. |

### 6.2 — Filet de sécurité commun

Un compte à supprimer peut être découvert hors de tout ticket de départ, notamment lors de la réaffectation d'un poste. Dans ce cas :

1. Désactiver le compte immédiatement.
2. Créer un ticket pour tracer la découverte.
3. Signaler le cas au service concerné et à la DRH.

IdentityDSI supprime le compte en fin de contrat lorsque l'ensemble des éléments a été restitué. La désactivation est une mesure conservatoire, jamais un état final.

## 7 — Points de vigilance

Points valables dans les deux cas :

- La suppression au départ ou à la mutation est une décision de la déléguée à la protection des données. Elle génère des réclamations d'utilisateurs, qui s'atténueront à mesure que la règle sera connue. Ces réclamations ne justifient pas une dérogation.
- Aucune donnée n'est conservée sur le compte supprimé. Les données utiles sont déplacées **avant** la date d'effet, sur l'espace de stockage de référence du service.
- Un compte désactivé et laissé en l'état est un écart. Il fait l'objet d'un ticket.

| 🟠 Service hors IdentityDSI | 🔵 Service raccordé à IdentityDSI |
| --- | --- |
| La création manuelle expose aux fautes de frappe et aux doublons. Contrôler l'identifiant avant validation. | Toute correction faite directement dans la console est écrasée au prochain cycle de provisionnement. Corriger dans le SIRH. |
| Rien ne déclenche la suppression automatiquement : elle dépend du ticket. Le suivi des départs est manuel. | Un retard de saisie dans le SIRH retarde d'autant le compte. Le délai relève de la DRH, pas de la CPA. |
| Les licences affectées manuellement ne sont pas reprises automatiquement. Les libérer explicitement. | Vérifier que l'agent est bien sorti du groupe dynamique, faute de quoi la licence reste consommée. |

## 8 — Procédures liées

- PROC-ID-H02 — Comptes hors SIRH, boîtes partagées et ressources
- PROC-ID-H03 — Déblocage MFA et gestion des licences
- PROC-STOCK-H02 — Dotation de matériel
- PROC-TER-H02 — Dotation sur site
- PROC-INT-H03 — Retrait et désinscription d'un appareil
