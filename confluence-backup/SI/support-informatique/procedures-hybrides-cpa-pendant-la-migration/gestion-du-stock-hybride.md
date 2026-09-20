<!-- confluence: SI / page 1736806 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/1736806 -->
<!-- parent_id: 1802375 · parent: ⚙️ Procédures hybrides CPA — pendant la migration -->

# Gestion du stock — hybride

**Statut : en vigueur pendant la migration**

Le stock reçoit simultanément du matériel préparé en usine et du matériel classique à préparer en interne. Les deux flux se croisent dans le même local et dans le même inventaire.

## Ce qui diffère selon le poste

| 🟠 Poste MDT | 🔵 Poste Intune |
| --- | --- |
| Étiquetage à réception par la cellule | Étiquetage réalisé en usine |
| Saisie du fichier d'injection GLPI | Import du bon de livraison fournisseur |
| Préparation en atelier avant dotation | Aucune préparation — le poste est enrôlé |

## Ce qui ne diffère pas

Le contrôle du bon de livraison, la règle de non-signature avant vérification, la sécurisation du stock, la réforme et la destruction des supports s'appliquent à l'identique aux deux flux.

## Procédures du domaine

- **PROC-STOCK-H01** — Réception et enregistrement du matériel
- **PROC-STOCK-H02** — Dotation de matériel
- **PROC-STOCK-H03** — Retour de matériel
- **PROC-STOCK-H04** — Réforme et destruction des données

## Point d'attention propre à la période

**Le stock contient deux populations qu'il faut distinguer physiquement.** Un poste enrôlé rangé parmi les postes à préparer sera repréparé inutilement ; un poste legacy rangé parmi les postes prêts sera livré non configuré. Le marquage des zones de rangement est un prérequis, pas un confort.
