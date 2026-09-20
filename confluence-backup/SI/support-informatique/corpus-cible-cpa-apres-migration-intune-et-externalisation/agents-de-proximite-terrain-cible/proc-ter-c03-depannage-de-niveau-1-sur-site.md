<!-- confluence: SI / page 1802281 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/1802281 -->
<!-- parent_id: 1769473 · parent: 🚗 Agents de proximité terrain — cible -->

# PROC-TER-C03 — Dépannage de niveau 1 sur site

|  |  |
| --- | --- |
| **Code** | PROC-TER-C03 |
| **Domaine** | Agents de proximité terrain |
| **Statut** | Cible à valider |
| **Criticité** | Moyenne |
| **Contrainte RGPD** | Non |
| **Outils** | Tauturu, AnyDesk, sac d'intervention |

> **Règle invariante CPA** — Toute dotation, intervention ou action manuelle sur le parc fait l'objet d'un ticket Tauturu.

## Objet

Résoudre sur site les incidents ne pouvant être traités à distance, ou décider de leur escalade vers l'atelier.

## Déclencheur

Ticket d'incident nécessitant un déplacement, après tentative de résolution à distance.

## Étapes

| # | Action | Qui | Résultat attendu |
| --- | --- | --- | --- |
| 1 | Consulter le ticket et le diagnostic initial avant le départ | Agent de proximité | Contexte compris |
| 2 | Se rendre sur site avec le sac d'intervention | Agent de proximité | Arrivée sur site |
| 3 | Reproduire l'incident et établir le diagnostic | Agent de proximité | Cause identifiée ou pressentie |
| 4 | Si un renfort est nécessaire, solliciter la télé-assistance pour un diagnostic conjoint | Agent de proximité | Diagnostic complété |
| 5 | Vérifier l'état de conformité du poste dans la console Intune | Agent de proximité | Écart de conformité écarté ou identifié |
| 6 | Résoudre l'incident sur place lorsque c'est possible | Agent de proximité | Incident résolu |
| 7 | Si la résolution n'est pas possible : informer le bénéficiaire, laisser le matériel en l'état, escalader à l'atelier | Agent de proximité | Escalade documentée |
| 8 | Mettre à jour le ticket au retour d'intervention | Agent de proximité | Ticket documenté |

## Points de vigilance

- **Un poste non conforme dans Intune explique une grande partie des incidents applicatifs.** L'étape 5 évite de chercher une cause locale à un problème de politique ou de déploiement.
- Un incident dont la cause relève du réseau, de la messagerie ou d'une application métier sort du périmètre de la cellule : il s'escalade vers la cellule compétente, sans traitement intermédiaire.
- Le filtrage des flux sortants ne relève plus de la cellule depuis l'arrêt du proxy. Un accès bloqué s'oriente vers le Bureau de la sécurité.

## Procédures liées

- PROC-ATL-C01 — SAV et incidents de niveau 2
- PROC-TER-C04 — Télé-assistance et interventions aux îles
