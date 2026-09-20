<!-- confluence: SI / page 1802458 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/1802458 -->
<!-- parent_id: 1736847 · parent: 🚗 Agents de proximité terrain — hybride -->

# PROC-TER-H02 — Dotation sur site

|  |  |
| --- | --- |
| **Code** | PROC-TER-H02 |
| **Domaine** | Agents de proximité terrain |
| **Statut** | En vigueur pendant la migration |
| **Discriminant** | État du poste livré |
| **Criticité** | Haute |

> **Règle invariante CPA** — Toute dotation, intervention ou action manuelle sur le parc fait l'objet d'un ticket Tauturu.

## Objet

Livrer et installer un poste chez le bénéficiaire, et l'accompagner jusqu'à ce qu'il soit opérationnel.

## Étapes communes

| # | Action | Qui |
| --- | --- | --- |
| 1 | Récupérer le matériel attribué sur l'étagère « Prêt à déployer » | Agent de proximité |
| 2 | **Vérifier l'état du poste avant le départ** et emporter l'outillage correspondant | Agent de proximité |
| 3 | Charger le véhicule avec câbles et périphériques | Agent de proximité |
| 4 | Se rendre sur le site, au rendez-vous convenu avec le bénéficiaire | Agent de proximité |
| 5 | Installer physiquement le poste : connexions, écran, périphériques | Agent de proximité |

## Étapes propres à l'état du poste

| # | 🟠 Poste MDT | 🔵 Poste Intune |
| --- | --- | --- |
| 6 | Ouvrir la session du bénéficiaire et laisser la configuration se terminer | Accompagner le premier démarrage : le bénéficiaire s'authentifie, les profils s'appliquent |
| 7 | Installer ou vérifier les applications métier non couvertes par l'image | Vérifier que les applications ciblées sont présentes ; leur absence relève du déploiement, pas du poste |
| 8 | Configurer manuellement les imprimantes et les accès réseau du service | Ces éléments sont appliqués par les politiques : vérifier, ne pas configurer |
| 9 | Reprendre les données depuis les serveurs de fichiers, ou depuis l'ancien poste | Vérifier l'accès aux bibliothèques SharePoint et la synchronisation |
| 10 | Vérifier le chiffrement du disque et l'installation de l'antivirus et de l'EDR | Vérifier l'état de conformité affiché dans la console |
| 11 | Durée à prévoir : **environ 45 min** | Durée à prévoir : **environ 15 min** |

## Étapes finales communes

| # | Action | Qui |
| --- | --- | --- |
| 12 | Présenter brièvement les nouveautés au bénéficiaire | Agent de proximité |
| 13 | Récupérer l'ancien poste s'il y a remplacement — voir PROC-STOCK-H03 | Agent de proximité |
| 14 | Mettre à jour le ticket au retour d'intervention | Agent de proximité |

## Points de vigilance

**Communs**

- La présence du bénéficiaire est obligatoire : c'est son authentification qui ouvre la session.
- Au-delà de trois dotations sur un même site, demander le renfort d'un agent atelier.
- Le véhicule est vidé à chaque retour d'intervention.

| 🟠 Poste MDT | 🔵 Poste Intune |
| --- | --- |
| Emporter les supports d'installation des applications métier : elles ne se déploieront pas toutes seules | Ne rien installer manuellement : une application ajoutée à la main sur un poste géré sera écrasée ou dupliquée au prochain cycle |
| Noter les configurations manuelles effectuées : elles devront être refaites à la prochaine réinstallation | Aucune configuration manuelle à noter : la console fait foi |
| Si le bénéficiaire disposait déjà d'un poste Intune, il découvre une régression d'expérience : le lui expliquer | Si le bénéficiaire venait d'un poste MDT, lui montrer où ses fichiers se trouvent désormais |

**Le cas le plus délicat est le remplacement d'un poste MDT par un poste Intune.** Le bénéficiaire change de poste et d'écosystème en même temps : ses fichiers ne sont plus au même endroit, ses raccourcis ont disparu, ses imprimantes se sont reconfigurées seules. Prévoir dix minutes d'accompagnement supplémentaires évite un ticket dans les jours qui suivent.

## Procédures liées

- PROC-STOCK-H02 — Dotation de matériel
- PROC-STOCK-H03 — Retour de matériel
- PROC-TER-H04 — Télé-assistance et interventions aux îles
