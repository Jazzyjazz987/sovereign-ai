"""
Agent Anone (GLiNER PII anonymisation)
Port 8080
"""
from fastapi import FastAPI
from transformers import pipeline

app = FastAPI()

# GLiNER pour détection PII multi-langue
try:
    ner = pipeline("token-classification", model="urchade/gliner_multi_pii-v1")
except:
    ner = None

@app.post("/anonymize")
async def anonymize(request: dict):
    """Détecte et anonymise PII avant envoi T5"""
    text = request.get("text", "")
    
    if not ner:
        return {"status": "error", "message": "GLiNER not loaded"}
    
    # Détection PII
    entities = ner(text)
    
    # Remplacement PII avec placeholders
    anonymized = text
    for entity in entities:
        entity_type = entity.get("entity_group", "")
        start = entity.get("start", 0)
        end = entity.get("end", len(text))
        anonymized = anonymized[:start] + f"[{entity_type}]" + anonymized[end:]
    
    return {
        "status": "ok",
        "original_pii_found": len(entities),
        "anonymized_text": anonymized
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "anone"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
