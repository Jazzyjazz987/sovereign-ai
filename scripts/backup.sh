#!/usr/bin/env bash
# Sauvegarde de l'état du stack Sovereign AI vers un disque (USB sécurisé).
# Usage :  scripts/backup.sh /media/usb/sovereign-backup
#
# Sauvegarde :
#   - PostgreSQL  (pg_dump — chunks RAG + embeddings + état) — RÉCUPÉRABLE aussi par
#     ré-ingestion depuis corpus/, mais le dump évite un re-embedding de ~25 s.
#   - modèle Ollama qwen2.5:7b (volume ollama_data) — CRITIQUE : non re-téléchargeable
#     en local cloisonné (pas de réseau). Sans lui, le système est mort.
#   - config/ , corpus/ , .env  (petits, mais indispensables au redémarrage)
set -euo pipefail

DEST="${1:?Usage: backup.sh <dossier de destination>}"
STAMP="$(date +%Y%m%d-%H%M%S)"
OUT="$DEST/$STAMP"
PROJECT="$(cd "$(dirname "$0")/.." && pwd)"
COMPOSE="docker compose -f $PROJECT/docker-compose.yml"

mkdir -p "$OUT"
echo "→ Sauvegarde vers $OUT"

# 1. PostgreSQL — dump logique cohérent
echo "  [1/4] PostgreSQL (pg_dump)…"
$COMPOSE exec -T postgres pg_dump -U claude -d langgraph_db --no-owner \
  | gzip > "$OUT/postgres_langgraph_db.sql.gz"

# 2. Volume Ollama (le modèle) — tar du volume à chaud (fichiers immuables)
echo "  [2/4] Volume ollama_data (modèle qwen2.5:7b ~4,7 Go)…"
docker run --rm -v sovereign-ai_ollama_data:/v -v "$OUT":/b alpine \
  tar czf /b/ollama_data.tgz -C /v .

# 3. Configuration + corpus + secrets
echo "  [3/4] config/ , corpus/ , .env …"
tar czf "$OUT/config_corpus_env.tgz" -C "$PROJECT" config corpus .env 2>/dev/null || \
  tar czf "$OUT/config_corpus_env.tgz" -C "$PROJECT" config corpus

# 4. Manifeste + empreintes
echo "  [4/4] manifeste…"
{
  echo "sovereign-ai backup — $STAMP"
  echo "hôte : $(hostname)"
  echo "commit : $(cd "$PROJECT" && git rev-parse --short HEAD 2>/dev/null || echo '?')"
  echo "images :"
  docker images --format '  {{.Repository}}:{{.Tag}} {{.ID}} {{.Size}}' | grep -iE 'sovereign|pgvector|ollama' || true
  echo "fichiers :"
  ( cd "$OUT" && sha256sum ./*.tgz ./*.gz )
} > "$OUT/MANIFEST.txt"

cat "$OUT/MANIFEST.txt"
echo "✓ Sauvegarde terminée : $OUT ($(du -sh "$OUT" | cut -f1))"
echo "  Restauration :  scripts/restore.sh $OUT"
