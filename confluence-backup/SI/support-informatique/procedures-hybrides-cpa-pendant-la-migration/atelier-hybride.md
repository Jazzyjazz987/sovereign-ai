<!-- confluence: SI / page 1736826 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/1736826 -->
<!-- parent_id: 1802375 · parent: ⚙️ Procédures hybrides CPA — pendant la migration -->

# Atelier — hybride

**Statut : en vigueur pendant la migration**

C'est le domaine le plus exposé à la période : l'atelier fait coexister une chaîne de production complète, pour les postes MDT, et un simple contrôle de conformité, pour les postes enrôlés.

## Ce qui diffère selon le poste

| 🟠 Poste MDT | 🔵 Poste Intune |
| --- | --- |
| Déploiement PXE, séquence MDT, environ 2 h par poste | Contrôle de conformité, quelques minutes |
| Image maintenue mensuellement en interne | Aucune image — configuration appliquée par la console |
| Contrôle qualité complet après installation | Vérification de l'enrôlement et des profils |

## Ce qui ne diffère pas

Le SAV de niveau 2 traite les deux populations. Le diagnostic diffère dans ses outils, pas dans sa démarche.

## Procédures du domaine

- **PROC-ATL-H01** — Préparation ou contrôle d'un poste avant dotation
- **PROC-ATL-H02** — SAV et incidents de niveau 2
- **PROC-ATL-H03** — Maintenance de l'image MDT

## Points d'attention propres à la période

**L'infrastructure MDT doit rester opérationnelle jusqu'au dernier poste legacy.** Le cluster qui l'héberge n'a pas de sauvegarde automatisée et dépend d'une compétence unique. Une panne pendant la période de transition bloque la préparation de tout le parc non migré — et la bascule d'urgence vers Intune n'est pas possible pour un poste sans TPM 2.0.

**PROC-ATL-H03 disparaîtra avec le dernier poste MDT.** Elle est maintenue ici parce qu'elle est encore exécutée ; elle n'existe pas dans le corpus cible.
