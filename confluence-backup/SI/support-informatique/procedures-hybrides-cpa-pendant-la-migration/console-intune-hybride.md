<!-- confluence: SI / page 1736867 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/1736867 -->
<!-- parent_id: 1802375 · parent: ⚙️ Procédures hybrides CPA — pendant la migration -->

# Console Intune — hybride

**Statut : en vigueur pendant la migration**

La console ne gère qu'une partie du parc. Tout raisonnement fondé sur ce qu'elle affiche doit tenir compte de ce que le parc contient en plus.

## Ce qui diffère selon le poste

| 🟠 Poste MDT | 🔵 Poste Intune |
| --- | --- |
| Absent de la console | Présent, avec état de conformité |
| Applications déployées par script ou installation manuelle | Applications déployées par la console |
| Pas de politique de sécurité poussée à distance | BitLocker, LAPS et lignes de base appliqués |
| Retrait : effacement manuel avant réforme | Retrait : désinscription puis effacement |

## Deux modes d'enrôlement coexistent

| Provenance | Mode |
| --- | --- |
| Commande sous l'ancien marché | Extraction du hash et enregistrement par la cellule |
| Commande sous le nouveau marché | Hash injecté et appareil enrôlé par le fournisseur |

Les deux se rencontrent aujourd'hui, selon le marché sur lequel le matériel a été commandé. PROC-INT-H01 traite les deux cas.

## Procédures du domaine

- **PROC-INT-H01** — Enrôlement et attribution d'un appareil
- **PROC-INT-H02** — Packaging et déploiement d'une application
- **PROC-INT-H03** — Retrait et désinscription d'un appareil

## Point d'attention propre à la période

**La console ne reflète pas le parc.** Un rapport de conformité à 100 % ne signifie pas que le parc est conforme : il signifie que les postes enrôlés le sont. Les postes MDT n'y figurent pas et ne sont donc ni mesurés ni protégés par les politiques. Toute restitution d'indicateurs doit préciser le périmètre couvert, sous peine de donner une image faussement rassurante.
