import pytest

from cbam.suggest import material, suggest_cn


@pytest.mark.parametrize("desc, cn, cbam", [
    ("Drahtstifte 3,1x80 mm, blank", "7317 00", False),
    ("Sechskantschrauben M16x60, 8.8, feuerverzinkt", "7318", True),
    ("Schrauben aus Aluminium M8", "7616 10 00", True),
    ("Aluminium-Strangpressprofile EN AW-6060", "7604", True),
    ("HEB-Träger 200, S235JR", "7216", True),
    ("Treppenwangen geschweißt, Stahl", "7308", True),
    ("Geländer aus Aluminium", "7610", True),
    ("Kugelhähne DN25, Messing", "8481", False),
    ("Aluminiumfolie 0,1 mm", "7607", True),
    ("Grey Portland cement", "2523 29 00", True),
])
def test_first_suggestion(desc, cn, cbam):
    s = suggest_cn(desc)
    assert s, desc
    assert s[0]["cn"] == cn
    assert s[0]["cbam"] is cbam


def test_no_suggestion_for_unknown_or_empty():
    assert suggest_cn("Bürostuhl, ergonomisch") == []
    assert suggest_cn("") == []
    assert suggest_cn(None) == []


def test_material():
    assert material("Profile EN AW-6063") == "alu"
    assert material("Rohr S355 verzinkt") == "steel"
    assert material("Kabel") is None
