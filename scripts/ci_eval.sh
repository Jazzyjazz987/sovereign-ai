#!/usr/bin/env bash
# Jeu d'éval RAG en mode CI — récupération seule (rapide, CPU), sans le pipeline complet.
# À câbler dans un hook pre-push ou une action GitHub. Échoue si recall@1 chute sous le seuil.
set -euo pipefail
cd "$(dirname "$0")/.."

MIN_R1="${MIN_R1:-85}"   # seuil recall@1 (%) sous lequel on échoue

if ! curl -sf http://localhost:8090/health >/dev/null 2>&1; then
  echo "!! service rag:8090 injoignable — démarrer la stack (docker compose up -d)" >&2
  exit 2
fi

OUT="$(python3 eval/run.py 2>&1)"
echo "$OUT"

# recall@1 minimal sur paliers 1+2 (les plus stables ; le pipeline complet et le
# palier 4 varient avec le tirage du 7B — testés à la main, pas en CI).
R1=$(echo "$OUT" | grep -E '^palier [12] ' | grep -oE 'recall@1 [0-9]+/[0-9]+ \([0-9]+%\)' \
     | grep -oE '\([0-9]+%\)' | tr -d '()%' | sort -n | head -1)

if [ -z "${R1:-}" ]; then echo "!! impossible de lire recall@1" >&2; exit 2; fi
echo "recall@1 min (paliers 1-2) = ${R1}%  (seuil ${MIN_R1}%)"
[ "$R1" -ge "$MIN_R1" ] || { echo "ÉCHEC : régression de récupération" >&2; exit 1; }
echo "OK"
