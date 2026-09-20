<!-- confluence: SI / page 1704018 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/1704018 -->
<!-- parent_id: 1703958 · parent: 📦 Gestion du stock — cible -->

# PROC-STOCK-C04 — Réforme et destruction des données

|  |  |
| --- | --- |
| **Code** | PROC-STOCK-C04 |
| **Domaine** | Gestion du stock |
| **Statut** | Cible à valider |
| **Criticité** | Haute |
| **Contrainte RGPD** | **Oui — priorité 1** |
| **Outils** | Tauturu, destructeur de supports, registre RGPD |

> **Règle invariante CPA** — Toute dotation, intervention ou action manuelle sur le parc fait l'objet d'un ticket Tauturu.

## Objet

Gérer la sortie définitive d'un équipement du parc, en garantissant la destruction sécurisée des supports de données et la traçabilité exigée par le règlement général sur la protection des données.

**Cette procédure n'est pas affectée par la migration.** Elle reste entièrement manuelle et concentre, à elle seule, la non-conformité la plus grave identifiée en audit.

## Déclencheur

Décision de réforme : obsolescence, panne irréparable, fin de vie.

## Acteurs

| Rôle | Responsabilité |
| --- | --- |
| Responsable de cellule | Décide la réforme et valide la procédure |
| Agent CPA chargé du stock | Extrait et détruit les supports, tient le registre, collecte le certificat |
| Prestataire de réforme | Évacue les carcasses et délivre le certificat de destruction |

## Étapes

| # | Action | Qui | Résultat attendu |
| --- | --- | --- | --- |
| 1 | Créer le ticket Tauturu de réforme, y documenter le motif et la liste des équipements | Responsable de cellule | Décision tracée |
| 2 | Désinscrire l'appareil de la console Intune | Agent CPA | Appareil retiré de la gestion |
| 3 | Extraire physiquement les supports de données | Agent CPA | Supports séparés |
| 4 | Détruire chaque support avec le destructeur de la cellule | Agent CPA | Destruction physique effectuée |
| 5 | **Enregistrer chaque destruction au registre RGPD : numéro de série, type de support, date, agent, méthode** | Agent CPA | Destruction tracée — conformité |
| 6 | Déposer les carcasses en zone d'évacuation | Agent CPA | Carcasses en attente |
| 7 | Récupérer le certificat de destruction auprès du prestataire à l'évacuation | Agent CPA | Certificat obtenu |
| 8 | Archiver le certificat au ticket et au registre | Agent CPA | Archive conforme |
| 9 | Passer le statut Tauturu à « Réformé » | Agent CPA | Inventaire à jour |

## Points de contrôle RGPD

**Écart de priorité 1 — action immédiate requise, indépendamment du projet de migration :**

- Aucun registre de traçabilité des destructions n'existe à ce jour. **Sa création est un prérequis de l'applicabilité de cette procédure** : les étapes 5 et 8 sont inexécutables sans lui.
- Aucun certificat de destruction n'est actuellement collecté auprès du prestataire. Cette exigence doit être portée au contrat, faute de quoi l'étape 7 restera lettre morte.
- Référence : RGPD, article 5.1.f — intégrité et confidentialité des données à caractère personnel.
- Référence : circulaire n° 4748/PR du 15 juillet 2025.

## Points de vigilance

- **Le formatage logiciel ne vaut pas destruction.** Le destructeur physique est l'outil obligatoire, pour les supports magnétiques comme pour les supports flash.
- Le registre doit permettre de retrouver, pour tout numéro de série réformé, la date et les conditions de destruction. C'est ce que demandera le DPO en cas de contrôle.
- L'évacuation par le prestataire donne systématiquement lieu à certificat. Une évacuation sans certificat est une rupture de chaîne de preuve.

## Procédures liées

- PROC-STOCK-C03 — Retour de matériel
- PROC-INT-C05 — Retrait et désinscription d'un appareil
