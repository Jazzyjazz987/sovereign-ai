#!/bin/bash
# Ollama — pré-chargement du modèle de la cascade (voir config/models.yaml).
# 2026-09-05 : qwen2.5:7b (Apache-2.0) pour T1-T4 ; guillaumetell/albert-spp écartés
# (RAG-only, voir docs/design-review/model-comparison-2026-09-05.md).

set -e
echo "=== Ollama : initialisation des modèles ==="

echo "Attente d'Ollama..."
for i in {1..30}; do
  if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "OK Ollama prêt"; break
  fi
  echo "  tentative $i/30..."; sleep 2
done

echo "[T1-T4] qwen2.5:7b"
ollama pull qwen2.5:7b 2>&1 | tail -1

echo "OK initialisation terminée. Modèles :"
curl -s http://localhost:11434/api/tags | jq -r '.models[].name' 2>/dev/null | head -10
exit 0
