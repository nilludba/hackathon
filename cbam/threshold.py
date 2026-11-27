"""50-tonne annual exemption threshold (CBAM Omnibus, Regulation (EU) 2025/2083).

Net mass of all CBAM goods imported by one importer in a calendar year is summed.
Electricity and hydrogen have no threshold: any import of them is in scope.
"""

from datetime import date, timedelta

THRESHOLD_T = 50.0
NEAR_SHARE = 0.8
NO_THRESHOLD_SECTORS = {"electricity", "hydrogen"}


def threshold_status(lines, year, today=None):
    """Lines need keys: cbam (bool), sector, net_mass_kg, date ('YYYY-MM-DD')."""
    year_lines = [l for l in lines if l.get("cbam") and str(l.get("date") or "").startswith(str(year))]
    no_threshold = [l for l in year_lines if l["sector"] in NO_THRESHOLD_SECTORS]
    counted = [l for l in year_lines if l["sector"] not in NO_THRESHOLD_SECTORS]
    total_t = sum(l.get("net_mass_kg") or 0 for l in counted) / 1000

    if no_threshold or total_t > THRESHOLD_T:
        status = "over"
    elif total_t >= NEAR_SHARE * THRESHOLD_T:
        status = "near"
    else:
        status = "exempt"

    return {
        "year": year,
        "total_t": round(total_t, 3),
        "threshold_t": THRESHOLD_T,
        "share": round(total_t / THRESHOLD_T, 4),
        "status": status,
        "no_threshold_goods": bool(no_threshold),
        "forecast_crossing": _forecast(counted, total_t, year, today) if status != "over" else None,
    }


def _forecast(lines, total_t, year, today):
    """Linear forecast from the year's average import rate up to `today`."""
    if not lines or total_t == 0:
        return None
    start = date(year, 1, 1)
    today = today or max(date.fromisoformat(l["date"]) for l in lines)
    days = (today - start).days + 1
    rate_t_per_day = total_t / days
    crossing = today + timedelta(days=(THRESHOLD_T - total_t) / rate_t_per_day)
    return crossing.isoformat() if crossing.year == year else None
