"""
Agent Anone (anonymisation PII via GLiNER)
Port 8080

RGPD — CLAUDE.md : anonymisation OBLIGATOIRE avant tout appel T5 (cloud).
Si le modèle n'est pas chargé ou qu'une erreur interne survient, /anonymize
renvoie HTTP 503 (jamais 200) pour que main.py bascule en repli local.
"""
import logging
import os

from fastapi import FastAPI, HTTPException
from gliner import GLiNER

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("anone")

app = FastAPI()

# Modèle GLiNER multi-langue spécialisé PII (surchargeable pour les tests / mirroirs).
MODEL_NAME = os.getenv("ANONE_MODEL", "urchade/gliner_multi_pii-v1")

# Jeu d'étiquettes PII figé. Clé = label GLiNER, valeur = préfixe du token de masquage.
# RGPD = données à caractère personnel (personnes physiques). On NE masque PAS les
# organisations / institutions publiques (CNIL, DSI, Conseil d'État...) : ce ne sont pas
# des données personnelles, et ce sont souvent le sujet même de la question — les masquer
# détruit le sens de la requête envoyée à T5.
PII_LABELS = {
    "person": "PERSON",
    "email": "EMAIL",
    "phone number": "PHONE",
    "national identification number": "NIR",
    "address": "ADDRESS",
    "iban": "IBAN",
}

# Chargement du modèle. `ner = None` reste la sentinelle « modèle indisponible ».
try:
    ner = GLiNER.from_pretrained(MODEL_NAME)
    logger.info("GLiNER chargé : %s", MODEL_NAME)
except Exception as exc:  # noqa: BLE001 — on veut tracer l'erreur réelle, pas la masquer
    logger.exception("Échec du chargement de GLiNER (%s) : %s", MODEL_NAME, exc)
    ner = None


@app.post("/anonymize")
async def anonymize(request: dict):
    """Détecte les PII et les remplace par des tokens uniques (<PERSON_0>, ...).

    Renvoie {status, anonymized_text, pii_mapping, entities_found}.
    HTTP 503 si le modèle n'est pas chargé ou en cas d'erreur interne.
    """
    if ner is None:
        raise HTTPException(status_code=503, detail="GLiNER non chargé")

    text = request.get("text", "")

    try:
        entities = ner.predict_entities(text, list(PII_LABELS.keys()), threshold=0.5)

        # Attribution des tokens dans l'ordre de lecture ; une même valeur => même token.
        pii_mapping = {}
        value_to_token = {}
        counters = {}
        for ent in sorted(entities, key=lambda e: e["start"]):
            value = text[ent["start"]:ent["end"]]
            prefix = PII_LABELS.get(ent["label"], "PII")
            token = value_to_token.get((prefix, value))
            if token is None:
                idx = counters.get(prefix, 0)
                counters[prefix] = idx + 1
                token = f"<{prefix}_{idx}>"
                value_to_token[(prefix, value)] = token
                pii_mapping[token] = value
            ent["_token"] = token

        # Substitution de droite à gauche : les offsets des entités restantes ne bougent pas.
        anonymized = text
        for ent in sorted(entities, key=lambda e: e["start"], reverse=True):
            anonymized = anonymized[:ent["start"]] + ent["_token"] + anonymized[ent["end"]:]
    except HTTPException:
        raise
    except Exception as exc:  # noqa: BLE001
        logger.exception("Erreur interne /anonymize : %s", exc)
        raise HTTPException(status_code=503, detail=f"erreur anonymisation: {exc}")

    return {
        "status": "ok",
        "anonymized_text": anonymized,
        "pii_mapping": pii_mapping,
        "entities_found": len(entities),
    }


@app.post("/deanonymize")
async def deanonymize(request: dict):
    """Restaure les valeurs d'origine à partir de pii_mapping (token -> valeur)."""
    try:
        text = request.get("text", "")
        mapping = request.get("pii_mapping", {})

        if not text:
            return {"text": "", "status": "no_text"}

        if not mapping:
            return {"text": text, "status": "no_mapping"}

        result = text
        for token, original_value in mapping.items():
            result = result.replace(token, original_value)

        return {"text": result, "status": "ok"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "anone", "model_loaded": ner is not None}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
