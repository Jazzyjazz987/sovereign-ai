<!-- confluence: SI / page 1769613 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/1769613 -->
<!-- parent_id: 1736867 · parent: 🖥️ Console Intune — hybride -->

# PROC-INT-H03 — Retrait et désinscription d'un appareil

| Champ | Valeur |
| --- | --- |
| **Code** | PROC-INT-H03 |
| **Domaine** | Console Intune — hybride |
| **Statut** | Hybride — applicable pendant la migration |
| **Discriminant** | État du poste retiré : 🟠 poste MDT / 🔵 poste Intune |
| **Criticité** | Haute |
| **Outils** | Tauturu (GLPI), console Intune, service Autopilot, atelier CPA |

> **Règle invariante.** Un poste retiré du service est sorti de toutes les chaînes qui le connaissent, et pas seulement de celle qui l'a déployé. Tant que le poste reste inscrit quelque part, il continue de compter dans les tableaux de bord et de fausser le suivi du parc.

## 1 — Objet

Cette procédure décrit le retrait d'un appareil du service : réforme, panne définitive, restitution au fournisseur ou réaffectation nécessitant une remise à zéro.

Elle couvre les postes déployés par MDT comme les postes enrôlés dans Intune.

## 2 — Déterminer l'état du poste

1. Ouvrir la fiche du poste dans Tauturu et relever son numéro de série.
2. Rechercher ce numéro de série dans la console Intune.
3. Le poste présent dans la console Intune est un poste 🔵. Sinon, c'est un poste 🟠.
4. Rechercher également le numéro de série dans le service Autopilot : un poste peut être inscrit à Autopilot en usine sans avoir jamais été enrôlé. Ce cas est traité au chapitre 5.

En cas de doute, traiter le poste comme un poste 🟠.

## 3 — Étapes communes — préparation du retrait

| # | Action |
| --- | --- |
| 1 | Recevoir ou créer le ticket de retrait dans Tauturu et en identifier le motif : réforme, panne, restitution, réaffectation. |
| 2 | Récupérer physiquement l'appareil et ses accessoires. |
| 3 | Vérifier auprès de l'utilisateur ou du service que les données utiles ont été déplacées sur l'espace de stockage de référence. |
| 4 | Vérifier qu'aucun compte de service ni aucune licence spécifique ne reste attaché à l'appareil. |

## 4 — Étapes propres à l'état du poste

| # | 🟠 Poste MDT | 🔵 Poste Intune |
| --- | --- | --- |
| 1 | Retirer le poste de l'annuaire local et de tout groupe de déploiement qui le référence. | Lancer la désinscription de l'appareil depuis la console Intune. |
| 2 | Effacer le disque en atelier par redéploiement ou par effacement sécurisé. | Déclencher l'action de réinitialisation ou d'effacement, puis contrôler son aboutissement dans la console. |
| 3 | *Sans objet — le poste n'est pas inscrit à Autopilot par la chaîne MDT.* | Décider du sort de l'inscription Autopilot : elle est **conservée** si le poste est réaffecté, **supprimée** si le poste quitte le parc. |
| 4 | Retirer le poste du partage de déploiement et de la séquence de tâches, s'il y figure nominativement. | Retirer l'appareil des groupes d'affectation d'applications et de configuration. |
| 5 | Vérifier qu'aucun enregistrement résiduel ne subsiste dans l'annuaire local. | Vérifier dans la console que l'appareil n'apparaît plus, ni comme appareil géré, ni comme appareil en attente. |

## 5 — Cas particulier : poste inscrit à Autopilot mais jamais enrôlé

Ce cas est propre à la période de migration : des postes sont livrés avec le hash injecté en usine et le tag défini, puis déployés par MDT faute d'avoir été enrôlés.

| # | Action |
| --- | --- |
| 1 | Traiter le poste selon la colonne 🟠 pour l'effacement et l'annuaire local. |
| 2 | Traiter l'inscription Autopilot selon l'étape 3 de la colonne 🔵 : conserver si réaffectation, supprimer si sortie du parc. |
| 3 | Mentionner explicitement ce double traitement dans le ticket. |

## 6 — Étapes finales communes

| # | Action |
| --- | --- |
| 1 | Mettre à jour le statut du poste dans Tauturu : réformé, en panne, restitué ou en stock. |
| 2 | Poursuivre selon PROC-STOCK-H03 en cas de retour en stock, ou selon PROC-STOCK-H04 en cas de réforme. |
| 3 | Consigner dans le ticket les chaînes dont le poste a été retiré. |
| 4 | Clore le ticket. |

## 7 — Points de vigilance

Points valables dans les deux cas :

- L'effacement est contrôlé, jamais supposé. Un poste dont l'effacement n'a pas été vérifié ne quitte pas l'atelier.
- Un poste retiré physiquement mais laissé actif dans un outil fausse durablement l'inventaire.
- La destruction ou la restitution d'un support de données relève de PROC-STOCK-H04 et des obligations de protection des données.

| 🟠 Poste MDT | 🔵 Poste Intune |
| --- | --- |
| L'oubli du retrait de l'annuaire local laisse un objet orphelin qui peut être réutilisé par erreur. | Supprimer l'inscription Autopilot d'un poste destiné à être réaffecté oblige à réinjecter le hash, opération à éviter. |
| Aucun contrôle automatique : la vérification est manuelle et doit être tracée dans le ticket. | Une désinscription lancée sur un appareil hors tension reste en attente. Vérifier l'aboutissement avant de clore. |

## 8 — Procédures liées

- PROC-INT-H01 — Enrôlement et attribution d'un appareil
- PROC-STOCK-H03 — Retour de matériel
- PROC-STOCK-H04 — Réforme et destruction des données
- PROC-ID-H01 — Cycle de vie d'un compte d'agent
