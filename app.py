"""CBAM-Lotse — Streamlit UI. Run: streamlit run app.py"""

from datetime import date
from pathlib import Path

import pandas as pd
import os

import streamlit as st

from cbam.agent import answer

from cbam.annex import check_annex_i, load_annex
from cbam.documents import report_pdf, supplier_letter
from cbam.cost import estimate_cost, load_default_values, load_prices
from cbam.threshold import THRESHOLD_T, threshold_status

ROOT = Path(__file__).resolve().parent
DEMO_CSV = ROOT / "demo" / "purchases_2026.csv"
COLUMNS = ["description", "cn", "net_mass_kg", "origin", "date", "supplier"]

OMNIBUS_URL = "https://eur-lex.europa.eu/eli/reg/2025/2083/oj"
CBAM_REG_URL = "https://eur-lex.europa.eu/eli/reg/2023/956/oj"
PRICE_URL = "https://taxation-customs.ec.europa.eu/carbon-border-adjustment-mechanism/price-cbam-certificates_en"

st.set_page_config(page_title="CBAM-Lotse", page_icon="🏭", layout="wide")


def try_load(loader):
    try:
        return loader()
    except FileNotFoundError:
        return None


annex = try_load(load_annex)
default_values = try_load(load_default_values)
prices = try_load(load_prices)

st.title("CBAM-Lotse")
st.caption("Betrifft mich CBAM? Prüfung Ihrer Stahl- und Aluminiumimporte gegen Anhang I "
           "und die 50-Tonnen-Schwelle — jede Zahl mit Quelle.")

if annex is None:
    st.error("data/annex_i.json fehlt — ohne Anhang I ist keine Prüfung möglich.")
    st.stop()

# 1. Importe erfassen
st.header("1. Importe erfassen")
tab_csv, tab_demo = st.tabs(["CSV hochladen", "Demo: Metallbau Gruber GmbH"])
lines = None
with tab_csv:
    st.write("Spalten: " + ", ".join(f"`{c}`" for c in COLUMNS))
    upload = st.file_uploader("Einkaufsliste (CSV)", type="csv")
    if upload:
        lines = pd.read_csv(upload, dtype={"cn": str})
with tab_demo:
    if DEMO_CSV.exists():
        if st.button("Demo-Rechnungen laden"):
            st.session_state["demo"] = True
        if st.session_state.get("demo"):
            lines = pd.read_csv(DEMO_CSV, dtype={"cn": str})
    else:
        st.info("Demo-Daten fehlen (demo/purchases_2026.csv).")

if lines is None:
    st.stop()

missing_cols = [c for c in COLUMNS if c not in lines.columns]
if missing_cols:
    st.error("Fehlende Spalten: " + ", ".join(missing_cols))
    st.stop()

st.write("Bitte KN-Codes und Gewichte prüfen — Sie können jede Zelle korrigieren.")
lines = st.data_editor(lines[COLUMNS + [c for c in lines.columns if c not in COLUMNS]], num_rows="dynamic", width="stretch")

# 2. Anhang I prüfen
st.header("2. Welche Waren sind CBAM-Waren?")
records = []
for row in lines.to_dict("records"):
    try:
        verdict = check_annex_i(row["cn"])
    except (ValueError, TypeError):
        verdict = {"cbam": None, "sector": None, "annex_entry": None, "description": None, "source": None}
    records.append({**row, **{k: verdict[k] for k in ("cbam", "sector", "annex_entry", "source")},
                    "annex_description": verdict["description"]})

result = pd.DataFrame(records)
st.dataframe(
    result[["description", "cn", "net_mass_kg", "origin", "cbam", "sector", "annex_entry", "annex_description", "source"]],
    width="stretch",
    column_config={"cbam": st.column_config.CheckboxColumn("CBAM-Ware"),
                   "annex_description": "Anhang I",
                   "source": st.column_config.LinkColumn("Quelle")},
)
unclear = result[result["cbam"].isna()]
if len(unclear):
    st.warning(f"{len(unclear)} Zeile(n) ohne gültigen KN-Code — bitte oben ergänzen.")

# 3. Schwelle
st.header("3. 50-Tonnen-Schwelle")
year = st.selectbox("Kalenderjahr", sorted({str(d)[:4] for d in result["date"]}, reverse=True))
status = threshold_status([r for r in records if r["cbam"]], int(year), today=date.today() if int(year) == date.today().year else None)
st.progress(min(status["share"], 1.0), text=f"{status['total_t']:.1f} t von {THRESHOLD_T:.0f} t CBAM-Waren im Jahr {year}")
if status["status"] == "exempt":
    st.success("Unter der Schwelle: von CBAM-Pflichten befreit. Die Befreiung ist in der Zollanmeldung anzugeben.")
elif status["status"] == "near":
    st.warning("Über 80 % der Schwelle — weitere Importe können die Pflicht auslösen.")
else:
    st.error("Schwelle überschritten (oder Strom/Wasserstoff importiert): Sie brauchen den Status "
             "als zugelassener CBAM-Anmelder.")
if status["forecast_crossing"]:
    st.write(f"Prognose beim bisherigen Tempo: Schwelle erreicht am **{status['forecast_crossing']}**.")
st.caption(f"Quelle: [Verordnung (EU) 2025/2083 (CBAM-Omnibus)]({OMNIBUS_URL}), Anhang I der [Verordnung (EU) 2023/956]({CBAM_REG_URL}).")

# 4. Kosten und Risiko
st.header("4. Kosten und Risiko")
cost = None
if default_values is None or prices is None:
    st.info("Standardwerte oder Zertifikatspreise fehlen noch (data/default_values.csv, data/cbam_prices.json).")
else:
    year_lines = [r for r in records if r["cbam"] and str(r["date"]).startswith(year)]
    cost = estimate_cost(year_lines, prices, default_values)
    c1, c2, c3 = st.columns(3)
    c1.metric("Graue Emissionen", f"{cost['total_emissions_t']:.1f} t CO₂e")
    c2.metric("Zertifikate (Quartalspreise)", f"€ {cost['certificate_cost_eur']:,.0f}")
    lo, hi = cost["penalty_range_eur"]
    c3.metric("Strafe ohne Zulassung", f"€ {lo:,.0f} – {hi:,.0f}")
    if cost["lines"]:
        st.dataframe(pd.DataFrame(cost["lines"])[["description", "cn", "origin", "quarter", "formula", "emissions_t", "certificate_eur", "factor_source"]],
                     width="stretch", column_config={"factor_source": "Quelle"})
    if cost["missing_default_value"]:
        st.warning(f"{len(cost['missing_default_value'])} Zeile(n) ohne Standardwert für Herkunftsland/KN — nicht geschätzt.")
    st.caption(f"Standardwerte inkl. Aufschlag des Jahres (DVO (EU) 2025/2621). Zertifikatspreis des Einfuhrquartals: "
               f"[Europäische Kommission]({PRICE_URL}). Strafe: 3–5 × € 100 je fehlendem Zertifikat, "
               "auf alle Emissionen des Jahres (Art. 26 Abs. 2a, vor Indexierung).")

# 5. Entscheidung
st.header("5. Ihre Optionen")
a, b, c = st.columns(3)
a.subheader("A · Unter 50 t bleiben")
a.write(f"Noch **{max(THRESHOLD_T - status['total_t'], 0):.1f} t** bis zur Schwelle. Käufe planen und dokumentieren.")
b.subheader("B · Zulassung beantragen")
b.write("Antrag als zugelassener CBAM-Anmelder beim AnEH (cbam@bmf.gv.at), bevor die Schwelle überschritten wird.")
CHECKLIST = ROOT / "data" / "declarant_checklist.md"
if CHECKLIST.exists():
    with b.expander("Checkliste Antrag"):
        st.markdown(CHECKLIST.read_text(encoding="utf-8"))
c.subheader("C · Lieferant fragen")
c.write("Echte Emissionsdaten beim Lieferanten anfordern — oft niedriger als die Standardwerte.")

# 6. Dokumente
st.header("6. Dokumente")
importer = st.text_input("Ihr Unternehmen", "Metallbau Gruber GmbH")
suppliers = sorted({r["supplier"] for r in records if r["cbam"] and isinstance(r.get("supplier"), str)})
if suppliers:
    s1, s2 = st.columns([3, 1])
    supplier = s1.selectbox("Brief an Lieferanten (Anfrage echter Emissionsdaten)", suppliers)
    lang = s2.radio("Sprache", ["de", "en"], horizontal=True)
    letter = supplier_letter(supplier, records, importer, lang)
    st.text_area("Brief", letter, height=320)
    st.download_button("Brief herunterladen (.txt)", letter, file_name=f"CBAM_Anfrage_{supplier[:20]}.txt")
pdf = report_pdf(importer, year, status, records, cost)
st.download_button("Bericht herunterladen (PDF)", pdf, file_name=f"CBAM_Bericht_{year}.pdf", mime="application/pdf")

# 7. Fragen an den Lotsen (KI)
st.header("7. Fragen an den Lotsen")
try:
    api_key = st.secrets.get("GEMINI_API_KEY")
except Exception:  # no secrets.toml locally
    api_key = None
api_key = api_key or os.environ.get("GEMINI_API_KEY")
if not api_key:
    st.caption("KI-Assistent aus (kein GEMINI_API_KEY) — Sie erhalten eine feste Zusammenfassung.")
question = st.chat_input("z. B. Was passiert, wenn ich im Herbst noch 20 t Profile kaufe?")
if question:
    ctx = {"lines": records, "year": int(year), "values": default_values,
           "prices": prices}
    with st.spinner("Der Lotse rechnet …"):
        text, calls = answer(question, ctx, api_key=api_key)
    st.chat_message("user").write(question)
    st.chat_message("assistant").write(text)
    for c in calls:
        with st.expander(f"Werkzeug: {c['name']}({c['args'] or ''})"):
            st.json(c["result"])
