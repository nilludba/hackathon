"""Sanity checks for data/default_values.csv and data/cbam_prices.json."""

import pytest

from cbam.cost import default_value, latest_price, load_default_values, load_prices


def test_prices_2026():
    p = load_prices()
    assert p["2026-Q1"] == 75.36 and p["2026-Q2"] == 75.28 and p["2026-Q3"] == 82.32
    assert latest_price(p) == ("2026-Q3", 82.32)
    assert p["source"].startswith("https://taxation-customs.ec.europa.eu/")


def test_default_values_cover_three_countries_with_source():
    rows = load_default_values()
    assert {r["country_iso"] for r in rows} == {"TR", "CN", "IN"}
    assert all(r["source"] for r in rows)
    assert {r["sector"] for r in rows} == {"iron_steel", "aluminium"}


@pytest.mark.parametrize("cn, country, total, markup_2026", [
    ("7308 90 59", "TR", 5.520, 6.072),   # steel structures, Turkey
    ("7318 15 88", "TR", 5.430, 5.973),   # screws, Turkey
    ("7318 15 88", "CN", 6.375, 7.013),
    ("7604 29 90", "CN", 4.881, 5.369),   # aluminium profiles, China
    ("7604 29 90", "IN", 3.444, 3.788),
    ("7216 33 10", "TR", 2.310, 2.541),   # H-sections fall back to heading 7216
])
def test_default_value_lookup(cn, country, total, markup_2026):
    dv = default_value(cn, country, load_default_values())
    assert dv is not None
    assert dv["total_tco2_per_t"] == pytest.approx(total)
    assert float(dv["total_incl_markup_2026"]) == pytest.approx(markup_2026, abs=0.0015)


def test_unknown_country_returns_none():
    assert default_value("7308 90 59", "RS", load_default_values()) is None
