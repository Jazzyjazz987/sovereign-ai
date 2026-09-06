# Comparaison modèles — tier juridique/admin (T4)

**2026-09-05, RTX 3080 Ti 12 Go.** Candidats issus de la recherche : la famille **Albert /
Guillaume Tell** (DINUM / Etalab — l'IA du gouvernement français POUR les agents administratifs).

Testés en GGUF Q4_K_M via Ollama, prompts CPA réalistes (cumul emploi fonctionnaire PF, reset
mot de passe M365, secret professionnel, dépannage imprimante).

## Verdict : ni l'un ni l'autre utilisable **nu** pour le POC

### `hf.co/mradermacher/guillaumetell-7b-GGUF:Q4_K_M` — ❌ (en l'état)
- **Question juridique (cumul emploi)** : réponse substantielle AVEC références orientées PF
  (Code des communes des TAAF/PF/Wallis-et-Futuna, Arrêté du 28 juillet 2004, JO PF) — **mais**
  références en partie **fabriquées** (`Art. R.1326-1` douteux) et **spam de "Note:"** évoquant
  une plateforme « EncycloLQ », des boutons « Soumettre un commentaire »… → le modèle **hallucine
  un contexte RAG/UI** vu à l'entraînement.
- **Prompts non juridiques (imprimante)** : **effondrement total** — fuite de template
  `### Instruction:` / `Réponse :` (style Alpaca) puis **boucle de fanfiction** (« Koba le
  chimpérien », « La planète des singes ») répétée ~10×, jusqu'à la limite de tokens.
  → **le GGUF `mradermacher` a un template cassé** (base = OpenHermes-2.5-Mistral = ChatML ; Ollama
  applique autre chose). Inutilisable tel quel.

### `hf.co/mradermacher/albert-spp-8b-GGUF:Q4_K_M` — ❌
- Bloqué en persona **« réponse automatique à une réclamation citoyenne »** : répond à *toute*
  question par « Merci pour votre témoignage / Votre question a été relayée auprès des services
  concernés / nous travaillons à mieux satisfaire les assurés ».
- Secret professionnel → hors-sujet complet. Reset M365 → étapes inventées.

## Pourquoi

Guillaume Tell et Albert-spp sont des **modèles RAG-only** : entraînés à répondre **à partir de
documents sources injectés**, pas depuis leur mémoire paramétrique. Utilisés nus (sans fiches
fournies), ils hallucinent ou retombent dans leur persona d'entraînement.

→ Ils ne deviennent intéressants **qu'avec la couche RAG** (Lexpol + service-public.pf + fiches
CPA), qui est exactement l'archi « portail à fiches citées » — mais elle n'est pas encore
construite (POC SHORTLIST B5).

## Décision

- **T4 revient à `mistral:7b`** en attendant.
- `guillaumetell-7b` : **candidat pour T4 quand (1) la couche RAG existe et (2) un GGUF au bon
  template ChatML est trouvé** (essayer `EZPK/guillaumetell-7b-Q4_K_M-GGUF`,
  `Marmeelade/…`, ou le GGUF officiel `AgentPublic`, ou écrire un Modelfile Ollama avec le
  template ChatML explicite).
- `mistral:7b` est lui-même **faible** (réponses bancales) → prochaine étape : tester un meilleur
  généraliste FR 7-8B (**Qwen2.5-7B-Instruct**, **Ministral-8B**) comme tier T1-T3.

## Vitesse (GPU)

T1 mistral:7b via `/query` : **~4 s** (chargement inclus au 1er appel), génération ~145 tok/s.
