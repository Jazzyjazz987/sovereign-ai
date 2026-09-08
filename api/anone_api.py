"""
Agent Anone (anonymisation PII via GLiNER)
Port 8080

RGPD — CLAUDE.md : anonymisation OBLIGATOIRE avant tout appel T5 (cloud).
Si le modèle n'est pas chargé ou qu'une erreur interne survient, /anonymize
renvoie HTTP 503 (jamais 200) pour que main.py bascule en repli local.
"""
import logging
import os
import re

from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from gliner import GLiNER
from prometheus_client import Counter, CONTENT_TYPE_LATEST, generate_latest

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("anone")

app = FastAPI()

# --- Métriques Prometheus (B6) — exposées sur GET /metrics --------------------------
ANONYMIZE_REQUESTS = Counter(
    "anonymize_requests_total", "Appels /anonymize par statut", ["status"]
)
ANONYMIZE_PII_MASKED = Counter(
    "anonymize_pii_masked_total", "Entités PII masquées cumulées"
)
ANONYMIZE_REGEX_HITS = Counter(
    "anonymize_regex_hits_total", "PII captées par la couche déterministe", ["kind"]
)
ANONYMIZE_LEAK_CANARY = Counter(
    "anonymize_leak_canary_total", "Texte encore porteur de PII après masquage (fail-closed)"
)

# Modèle GLiNER multi-langue spécialisé PII (surchargeable pour les tests / mirroirs).
MODEL_NAME = os.getenv("ANONE_MODEL", "urchade/gliner_multi_pii-v1")
# Seuil bas = sur-masquer : la direction sûre pour un garde-fou fail-closed vers le cloud.
THRESHOLD = float(os.getenv("ANONE_THRESHOLD", "0.4"))

# --- Couche déterministe (revue de conception R1.2 — meilleure valeur/effort) --------
# Regex + checksum pour les identifiants structurés à plus fort risque. Exécutée AVANT
# GLiNER ; ses captures sont fusionnées avec celles du modèle. Un canari post-masquage
# re-teste ces motifs : s'il reste une correspondance, on renvoie 503 (fail-closed).
def _nir_ok(digits: str) -> bool:
    """Clé de contrôle du NIR français : 97 - (nombre mod 97), Corse 2A/2B -> 19/18."""
    body, key = digits[:13], digits[13:15]
    body = body.replace("2A", "19").replace("2B", "18")
    try:
        return int(key) == 97 - (int(body) % 97)
    except ValueError:
        return False


def _iban_ok(iban: str) -> bool:
    s = re.sub(r"\s", "", iban).upper()
    s = s[4:] + s[:4]
    n = "".join(str(ord(c) - 55) if c.isalpha() else c for c in s)
    try:
        return int(n) % 97 == 1
    except ValueError:
        return False


DETERMINISTIC = [
    ("EMAIL", "EMAIL", re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"), None),
    # Téléphone Polynésie française : +689 puis 6 (fixe 40/44) ou 8 (mobile 87/89) chiffres,
    # ou groupes locaux 40 XX XX / 87 XX XX XX.
    ("PHONE", "PHONE", re.compile(
        r"(?<![\d.])(?:\+?689[\s.\-]?)?(?:4[04]|8[79]|2[0-9])[\s.\-]?\d{2}[\s.\-]?\d{2}"
        r"(?:[\s.\-]?\d{2})?(?![\d.])"), None),
    ("NIR", "NIR", re.compile(
        r"\b[12][\s.]?\d{2}[\s.]?(?:0[1-9]|1[0-2])[\s.]?(?:\d{2}|2[AB])[\s.]?\d{3}[\s.]?\d{3}"
        r"(?:[\s.]?\d{2})?\b"), _nir_ok),
    ("IBAN", "IBAN", re.compile(r"\b[A-Z]{2}\d{2}(?:[\s]?[A-Z0-9]{4}){2,7}(?:[\s]?[A-Z0-9]{1,3})?\b"),
     _iban_ok),
    # Matricule agent DSI (à ajuster au format réel — placeholder large, marqué à part).
    ("MATRICULE", "MATRICULE", re.compile(r"\bmatricule\s*:?\s*([A-Z]?\d{5,8})\b", re.I), None),
]


def _deterministic_spans(text: str) -> list[dict]:
    spans = []
    for kind, prefix, rx, check in DETERMINISTIC:
        for m in rx.finditer(text):
            raw = m.group(0)
            if check is not None:
                digits = re.sub(r"[^\dAB]", "", raw.upper())
                if not check(digits if kind == "NIR" else raw):
                    continue
            spans.append({"start": m.start(), "end": m.end(), "label": prefix,
                          "_prefix": prefix, "_kind": kind, "_src": "regex"})
            ANONYMIZE_REGEX_HITS.labels(kind=kind).inc()
    return spans


def _residual_pii(text: str) -> str | None:
    """Canari : le texte masqué contient-il encore un motif structuré ? -> nom du motif."""
    for kind, _p, rx, check in DETERMINISTIC:
        for m in rx.finditer(text):
            if check is None:
                return kind
            digits = re.sub(r"[^\dAB]", "", m.group(0).upper())
            if check(digits if kind == "NIR" else m.group(0)):
                return kind
    return None

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
        ANONYMIZE_REQUESTS.labels(status="503").inc()
        raise HTTPException(status_code=503, detail="GLiNER non chargé")

    text = request.get("text", "")

    try:
        gliner_ents = ner.predict_entities(text, list(PII_LABELS.keys()), threshold=THRESHOLD)
        for e in gliner_ents:
            e["_prefix"] = PII_LABELS.get(e["label"], "PII")
            e["_src"] = "gliner"

        # Fusion regex (déterministe) + GLiNER ; en cas de chevauchement, on garde le
        # span le plus long (les offsets restants ne bougent pas si on substitue de
        # droite à gauche et qu'aucun span ne se chevauche).
        cand = _deterministic_spans(text) + gliner_ents
        cand.sort(key=lambda e: (e["start"], -(e["end"] - e["start"])))
        merged = []
        for e in cand:
            if merged and e["start"] < merged[-1]["end"]:
                continue  # chevauche le précédent (plus long) — ignoré
            merged.append(e)

        # Attribution des tokens ; une même valeur => même token.
        pii_mapping, value_to_token, counters = {}, {}, {}
        for ent in merged:
            value = text[ent["start"]:ent["end"]]
            prefix = ent["_prefix"]
            token = value_to_token.get((prefix, value))
            if token is None:
                idx = counters.get(prefix, 0)
                counters[prefix] = idx + 1
                token = f"<{prefix}_{idx}>"
                value_to_token[(prefix, value)] = token
                pii_mapping[token] = value
            ent["_token"] = token

        anonymized = text
        for ent in sorted(merged, key=lambda e: e["start"], reverse=True):
            anonymized = anonymized[:ent["start"]] + ent["_token"] + anonymized[ent["end"]:]

        # Canari post-masquage : un identifiant structuré encore présent = fuite -> 503.
        leak = _residual_pii(anonymized)
        if leak:
            ANONYMIZE_LEAK_CANARY.inc()
            ANONYMIZE_REQUESTS.labels(status="leak").inc()
            logger.warning("canari : PII résiduelle après masquage (%s)", leak)
            raise HTTPException(status_code=503, detail=f"pii residuelle: {leak}")
    except HTTPException:
        raise
    except Exception as exc:  # noqa: BLE001 — jamais str(exc) vers l'extérieur (contient de la PII)
        logger.exception("Erreur interne /anonymize")
        ANONYMIZE_REQUESTS.labels(status="503").inc()
        raise HTTPException(status_code=503, detail="erreur interne anonymisation")

    ANONYMIZE_REQUESTS.labels(status="ok").inc()
    ANONYMIZE_PII_MASKED.inc(len(merged))
    return {
        "status": "ok",
        "anonymized_text": anonymized,
        "pii_mapping": pii_mapping,
        "entities_found": len(merged),
        "by_source": {"regex": sum(1 for e in merged if e.get("_src") == "regex"),
                      "gliner": sum(1 for e in merged if e.get("_src") == "gliner")},
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


@app.get("/metrics")
async def metrics():
    """Métriques Prometheus (B6) — scrapées par le job 'anone'."""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "anone", "model_loaded": ner is not None}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
