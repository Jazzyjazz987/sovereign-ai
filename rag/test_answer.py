"""Boucle complète : question -> /search -> réponse citée par qwen2.5:7b.

Démo du portail à fiches citées (POC). Le modèle ne répond QUE depuis les extraits.
"""
import sys
import textwrap
import httpx

from embed import embed_query
import store

OLLAMA = "http://localhost:11434"
MODEL = "qwen2.5:7b"

SYS = (
    "Tu es l'assistant interne de la cellule Parc & Assistance (support informatique) de la "
    "DSI de Polynésie française. Tu aides un agent de support.\n"
    "Réponds UNIQUEMENT à partir des EXTRAITS fournis. Si l'information n'y est pas, dis "
    "« Je n'ai pas de fiche sur ce point. » N'invente aucune référence ni procédure.\n"
    "Cite les fiches utilisées par leur code (ex. PROC-ID-004) à la fin."
)


def answer(question: str, k: int = 5):
    hits = store.search(embed_query(question), k=k)
    ctx = "\n\n".join(
        f"[{h['proc_code'] or h['doc_id']} §{h['section']}]\n{h['text'].split(chr(10), 1)[-1]}"
        for h in hits
    )
    prompt = f"EXTRAITS :\n{ctx}\n\nQUESTION : {question}\n\nRÉPONSE :"
    r = httpx.post(f"{OLLAMA}/api/generate",
                   json={"model": MODEL, "system": SYS, "prompt": prompt, "stream": False},
                   timeout=120)
    out = r.json()["response"].strip()
    print(f"\n### {question}\n")
    print(textwrap.fill(out, 100))
    print("\nfiches récupérées :", ", ".join(
        f"{h['proc_code'] or h['doc_id']}({h['score']:.2f})" for h in hits))
    print("source :", hits[0]["source_url"])


if __name__ == "__main__":
    q = " ".join(sys.argv[1:]) or "un agent a oublié son mot de passe M365, quelle est la procédure ?"
    answer(q)
