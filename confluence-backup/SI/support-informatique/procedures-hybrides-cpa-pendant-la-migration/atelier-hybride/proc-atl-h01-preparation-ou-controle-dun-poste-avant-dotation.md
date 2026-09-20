<!-- confluence: SI / page 1704158 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/1704158 -->
<!-- parent_id: 1736826 · parent: 🔧 Atelier — hybride -->

# PROC-ATL-H01 — Préparation ou contrôle d'un poste avant dotation

|  |  |
| --- | --- |
| **Code** | PROC-ATL-H01 |
| **Domaine** | Atelier |
| **Statut** | En vigueur pendant la migration |
| **Discriminant** | État du poste |
| **Criticité** | Haute |
| **Outils** | Cluster MDT, switch PXE, console Intune, Tauturu |

> **Règle invariante CPA** — Toute dotation, intervention ou action manuelle sur le parc fait l'objet d'un ticket Tauturu.

## Objet

Rendre un poste utilisable avant sa remise au bénéficiaire.

**C'est la procédure la plus dissymétrique du corpus hybride.** Sur un poste MDT, l'atelier fabrique la configuration en deux heures. Sur un poste Intune, il vérifie en quelques minutes une configuration déjà appliquée.

## Déterminer l'état du poste

| Vérification | Résultat | Colonne |
| --- | --- | --- |
| L'appareil figure-t-il dans la console Intune ? | Oui | 🔵 |
|  | Non | 🟠 |
| Le poste dispose-t-il d'un TPM 2.0 et est-il éligible à Windows 11 ? | Non | 🟠 obligatoirement |

## Étapes

| # | 🟠 Poste MDT | 🔵 Poste Intune |
| --- | --- | --- |
| 1 | Vérifier le ticket de dotation et le type de poste à préparer | Vérifier le ticket de dotation et identifier l'appareil par son numéro de série |
| 2 | Connecter le poste au réseau PXE dédié | Vérifier la présence de l'appareil dans la console et la cohérence du tag de déploiement |
| 3 | Démarrer en mode PXE et sélectionner l'image appropriée | Corriger le tag si le profil attendu diffère du profil affecté |
| 4 | Lancer le déploiement MDT et attendre — environ 2 h | Vérifier l'appartenance aux groupes dynamiques attendus |
| 5 | Contrôle qualité : système, applications, pilotes, EDR, antivirus, chiffrement | Démarrer le poste et vérifier l'application des profils et l'état de conformité |
| 6 | Placer le poste sur l'étagère « Prêt à déployer » | Placer le poste sur l'étagère « Prêt à déployer » |
| 7 | Mettre à jour le statut Tauturu et le ticket de dotation | Mettre à jour le statut Tauturu et le ticket de dotation |

## Points de vigilance

| 🟠 Poste MDT | 🔵 Poste Intune |
| --- | --- |
| Vérifier la fraîcheur de l'image avant tout déploiement massif — voir PROC-ATL-H03 | Le tag conditionne profil, groupes et applications : une erreur se découvre à l'ouverture de session du bénéficiaire |
| Le cluster est administré par une seule personne : escalader immédiatement toute panne d'infrastructure | L'appartenance aux groupes dynamiques se recalcule avec un délai — une vérification trop précoce donne un résultat incomplet |
| Pour préparer plusieurs postes en parallèle, ajouter un switch supplémentaire | Un appareil absent de la console alors qu'il figure au bon de livraison est un écart de livraison, à traiter avec le fournisseur |
| **Le chiffrement et la rotation des mots de passe administrateur ne sont pas poussés à distance : les vérifier explicitement** | Ces éléments sont appliqués par les politiques de la console |

**Toujours se poser la question de l'éligibilité.** Un poste legacy en cours de préparation qui remplit les conditions d'enrôlement devrait être orienté vers la colonne 🔵 plutôt que préparé sous MDT. Chaque poste préparé à l'ancienne est un poste à migrer plus tard.

## Procédures liées

- PROC-STOCK-H02 — Dotation de matériel
- PROC-ATL-H03 — Maintenance de l'image MDT
- PROC-INT-H01 — Enrôlement et attribution d'un appareil
