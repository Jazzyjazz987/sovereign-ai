<!-- confluence: SI / page 1802396 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/1802396 -->
<!-- parent_id: 1802375 · parent: ⚙️ Procédures hybrides CPA — pendant la migration -->

# EntraID / Exchange — hybride

**Statut : en vigueur pendant la migration**

> **Attention — le discriminant n'est pas le poste.** Dans ce domaine, les deux colonnes ne distinguent pas un poste MDT d'un poste Intune : elles distinguent **l'avant et l'après mise en service d'IdentityDSI**. Un agent doté d'un poste Intune peut avoir un compte créé manuellement, et réciproquement.

## Ce qui diffère selon la bascule

| 🟠 Avant IdentityDSI | 🔵 Après IdentityDSI |
| --- | --- |
| Compte créé par la cellule, sur ticket | Compte créé automatiquement, depuis le contrat au SIRH |
| Création dans LDAP **puis** dans EntraID | Création dans EntraID seul |
| Modèle de poste appliqué à la main | Modèle de poste appliqué par l'application |
| Suppression décidée au cas par cas | Suppression au départ comme à la mutation |
| La cellule est responsable du cycle de vie | La cellule vérifie, signale et désactive |

## Ce qui ne diffère pas

Les comptes hors SIRH — prestataires externes, comptes de service, boîtes aux lettres partagées, ressources Exchange — restent intégralement à la charge de la cellule, avant comme après la bascule. Le déblocage de l'authentification multifacteur et la gestion des licences également.

## Procédures du domaine

- **PROC-ID-H01** — Cycle de vie d'un compte d'agent
- **PROC-ID-H02** — Comptes hors SIRH, boîtes partagées et ressources
- **PROC-ID-H03** — Déblocage MFA et gestion des licences

## Points d'attention propres à la période

**Le double annuaire subsiste tant que LDAP n'est pas abandonné.** Une création manuelle dans EntraID sans création LDAP correspondante produit un agent qui accède à la messagerie mais pas aux applications métier — et l'incident remonte plusieurs jours plus tard, sans lien apparent avec la création du compte.

**Après la bascule, la cellule perd la main sur la création sans la perdre sur ses conséquences.** Un provisionnement erroné se corrige à la source, dans le SIRH, jamais dans EntraID : corriger localement masque la cause et la faute se reproduira à chaque synchronisation.

**La suppression à la mutation emporte la boîte aux lettres et le OneDrive.** C'est la règle validée par la DPO. Elle ne s'applique qu'après mise en service d'IdentityDSI : avant, la cellule conserve sa marge d'appréciation au cas par cas.
