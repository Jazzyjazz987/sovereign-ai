<!-- confluence: SI / page 1769593 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/1769593 -->
<!-- parent_id: 1703937 · parent: 🎯 Corpus cible CPA — après migration Intune et externalisation -->

# Matrice RACI cible

**Statut : cible à valider** — 20 procédures · 5 domaines · 7 acteurs

Cette matrice est la source de vérité des responsabilités dans l'organisation cible. Toute modification d'une procédure s'accompagne d'une mise à jour de cette page.

## Légende

| Code | Signification | Portée |
| --- | --- | --- |
| **R** | Réalise | Exécute l'action |
| **A** | Approuve | Valide ou arbitre — un seul A par ligne |
| **C** | Consulté | Fournit un avis ou une expertise avant ou pendant l'action |
| **I** | Informé | Est notifié du résultat |
| — | Hors périmètre | N'intervient pas |

## Acteurs

| Acteur | Périmètre |
| --- | --- |
| **RC** | Responsable de cellule CPA |
| **CPA** | Agent CPA polyvalent — console, stock, identités |
| **ATL** | Agent CPA en fonction atelier |
| **TER** | Agent CPA en fonction terrain ou télé-assistance |
| **CSO** | Cellule Sécurité Opérationnelle |
| **IDSI** | IdentityDSI et DRH, par le SIRH |
| **FOU** | Fournisseur titulaire du marché |

> **Principe de polyvalence** — Les agents disposent des mêmes accès aux outils. Les colonnes CPA, ATL et TER désignent des responsabilités fonctionnelles, non des habilitations différenciées. Tout agent peut exécuter toute procédure en l'absence de son titulaire habituel.

## Matrice

### 📦 Gestion du stock

| Procédure | RC | CPA | ATL | TER | CSO | IDSI | FOU |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C01 — Réception et injection | **A** | **R** | C | — | — | — | C |
| C02 — Dotation de matériel | **A** | **R** | I | C | — | I | — |
| C03 — Retour de matériel | I | **R** | C | C | — | I | — |
| C04 — Réforme et destruction | **A** | **R** | C | — | I | — | C |

### 🔧 Atelier

| Procédure | RC | CPA | ATL | TER | CSO | IDSI | FOU |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C01 — SAV et incidents N2 | **A** | C | **R** | C | — | — | C |
| C02 — Contrôle de conformité | **A** | C | **R** | — | — | — | C |

### 🚗 Agents de proximité terrain

| Procédure | RC | CPA | ATL | TER | CSO | IDSI | FOU |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C01 — Planification et priorisation | **A** | C | C | **R** | — | — | — |
| C02 — Dotation sur site | I | C | I | **R** | — | — | — |
| C03 — Dépannage N1 sur site | I | C | C | **R** | I | — | — |
| C04 — Télé-assistance et îles | **A** | C | C | **R** | C | — | — |

### 🖥️ Console Intune

| Procédure | RC | CPA | ATL | TER | CSO | IDSI | FOU |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C01 — Attribution d'un appareil enrôlé | I | **R** | C | I | — | — | **A** |
| C02 — Tablettes Android Enterprise | **A** | **R** | C | I | I | — | — |
| C03 — Packaging et déploiement | **A** | **R** | — | I | **R** | — | — |
| C04 — Profils et groupes dynamiques | **A** | **R** | — | I | C | I | — |
| C05 — Retrait et désinscription | **A** | **R** | C | — | C | — | — |

### 👤 EntraID / Exchange

| Procédure | RC | CPA | ATL | TER | CSO | IDSI | FOU |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C01 — Vérification des comptes provisionnés | I | **R** | — | C | — | **A** | — |
| C02 — Création d'un compte hors SIRH | **A** | **R** | — | — | C | I | — |
| C03 — BALP et ressources Exchange | **A** | **R** | — | — | — | — | — |
| C04 — Déblocage et réinitialisation MFA | I | **R** | — | C | **A** | — | — |
| C05 — Licences M365 | **A** | **R** | — | — | — | C | — |

## Lectures particulières

**PROC-INT-C03 comporte deux R.** C'est délibéré : le packaging est réalisé par un agent CPA **ou** par un agent CSO, selon l'affectation du ticket. Le responsable de cellule affecte, et c'est cette affectation qui désigne le R effectif sur chaque occurrence. Les applications stratégiques de la CSO sont intégrées en phase de tests.

**PROC-INT-C01 porte le A sur le fournisseur.** L'enrôlement et le tag sont réalisés en usine selon une procédure certifiée : la conformité de l'appareil relève du titulaire du marché, la cellule l'attribue et la contrôle.

**PROC-ID-C01 porte le A sur IdentityDSI.** Le cycle de vie des comptes d'agents sous contrat est piloté par le SIRH. La cellule vérifie, signale et désactive ; elle ne décide pas.

**PROC-ID-C04 porte le A sur la CSO.** Un blocage consécutif à une détection de risque est un incident de sécurité avant d'être une demande de support.

## Charge par acteur

| Acteur | Procédures pilotées (R) | Procédures validées (A) |
| --- | --- | --- |
| **Responsable de cellule** | — | 12 |
| **Agent CPA** | 12 | — |
| **Agent atelier** | 2 | — |
| **Agent terrain** | 4 | — |
| **CSO** | 1 (partagée) | 1 |
| **IdentityDSI** | — | 1 |
| **Fournisseur** | — | 1 |

## Procédures sous contrainte RGPD

Huit procédures sur vingt portent une contrainte RGPD explicite, soit deux sur cinq.

| Code | Procédure | Enjeu |
| --- | --- | --- |
| STOCK-C03 | Retour de matériel | Données présentes sur le poste retourné |
| STOCK-C04 | Réforme et destruction | **Registre et certificats — écart de priorité 1** |
| TER-C04 | Télé-assistance et îles | Consentement à la prise en main |
| INT-C05 | Retrait et désinscription | Traçabilité des effacements |
| ID-C01 | Vérification des comptes | Suppression emportant les données |
| ID-C02 | Compte hors SIRH | Accès de tiers aux données de l'administration |
| ID-C03 | BALP et ressources | Accès à la correspondance |
| ID-C04 | Déblocage MFA | Vérification d'identité avant réinitialisation |
