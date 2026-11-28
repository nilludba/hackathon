"""Check whether a CN code is a CBAM good under Annex I of Regulation (EU) 2023/956."""

import json
import re
from functools import lru_cache
from pathlib import Path

ANNEX_FILE = Path(__file__).resolve().parent.parent / "data" / "annex_i.json"


def normalize_cn(cn):
    """'7318 15 88' -> '73181588'. Raises ValueError if fewer than 4 digits."""
    digits = re.sub(r"\D", "", str(cn))
    if len(digits) < 4:
        raise ValueError(f"CN code needs at least 4 digits: {cn!r}")
    return digits


@lru_cache(maxsize=None)
def load_annex(path=ANNEX_FILE):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _excluded(code, entry):
    if any(code.startswith(x) for x in entry.get("include_back", [])):
        return False
    return any(code.startswith(x) for x in entry.get("exclude", []))


def check_annex_i(cn, entries=None):
    """Return the Annex I verdict for one CN code.

    The longest matching Annex I prefix wins; an entry does not match if the code
    falls under its `exclude` list (unless it is in `include_back`).
    """
    code = normalize_cn(cn)
    entries = load_annex() if entries is None else entries
    best = None
    for entry in entries:
        if code.startswith(entry["cn"]) and not _excluded(code, entry):
            if best is None or len(entry["cn"]) > len(best["cn"]):
                best = entry
    return {
        "cn": code,
        "cbam": best is not None,
        "sector": best["sector"] if best else None,
        "annex_entry": best["cn"] if best else None,
        "description": best.get("description_de") if best else None,
        "source": best.get("source") if best else None,
    }


# --- Origin: CBAM covers goods originating in a third country (Art. 2(1) Reg. 2023/956) ---------

EU_MEMBER_STATES = {"AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "GR", "EL", "HU", "IE", "IT",
                    "LV", "LT", "LU", "MT", "NL", "PL", "PT", "RO", "SK", "SI", "ES", "SE"}
EU_CUSTOMS_EXTRA = {"MC"}  # Monaco belongs to the customs territory of the Union (Art. 4 UCC)
# Annex III point 1 Reg. 2023/956: countries in or linked to the EU ETS, and five territories
ANNEX_III = {"IS": "Island", "LI": "Liechtenstein", "NO": "Norwegen", "CH": "Schweiz",
             "XB": "Büsingen", "XH": "Helgoland", "XV": "Livigno", "XC": "Ceuta", "XL": "Melilla"}
# XC/XL are the EU statistics codes for Ceuta/Melilla; XB/XH/XV are our own codes for the other three.


def origin_exemption(origin):
    """Why goods of this origin are outside CBAM, or None if CBAM applies.

    Returns {"reason": "eu" | "annex_iii", "label": ...}. What counts is the origin of the goods,
    not where the supplier sits: Chinese steel bought from a Swiss trader is still a CBAM good."""
    o = str(origin or "").strip().upper()
    if o in EU_MEMBER_STATES or o in EU_CUSTOMS_EXTRA or o == "EU":
        return {"reason": "eu", "label": o}
    if o in ANNEX_III:
        return {"reason": "annex_iii", "label": ANNEX_III[o]}
    return None
