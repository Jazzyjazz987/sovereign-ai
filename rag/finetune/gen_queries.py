"""Génère des questions synthétiques par procédure avec qwen2.5:7b (local, souverain).

Sortie : rag/finetune/queries.jsonl  — {q, proc_code, source}
En attendant les vrais tickets/mails, c'est la graine du jeu d'entraînement du reranker.
"""
from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

import httpx

OLLAMA = "http://localhost:11434"
MODEL = "qwen2.5:7b"
# Migration 2026-09-19 : générer sur le corpus RÉELLEMENT actif (hybride en vigueur +
# les 6 procédures legacy non hybridées), pas sur l'ancien corpus dans son ensemble —
# 25 des 31 fiches legacy sont archivées, un reranker entraîné dessus désapprend le
# vocabulaire des fiches hybrides (tableaux 🟠/🔵, chapitres numérotés).
CORPORA = [Path("corpus/02-procedures-hybride"), Path("corpus/01-procedures-legacy")]
OUT = Path("rag/finetune/queries.jsonl")

SYS = (
    "Tu génères des questions d'utilisateurs pour entraîner un moteur de recherche interne.\n"
    "À partir d'une fiche de procédure de la cellule support informatique (DSI Polynésie "
    "française), produis des questions COURTES, variées, en français, telles qu'un agent de "
    "support les taperait, et auxquelles CETTE fiche répond.\n"
    "Varie les formulations : question directe, mots-clés, cas concret, « comment… », "
    "« que faire quand… », « procédure pour… », abréviations métier.\n"
    "Rends un JSON : {\"questions\": [\"...\", ...]}. Rien d'autre."
)


def _meta(text: str) -> tuple[str, str]:
    title = ""
    m = re.search(r"^#\s+(.+)$", text, re.M)
    if m:
        title = m.group(1).strip()
    obj = ""
    m = re.search(r"##\s*🎯?\s*Objet\s*\n+(.+?)(?:\n##|\Z)", text, re.S)
    if m:
        obj = " ".join(m.group(1).split())[:400]
    return title, obj


def gen_for(path: Path, n: int = 8) -> list[str]:
    text = path.read_text(encoding="utf-8")
    title, obj = _meta(text)
    prompt = f"FICHE : {title}\nOBJET : {obj}\n\nGénère {n} questions."
    r = httpx.post(f"{OLLAMA}/api/generate", json={
        "model": MODEL, "system": SYS, "prompt": prompt, "stream": False, "format": "json",
        "options": {"temperature": 0.9, "num_predict": 500},
    }, timeout=120)
    try:
        qs = json.loads(r.json()["response"]).get("questions", [])
    except Exception:  # noqa: BLE001
        return []
    return [q.strip() for q in qs if isinstance(q, str) and 6 <= len(q.strip()) <= 160]


def main():
    procs = sorted(p for c in CORPORA for p in c.glob("PROC-*.md"))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    seen = set()
    with OUT.open("w", encoding="utf-8") as f:
        # graine : les questions du jeu d'éval (vraies formulations d'opérateur)
        for line in Path("eval/dataset.yaml").read_text().splitlines():
            pass  # (chargé à part dans build_dataset)
        for i, p in enumerate(procs, 1):
            code = p.stem
            for attempt in range(2):
                qs = gen_for(p)
                if qs:
                    break
                time.sleep(1)
            kept = 0
            for q in qs:
                key = q.lower()
                if key in seen:
                    continue
                seen.add(key)
                f.write(json.dumps({"q": q, "proc_code": code, "source": "qwen"},
                                   ensure_ascii=False) + "\n")
                kept += 1
            print(f"[{i:2}/{len(procs)}] {code}: {kept} questions", flush=True)
    print(f"\n→ {OUT}  ({sum(1 for _ in OUT.open())} lignes)")


if __name__ == "__main__":
    sys.exit(main())
