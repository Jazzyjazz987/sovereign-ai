<!-- confluence: SI / page 1802499 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/1802499 -->
<!-- parent_id: 1802396 · parent: 👤 EntraID / Exchange — hybride -->

# PROC-ID-H02 — Comptes hors SIRH, boîtes partagées et ressources

| Champ | Valeur |
| --- | --- |
| **Code** | PROC-ID-H02 |
| **Domaine** | EntraID / Exchange — hybride |
| **Statut** | Hybride — applicable pendant la migration |
| **Discriminant** | Origine de l'objet : 🟠 objet créé avant IdentityDSI / 🔵 objet créé après IdentityDSI |
| **Criticité** | Haute |
| **Outils** | Tauturu (GLPI), IdentityDSI, console EntraID, Exchange Online |

> **Règle invariante.** Tout objet qui n'est pas un agent du SIRH possède un **propriétaire nommé** et une **date de revue**. Sans ces deux éléments, l'objet n'est pas créé. Cette règle vaut quelle que soit la colonne.

> **Attention — le discriminant n'est pas le poste.** Les deux colonnes distinguent les objets antérieurs à la mise en service d'IdentityDSI, créés à la main et sans propriétaire formalisé, des objets créés depuis, sous le cadre actuel.

## 1 — Objet

Cette procédure traite les objets d'annuaire et de messagerie qui ne proviennent pas du SIRH :

- comptes de prestataire, de stagiaire et comptes temporaires ;
- comptes de service et comptes applicatifs ;
- boîtes aux lettres partagées ;
- listes de distribution ;
- ressources : salles et équipements réservables.

IdentityDSI ne provisionne pas ces objets. Ils restent créés et gérés par la CPA dans les deux colonnes. Ce qui change entre les colonnes, c'est l'état de l'existant et le niveau de contrôle attendu.

## 2 — Déterminer l'état de l'objet

1. Rechercher l'objet dans la console EntraID ou Exchange Online.
2. Consulter sa date de création et la présence d'un propriétaire déclaré.
3. Objet créé avant la mise en service d'IdentityDSI, ou sans propriétaire déclaré : colonne 🟠.
4. Objet créé après, avec propriétaire et date de revue renseignés : colonne 🔵.

Pour une **création**, la colonne est toujours 🔵 : tout nouvel objet est créé sous le cadre actuel.

En cas de doute sur un objet existant, traiter selon la colonne 🟠.

## 3 — Création d'un objet — étapes communes

| # | Action |
| --- | --- |
| 1 | Recevoir le ticket dans Tauturu et identifier la nature de l'objet demandé. |
| 2 | Vérifier que la demande émane d'un responsable de service habilité. |
| 3 | Recueillir le **propriétaire nommé** de l'objet, agent identifié au SIRH. |
| 4 | Recueillir la **date de revue** et, pour un compte temporaire, la date d'expiration. |
| 5 | Vérifier que l'objet n'existe pas déjà sous un autre nom. |
| 6 | Créer l'objet selon la convention de nommage propre à sa nature. |
| 7 | Renseigner le propriétaire et la date de revue dans les attributs de l'objet. |
| 8 | Affecter la licence uniquement si la nature de l'objet l'exige. |
| 9 | Consigner la création dans le ticket et clore. |

> Un compte temporaire est créé avec une date d'expiration effective, jamais « pour la durée de la mission ».

## 4 — Traitement de l'existant

| # | 🟠 Objet antérieur à IdentityDSI | 🔵 Objet créé sous le cadre actuel |
| --- | --- | --- |
| 1 | Identifier le propriétaire réel par enquête auprès du service utilisateur. | Le propriétaire est renseigné dans l'objet. Aucune enquête n'est nécessaire. |
| 2 | Renseigner rétroactivement le propriétaire et une date de revue dans l'objet. | Vérifier que la date de revue n'est pas dépassée. |
| 3 | Si aucun propriétaire n'est identifiable, désactiver l'objet et créer un ticket de décision. | Si le propriétaire a quitté la collectivité, demander au service un nouveau propriétaire avant la date de revue. |
| 4 | Vérifier que l'objet est encore utilisé : dernière connexion, dernière réception, dernière réservation. | Vérifier l'usage de l'objet lors de la revue périodique. |
| 5 | Retirer les délégations accordées à des agents partis. | Contrôler que les délégations correspondent aux agents encore en poste. |
| 6 | Inscrire l'objet régularisé dans le registre des objets hors SIRH. | L'objet figure déjà au registre. |

## 5 — Revue périodique — commune aux deux colonnes

| # | Action |
| --- | --- |
| 1 | À échéance de la date de revue, adresser au propriétaire une demande de confirmation. |
| 2 | Objet confirmé : reporter la date de revue et consigner la confirmation. |
| 3 | Objet non confirmé dans le délai : désactiver l'objet, sans le supprimer. |
| 4 | Objet désactivé et non réclamé au terme du délai de conservation : supprimer l'objet et consigner la suppression. |
| 5 | Mettre à jour le registre des objets hors SIRH. |

## 6 — Points de vigilance

Points valables dans les deux cas :

- Un compte de service ne porte jamais le nom d'un agent. Son nom désigne la fonction, pas la personne.
- Une boîte partagée n'est pas un contournement de la suppression du compte d'un agent parti. Les deux sujets sont distincts.
- Les objets hors SIRH échappent au provisionnement automatique : ils ne sont maîtrisés que par la revue. Une revue non tenue vaut absence de maîtrise.
- Le registre des objets hors SIRH est la seule vue complète de ce périmètre. Il est tenu à jour à chaque création, régularisation et suppression.

| 🟠 Objet antérieur à IdentityDSI | 🔵 Objet créé sous le cadre actuel |
| --- | --- |
| Le stock d'objets orphelins est la principale source de risque du domaine. Le traiter par lots planifiés, pas au fil de l'eau. | Le risque porte sur le respect de la date de revue, pas sur l'identification du propriétaire. |
| La désactivation d'un objet dont le propriétaire est inconnu peut interrompre un service métier. Prévenir le service avant d'agir. | Un propriétaire parti laisse un objet sans responsable. Traiter le cas au départ de l'agent, pas à la revue suivante. |

## 7 — Procédures liées

- PROC-ID-H01 — Cycle de vie d'un compte d'agent
- PROC-ID-H03 — Déblocage MFA et gestion des licences
