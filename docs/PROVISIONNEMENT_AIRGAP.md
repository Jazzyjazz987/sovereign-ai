# Provisionnement air-gap & sauvegarde

La boîte de production tourne dans un **local fermé sous badge, hors réseau internet**.
Tout ce qui a besoin d'internet se fait **avant** la mise en salle. Ce document liste
les étapes et la procédure de sauvegarde/restauration (revue globale, constat 7).

---

## 1. Ce qui a besoin d'internet (à faire AVANT la salle fermée)

| Élément | Comment | Où ça atterrit |
|---|---|---|
| Images Docker de base | `docker compose pull` (ollama, pgvector, prometheus, grafana, node/pg-exporter) | cache d'images local |
| Image `sovereign-ai-rag` | `docker compose build rag` — **bake e5-base + bge-reranker-base** dans l'image (C5) | image |
| Image `sovereign-ai-anone` | `docker compose build anone` — télécharge GLiNER dans `anone_hf_cache` | volume `anone_hf_cache` |
| Image `sovereign-ai-langgraph` | `docker compose build langgraph` | image |
| **Modèle `qwen2.5:7b`** | `docker compose up ollama` puis attendre `ollama_init.sh` (`ollama pull qwen2.5:7b`) | **volume `ollama_data` (~4,7 Go)** |

Vérifier avant transfert :
```bash
docker compose up -d
sleep 60
curl -s localhost:8888/health   # tout "healthy", rag.contract == "ok"
docker compose exec ollama ollama list   # qwen2.5:7b présent
```

Puis, dans `.env` : `HF_HUB_OFFLINE=1`, `TRANSFORMERS_OFFLINE=1` (déjà par défaut). La
boîte ne doit plus tenter d'accès réseau.

---

## 2. Transfert vers la salle fermée (clé USB sécurisée)

Deux options :

**A. Transfert des images + volumes (machine identique).**
```bash
# côté machine connectée
docker save $(docker images --format '{{.Repository}}:{{.Tag}}' | grep -iE 'sovereign|pgvector|ollama|prom|grafana|node-exporter|postgres-exporter') \
  | gzip > /media/usb/images.tgz
scripts/backup.sh /media/usb/sovereign-backup      # volumes + config + corpus + .env
git bundle create /media/usb/repo.bundle --all      # le code
```
```bash
# côté boîte cloisonnée (dépôt cloné depuis le bundle)
gunzip -c /media/usb/images.tgz | docker load
scripts/restore.sh /media/usb/sovereign-backup/<horodatage>
```

**B. Rebuild sur la boîte** (si elle a un accès réseau *temporaire et contrôlé* au
premier démarrage) : `git clone` + `docker compose build` + `docker compose up`, puis
couper le réseau.

---

## 3. Sauvegarde régulière (en fonctionnement)

```bash
scripts/backup.sh /media/usb/sovereign-backup
```
Produit `<horodatage>/` contenant :
- `postgres_langgraph_db.sql.gz` — chunks RAG + embeddings + état langgraph
- `ollama_data.tgz` — **le modèle `qwen2.5:7b`** (critique : non re-téléchargeable ici)
- `config_corpus_env.tgz` — `config/`, `corpus/`, `.env`
- `MANIFEST.txt` — commit, images, empreintes sha256

**Cadence recommandée :** après chaque ré-ingestion de corpus, après chaque changement
de `config/*.yaml`, sinon 1×/semaine. Garder 2-3 rotations sur l'USB.

## 4. Restauration

Sur une machine avec le dépôt cloné + Docker + les images chargées :
```bash
scripts/restore.sh /media/usb/sovereign-backup/<horodatage>
curl -s localhost:8888/health
```

## 5. Test de restauration (à faire au moins une fois — non fait à ce jour)

Le seul moyen de savoir qu'une sauvegarde fonctionne est de la restaurer.
```bash
# sur une 2e machine ou un projet Docker isolé
git clone <bundle> restore-test && cd restore-test
gunzip -c /media/usb/images.tgz | docker load
scripts/restore.sh /media/usb/sovereign-backup/<horodatage>
# valider : /health OK, une requête /query renvoie une fiche
```

---

## Ce qui reste à sécuriser (constats de la revue)

- **Aucun onduleur / plan GPU mort documenté** — où la boîte est physiquement, coupure
  de courant, délai d'appro d'une RTX depuis Tahiti (facette non revue).
- Le `.env` contient la clé Anthropic + les mots de passe en clair — permissions
  fichier strictes sur la boîte cloisonnée (décision opérateur : pas de vault).
- `git remote origin` embarque un PAT GitHub en clair — à retirer avant que le dépôt
  ne circule sur l'USB (`git remote set-url origin <url sans token>`).
