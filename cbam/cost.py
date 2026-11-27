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
    return rows


@lru_cache(maxsize=None)
def load_prices(path=DATA_DIR / "cbam_prices.json"):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def latest_price(prices):
    quarters = sorted(k for k in prices if k[:4].isdigit())
    return quarters[-1], prices[quarters[-1]]


def default_value(cn, country, values):
    """Longest-prefix default value for (CN code, origin country), or None."""
    code = normalize_cn(cn)
    matches = [v for v in values if v["country_iso"] == country and code.startswith(v["cn"])]
    return max(matches, key=lambda v: len(v["cn"])) if matches else None


def estimate_cost(lines, price_eur, values):
    """Lines need: cbam, cn, origin, net_mass_kg. Returns per-line and total figures."""
    rows, missing = [], []
    for l in lines:
        if not l.get("cbam"):
            continue
        dv = default_value(l["cn"], l["origin"], values)
        if dv is None:
            missing.append(l)
            continue
        mass_t = l["net_mass_kg"] / 1000
        emissions = mass_t * dv["total_tco2_per_t"]
        rows.append({
            **l,
            "mass_t": mass_t,
            "factor_tco2_per_t": dv["total_tco2_per_t"],
            "emissions_t": emissions,
            "certificate_eur": emissions * price_eur,
            "factor_source": dv.get("source"),
            "formula": f"{mass_t:g} t x {dv['total_tco2_per_t']:g} tCO2e/t x EUR {price_eur:g}",
        })
    total_emissions = sum(r["emissions_t"] for r in rows)
    return {
        "lines": rows,
        "missing_default_value": missing,
        "total_emissions_t": total_emissions,
        "price_eur": price_eur,
        "certificate_cost_eur": total_emissions * price_eur,
        "penalty_range_eur": tuple(total_emissions * p for p in PENALTY_EUR_PER_T),
    }
