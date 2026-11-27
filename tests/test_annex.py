import json
from pathlib import Path

import pytest

from cbam.annex import check_annex_i, normalize_cn

ENTRIES = json.loads((Path(__file__).parent / "fixtures" / "annex_sample.json").read_text(encoding="utf-8"))


@pytest.mark.parametrize("cn, cbam, sector", [
    ("7318 15 88", True, "iron_steel"),      # screws are in scope
    ("7308 90 59", True, "iron_steel"),      # steel structures
    ("7208 51 20", True, "iron_steel"),      # flat-rolled steel, chapter 72
    ("7204 49 10", False, None),             # ferrous scrap excluded
    ("7202 11 20", True, "iron_steel"),      # ferro-manganese stays in scope
    ("7202 21 00", False, None),             # ferro-silicon excluded
    ("7202 41 10", True, "iron_steel"),      # ferro-chromium stays in scope
    ("7604 29 10", True, "aluminium"),       # aluminium profiles
    ("7616 99 90", True, "aluminium"),
    ("7615 10 10", False, None),             # aluminium kitchen ware not listed
    ("2507 00 80", True, "cement"),          # calcined clay only
    ("2507 00 20", False, None),
    ("3105 20 10", True, "fertilisers"),
    ("3105 60 00", False, None),             # carved out
    ("2804 10 00", True, "hydrogen"),
    ("2716 00 00", True, "electricity"),
    ("8481 80 85", False, None),             # valves: machinery, not CBAM
    ("9403 20 80", False, None),             # metal furniture: not CBAM
])
def test_check_annex_i(cn, cbam, sector):
    result = check_annex_i(cn, ENTRIES)
    assert result["cbam"] is cbam
    assert result["sector"] == sector


def test_longest_prefix_wins():
    assert check_annex_i("7318 15", ENTRIES)["annex_entry"] == "7318"


def test_result_carries_source():
    assert check_annex_i("7604", ENTRIES)["source"] == "test fixture"


@pytest.mark.parametrize("bad", ["", "73", "abc"])
def test_too_short_code_rejected(bad):
    with pytest.raises(ValueError):
        normalize_cn(bad)
