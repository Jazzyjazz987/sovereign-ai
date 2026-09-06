#!/bin/bash
# Ollama — pré-chargement des modèles de la cascade (voir config/models.yaml).
# 2026-09-05 : retrait de dolphin-mixtral / neural-chat (fine-tunes non censurés).

set -e
echo "=== Ollama : initialisation des modèles ==="

echo "Attente d'Ollama..."
for i in {1..30}; do
  if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "OK Ollama prêt"; break
  fi
  echo "  tentative $i/30..."; sleep 2
done

# T1/T2/T3 — généraliste français
echo "[T1-T3] mistral:7b"
ollama pull mistral:7b 2>&1 | tail -1 &

# T4 — juridique / administratif : Guillaume Tell (Albert / DINUM), RAG + citation, Apache-2.0
echo "[T4] guillaumetell-7b (GGUF Q4_K_M)"
ollama pull hf.co/mradermacher/guillaumetell-7b-GGUF:Q4_K_M 2>&1 | tail -1 &

wait 2>/dev/null || true

echo "OK initialisation terminée. Modèles :"
curl -s http://localhost:11434/api/tags | jq -r '.models[].name' 2>/dev/null | head -10
exit 0
