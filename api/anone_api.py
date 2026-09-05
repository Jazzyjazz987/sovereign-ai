"""
Agent Anone (GLiNER PII anonymisation)
Port 8080
"""
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Agent Anone - PII Anonymization", version="2.0")

# GLiNER pour détection PII multi-langue
try:
    from transformers import pipeline
    ner = pipeline("token-classification", model="urchade/gliner_multi_pii-v1")
except Exception:
    ner = None


@app.post("/anonymize")
async def anonymize(request: dict):
    """
    Detect and anonymize PII before sending to T5 cloud.

    Input:  {"text": "Jean Dupont appelle au 0612345678"}
    Output: {
        "status": "ok",
        "anonymized_text": "PERSON-0 appelle au PHONE-0",
        "pii_mapping": {"PERSON-0": "Jean Dupont", "PHONE-0": "0612345678"},
        "original_pii_found": 2
    }
    """
    text = request.get("text", "")

    if not ner:
        # Fallback: return text unchanged when model not loaded
        return {
            "status": "ok",
            "anonymized_text": text,
            "pii_mapping": {},
            "original_pii_found": 0,
            "warning": "GLiNER not loaded — text passed through unchanged"
        }

    # Detect PII entities
    entities = ner(text)

    # Build PII mapping and replace with tokens
    anonymized = text
    pii_mapping: dict[str, str] = {}
    entity_counters: dict[str, int] = {}

    # Sort entities in reverse order to replace without index shift
    sorted_entities = sorted(entities, key=lambda e: e.get("start", 0), reverse=True)

    for entity in sorted_entities:
        entity_type = entity.get("entity_group", "ENTITY").upper()
        start = entity.get("start", 0)
        end = entity.get("end", len(text))
        original_value = text[start:end]

        # Generate unique token for this entity type
        count = entity_counters.get(entity_type, 0)
        token = f"{entity_type}-{count}"
        entity_counters[entity_type] = count + 1

        pii_mapping[token] = original_value
        anonymized = anonymized[:start] + token + anonymized[end:]

    return {
        "status": "ok",
        "anonymized_text": anonymized,
        "pii_mapping": pii_mapping,
        "original_pii_found": len(entities)
    }


@app.post("/deanonymize")
async def deanonymize(request: dict):
    """
    Reverse PII anonymization by restoring original values from mapping.

    Input: {
        "text": "PERSON-0 travaille à EMAIL-0",
        "pii_mapping": {
            "PERSON-0": "Jean Dupont",
            "EMAIL-0": "jean.dupont@company.fr"
        }
    }
    Output: {"text": "Jean Dupont travaille à jean.dupont@company.fr", "status": "ok"}
    """
    try:
        text = request.get("text", "")
        mapping = request.get("pii_mapping", {})

        if not text:
            return {"text": text, "status": "ok"}

        if not mapping:
            return {"text": text, "status": "no_mapping"}

        result = text
        for anonymized_token, original_value in mapping.items():
            result = result.replace(anonymized_token, original_value)

        return {"text": result, "status": "ok"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "anone",
        "gliner_loaded": ner is not None
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
