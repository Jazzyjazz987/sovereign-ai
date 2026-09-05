"""Fixtures et stubs partagés pour la suite de tests hors-ligne (B5)."""
import sys
import types

# anone_api.py fait `from transformers import pipeline` au chargement du module.
# transformers + torch sont lourds et totalement inutiles pour ces tests unitaires.
# On injecte un stub minimal AVANT toute importation d'anone_api : pipeline()
# renvoie None, donc anone_api.ner vaut None et aucun modèle n'est téléchargé.
if "transformers" not in sys.modules:
    _fake_transformers = types.ModuleType("transformers")
    _fake_transformers.pipeline = lambda *args, **kwargs: None
    sys.modules["transformers"] = _fake_transformers
