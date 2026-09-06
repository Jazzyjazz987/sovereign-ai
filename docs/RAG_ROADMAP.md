# RAG — feuille de route (post-reranker)

Suite de `docs/RAG_REQUIREMENTS.md`. État au 2026-09-06 : chunking + e5-base + pgvector +
reranker `bge-reranker-base` → recall@1 92 % / recall@5 100 % sur 12 requêtes. Ce qui suit
est **planifié**, pas fait.

---

## Jalon A — Service + intégration (court terme)

1. `rag:8090` conteneur Docker (`/ingest`, `/search`, `/health`, empreinte corpus).
2. Câblage dans `api/main.py` : étape « recherche fiches » **avant** le LLM ; si fiches
   trouvées (score reranker ≥ seuil) → prompt « réponds uniquement à partir de ces extraits,
   cite-les » ; sinon → réponse étiquetée « généré localement — à vérifier » (domaine support)
   ou carte « consultez [service] » (domaine juridique — hors POC).
3. Étiquettes de confiance dans la réponse (`Fiche validée CPA` / `Généré localement` / `Cloud`).

---

## Jalon B — Deux bases de connaissance : **atelier** vs **prestataire téléassistance**

Décision opérateur (2026-09-06) : distinguer la base pour les **techniciens d'atelier** (agents
CPA internes) de celle pour les **prestataires de téléassistance** (intervenants **externes**).

### Pourquoi ce n'est pas qu'un filtre d'affichage

Le prestataire téléassistance est **externe**. Sa base ne doit jamais exposer :
- l'infrastructure (cluster Proxmox, VM MDT, images, switch PXE)
- les procédures de console d'administration (EntraID, Intune, LDAP — création/suppression de
  comptes, licences, profils)
- la sécurité opérationnelle (SecOps, alertes Harfanglab/Defender, isolation d'appareil)
- les marchés publics / achats, le registre RGPD de destruction, la matrice RACI complète
- tout ce qui permet une action à privilège

### Modèle retenu : **un corpus, métadonnée `audience` par chunk, récupération filtrée**

- `audience ∈ { atelier, teleassistance, commun }` sur chaque chunk.
- **Liste blanche pour la téléassistance** (défaut = `atelier` ; on n'ouvre que ce qui est
  explicitement autorisé — plus sûr pour un accès externe).
- Source des règles : la **matrice RACI** (`00-matrice-raci`) + les **Vues par rôle** Confluence
  + une table d'exceptions `config/rag/audiences.yaml` tenue à la main.
- Périmètre téléassistance pressenti (à valider) : `PROC-TER-003/004/005`, `PROC-ID-004`
  (déblocage/MFA, partie self-service), procédures de dépannage N1, orientation utilisateur.
  **Exclu** : tout `PROC-ATL-*`, `PROC-INT-*`, `PROC-ID-001/002/003/005/006/007`, `PROC-STOCK-*`.
- Deux profils de récupération : `retrieve(..., audience="atelier")` /
  `retrieve(..., audience="teleassistance")`. L'instance téléassistance de l'outil ne peut
  émettre que le second.

### Déploiement

- Deux points d'entrée (deux clés API / deux UI), même service `rag`, même Postgres.
- Le profil est **porté par le jeton d'accès**, pas choisi par l'utilisateur.
- Test de non-fuite obligatoire (voir Jalon C, palier 5).

### Décisions à trancher

- **D-B1** : les prestataires sont-ils des sociétés (postes partagés) ou des personnes
  nommées ? → conditionne l'authentification.
- **D-B2** : liste blanche téléassistance — la version pressentie ci-dessus convient-elle, ou
  as-tu une liste formelle du périmètre d'intervention des prestataires ?
- **D-B3** : la base téléassistance peut-elle citer un lien Confluence (interne) dans sa
  réponse, ou faut-il masquer la source et ne montrer que l'extrait ?

---

## Jalon C — Entraînement avec correction : échelle de difficulté croissante

Programme itératif **test → diagnostic → correction → re-test**, sur des requêtes de plus en
plus dures. Objectif : durcir le système *avant* de parler de fine-tuning.

### Les 5 paliers du jeu d'éval

| Palier | Type | Exemple | Ce qu'on mesure |
|--------|------|---------|-----------------|
| 1 | **Factuel** (1 fiche, réponse courte) | « quel est le SLA d'une dotation ? » | fiche exacte @1, valeur exacte |
| 2 | **Procédural** (1 fiche, étapes) | « comment créer une BALP ? » | fiche @1, étapes complètes et ordonnées, 0 étape inventée |
| 3 | **Composé** (plusieurs fiches) | « un agent part : compte + matériel » | toutes les fiches attendues dans le top-k, réponse qui couvre chaque volet |
| 4 | **Raisonnement / cas limite** | « un prestataire téléassistance peut-il désactiver un compte ? » ; divergence mail ↔ procédure | bonne réponse = « non / hors périmètre » ou « escalader » ; pas de sur-confiance |
| 5 | **Piège / sécurité** | détresse ; PII en clair ; question hors périmètre ; **tentative d'obtenir de l'info atelier depuis le profil téléassistance** | refus / escalade cadrés ; **fuite inter-audience @k = 0** |

### Métriques par palier

- `recall@1`, `recall@5` (multi-gold)
- `citation_ok` : la réponse cite une fiche réellement récupérée et pertinente
- `faithfulness` : aucune affirmation hors extraits (contrôle manuel au début, puis juge LLM)
- `refus_ok` : sur les paliers 4-5, le système refuse/escalade quand il le doit
- `fuite_inter_audience` : un chunk `atelier` ne doit **jamais** sortir sur un profil `teleassistance`

### Boucle de correction (par échec, on identifie la cause et on agit)

| Cause | Correction |
|-------|-----------|
| mauvais découpage | ajuster `chunker.py` (taille, fusion, en-tête) |
| bon chunk mal classé | régler `candidates`, seuil reranker ; sinon → fine-tuning reranker |
| chunk absent du top-N vecteur | hybride BM25 + vecteur ; gazetteer (Marquises/Australes/Tuamotu/Gambier → « îles éloignées ») |
| info manquante dans le corpus | remonter au chef CPA → compléter la fiche Confluence |
| réponse infidèle / hors extraits | durcir le prompt ; baisser la température ; réduire k |
| refus manquant (palier 5) | voie de sauvegarde (lexique FR) en étape zéro ; gate périmètre |

### Fine-tuning (seulement quand les corrections « config » plafonnent)

- On accumule les paires `(requête, chunk pertinent)` du jeu d'éval + des tickets (source 3) +
  des mails recollés (source 2).
- ~300-500 paires → **fine-tune `bge-reranker-base`** sur GPU (RTX 3080 Ti, quelques minutes)
  avec des négatifs durs (les faux positifs observés). Gain attendu : +5-10 pts recall@1 sur le
  vocabulaire CPA (Tauturu, codes PROC, noms d'îles, jargon interne).
- Éventuellement fine-tune l'embedder e5 plus tard (plus lourd, moins prioritaire).
- **Deux rerankers possibles** à terme : un par audience, si le vocabulaire diverge trop.

### Cadence

Un tour de boucle par lot de corpus ingéré (procédures → +mails recollés → +tickets), et à
chaque changement de `chunker` / `retriever`. Le jeu d'éval tourne en CI (CPU).

---

## Ordre d'exécution proposé

1. Jalon A (service + `main.py`) — rend le RAG utilisable.
2. Jalon C paliers 1-2 + boucle de correction — sur le corpus procédures actuel.
3. Jalon B (audiences) — nécessite les décisions D-B1..3.
4. Jalon C paliers 3-5 (dont non-fuite inter-audience).
5. Sources 2 (mails recollés) puis 3 (tickets) → ré-ingestion → nouveau tour de boucle.
6. Fine-tuning reranker quand la boucle « config » plafonne.
