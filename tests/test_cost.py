import pytest

from cbam.cost import default_value, estimate_cost, latest_price, price_for

VALUES = [
    {"country_iso": "TR", "cn": "73", "total_tco2_per_t": 2.0, "source": "test"},
    {"country_iso": "TR", "cn": "7318", "total_tco2_per_t": 2.5, "source": "test"},
    {"country_iso": "CN", "cn": "7604", "total_tco2_per_t": 10.0, "source": "test"},
]


def test_longest_prefix_default_value():
    assert default_value("7318 15 88", "TR", VALUES)["total_tco2_per_t"] == 2.5
    assert default_value("7308 90", "TR", VALUES)["total_tco2_per_t"] == 2.0
    assert default_value("7318 15", "CN", VALUES) is None


def test_estimate_cost_formula():
    lines = [
        {"cbam": True, "cn": "7318 15", "origin": "TR", "net_mass_kg": 4_000},   # 4 t x 2.5 = 10 t
        {"cbam": True, "cn": "7604 29", "origin": "CN", "net_mass_kg": 2_000},   # 2 t x 10 = 20 t
        {"cbam": False, "cn": "8481 80", "origin": "CN", "net_mass_kg": 9_000},
    ]
    r = estimate_cost(lines, 80.0, VALUES)
    assert r["total_emissions_t"] == pytest.approx(30.0)
    assert r["certificate_cost_eur"] == pytest.approx(2_400.0)
    assert r["penalty_range_eur"] == pytest.approx((9_000.0, 15_000.0))
    assert len(r["lines"]) == 2


def test_missing_default_value_is_reported_not_guessed():
    r = estimate_cost([{"cbam": True, "cn": "7318", "origin": "IN", "net_mass_kg": 1_000}], 80.0, VALUES)
    assert r["total_emissions_t"] == 0 and len(r["missing_default_value"]) == 1


def test_latest_price_picks_last_quarter():
    prices = {"2026-Q1": 75.36, "2026-Q3": 82.32, "2026-Q2": 75.28, "source": "x"}
    assert latest_price(prices) == ("2026-Q3", 82.32)


def test_price_per_quarter_and_markup():
    values = [{"country_iso": "TR", "cn": "7318", "total_tco2_per_t": 2.0,
               "total_incl_markup_2026": 2.2, "source": "test"}]
    prices = {"2026-Q1": 75.0, "2026-Q3": 82.0, "source": "x"}
    lines = [
        {"cbam": True, "cn": "7318", "origin": "TR", "net_mass_kg": 10_000, "date": "2026-02-01"},  # Q1
        {"cbam": True, "cn": "7318", "origin": "TR", "net_mass_kg": 10_000, "date": "2026-11-01"},  # Q4 -> Q3 price
    ]
    r = estimate_cost(lines, prices, values)
    assert r["total_emissions_t"] == pytest.approx(44.0)          # 20 t x 2.2 (2026 mark-up)
    assert r["certificate_cost_eur"] == pytest.approx(22 * 75 + 22 * 82)
    assert price_for("2026-11-01", prices) == ("2026-Q3 (Schätzung für 2026-Q4)", 82.0)
