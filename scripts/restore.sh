#!/usr/bin/env bash
# Restauration d'une sauvegarde produite par backup.sh.
# Usage :  scripts/restore.sh /media/usb/sovereign-backup/20260907-120000
#
# À exécuter sur une machine où le dépôt est cloné et Docker installé. Écrase
# l'état existant (postgres_data, ollama_data) — demander confirmation.
set -euo pipefail

SRC="${1:?Usage: restore.sh <dossier de sauvegarde>}"
PROJECT="$(cd "$(dirname "$0")/.." && pwd)"
COMPOSE="docker compose -f $PROJECT/docker-compose.yml"

[ -f "$SRC/MANIFEST.txt" ] || { echo "MANIFEST.txt absent — pas une sauvegarde valide" >&2; exit 1; }
echo "=== Sauvegarde à restaurer ==="; cat "$SRC/MANIFEST.txt"; echo
( cd "$SRC" && sha256sum -c <(grep -A99 'fichiers :' MANIFEST.txt | tail -n +2) ) \
  || { echo "⚠ empreintes non vérifiées (format) — poursuite manuelle possible"; }

read -rp "Écraser l'état actuel du stack ? [tape OUI] : " ok
[ "$ok" = "OUI" ] || { echo "annulé"; exit 1; }

echo "→ Arrêt du stack…"
$COMPOSE down

echo "→ Restauration config/ corpus/ .env …"
tar xzf "$SRC/config_corpus_env.tgz" -C "$PROJECT"

echo "→ Restauration du volume ollama_data …"
docker volume create sovereign-ai_ollama_data >/dev/null
docker run --rm -v sovereign-ai_ollama_data:/v -v "$SRC":/b alpine \
  sh -c "rm -rf /v/* ; tar xzf /b/ollama_data.tgz -C /v"

echo "→ Démarrage postgres seul + restauration du dump…"
docker volume rm sovereign-ai_postgres_data >/dev/null 2>&1 || true
$COMPOSE up -d postgres
until $COMPOSE exec -T postgres pg_isready -U claude >/dev/null 2>&1; do sleep 2; done
gunzip -c "$SRC/postgres_langgraph_db.sql.gz" | $COMPOSE exec -T postgres psql -U claude -d langgraph_db -q

echo "→ Démarrage du stack complet…"
$COMPOSE up -d
echo "✓ Restauration terminée. Vérifier :  curl -s localhost:8888/health"
