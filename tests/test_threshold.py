from datetime import date

from cbam.threshold import threshold_status


def line(kg, day, sector="iron_steel", cbam=True):
    return {"cbam": cbam, "sector": sector, "net_mass_kg": kg, "date": day}


def test_below_threshold_is_exempt():
    s = threshold_status([line(20_000, "2026-03-01")], 2026)
    assert s["status"] == "exempt" and s["total_t"] == 20.0


def test_exactly_50_t_is_not_over():
    s = threshold_status([line(50_000, "2026-03-01")], 2026)
    assert s["status"] == "near"


def test_just_over_threshold():
    s = threshold_status([line(49_900, "2026-03-01"), line(200, "2026-04-01")], 2026)
    assert s["status"] == "over" and s["total_t"] == 50.1


def test_near_threshold_at_80_percent():
    assert threshold_status([line(40_000, "2026-05-01")], 2026)["status"] == "near"


def test_steel_and_aluminium_are_summed():
    s = threshold_status([line(30_000, "2026-02-01"), line(25_000, "2026-06-01", "aluminium")], 2026)
    assert s["status"] == "over" and s["total_t"] == 55.0


def test_non_cbam_and_other_years_ignored():
    s = threshold_status([
        line(40_000, "2026-02-01", cbam=False),
        line(40_000, "2025-12-31"),
        line(1_000, "2026-01-15"),
    ], 2026)
    assert s["total_t"] == 1.0


def test_electricity_has_no_threshold():
    s = threshold_status([line(1, "2026-02-01", "electricity")], 2026)
    assert s["status"] == "over" and s["no_threshold_goods"]


def test_forecast_crossing_date():
    # 25 t in 181 days -> the remaining 25 t take another 181 days: 30 June + 181 = 28 December
    s = threshold_status([line(25_000, "2026-06-30")], 2026, today=date(2026, 6, 30))
    assert s["forecast_crossing"] == "2026-12-28"


def test_no_forecast_if_not_reached_this_year():
    s = threshold_status([line(5_000, "2026-06-30")], 2026, today=date(2026, 6, 30))
    assert s["forecast_crossing"] is None
