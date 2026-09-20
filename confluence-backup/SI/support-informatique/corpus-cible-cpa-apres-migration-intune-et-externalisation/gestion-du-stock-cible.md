<!-- confluence: SI / page 1703958 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/1703958 -->
<!-- parent_id: 1703937 · parent: 🎯 Corpus cible CPA — après migration Intune et externalisation -->

# Gestion du stock — cible

**Statut : cible à valider**

Le domaine stock est le plus transformé par la migration. Le matériel arrive préparé d'usine ; la cellule ne fabrique plus, elle contrôle, attribue et trace. La saisie disparaît au profit de l'import et de l'inventaire automatique.

## Ce qui change

| Avant | Cible |
| --- | --- |
| Étiquetage manuel à réception | Étiquetage réalisé en usine |
| Fichier d'injection GLPI rempli à la main | Import du bon de livraison fournisseur |
| Double saisie GLPI + Excel SharePoint | Tauturu source unique |
| Inventaire au fil de l'eau | Agent d'inventaire GLPI |
| 7 procédures | 4 procédures |

## Ce qui ne change pas

La réforme, la destruction des supports et la traçabilité RGPD associée restent intégralement manuelles et à la charge de la cellule. **C'est le seul domaine où la non-conformité RGPD de priorité 1 subsiste après migration.**

## Procédures du domaine

- **PROC-STOCK-C01** — Réception et injection du matériel
- **PROC-STOCK-C02** — Dotation de matériel
- **PROC-STOCK-C03** — Retour de matériel
- **PROC-STOCK-C04** — Réforme et destruction des données

## Points d'attention

Le stockage à la DSI est maintenu dans cette version. Un marché imposant le stockage chez le titulaire est envisagé : sa notification entraînera la reprise des procédures C01 et C02.
