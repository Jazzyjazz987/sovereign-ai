"""Fixtures et stubs partagés pour la suite de tests hors-ligne (B5)."""
import os
import sys
import tempfile
import types

# main.py charge config/prompts.yaml au démarrage (fail-fast). En test, le dossier config/
# n'est pas monté : on écrit un pack minimal dans un tmp et on pointe PROMPTS_PATH dessus
# AVANT toute importation de main.
if "PROMPTS_PATH" not in os.environ:
    _p = os.path.join(tempfile.gettempdir(), "prompts_test.yaml")
    with open(_p, "w", encoding="utf-8") as _f:
        _f.write("version: 1\ncommun: 'C'\ntiers:\n  T1: '{commun} t1'\n  T4: '{commun} t4'\n")
    os.environ["PROMPTS_PATH"] = _p

# anone_api.py fait `from gliner import GLiNER` au chargement du module. gliner
# (+ transformers + torch) est lourd et inutile pour ces tests : on injecte un
# stub minimal AVANT toute importation d'anone_api. GLiNER.from_pretrained lève,
# donc anone_api.ner vaut None ; les tests qui ont besoin d'un modèle
# monkeypatchent directement anone_api.ner.
if "gliner" not in sys.modules:
    _fake_gliner = types.ModuleType("gliner")

    class _StubGLiNER:
        @classmethod
        def from_pretrained(cls, *args, **kwargs):
            raise RuntimeError("gliner stub — pas de modèle en test")

    _fake_gliner.GLiNER = _StubGLiNER
    sys.modules["gliner"] = _fake_gliner
