"""Checks the real data/annex_i.json against Annex I of Regulation (EU) 2023/956."""

import pytest

from cbam.annex import check_annex_i, load_annex


def test_annex_has_42_entries_with_sources():
    entries = load_annex()
    assert len(entries) == 42
    assert all(e["source"].startswith("https://eur-lex.europa.eu/") for e in entries)
    assert {e["sector"] for e in entries} == {
        "iron_steel", "aluminium", "cement", "fertilisers", "hydrogen", "electricity"}


@pytest.mark.parametrize("cn, cbam, sector", [
    # iron and steel
    ("7318 15 88", True, "iron_steel"),    # screws
    ("7308 90 59", True, "iron_steel"),    # structures
    ("7216 33 10", True, "iron_steel"),    # H-sections, chapter 72
    ("7208 51 20", True, "iron_steel"),    # flat-rolled
    ("7326 90 98", True, "iron_steel"),
    ("2601 12 00", True, "iron_steel"),    # agglomerated iron ore
    ("2601 11 00", False, None),           # non-agglomerated ore
    ("7204 49 10", False, None),           # scrap
    ("7202 11 20", True, "iron_steel"),    # ferro-manganese
    ("7202 41 10", True, "iron_steel"),    # ferro-chromium
    ("7202 60 00", True, "iron_steel"),    # ferro-nickel
    ("7202 21 00", False, None),           # ferro-silicon
    ("7202 30 00", False, None),           # ferro-silico-manganese
    ("7202 99 80", False, None),
    ("7317 00 20", False, None),           # nails: not listed
    ("7312 10 20", False, None),           # stranded wire of steel: not listed
    # aluminium
    ("7604 29 10", True, "aluminium"),
    ("7601 10 00", True, "aluminium"),
    ("7616 99 90", True, "aluminium"),
    ("7602 00 90", False, None),           # aluminium scrap
    ("7615 10 10", False, None),           # kitchen ware
    # others
    ("2523 29 00", True, "cement"),
    ("2507 00 80", True, "cement"),
    ("2507 00 20", False, None),
    ("3105 20 10", True, "fertilisers"),
    ("3105 60 00", False, None),
    ("2814 10 00", True, "fertilisers"),
    ("2804 10 00", True, "hydrogen"),
    ("2716 00 00", True, "electricity"),
    ("8481 80 85", False, None),           # valves
    ("9403 20 80", False, None),           # metal furniture
])
def test_real_annex(cn, cbam, sector):
    r = check_annex_i(cn)
    assert r["cbam"] is cbam
    assert r["sector"] == sector
    if cbam:
        assert r["source"]
