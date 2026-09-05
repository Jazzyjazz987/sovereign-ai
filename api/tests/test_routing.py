"""Tests unitaires purs du routeur de cascade (CascadeRouter, main.py)."""
from main import TIERS, CascadeRouter

router = CascadeRouter()
TIER_MODEL = {label: model for label, model in TIERS}


def test_complexity_reste_dans_les_bornes():
    """Le score de complexité reste toujours dans [1.0, 5.0]."""
    assert router.calculate_complexity("") >= 1.0
    assert 1.0 <= router.calculate_complexity("bonjour") <= 5.0
    # Requête saturée de mots-clés code + avancés et très longue -> plafonnée à 5.0
    lourde = router.calculate_complexity(
        "écris du code python function class debug api rest endpoint sql test "
        "architecture design pattern kubernetes docker terraform rgpd security "
        "compliance governance analyse strategy plan evaluate " * 4
    )
    assert lourde == 5.0


def test_complexity_croit_avec_mots_cles_et_longueur():
    """La complexité augmente avec les mots-clés code/avancés puis la longueur."""
    simple = router.calculate_complexity("salut ça va")
    code = router.calculate_complexity(
        "écris une function python pour debug cette api rest endpoint"
    )
    avance = router.calculate_complexity(
        "architecture design pattern microservices kubernetes docker "
        "rgpd compliance governance security"
    )
    assert simple < code < avance

    # À mots-clés identiques, une requête plus longue est plus complexe.
    court = router.calculate_complexity("analyse ce plan")
    long = router.calculate_complexity("analyse ce plan " + "et détaille chaque point " * 10)
    assert long > court


def test_route_mappe_les_bandes_de_complexite_vers_les_tiers():
    """1.0->T1, 2.0->T2, 3.0->T3, 4.0->T4, 5.0->T5 (conforme à TIERS)."""
    attendu = {1.0: "T1", 2.0: "T2", 3.0: "T3", 4.0: "T4", 5.0: "T5"}
    for score, label in attendu.items():
        model, complexity, tier = router.route("peu importe", complexity_override=score)
        assert tier == label
        assert model == TIER_MODEL[label]
        assert complexity == score


def test_route_modele_force():
    """'t1'..'t5' force le tier correspondant ; un modèle bidon retombe sur T1."""
    for label, model in TIERS:
        m, _, t = router.route("q", forced_model=label.lower())
        assert (t, m) == (label, model)

    m, _, t = router.route("q", forced_model="t9")
    assert t == "T1"
    assert m == TIER_MODEL["T1"]


def test_override_complexite_prime_sur_les_mots_cles():
    """Le paramètre complexity override l'emporte sur le score par mots-clés."""
    q = "architecture rgpd compliance kubernetes docker security governance analyse"
    _, _, tier_auto = router.route(q)
    assert tier_auto in ("T4", "T5")  # forte complexité par mots-clés

    _, _, tier_override = router.route(q, complexity_override=1.0)
    assert tier_override == "T1"
