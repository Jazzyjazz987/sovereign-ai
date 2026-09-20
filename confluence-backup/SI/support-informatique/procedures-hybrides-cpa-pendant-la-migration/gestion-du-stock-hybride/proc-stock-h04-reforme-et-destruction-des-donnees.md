<!-- confluence: SI / page 1736907 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/1736907 -->
<!-- parent_id: 1736806 · parent: 📦 Gestion du stock — hybride -->

# PROC-STOCK-H04 — Réforme et destruction des données

|  |  |
| --- | --- |
| **Code** | PROC-STOCK-H04 |
| **Domaine** | Gestion du stock |
| **Statut** | En vigueur pendant la migration |
| **Discriminant** | État du poste réformé |
| **Criticité** | Haute |
| **Contrainte RGPD** | **Oui — priorité 1** |

> **Règle invariante CPA** — Toute dotation, intervention ou action manuelle sur le parc fait l'objet d'un ticket Tauturu.

## Objet

Sortir définitivement un équipement du parc, en garantissant la destruction sécurisée des supports de données et la traçabilité exigée par le RGPD.

**La migration ne change presque rien à cette procédure.** Seule l'étape de retrait de la gestion diffère. Le reste — extraction, destruction physique, registre, certificat — est identique et reste entièrement manuel.

## Déclencheur

Décision de réforme : obsolescence, panne irréparable, fin de vie.

## Étape propre à l'état du poste

| # | 🟠 Poste MDT | 🔵 Poste Intune |
| --- | --- | --- |
| 2 | Retirer le poste des inventaires de déploiement et du fichier Excel de suivi | Désinscrire l'appareil de la console Intune — voir PROC-INT-H03 |

## Étapes communes

| # | Action | Qui |
| --- | --- | --- |
| 1 | Créer le ticket Tauturu de réforme, y documenter le motif et la liste des équipements | Responsable de cellule |
| 3 | Extraire physiquement les supports de données | Agent CPA |
| 4 | Détruire chaque support avec le destructeur de la cellule | Agent CPA |
| 5 | **Enregistrer chaque destruction au registre RGPD : numéro de série, type de support, date, agent, méthode** | Agent CPA |
| 6 | Déposer les carcasses en zone d'évacuation | Agent CPA |
| 7 | Récupérer le certificat de destruction auprès du prestataire à l'évacuation | Agent CPA |
| 8 | Archiver le certificat au ticket et au registre | Agent CPA |
| 9 | Passer le statut Tauturu à « Réformé » | Agent CPA |

## Points de contrôle RGPD

**Écart de priorité 1 — action immédiate requise, indépendamment de la migration :**

- Aucun registre de traçabilité des destructions n'existe à ce jour. **Sa création est un prérequis de l'applicabilité de cette procédure** : les étapes 5 et 8 sont inexécutables sans lui.
- Aucun certificat de destruction n'est collecté auprès du prestataire. L'exigence doit être portée au contrat.
- Référence : RGPD, article 5.1.f. Circulaire n° 4748/PR du 15 juillet 2025.

## Points de vigilance

**Communs**

- Le formatage logiciel ne vaut pas destruction. Le destructeur physique est l'outil obligatoire.
- Une évacuation sans certificat est une rupture de chaîne de preuve.

| 🟠 Poste MDT | 🔵 Poste Intune |
| --- | --- |
| Le poste n'est référencé dans aucune console : vérifier qu'il sort bien de tous les inventaires locaux | La désinscription de la console **n'efface pas les données** : elle ne dispense en aucun cas des étapes 3 à 5 |

**Le volume de réforme augmente pendant la migration.** Le remplacement du parc legacy produit un flux de postes à réformer sans commune mesure avec le rythme habituel. Sans registre en place, c'est précisément la période où le plus grand nombre de destructions se fera sans trace — et la période sur laquelle portera un éventuel contrôle.

## Procédures liées

- PROC-STOCK-H03 — Retour de matériel
- PROC-INT-H03 — Retrait et désinscription d'un appareil
