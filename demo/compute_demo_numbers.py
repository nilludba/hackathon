"""Recompute the numbers in demo/demo_script.md from the demo PDFs.  Run: python demo/compute_demo_numbers.py"""
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from cbam.annex import check_annex_i  # noqa: E402
from cbam.cost import estimate_cost, load_default_values, load_prices  # noqa: E402
from cbam.extract import read_documents  # noqa: E402
from cbam.threshold import threshold_status  # noqa: E402


def mark(lines):
    out = []
    for l in lines:
        try:
            r = check_annex_i(l["cn"])
            out.append({**l, "cbam": r["cbam"], "sector": r["sector"]})
        except (ValueError, TypeError):
            out.append({**l, "cbam": False, "sector": None})
    return out


def main():
    imported, planned, errors = read_documents([(p, p.name) for p in sorted((ROOT / "demo").glob("*.pdf"))])
    imported, planned = mark(imported), mark(planned)
    cbam = [l for l in imported if l["cbam"]]
    status = threshold_status(cbam, 2026, today=date(2026, 11, 28))
    prices, values = load_prices(), load_default_values()
    now = estimate_cost(cbam, prices, values)
    after = estimate_cost(cbam + [l for l in planned if l["cbam"]], prices, values)
    planned_t = sum(l["net_mass_kg"] for l in planned if l["cbam"]) / 1000
    print(f"lines: {len(imported)}, CBAM: {len(cbam)}, errors: {errors}")
    print(f"imported 2026: {status['total_t']:.1f} t ({status['share']:.0%}), status {status['status']}")
    print(f"emissions {now['total_emissions_t']:.1f} t CO2e, certificates EUR {now['certificate_cost_eur']:,.0f}")
    print(f"after order (+{planned_t:.1f} t): {status['total_t'] + planned_t:.1f} t, "
          f"{after['total_emissions_t']:.1f} t CO2e, EUR {after['certificate_cost_eur']:,.0f}, "
          f"penalty EUR {after['penalty_range_eur'][0]:,.0f}-{after['penalty_range_eur'][1]:,.0f}")
    for r in now["lines"]:
        print(f"  {r['invoice']}  {r['cn']}  {r['origin']}  {r['formula']}  = EUR {r['certificate_eur']:,.0f}")


if __name__ == "__main__":
    main()
