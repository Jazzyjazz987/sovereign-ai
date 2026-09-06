# RAG — cahier des besoins (POC)

**Statut : BROUILLON — à valider avec l'opérateur.** 2026-09-05.
Découle de `DESIGN_REVIEW.md` § POC SHORTLIST B ( « la base de fiches citées EST le produit,
la cascade LLM est le repli du long tail » ).

Ce document définit **ce que le RAG doit faire** avant d'écrire une ligne de code. Chaque section
porte une **reco** (ce que je propose par défaut) et, si besoin, une **[DÉCISION]** attendue de toi.

---

## 1. À quoi sert le RAG — usages

Le RAG sert **deux gestes** de l'agent CPA, pas un chatbot ouvert :

| # | Geste | Entrée | Sortie |
|---|-------|--------|--------|
| U1 | **Répondre à une question métier** | « comment réinitialiser le MFA d'un agent ? » | réponse courte **+ fiche(s) citée(s)** (titre, réf/lien, extrait) |
| U2 | **Rédiger la réponse au ticket** | le texte du problème de l'utilisateur final | brouillon de réponse en français, cadré par les fiches trouvées, que l'agent relit et envoie |

**Reco :** POC = U1 + U2. Pas de « conversation » multi-tours, pas de synthèse documentaire libre.

---

> **Décisions opérateur (2026-09-06) :**
> - **Périmètre POC = les procédures de traitement des agents de la CPA** (support informatique).
> - Sources, dans l'ordre : (1) **procédures « legacy » CPA**, (2) **mails de la BAL partagée**
>   envoyés aux utilisateurs, (3) tickets résolus (plus tard).
> - Juridique / statutaire PF : **hors périmètre POC** (DÉCISION 1 tranchée).
> - Dépôt des fichiers : `corpus/01-procedures-legacy/`, `corpus/02-mails-bal-partagee/`,
>   `corpus/03-tickets/` (dossier hors git — cf. `corpus/README.md`).

## 2. Domaines couverts (POC vs cible)

| Domaine | POC ? | Corpus |
|---------|-------|--------|
| Procédures internes CPA (onboarding poste, MFA, VPN, imprimantes, habilitations…) | ✅ **oui** | fiches CPA internes |
| Bureautique / M365 F3 (Outlook, Teams, OneDrive, partage) | ✅ **oui** | fiches CPA + doc Microsoft récupérée |
| Dépannage matériel (postes, périphériques) | ✅ **oui** | fiches CPA + notes constructeur |
| Juridique / statutaire / RH de la fonction publique **de la PF** | 🟠 **cible, pas POC** | Lexpol / JOPF / service-public.pf — corpus lourd, à ingérer plus tard |

**Reco :** le POC se limite aux 3 premiers domaines (support informatique pur). Le juridique PF
reste derrière le *gate fiche citée* : sans fiche pertinente → carte « consultez le service
juridique / DRH », **jamais** de prose du modèle. On l'active quand le corpus Lexpol existe.

**[DÉCISION 1]** — d'accord pour sortir le juridique PF du périmètre POC ?

---

## 3. Sources du corpus — ce qu'il faut que tu fournisses

C'est le point bloquant. Pour chaque source : **format**, **volume**, **où on l'exporte**,
**qui la valide**.

| Source | Question |
|--------|----------|
| **Base de connaissances existante** | La CPA a-t-elle déjà une KB ? (GLPI ? wiki ? SharePoint ? classeur Word ?) Sous quel format on peut l'exporter en masse ? |
| **Fiches / procédures** | Combien ? Word / PDF / pages web ? Y a-t-il un « propriétaire » par fiche (qui la tient à jour) ? |
| **Historique de tickets** | Quel outil ITSM ? (GLPI, GLPI+, autre ?) Peut-on exporter un lot de tickets résolus (question + réponse de l'agent) ? C'est la meilleure graine pour U2 et le jeu d'éval. |
| **Doc Microsoft M365** | On récupère les pages `learn.microsoft.com` pertinentes **avant** l'air-gap. Liste des sujets prioritaires ? |
| **service-public.pf / Lexpol** | Pour plus tard (domaine juridique). Existe-t-il un export ? une API ? sinon crawl ciblé avant air-gap. |

**[DÉCISION 2]** — quelle source tu peux fournir **en premier** (même 10 fiches Word suffisent
pour démarrer et valider la chaîne) ?

---

## 4. Contrat de réponse (garde-fous produit)

Non négociable pour le POC :

1. **Toute réponse U1/U2 cite ses sources** : liste de fiches (titre + référence + extrait exact
   utilisé). Pas de citation = pas de réponse « validée ».
2. **Rien trouvé de pertinent** (meilleur score < seuil) →
   - domaines support : réponse du modèle **étiquetée « généré localement — à vérifier »**, sans
     fabriquer de référence ;
   - domaine juridique/statutaire : **carte « consultez [service] »**, zéro prose modèle.
3. **Jamais** de référence, article, ou numéro de texte inventé. Le prompt impose : « si
   l'information n'est pas dans les extraits fournis, dis-le ».
4. **3 étiquettes de confiance** (déjà prévues) : `Fiche validée CPA` / `Généré localement — à
   vérifier` / `Réponse cloud` (POC only).
5. Langue : **français**. Entrée non-française détectée → routage humain (gate langue, phase 2).

---

## 5. Qualité — comment on saura que ça marche

**Jeu d'éval** : 30-50 vrais tickets CPA (anonymisés via Anone), chacun avec la fiche attendue
et/ou la réponse de référence. Métriques, mesurées en CI CPU :

| Métrique | Cible POC |
|----------|-----------|
| **Recall@5** (la bonne fiche est dans le top 5 renvoyé) | ≥ 0,80 |
| Taux de « je ne sais pas » **abusif** (fiche existait mais non trouvée) | ≤ 0,15 |
| Taux d'**hallucination de référence** (réf. citée absente du corpus) | **0** |
| Latence `/search` (CPU, corpus POC) | < 500 ms |

**[DÉCISION 3]** — peux-tu réunir ~30 tickets résolus représentatifs (les plus fréquents) ?

---

## 6. Contraintes non-fonctionnelles

- **100 % local / air-gap** : tout téléchargement (modèle d'embeddings, doc Microsoft, crawl
  service-public.pf) se fait **avant** le passage en salle fermée. Ré-ingestion ultérieure = script
  + clé USB.
- **Embeddings sur CPU** : `intfloat/multilingual-e5-base` (~280 Mo, FR natif, licence MIT).
  Toute la VRAM 12 Go reste au LLM.
- **Stockage** : extension **pgvector** dans le PostgreSQL déjà présent — pas de nouvelle base.
- **Volume POC** : quelques centaines à ~5 000 chunks → trivial (index en RAM, pas de tuning).
- **Mise à jour du corpus** : manuelle, versionnée (empreinte du corpus dans `/health`, comme
  `prompt_set`).

---

## 7. Hors périmètre POC (à acter)

- ACL par groupe Entra sur les fiches (pas d'auth dans le POC — cf. DESIGN_REVIEW Phase 2).
- Suppression / droits des personnes sur les documents indexés (volet données hors périmètre).
- Multi-langue reo Mā'ohi / Marquisien / Pa'umotu (gate langue = phase 2).
- Re-ranking cross-encoder, RAG agentique / multi-hop, réécriture de requête par LLM.
- Ingestion Lexpol / juridique PF (phase suivante).

---

## 8. Esquisse d'architecture (pour situer — à détailler après validation)

```
                  ┌──────────────┐
requête agent ───▶│ orchestrateur│
                  │  (main.py)   │
                  └──────┬───────┘
                         │ 1. /search (k=5)
                  ┌──────▼───────┐   pgvector + e5-base (CPU)
                  │ service rag  │   /ingest  /search  /health
                  │   :8090      │
                  └──────┬───────┘
                         │ 2. extraits trouvés ?
              oui ┌──────┴───────┐ non
                  ▼              ▼
     prompt « réponds        domaine support → LLM + label « à vérifier »
     UNIQUEMENT à partir     domaine juridique → carte « consultez [service] »
     de ces extraits,
     cite-les » → LLM local
                  │
                  ▼
     réponse + fiches citées + étiquette de confiance
```

- `service rag` : nouveau conteneur, `/ingest` (doc → chunks → embeddings → pgvector),
  `/search` (requête → top-k chunks + score + métadonnées fiche), `/health` (empreinte corpus).
- Chunking : ~500 tokens, chevauchement ~50, découpe sur titres/paragraphes.
- Ingestion : loaders par format (Markdown, PDF via `pypdf`, HTML via `trafilatura`).

---

## 9. Prochaine étape

Une fois §2, §3, §5 tranchés (DÉCISIONS 1-3) → j'écris le `service rag` minimal (`/ingest` +
`/search`) contre un corpus-jouet de 10 fiches, je câble l'étape recherche dans `main.py`, et on
mesure le recall sur le premier lot de tickets.
