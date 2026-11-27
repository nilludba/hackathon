"""Embedded emissions, CBAM certificate cost and penalty scenario.

Emissions use the Commission's default values (Implementing Regulation (EU) 2025/2621)
from data/default_values.csv. Price comes from data/cbam_prices.json.
Penalty for exceeding the threshold without authorised-declarant status:
3-5 times EUR 100 per uncovered certificate, i.e. EUR 300-500 per t CO2e before
indexation, on all emissions of the year (Art. 26(2a) as amended by 2025/2083).
"""

import csv
import json
from functools import lru_cache
from pathlib import Path

from cbam.annex import normalize_cn

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
PENALTY_EUR_PER_T = (300, 500)


@lru_cache(maxsize=None)
def load_default_values(path=DATA_DIR / "default_values.csv"):
    with open(path, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["cn"] = normalize_cn(r["cn"])
        r["total_tco2_per_t"] = float(r["total_tco2_per_t"])
        for k in [k for k in r if k.startswith("total_incl_markup_")]:
            r[k] = float(r[k]) if r[k] else None
    return rows


@lru_cache(maxsize=None)
def load_prices(path=DATA_DIR / "cbam_prices.json"):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def latest_price(prices):
    quarters = sorted(k for k in prices if k[:4].isdigit())
    return quarters[-1], prices[quarters[-1]]


def price_for(day, prices):
    """(quarter, EUR) for the import date: 2026 imports use the price of their quarter.
    Quarter not yet published -> latest known price, quarter marked as estimate."""
    q = f"{str(day)[:4]}-Q{(int(str(day)[5:7]) - 1) // 3 + 1}"
    if q in prices:
        return q, prices[q]
    lq, lp = latest_price(prices)
    return f"{lq} (Schätzung für {q})", lp


def factor(dv, year):
    """Default value incl. the mark-up of the declaration year (Impl. Reg. 2025/2621), if given."""
    return dv.get(f"total_incl_markup_{year}") or dv["total_tco2_per_t"]


def default_value(cn, country, values):
    """Longest-prefix default value for (CN code, origin country), or None."""
    code = normalize_cn(cn)
    matches = [v for v in values if v["country_iso"] == country and code.startswith(v["cn"])]
    return max(matches, key=lambda v: len(v["cn"])) if matches else None


def estimate_cost(lines, price, values):
    """Lines need: cbam, cn, origin, net_mass_kg, date (if price is a dict).
    price: one EUR price, or the cbam_prices.json dict for per-quarter prices."""
    rows, missing = [], []
    for l in lines:
        if not l.get("cbam"):
            continue
        dv = default_value(l["cn"], l["origin"], values)
        if dv is None:
            missing.append(l)
            continue
        quarter, price_eur = price_for(l["date"], price) if isinstance(price, dict) else (None, price)
        f = factor(dv, str(l.get("date", ""))[:4])
        mass_t = l["net_mass_kg"] / 1000
        emissions = mass_t * f
        rows.append({
            **l,
            "mass_t": mass_t,
            "factor_tco2_per_t": f,
            "emissions_t": emissions,
            "quarter": quarter,
            "price_eur": price_eur,
            "certificate_eur": emissions * price_eur,
            "factor_source": dv.get("source"),
            "formula": f"{mass_t:g} t x {f:g} tCO2e/t x EUR {price_eur:g}",
        })
    total_emissions = sum(r["emissions_t"] for r in rows)
    return {
        "lines": rows,
        "missing_default_value": missing,
        "total_emissions_t": total_emissions,
        "certificate_cost_eur": sum(r["certificate_eur"] for r in rows),
        "penalty_range_eur": tuple(total_emissions * p for p in PENALTY_EUR_PER_T),
    }
