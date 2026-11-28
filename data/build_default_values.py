"""Build data/default_values.csv from the Commission's Excel of default values (all countries).

Source: "DV correcting act_final update_06.08.xlsx" (EC, Annex I of Impl. Reg. (EU) 2025/2621
as corrected by Impl. Reg. (EU) 2026/1740). Download it from the CBAM page of DG TAXUD and run:
    python data/build_default_values.py "DV correcting act_final update_06.08.xlsx"
Needs openpyxl (dev only, not used by the app).

Only iron/steel and aluminium are kept (the goods of our users). For these, CBAM counts direct
emissions only (Annex II Reg. 2023/956), so total = direct; indirect is kept for information.
The sheet "Other Countries and Territories" becomes country_iso XX: it applies where a country is
not listed or has no value for a good (Annex I, introductory note) - see cbam.cost.default_value.
"""

import csv
import sys
from pathlib import Path

import openpyxl

SRC = ("https://taxation-customs.ec.europa.eu/document/download/1c05d211-80cb-4aaa-8ef0-e08005a95d7e_en"
       "?filename=DV%20correcting%20act_final%20update_06.08.xlsx (EC Excel v2, Annex I of Impl. Reg. "
       "(EU) 2025/2621 as corrected by Impl. Reg. (EU) 2026/1740)")
OUT = Path(__file__).resolve().parent / "default_values.csv"
MARKUP = {"2026": 0.10, "2027": 0.20, "2028": 0.30}

ISO = {  # sheet names as in the Excel (Excel cuts them at 31 characters)
    "Albania": "AL", "Algeria": "DZ", "Angola": "AO", "Argentina": "AR", "Armenia": "AM", "Australia": "AU",
    "Azerbaijan": "AZ", "Bangladesh": "BD", "Bahrain": "BH", "Belarus": "BY", "Benin": "BJ", "Bolivia": "BO",
    "Bosnia and Herzegovina": "BA", "Brazil": "BR", "Brunei": "BN", "Cambodia": "KH", "Cameroon": "CM",
    "Canada": "CA", "Chile": "CL", "China": "CN", "Colombia": "CO", "Congo": "CG",
    "Congo, Democratic Republic of": "CD", "Costa Rica": "CR", "Cuba": "CU", "Curaçao": "CW",
    "Dominican Republic": "DO", "Ecuador": "EC", "Egypt": "EG", "El Salvador": "SV", "Equatorial Guinea": "GQ",
    "Eritrea": "ER", "Eswatini": "SZ", "Ethiopia": "ET", "Gabon": "GA", "Georgia": "GE", "Ghana": "GH",
    "Guatemala": "GT", "Haiti": "HT", "Honduras": "HN", "Hong Kong": "HK", "India": "IN", "Indonesia": "ID",
    "Iran, Islamic Republic of": "IR", "Iraq": "IQ", "Israel": "IL", "Ivory Coast": "CI", "Jamaica": "JM",
    "Japan": "JP", "Jordan": "JO", "Kazakhstan": "KZ", "Kenya": "KE", "Korea, Republic of (South Korea": "KR",
    "Kuwait": "KW", "Kyrgyzstan": "KG", "Laos": "LA", "Lebanon": "LB", "Liberia": "LR", "Libya": "LY",
    "Madagascar": "MG", "Malaysia": "MY", "Mali": "ML", "Mauritania": "MR", "Mauritius": "MU", "Mexico": "MX",
    "Moldova, Republic of": "MD", "Mongolia": "MN", "Montenegro": "ME", "Morocco": "MA", "Mozambique": "MZ",
    "Myanmar": "MM", "Namibia": "NA", "Nepal": "NP", "New Caledonia and dependencies": "NC",
    "New Zealand": "NZ", "Nicaragua": "NI", "Niger": "NE", "Nigeria": "NG",
    "North Korea (Democratic People’": "KP", "North Macedonia": "MK", "Oman": "OM", "Pakistan": "PK",
    "Panama": "PA", "Papua New Guinea": "PG", "Paraguay": "PY", "Peru": "PE", "Philippines": "PH", "Qatar": "QA",
    "Russian Federation": "RU", "Rwanda": "RW", "Saudi Arabia": "SA", "Senegal": "SN", "Serbia": "RS",
    "Sierra Leone": "SL", "Singapore": "SG", "South Africa": "ZA", "Sri Lanka": "LK", "Sudan": "SD",
    "Suriname": "SR", "Syria": "SY", "Taiwan": "TW", "Tajikistan": "TJ", "Tanzania, United Republic of": "TZ",
    "Thailand": "TH", "Togo": "TG", "Trinidad and Tobago": "TT", "Tunisia": "TN", "Türkiye": "TR",
    "Turkmenistan": "TM", "Uganda": "UG", "Ukraine": "UA", "United Arab Emirates": "AE", "United Kingdom": "GB",
    "United States": "US", "Uruguay": "UY", "Uzbekistan": "UZ", "Venezuela": "VE", "Viet Nam": "VN",
    "Yemen": "YE", "Zambia": "ZM", "Zimbabwe": "ZW", "_Other Countries and Territorie": "XX",
}
SKIP = {"Overview", "Version History", "Annex IV"}


def num(x):
    try:
        return float(str(x).replace(",", "."))
    except (TypeError, ValueError):
        return None  # "-", "see below", empty


def rows_of(ws):
    sector = None
    for cn, _desc, direct, _ind, total, route, *_ in ws.iter_rows(min_row=1, values_only=True):
        cn = str(cn or "").strip()
        if cn and not any(ch.isdigit() for ch in cn):  # section header: "Iron and steel", "Aluminium", ...
            low = cn.lower()
            sector = "iron_steel" if ("iron" in low or "steel" in low) else "aluminium" if "alumin" in low else None
            continue
        d, t = num(direct), num(total)
        if sector and cn[:1].isdigit() and d is not None:
            yield cn.replace(" ", ""), sector, d, (t if t is not None else d), str(route or "").strip()


def main(xlsx):
    wb = openpyxl.load_workbook(xlsx, read_only=True, data_only=True)
    unknown = [n for n in wb.sheetnames if n not in SKIP and n not in ISO]
    if unknown:
        sys.exit(f"sheets without ISO code: {unknown}")
    out = []
    for name in wb.sheetnames:
        if name in SKIP:
            continue
        for cn, sector, d, t, route in rows_of(wb[name]):
            ind = round(t - d, 3)
            note = [f"Route {route}"] if route else []
            if ind:
                note.append("total = direct (Anhang II VO 2023/956); indirect nur informativ")
            if ISO[name] == "XX":
                note.append("Other countries and territories: gilt für nicht gelistete Länder/Waren")
            out.append([ISO[name], cn, sector, f"{d:.3f}", f"{ind:.3f}" if ind else "", f"{d:.3f}",
                        *[f"{round(d * (1 + m) + 1e-9, 3):.3f}" for m in MARKUP.values()], SRC, "; ".join(note)])
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["country_iso", "cn", "sector", "direct_tco2_per_t", "indirect_tco2_per_t", "total_tco2_per_t",
                    *[f"total_incl_markup_{y}" for y in MARKUP], "source", "note"])
        w.writerows(out)
    print(f"{len(out)} rows, {len({r[0] for r in out})} countries -> {OUT}")


if __name__ == "__main__":
    main(sys.argv[1])
