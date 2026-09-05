#!/bin/bash
# Test T1 et T2 - Vérification complète avec screenshots (simulations)

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║        TEST T1 & T2 - VÉRIFICATION COMPLÈTE                ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

LOG_DIR="/tmp/test_results"
mkdir -p "$LOG_DIR"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

results_file="$LOG_DIR/results_${TIMESTAMP}.txt"

echo "=== TEST T1 & T2 ===" > "$results_file"
echo "Date: $(date)" >> "$results_file"
echo "" >> "$results_file"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo -e "${BLUE}[1/6] Vérification de la connexion API...${NC}"
echo "" | tee -a "$results_file"

if curl -s http://localhost:8888/health | jq . > /dev/null 2>&1; then
    echo -e "${GREEN}✅ API est disponible${NC}" | tee -a "$results_file"
    HEALTH=$(curl -s http://localhost:8888/health | jq '.')
    echo "Status: $HEALTH" >> "$results_file"
else
    echo -e "${RED}❌ API non disponible${NC}" | tee -a "$results_file"
    exit 1
fi
echo ""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo -e "${BLUE}[2/6] TEST T1 (Mistral 7B) - Requête simple${NC}"
echo "" | tee -a "$results_file"

QUERY_T1="Bonjour, qui es-tu?"
echo "Question: $QUERY_T1" | tee -a "$results_file"
echo ""

START_TIME=$(date +%s%N)
RESPONSE_T1=$(curl -s -X POST http://localhost:8888/query \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"$QUERY_T1\", \"model\": \"t1\"}")
END_TIME=$(date +%s%N)
DURATION=$((($END_TIME - $START_TIME) / 1000000)) # ms

echo "Réponse T1:" | tee -a "$results_file"
RESPONSE_TEXT=$(echo "$RESPONSE_T1" | jq -r '.response // .message // "ERROR"' 2>/dev/null)
echo "$RESPONSE_TEXT" | tee -a "$results_file"
echo ""

# Vérification
if echo "$RESPONSE_T1" | jq -e '.status == "ok"' > /dev/null 2>&1; then
    echo -e "${GREEN}✅ T1 répond correctement (${DURATION}ms)${NC}" | tee -a "$results_file"
    MODEL_USED=$(echo "$RESPONSE_T1" | jq -r '.model_used // "unknown"')
    echo "Modèle utilisé: $MODEL_USED" | tee -a "$results_file"
else
    echo -e "${RED}❌ T1 erreur${NC}" | tee -a "$results_file"
fi
echo ""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo -e "${BLUE}[3/6] TEST T2 (Llama 2 7B) - Requête code${NC}"
echo "" | tee -a "$results_file"

QUERY_T2="Écris une fonction Python pour calculer la suite Fibonacci"
echo "Question: $QUERY_T2" | tee -a "$results_file"
echo ""

START_TIME=$(date +%s%N)
RESPONSE_T2=$(curl -s -X POST http://localhost:8888/query \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"$QUERY_T2\", \"model\": \"t2\"}")
END_TIME=$(date +%s%N)
DURATION=$((($END_TIME - $START_TIME) / 1000000)) # ms

echo "Réponse T2 (premiers 300 caractères):" | tee -a "$results_file"
RESPONSE_TEXT=$(echo "$RESPONSE_T2" | jq -r '.response // .message // "ERROR"' 2>/dev/null | head -c 300)
echo "$RESPONSE_TEXT..." | tee -a "$results_file"
echo ""

# Vérification
if echo "$RESPONSE_T2" | jq -e '.status == "ok"' > /dev/null 2>&1; then
    echo -e "${GREEN}✅ T2 répond correctement (${DURATION}ms)${NC}" | tee -a "$results_file"
    MODEL_USED=$(echo "$RESPONSE_T2" | jq -r '.model_used // "unknown"')
    echo "Modèle utilisé: $MODEL_USED" | tee -a "$results_file"
else
    echo -e "${RED}❌ T2 erreur${NC}" | tee -a "$results_file"
fi
echo ""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo -e "${BLUE}[4/6] TEST Auto-routing${NC}"
echo "" | tee -a "$results_file"

# Simple query
SIMPLE_QUERY="Salut"
echo "Query simple: '$SIMPLE_QUERY'" | tee -a "$results_file"
RESPONSE_AUTO_SIMPLE=$(curl -s -X POST http://localhost:8888/query \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"$SIMPLE_QUERY\", \"model\": \"auto\"}")
MODEL_SIMPLE=$(echo "$RESPONSE_AUTO_SIMPLE" | jq -r '.model_used // "unknown"')
echo "→ Modèle sélectionné: $MODEL_SIMPLE" | tee -a "$results_file"
echo ""

# Complex query
COMPLEX_QUERY="Explique architecture microservices avec Kubernetes et RGPD compliance"
echo "Query complexe: '$COMPLEX_QUERY'" | tee -a "$results_file"
RESPONSE_AUTO_COMPLEX=$(curl -s -X POST http://localhost:8888/query \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"$COMPLEX_QUERY\", \"model\": \"auto\"}")
MODEL_COMPLEX=$(echo "$RESPONSE_AUTO_COMPLEX" | jq -r '.model_used // "unknown"')
echo "→ Modèle sélectionné: $MODEL_COMPLEX" | tee -a "$results_file"
echo ""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo -e "${BLUE}[5/6] État des modèles${NC}"
echo "" | tee -a "$results_file"

MODELS=$(curl -s http://localhost:8888/models | jq '.models[]? | .name' 2>/dev/null || echo "Erreur")
echo "Modèles disponibles:" | tee -a "$results_file"
echo "$MODELS" | tee -a "$results_file"
echo ""

GPU_STATUS=$(nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader 2>/dev/null)
echo "GPU:" | tee -a "$results_file"
echo "VRAM: $GPU_STATUS" | tee -a "$results_file"
echo ""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo -e "${BLUE}[6/6] Résumé${NC}"
echo "" | tee -a "$results_file"

echo "═════════════════════════════════════════════════════════════" | tee -a "$results_file"
echo "RÉSUMÉ DES TESTS" | tee -a "$results_file"
echo "═════════════════════════════════════════════════════════════" | tee -a "$results_file"
echo "" | tee -a "$results_file"

# Check results
T1_OK=0
T2_OK=0
AUTO_OK=0

if echo "$RESPONSE_T1" | jq -e '.status == "ok"' > /dev/null 2>&1; then
    T1_OK=1
    echo -e "${GREEN}✅ T1 (Mistral 7B)${NC} - Opérationnel" | tee -a "$results_file"
else
    echo -e "${RED}❌ T1 (Mistral 7B)${NC} - Erreur" | tee -a "$results_file"
fi

if echo "$RESPONSE_T2" | jq -e '.status == "ok"' > /dev/null 2>&1; then
    T2_OK=1
    echo -e "${GREEN}✅ T2 (Llama 2 7B)${NC} - Opérationnel" | tee -a "$results_file"
else
    echo -e "${RED}❌ T2 (Llama 2 7B)${NC} - Erreur" | tee -a "$results_file"
fi

if echo "$RESPONSE_AUTO_SIMPLE" | jq -e '.status == "ok"' > /dev/null 2>&1; then
    AUTO_OK=1
    echo -e "${GREEN}✅ Auto-routing${NC} - Fonctionne" | tee -a "$results_file"
else
    echo -e "${RED}❌ Auto-routing${NC} - Erreur" | tee -a "$results_file"
fi

echo "" | tee -a "$results_file"

# Overall status
if [ $T1_OK -eq 1 ] && [ $T2_OK -eq 1 ] && [ $AUTO_OK -eq 1 ]; then
    echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}" | tee -a "$results_file"
    echo -e "${GREEN}✅ TOUS LES TESTS PASSENT - SYSTÈME OPÉRATIONNEL${NC}" | tee -a "$results_file"
    echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}" | tee -a "$results_file"
    EXIT_CODE=0
else
    echo -e "${YELLOW}⚠️ CERTAINS TESTS ONT ÉCHOUÉ${NC}" | tee -a "$results_file"
    EXIT_CODE=1
fi

echo "" | tee -a "$results_file"
echo "Rapport sauvegardé: $results_file" | tee -a "$results_file"
echo ""
echo "Voir le rapport complet:"
echo "  cat $results_file"
echo ""

exit $EXIT_CODE
