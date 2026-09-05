"""Fixtures et stubs partagés pour la suite de tests hors-ligne (B5)."""
import sys
import types

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
