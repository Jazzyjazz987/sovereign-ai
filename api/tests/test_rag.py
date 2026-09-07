"""Tests de l'étape RAG (fiches citées) + filtres de screening dans main.py."""
import pytest

import main
import screening
import parcours


# --- _SMALLTALK ---------------------------------------------------------------------
def test_smalltalk_regex_matche_les_salutations():
    for s in ["bonjour", "Salut, ça va ?", "merci beaucoup", "qui es-tu ?",
              "tu fais quoi comme travail", "c'est quoi ton rôle"]:
        assert main._SMALLTALK.match(s), s
    for s in ["comment créer un compte utilisateur", "procédure de réforme d'un poste"]:
        assert not main._SMALLTALK.match(s), s


# --- voie de sauvegarde ------------------------------------------------------------
def test_safeguarding_declenche_sur_signal_de_detresse():
    # E5 : variantes de formulation qui échouaient auparavant
    for s in ["je pense au suicide", "j'ai envie d'en finir", "un agent veut se faire du mal",
              "je veux en finir avec tout ça", "je n'en peux plus, je pense à en finir",
              "je suis à bout, je craque, je n'ai plus goût à rien"]:
        r = screening.safeguarding(s)
        assert r is not None and r["tier"] == "sauvegarde" and r["model_used"] is None

    for s in ["mon poste ne démarre plus", "créer une boîte partagée",
              "comment débloquer un compte verrouillé ?"]:
        assert screening.safeguarding(s) is None


def test_safeguarding_insensible_accents_casse():
    assert screening.safeguarding("ME SUICIDER") is not None


# --- hors périmètre --------------------------------------------------------------
def test_looks_in_scope():
    assert screening.looks_in_scope("mon mot de passe M365 ne marche plus")
    assert screening.looks_in_scope("problème d'imprimante au bureau")
    assert not screening.looks_in_scope("quelle est la capitale de l'Australie ?")
    assert not screening.looks_in_scope("écris-moi un poème sur la mer")


def test_is_out_of_scope():
    for s in ["quelle est la capitale de l'Australie ?", "donne-moi la recette du poisson cru",
              "écris-moi un poème sur le lagon", "traduis cette phrase en anglais"]:
        assert screening.is_out_of_scope(s), s
    # un terme support annule le hors-périmètre même si un motif matche
    assert not screening.is_out_of_scope("traduis le message d'erreur de mon poste")
    # une vraie question support ne matche aucun motif
    for s in ["mon ordi rame à mort", "je n'ai plus accès à ma boîte mail"]:
        assert not screening.is_out_of_scope(s), s


def test_out_of_scope_card():
    r = screening.out_of_scope_card("recette du poisson cru")
    assert r["tier"] == "hors-perimetre" and r["model_used"] is None


# --- _rag_search / _rag_answer ---------------------------------------------------
@pytest.mark.asyncio
async def test_rag_search_none_si_service_injoignable(monkeypatch):
    monkeypatch.setattr(main, "RAG_URL", "http://127.0.0.1:9")  # port fermé -> échec rapide
    assert await main._rag_search("comment créer une BALP ?") is None


@pytest.mark.asyncio
async def test_rag_answer_none_si_pas_de_hits():
    assert await main._rag_answer("q", None) is None
    assert await main._rag_answer("q", []) is None


@pytest.mark.asyncio
async def test_rag_answer_none_si_hits_sous_le_plancher(monkeypatch):
    monkeypatch.setattr(main, "RAG_SCORE_FLOOR", -1.0)
    hits = [{"proc_code": "PROC-X", "section": "Étapes", "text": "p: x\ncorps",
             "rerank_score": -5.0, "domaine": "Test"}]
    assert await main._rag_answer("question", hits) is None


@pytest.mark.asyncio
async def test_rag_answer_ignore_les_pages_00_comme_primaire():
    """E1 : une page sans proc_code ne peut pas être la fiche primaire -> None."""
    hits = [{"doc_id": "00-registre-rgpd", "proc_code": None, "section": "Fiche",
             "text": "p: x\ncorps", "rerank_score": 0.9, "domaine": "RGPD"}]
    assert await main._rag_answer("question", hits) is None


@pytest.mark.asyncio
async def test_rag_answer_json_contrat(monkeypatch):
    """C2 : le modèle rend un JSON ; repond=false -> None, citation inconnue -> None."""
    hits = [{"proc_code": "PROC-ID-005", "section": "Étapes", "text": "p: x\ncorps",
             "rerank_score": 0.8, "domaine": "EntraID", "titre": "BALP"}]

    async def fake(*a, **k):
        return fake.out
    monkeypatch.setattr(main, "query_ollama", fake)

    fake.out = '{"repond": false, "reponse": "", "fiches": []}'
    assert await main._rag_answer("q", hits) is None

    fake.out = '{"repond": true, "reponse": "Voir PROC-ZZ-999.", "fiches": ["PROC-ZZ-999"]}'
    assert await main._rag_answer("q", hits) is None            # C3 : citation hors extraits

    # D2 : code hallucine dans la PROSE (pas dans `fiches`) -> rejet aussi
    fake.out = '{"repond": true, "reponse": "Faire X puis voir PROC-ZZ-999.", "fiches": []}'
    assert await main._rag_answer("q", hits) is None

    fake.out = '{"repond": true, "reponse": "Créer via Exchange (PROC-ID-005).", "fiches": ["PROC-ID-005"]}'
    r = await main._rag_answer("q", hits)
    assert r["tier"] == "RAG" and r["fiches"][0]["code"] == "PROC-ID-005"
    assert r["label"] == "Fondé sur fiches CPA"                 # score 0.8 >= HIGH

    fake.out = 'pas du json'
    assert await main._rag_answer("q", hits) is None


@pytest.mark.asyncio
async def test_query_cascade_bout_en_bout_rag(monkeypatch):
    """C20 : /query -> RAG (search + modèle mockés)."""
    monkeypatch.setattr(main, "RAG_ENABLED", True)
    monkeypatch.setattr(main, "RAG_CACHE_TTL", 0)  # pas de cache dans le test

    async def fake_search(q):
        return [{"chunk_id": "PROC-ID-005#1", "proc_code": "PROC-ID-005", "titre": "BALP",
                 "section": "Étapes", "domaine": "EntraID", "text": "passage: x\n1. Exchange…",
                 "rerank_score": 0.7, "source_url": "http://x"}]

    async def fake_ollama(*a, **k):
        return '{"repond": true, "reponse": "Créer via Exchange (PROC-ID-005).", "fiches": ["PROC-ID-005"]}'

    monkeypatch.setattr(main, "_rag_search", fake_search)
    monkeypatch.setattr(main, "query_ollama", fake_ollama)
    r = await main._query_cascade(main.QueryRequest(query="comment créer une BALP ?"))
    assert r["tier"] == "RAG" and r["fiches"][0]["code"] == "PROC-ID-005"


def test_parcours_depart_vs_mutation():
    d = parcours.match("un agent quitte l'administration, que faire ?")
    assert d and d["parcours_id"] == "depart-agent"
    assert {"PROC-ID-003", "PROC-STOCK-005"} <= {f["code"] for f in d["fiches"]}
    # « mutation » ne doit pas capter le parcours départ (anti)
    m = parcours.match("un agent est muté, changement de service")
    assert m and m["parcours_id"] == "mutation-agent"
    assert parcours.match("comment réinitialiser un MFA ?") is None


@pytest.mark.asyncio
async def test_query_cascade_parcours_avant_rag(monkeypatch):
    async def boom(*a, **k):
        raise AssertionError("le RAG ne doit pas être appelé sur un parcours")
    monkeypatch.setattr(main, "_rag_search", boom)
    r = await main._query_cascade(main.QueryRequest(query="un agent quitte l'administration"))
    assert r["tier"] == "parcours"


@pytest.mark.asyncio
async def test_query_cascade_safeguarding_prioritaire(monkeypatch):
    async def boom(*a, **k):
        raise AssertionError("aucun appel RAG/modèle sur un signal de détresse")
    monkeypatch.setattr(main, "_rag_search", boom)
    r = await main._query_cascade(main.QueryRequest(query="je pense à en finir"))
    assert r["tier"] == "sauvegarde"


def test_cache_key_normalise_accents_et_espaces_et_corpus(monkeypatch):
    """D3/D11 : accents + espaces ignorés ; l'empreinte corpus change la clé."""
    a = main._cache_key("Comment  créer   une BALP ?", "cfp1")
    b = main._cache_key("comment creer une balp ?", "cfp1")
    c = main._cache_key("comment creer une balp ?", "cfp2")
    assert a == b and a != c


def test_no_fiche_response():
    hits = [{"proc_code": "PROC-ID-003", "titre": "Désactivation", "section": "Étapes",
             "rerank_score": 0.2, "source_url": "http://x"},
            {"doc_id": "00-index", "proc_code": None, "rerank_score": 0.9}]
    r = main._no_fiche_response("q", hits)
    assert r["tier"] == "aucune-fiche" and r["model_used"] is None
    assert [f["code"] for f in r["fiches"]] == ["PROC-ID-003"]  # 00-* exclu
    assert "je n'ai pas de fiche" in r["response"].lower()
