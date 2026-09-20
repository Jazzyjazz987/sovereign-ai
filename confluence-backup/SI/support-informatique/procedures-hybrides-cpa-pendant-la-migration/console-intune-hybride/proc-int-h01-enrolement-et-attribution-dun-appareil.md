<!-- confluence: SI / page 1737007 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/1737007 -->
<!-- parent_id: 1736867 · parent: 🖥️ Console Intune — hybride -->

# PROC-INT-H01 — Enrôlement et attribution d'un appareil

|  |  |
| --- | --- |
| **Code** | PROC-INT-H01 |
| **Domaine** | Console Intune |
| **Statut** | En vigueur pendant la migration |
| **Discriminant** | Origine de l'appareil |
| **Criticité** | Haute |

> **Règle invariante CPA** — Toute dotation, intervention ou action manuelle sur le parc fait l'objet d'un ticket Tauturu.

## Objet

Inscrire un appareil dans la console et le rattacher au bon profil de déploiement.

**Deux origines coexistent :** les appareils enrôlés par le fournisseur, et ceux que la cellule enrôle elle-même — matériel de l'ancien marché, ou poste legacy migré.

## Déterminer l'origine

| Constat | Colonne |
| --- | --- |
| L'appareil figure déjà dans la console à réception | 🔵 Enrôlé par le fournisseur |
| L'appareil n'y figure pas et doit être inscrit | 🟠 Enrôlement par la cellule |

## Étapes

| # | 🟠 Enrôlement par la cellule | 🔵 Enrôlé par le fournisseur |
| --- | --- | --- |
| 1 | Vérifier l'éligibilité de l'appareil : Windows 11, TPM 2.0 | *Sans objet — vérifié en amont* |
| 2 | Extraire le hash matériel de l'appareil | *Sans objet — injecté en usine* |
| 3 | Enregistrer le hash dans la console | *Sans objet* |
| 4 | Affecter le tag de groupe de déploiement | Vérifier le tag affecté en usine, et le corriger s'il ne correspond pas au besoin |
| 5 | Lancer le préprovisionnement ; procéder à une réinitialisation si le réseau du service destinataire l'exige | *Sans objet — l'appareil est prêt* |
| 6 | Vérifier l'appartenance aux groupes dynamiques attendus | Vérifier l'appartenance aux groupes dynamiques attendus |
| 7 | Contrôler l'application des politiques : chiffrement, rotation des mots de passe administrateur, antivirus, EDR | Contrôler l'application des politiques |
| 8 | Documenter l'enrôlement dans le ticket | Documenter l'attribution dans le ticket |
| 9 | Mettre à jour le statut dans Tauturu | Mettre à jour le statut dans Tauturu |

## Cas particulier : migration d'un poste legacy

Un poste MDT éligible peut être enrôlé plutôt que remplacé. Il suit alors la colonne 🟠, avec trois précautions supplémentaires :

| # | Action |
| --- | --- |
| a | **Sauvegarder les données locales avant enrôlement** — l'opération efface le poste |
| b | Vérifier que l'agent bénéficiaire dispose bien d'un accès à SharePoint avant de lui retirer ses serveurs de fichiers |
| c | Retirer le poste des inventaires de déploiement legacy pour éviter qu'il ne soit repris par une séquence MDT |

L'étape **c** est celle qu'on oublie : un poste enrôlé mais toujours référencé côté legacy peut être réinstallé par erreur lors d'une campagne, ce qui annule la migration et efface le poste une seconde fois.

## Points de vigilance

| 🟠 Enrôlement par la cellule | 🔵 Enrôlé par le fournisseur |
| --- | --- |
| L'enrôlement exige une connexion Internet au premier démarrage : à vérifier avant d'envoyer un poste aux îles | Aucune contrainte de connexion : le poste arrive inscrit |
| L'extraction du hash est manuelle : une erreur de saisie produit un appareil introuvable dans la console | La procédure d'injection en usine est certifiée ; un écart relève du fournisseur et se traite par lot |
| Prévoir de 30 min à 2 h selon que la réinitialisation est nécessaire | Quelques minutes de contrôle |

**Le tag conditionne tout le reste** — profil, groupes, applications. Une erreur de tag ne se voit qu'à l'ouverture de session du bénéficiaire, et c'est lui qui la découvre.

## Procédures liées

- PROC-ATL-H01 — Préparation ou contrôle d'un poste avant dotation
- PROC-STOCK-H02 — Dotation de matériel
- PROC-INT-H03 — Retrait et désinscription d'un appareil
