"""Fine-tune bge-reranker-base sur le corpus CPA (GPU). À lancer avec .venv-ft.

    .venv-ft/bin/python rag/finetune/train.py

Sortie : rag/finetune/model/  (nouveau reranker). Pour l'activer en prod :
    RAG_RERANK_MODEL=/models/hf/... (monter le dossier)  — ou baker dans l'image rag.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import torch
from torch.utils.data import DataLoader
from sentence_transformers import InputExample
from sentence_transformers.cross_encoder import CrossEncoder
from sentence_transformers.cross_encoder.evaluation import CEBinaryClassificationEvaluator

FT = Path("rag/finetune")
BASE = "BAAI/bge-reranker-base"
OUT = str(FT / "model")
EPOCHS = 3
BATCH = 16


def _read(name: str) -> list[InputExample]:
    return [InputExample(texts=[e["query"], e["passage"]], label=float(e["label"]))
            for e in (json.loads(l) for l in (FT / name).read_text().splitlines() if l.strip())]


def main():
    assert torch.cuda.is_available(), "GPU requis"
    train, val = _read("train.jsonl"), _read("val.jsonl")
    print(f"train {len(train)} · val {len(val)} · GPU {torch.cuda.get_device_name(0)}")

    model = CrossEncoder(BASE, num_labels=1, max_length=512, device="cuda")
    dl = DataLoader(train, shuffle=True, batch_size=BATCH)
    evaluator = CEBinaryClassificationEvaluator.from_input_examples(val, name="cpa-val")
    warmup = math.ceil(len(dl) * EPOCHS * 0.1)

    model.fit(
        train_dataloader=dl,
        evaluator=evaluator,
        epochs=EPOCHS,
        warmup_steps=warmup,
        optimizer_params={"lr": 2e-5},
        weight_decay=0.01,
        use_amp=True,
        evaluation_steps=max(1, len(dl) // 2),
        output_path=OUT,
        save_best_model=True,
        show_progress_bar=True,
    )
    print(f"\n→ modèle fine-tuné : {OUT}")


if __name__ == "__main__":
    main()
