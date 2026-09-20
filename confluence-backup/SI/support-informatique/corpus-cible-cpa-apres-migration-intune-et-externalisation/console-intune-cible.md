<!-- confluence: SI / page 1802241 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/1802241 -->
<!-- parent_id: 1703937 · parent: 🎯 Corpus cible CPA — après migration Intune et externalisation -->

# Console Intune — cible

**Statut : cible à valider**

Intune devient la source de vérité technique du parc : conformité, applications, chiffrement. Tauturu reste la source de vérité patrimoniale. La console est co-administrée avec la Cellule Sécurité Opérationnelle.

## Ce qui change

| Avant | Cible |
| --- | --- |
| Enrôlement Autopilot par extraction du hash en atelier | Hash injecté et appareil enrôlé par le fournisseur |
| Packaging assuré par la CPA | Packaging assuré par la CPA ou la CSO, selon l'affectation du ticket |
| Périmètre de responsabilité non formalisé avec la CSO | Répartition établie, voir la matrice RACI cible |

## Ce qui ne change pas

Les politiques de conformité et de configuration — BitLocker, LAPS, lignes de base Defender — restent figées dans la configuration, aux paramètres actuels. La conformité est obtenue par construction : un poste enrôlé est conforme.

## Procédures du domaine

- **PROC-INT-C01** — Attribution d'un appareil enrôlé
- **PROC-INT-C02** — Enrôlement et gestion des tablettes Android Enterprise
- **PROC-INT-C03** — Packaging et déploiement d'une application
- **PROC-INT-C04** — Gestion des profils et groupes dynamiques
- **PROC-INT-C05** — Retrait et désinscription d'un appareil

## Points d'attention

Le packaging est réalisé indifféremment par un agent CPA ou CSO selon l'affectation du ticket. Faute de règle d'affectation écrite, les tickets rebondiront entre les deux cellules : la procédure C03 nomme qui affecte et sur quel critère.

Deux écarts relevés en audit restent ouverts et ne sont pas résolus par la migration : l'absence de versioning et de revue par les pairs des scripts PowerShell, et l'absence de veille sur les mises à jour applicatives.
