<!-- confluence: SI / page 66143 — https://williamsjosiah.atlassian.net/wiki/spaces/SI/pages/66143 -->
<!-- parent_id: 66127 · parent: ⚠️ Conformité et RGPD -->

# 🔴 Registre des procédures à contrainte RGPD

**Avertissement :** Ce registre liste les procédures CPA identifiées comme comportant des traitements
de données personnelles soumis au RGPD. Les actions P1 doivent être traitées en priorité absolue.

| Code | Procédure | Criticité | Points de contrôle RGPD |
| --- | --- | --- | --- |
| PROC-STOCK-005 | Retour matériel | Moyenne | Conservation des données 30 jours avant réinitialisation — non formalisé : créer une politique RGPD écrite (P1). Le bénéficiaire doit être informé du délai de conservation avant réinitialisation |
| PROC-STOCK-006 | Réforme et destruction de données | Haute | Créer et tenir à jour un registre RGPD de traçabilité des destructions (action P1 — délai : immédiat). Exiger un certificat de destruction à chaque évacuation du prestataire (action P1). Formaliser une politique de destruction des données dans la gouvernance DSI. Référence : RGPD Art. 5(1)(f) — intégrité et confidentialité des données personnelles |
| PROC-TER-006 | Récupération matériel et retour stock | Moyenne | Le matériel récupéré contient potentiellement des données personnelles — appliquer obligatoirement PROC-STOCK-005 (conservation 30 jours) |
| PROC-INT-005 | Retrait et désinscription appareil Intune | Haute | Tracer l'effacement des données dans le ticket Tauturu (date, agent, méthode). En cas de perte/vol : obligation de signalement RGPD potentielle — alerter le chef CPA et le RSSI |
| PROC-ID-003 | Désactivation et suppression de compte | Haute | Définir et appliquer une politique d'archivage des boîtes aux lettres avant suppression (délai recommandé : 6 mois minimum) — action P1. Utiliser les stratégies de rétention Microsoft 365 pour automatiser l'archivage. Tracer la date de suppression et l'identité de l'agent dans le ticket Tauturu. Référence : RGPD Art. 5 — limitation de la conservation des données personnelles |

## Plan d'action RGPD — Horizon 0-12 mois

| Priorité | Action | Responsable | Délai cible |
| --- | --- | --- | --- |
| 🔴 P1 — IMMÉDIAT | Créer le registre RGPD de traçabilité des destructions de disques (PROC-STOCK-006) | Chef CPA + Gestionnaire stock | 0-1 mois |
| 🔴 P1 — IMMÉDIAT | Exiger les certificats de destruction auprès du prestataire de réforme | Chef CPA | 0-1 mois |
| 🔴 P1 — IMMÉDIAT | Définir la politique d'archivage des boîtes aux lettres avant suppression (6 mois min) | Chef CPA + DSI | 0-2 mois |
| 🔴 P1 | Mettre en place le suivi des licences M365 (tableau de bord PowerShell) | Gestionnaire comptes | 0-2 mois |
| 🟠 P2 | Formaliser la politique de conservation des données 30 jours (PROC-STOCK-005) | Chef CPA | 2-3 mois |
| 🟠 P2 | Activer le monitoring des logs EntraID (alertes créations/suppressions) | Gestionnaire comptes | 3-6 mois |
| 🟡 P3 | Définir les SLA dans Tauturu et les communiquer aux services | Chef CPA | 6-12 mois |
