FROM python:3.11-slim

WORKDIR /app

# torch CPU d'abord (index dédié) pour éviter les wheels CUDA
RUN pip install --no-cache-dir torch==2.14.0 --index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt .
# torch déjà installé — on retire la ligne pour ne pas la réinstaller
RUN grep -v '^torch' requirements.txt > /tmp/req.txt && \
    pip install --no-cache-dir -r /tmp/req.txt

ENV HF_HOME=/models/hf \
    RAG_TORCH_THREADS=8 \
    RAG_EMBED_MODEL=intfloat/multilingual-e5-base \
    RAG_RERANK_MODEL=BAAI/bge-reranker-base

# C5 — modèles embarqués dans l'image (air-gap). Le build a besoin d'un accès réseau ;
# au runtime le service tourne hors-ligne (HF_HUB_OFFLINE=1 par défaut en compose).
RUN python -c "\
from sentence_transformers import SentenceTransformer, CrossEncoder; \
SentenceTransformer('intfloat/multilingual-e5-base', device='cpu'); \
CrossEncoder('BAAI/bge-reranker-base', device='cpu', max_length=512); \
print('modèles téléchargés dans /models/hf')"

COPY *.py ./

EXPOSE 8090

CMD ["python", "-m", "uvicorn", "service:app", "--host", "0.0.0.0", "--port", "8090"]
