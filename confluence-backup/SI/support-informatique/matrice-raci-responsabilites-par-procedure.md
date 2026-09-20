<!-- confluence: SI / page 98624 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/98624 -->
<!-- parent_id: 65813 · parent: Support informatique -->

# Matrice RACI — Procédures opérationnelles CPA

**31 procédures · 5 domaines · 6 rôles**  |  5 procédures RGPD  18 procédures criticité haute  
  
_Cette matrice est la source de vérité des responsabilités CPA. Toute modification d'une procédure doit s'accompagner d'une mise à jour de cette page._

## Légende

| Code | Signification | Description |
| --- | --- | --- |
| R/A | Responsable + Autorité | Exécute l'action ET valide le résultat — rôle pivot de la procédure |
| R | Responsable | Exécute l'action |
| A | Autorité | Valide, approuve ou arbitre — un seul A par procédure |
| C | Consulté | Fournit une expertise ou un avis avant ou pendant l'action |
| I | Informé | Est notifié du résultat — ne participe pas à l'exécution |

**Principe polyvalence CPA :** tous les agents disposent des mêmes droits d'accès aux outils. La matrice RACI reflète les _responsabilités fonctionnelles_ par rôle, pas des droits techniques différenciés. N'importe quel agent peut exécuter n'importe quelle procédure en cas d'absence de son titulaire habituel.

## Matrice complète

| Code | Procédure | Chef CPA | Agt atelier | Agt terrain | Gest. stock | Gest. comptes | Téléassis. | RGPD | Criticité |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **📦 GESTION DU STOCK** |  |  |  |  |  |  |  |  |  |
| `STOCK-001` | Réception et contrôle livraison | A | C | — | R/A | — | — | — | Haute |
| `STOCK-002` | Étiquetage et injection GLPI | I | C | — | R/A | — | — | — | Haute |
| `STOCK-003` | Inventaire périodique | A | C | — | R | — | — | — | Moyenne |
| `STOCK-004` | Dotation matériel | A | R/A | R | C | — | — | — | Haute |
| `STOCK-005` | Retour matériel | I | C | R | R | — | — | RGPD | Moyenne |
| `STOCK-006` | Réforme et destruction | A | — | — | R/A | — | — | RGPD | Haute |
| `STOCK-007` | Marchés publics et achats | R/A | — | — | C | — | — | — | Haute |
| **🔧 ATELIER** |  |  |  |  |  |  |  |  |  |
| `ATL-001` | Préparation poste MDT | I | R/A | — | — | C | — | — | Haute |
| `ATL-002` | Préparation poste Intune/Autopilot | I | R/A | — | — | C | — | — | Haute |
| `ATL-003` | SAV et incidents N2 | A | R/A | C | — | — | I | — | Moyenne |
| `ATL-004` | Maintenance image MDT | R/A | C | — | — | R | — | — | Haute |
| `ATL-005` | Organisation physique et KPI | A | R/A | — | I | — | — | — | Faible |
| **🚗 AGENTS DE PROXIMITÉ TERRAIN** |  |  |  |  |  |  |  |  |  |
| `TER-001` | Planification et priorisation | A | C | R/A | — | — | I | — | Haute |
| `TER-002` | Dotation sur site | I | C | R/A | I | — | — | — | Haute |
| `TER-003` | Dépannage N1 sur site | I | C | R/A | — | — | C | — | Moyenne |
| `TER-004` | Téléassistance et escalade | A | R | C | — | — | R/A | — | Moyenne |
| `TER-005` | Interventions îles éloignées | A | I | R | C | — | R/A | — | Moyenne |
| `TER-006` | Récupération matériel | I | A | R | C | — | — | RGPD | Moyenne |
| **🖥️ CONSOLE INTUNE** |  |  |  |  |  |  |  |  |  |
| `INT-001` | Enrôlement Autopilot Windows 11 | I | R/A | — | — | C | — | — | Haute |
| `INT-002` | Enrôlement Android Enterprise | I | R/A | — | — | C | — | — | Moyenne |
| `INT-003` | Packaging et déploiement application | A | R | — | — | R/A | — | — | Haute |
| `INT-004` | Gestion profils et groupes Intune | A | R | — | — | R/A | — | — | Haute |
| `INT-005` | Retrait et désinscription appareil | A | R/A | — | — | C | — | RGPD | Haute |
| `INT-006` | SecOps — alertes Harfanglab/Defender | R/A | C | — | — | R | — | — | Haute |
| **👤 ENTRAID / EXCHANGE** |  |  |  |  |  |  |  |  |  |
| `ID-001` | Création compte utilisateur | I | — | — | — | R/A | — | — | Haute |
| `ID-002` | Modification compte | I | — | — | — | R/A | — | — | Moyenne |
| `ID-003` | Désactivation et suppression | A | — | — | — | R/A | — | RGPD | Haute |
| `ID-004` | Déblocage et réinitialisation MFA | I | — | — | — | R/A | C | — | Moyenne |
| `ID-005` | Création et gestion BALP | I | — | — | — | R/A | — | — | Moyenne |
| `ID-006` | Gestion ressources Exchange | I | — | — | — | R/A | — | — | Faible |
| `ID-007` | Attribution et suivi licences M365 | R/A | — | — | — | R | — | — | Haute |

## Lecture par rôle

| Rôle | Procédures R/A (pilote) | Procédures A (valide) | Charge principale |
| --- | --- | --- | --- |
| Chef de cellule CPA | STOCK-007, ATL-004, INT-006, ID-007 | STOCK-001/003/004/006, ATL-003/005, TER-001/004/005, INT-003/004/005, ID-003 | Autorité transversale, sécurité, marchés |
| Agent atelier | ATL-001/002/003/005, INT-001/002/005 | TER-006 | Préparation postes, SAV, enrôlement Intune |
| Agent de proximité terrain | TER-001/002/003 | — | Dotations sur site, dépannage N1 |
| Gestionnaire de stock | STOCK-001/002/004/005/006 | — | Cycle de vie matériel, RGPD destructions |
| Gestionnaire de comptes (ingénieur) | ATL-004, INT-003/004, ID-001/002/003/004/005/006 | — | Identités, Exchange, Intune avancé |
| Agent téléassistance | TER-004/005 | — | Support à distance, escalade, îles |

## Procédures à contrainte RGPD — Surveillance renforcée

| Code | Procédure | Risque RGPD | Action prioritaire |
| --- | --- | --- | --- |
| STOCK-005 | Retour matériel | Conservation données 30 jours non formalisée | Formaliser la politique de rétention |
| STOCK-006 | Réforme et destruction | Absence de registre et de certificats de destruction | P1 — IMMÉDIAT |
| TER-006 | Récupération matériel | Données personnelles sur poste récupéré | Appliquer systématiquement STOCK-005 |
| INT-005 | Retrait appareil Intune | Effacement données — traçabilité obligatoire | Documenter chaque effacement dans Tauturu |
| ID-003 | Désactivation compte utilisateur | Suppression sans archivage préalable | P1 — IMMÉDIAT |
