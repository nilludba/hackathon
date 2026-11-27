"""CBAM-Lotse — Streamlit UI. Run: streamlit run app.py"""

from datetime import date
from pathlib import Path

import pandas as pd
import os

import streamlit as st

from i18n import LANGS, tr

from cbam.agent import answer

from cbam.annex import check_annex_i, load_annex
from cbam.documents import report_pdf, supplier_letter
from cbam.extract import read_documents
from cbam.cost import estimate_cost, load_default_values, load_prices
from cbam.threshold import THRESHOLD_T, threshold_status

ROOT = Path(__file__).resolve().parent
DEMO_CSV = ROOT / "demo" / "purchases_2026.csv"
DEMO_PDFS = sorted((ROOT / "demo").glob("*.pdf"))
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

L = LANGS[st.radio("Sprache / Language / Язык", list(LANGS), horizontal=True, key="ui_lang")]


def _(text, **kw):
    return tr(text, L, **kw)


st.title("CBAM-Lotse")
st.caption(_("Betrifft mich CBAM? Prüfung Ihrer Stahl- und Aluminiumimporte gegen Anhang I und die 50-Tonnen-Schwelle — jede Zahl mit Quelle."))

if annex is None:
    st.error(_("data/annex_i.json fehlt — ohne Anhang I ist keine Prüfung möglich."))
    st.stop()

# 1. Importe erfassen
st.header(_("1. Importe erfassen"))
tab_pdf, tab_csv, tab_demo = st.tabs([_("Rechnungen (PDF) hochladen"), _("CSV hochladen"), "Demo: Metallbau Gruber GmbH"])
lines = None
planned_lines = []  # order confirmations: planned imports, never counted as imported


def use_documents(files):
    """Read PDFs with cbam.extract; returns invoice lines as DataFrame (or None)."""
    global planned_lines
    imported, planned_lines, errors = read_documents(files)
    for e in errors:
        st.warning(e)
    st.caption(_("{n} Dokument(e) gelesen: {inv} Rechnungszeile(n), {plan} geplante Zeile(n) aus Auftragsbestätigungen.",
                 n=len(files), inv=len(imported), plan=len(planned_lines)))
    return pd.DataFrame(imported) if imported else None


with tab_pdf:
    st.write(_("Rechnungen und Auftragsbestätigungen als PDF (mit Textebene). Auftragsbestätigungen zählen als **geplante** Einfuhr, nicht als bereits eingeführt."))
    pdfs = st.file_uploader(_("PDF-Dokumente"), type="pdf", accept_multiple_files=True)
    if pdfs:
        lines = use_documents([(f, f.name) for f in pdfs])
with tab_csv:
    st.write(_("Spalten: ") + ", ".join(f"`{c}`" for c in COLUMNS))
    upload = st.file_uploader(_("Einkaufsliste (CSV)"), type="csv")
    if upload:
        lines = pd.read_csv(upload, dtype={"cn": str})
with tab_demo:
    if DEMO_CSV.exists():
        d1, d2 = st.columns(2)
        if d1.button(_("Demo-Rechnungen laden (CSV)")):
            st.session_state["demo"] = "csv"
        if DEMO_PDFS and d2.button(_("Demo-PDFs einlesen ({n} Dokumente)", n=len(DEMO_PDFS))):
            st.session_state["demo"] = "pdf"
        if st.session_state.get("demo") == "csv":
            lines = pd.read_csv(DEMO_CSV, dtype={"cn": str})
        elif st.session_state.get("demo") == "pdf":
            lines = use_documents([(p, p.name) for p in DEMO_PDFS])
    else:
        st.info(_("Demo-Daten fehlen (demo/purchases_2026.csv)."))

if lines is None:
    st.stop()

missing_cols = [c for c in COLUMNS if c not in lines.columns]
if missing_cols:
    st.error(_("Fehlende Spalten: ") + ", ".join(missing_cols))
    st.stop()

st.write(_("Bitte KN-Codes und Gewichte prüfen — Sie können jede Zelle korrigieren."))
lines = st.data_editor(lines[COLUMNS + [c for c in lines.columns if c not in COLUMNS]], num_rows="dynamic", width="stretch")

# 2. Anhang I prüfen
st.header(_("2. Welche Waren sind CBAM-Waren?"))
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
    column_config={"cbam": st.column_config.CheckboxColumn(_("CBAM-Ware")),
                   "annex_description": _("Anhang I"),
                   "source": st.column_config.LinkColumn(_("Quelle"))},
)
unclear = result[result["cbam"].isna()]
if len(unclear):
    st.warning(_("{n} Zeile(n) ohne gültigen KN-Code — bitte oben ergänzen.", n=len(unclear)))

# 3. Schwelle
st.header(_("3. 50-Tonnen-Schwelle"))
year = st.selectbox(_("Kalenderjahr"), sorted({str(d)[:4] for d in result["date"]}, reverse=True))
status = threshold_status([r for r in records if r["cbam"]], int(year), today=date.today() if int(year) == date.today().year else None)
st.progress(min(status["share"], 1.0), text=_("{t:.1f} t von {max:.0f} t CBAM-Waren im Jahr {year}", t=status["total_t"], max=THRESHOLD_T, year=year))
if status["status"] == "exempt":
    st.success(_("Unter der Schwelle: von CBAM-Pflichten befreit. Die Befreiung ist in der Zollanmeldung anzugeben."))
elif status["status"] == "near":
    st.warning(_("Über 80 % der Schwelle — weitere Importe können die Pflicht auslösen."))
else:
    st.error(_("Schwelle überschritten (oder Strom/Wasserstoff importiert): Sie brauchen den Status als zugelassener CBAM-Anmelder."))
if status["forecast_crossing"]:
    st.write(_("Prognose beim bisherigen Tempo: Schwelle erreicht am **{d}**.", d=status["forecast_crossing"]))


def _is_cbam(cn):
    try:
        return check_annex_i(cn)["cbam"]
    except (ValueError, TypeError):
        return False


planned_cbam = [l for l in planned_lines if str(l.get("date", "")).startswith(year) and _is_cbam(l.get("cn"))]
if planned_cbam:
    planned_t = sum(l["net_mass_kg"] for l in planned_cbam) / 1000
    after_t = status["total_t"] + planned_t
    msg = _("Geplante Lieferungen laut Auftragsbestätigung: **{p:.1f} t** CBAM-Waren → danach **{a:.1f} t** von {max:.0f} t.",
            p=planned_t, a=after_t, max=THRESHOLD_T)
    if after_t > THRESHOLD_T and status["status"] != "over":
        st.error(msg + _(" Diese Lieferung würde die Schwelle überschreiten — Zulassung vorher beantragen (Option B) oder Menge reduzieren (Option A)."))
    else:
        st.info(msg)
st.caption(_("Quelle: [Verordnung (EU) 2025/2083 (CBAM-Omnibus)]({o}), Anhang I der [Verordnung (EU) 2023/956]({r}).", o=OMNIBUS_URL, r=CBAM_REG_URL))

# 4. Kosten und Risiko
st.header(_("4. Kosten und Risiko"))
cost = None
if default_values is None or prices is None:
    st.info(_("Standardwerte oder Zertifikatspreise fehlen noch (data/default_values.csv, data/cbam_prices.json)."))
else:
    year_lines = [r for r in records if r["cbam"] and str(r["date"]).startswith(year)]
    cost = estimate_cost(year_lines, prices, default_values)
    c1, c2, c3 = st.columns(3)
    c1.metric(_("Graue Emissionen"), f"{cost['total_emissions_t']:.1f} t CO₂e")
    c2.metric(_("Zertifikate (Quartalspreise)"), f"€ {cost['certificate_cost_eur']:,.0f}")
    lo, hi = cost["penalty_range_eur"]
    c3.metric(_("Strafe ohne Zulassung"), f"€ {lo:,.0f} – {hi:,.0f}")
    if cost["lines"]:
        st.dataframe(pd.DataFrame(cost["lines"])[["description", "cn", "origin", "quarter", "formula", "emissions_t", "certificate_eur", "factor_source"]],
                     width="stretch", column_config={"factor_source": _("Quelle")})
    if cost["missing_default_value"]:
        st.warning(_("{n} Zeile(n) ohne Standardwert für Herkunftsland/KN — nicht geschätzt.", n=len(cost["missing_default_value"])))
    st.caption(_("Standardwerte inkl. Aufschlag des Jahres (DVO (EU) 2025/2621). Zertifikatspreis des Einfuhrquartals: [Europäische Kommission]({u}). Strafe: 3–5 × € 100 je fehlendem Zertifikat, auf alle Emissionen des Jahres (Art. 26 Abs. 2a, vor Indexierung).", u=PRICE_URL))

# 5. Entscheidung
st.header(_("5. Ihre Optionen"))
a, b, c = st.columns(3)
a.subheader(_("A · Unter 50 t bleiben"))
a.write(_("Noch **{t:.1f} t** bis zur Schwelle. Käufe planen und dokumentieren.", t=max(THRESHOLD_T - status["total_t"], 0)))
b.subheader(_("B · Zulassung beantragen"))
b.write(_("Antrag als zugelassener CBAM-Anmelder beim AnEH (cbam@bmf.gv.at), bevor die Schwelle überschritten wird."))
CHECKLIST = ROOT / "data" / "declarant_checklist.md"
if CHECKLIST.exists():
    with b.expander(_("Checkliste Antrag")):
        st.markdown(CHECKLIST.read_text(encoding="utf-8"))
c.subheader(_("C · Lieferant fragen"))
c.write(_("Echte Emissionsdaten beim Lieferanten anfordern — oft niedriger als die Standardwerte."))

# 6. Dokumente
st.header(_("6. Dokumente"))
importer = st.text_input(_("Ihr Unternehmen"), "Metallbau Gruber GmbH")
suppliers = sorted({r["supplier"] for r in records if r["cbam"] and isinstance(r.get("supplier"), str)})
if suppliers:
    s1, s2 = st.columns([3, 1])
    supplier = s1.selectbox(_("Brief an Lieferanten (Anfrage echter Emissionsdaten)"), suppliers)
    lang = s2.radio(_("Sprache des Briefs"), ["de", "en"], horizontal=True)
    letter = supplier_letter(supplier, records, importer, lang)
    st.text_area(_("Brief"), letter, height=320)
    st.download_button(_("Brief herunterladen (.txt)"), letter, file_name=f"CBAM_Anfrage_{supplier[:20]}.txt")
pdf = report_pdf(importer, year, status, records, cost)
st.download_button(_("Bericht herunterladen (PDF)"), pdf, file_name=f"CBAM_Bericht_{year}.pdf", mime="application/pdf")

# 7. Fragen an den Lotsen (KI)
st.header(_("7. Fragen an den Lotsen"))
try:
    api_key = st.secrets.get("GEMINI_API_KEY")
except Exception:  # no secrets.toml locally
    api_key = None
api_key = api_key or os.environ.get("GEMINI_API_KEY")
if not api_key:
    st.caption(_("KI-Assistent aus (kein GEMINI_API_KEY) — Sie erhalten eine feste Zusammenfassung."))
question = st.chat_input(_("z. B. Was passiert, wenn ich im Herbst noch 20 t Profile kaufe?"))
if question:
    ctx = {"lines": records, "year": int(year), "values": default_values,
           "prices": prices}
    with st.spinner(_("Der Lotse rechnet …")):
        text, calls = answer(question, ctx, api_key=api_key, language={"de": "Deutsch", "en": "Englisch", "ru": "Russisch"}[L])
    st.chat_message("user").write(question)
    st.chat_message("assistant").write(text)
    for c in calls:
        with st.expander(f"{_('Werkzeug')}: {c['name']}({c['args'] or ''})"):
            st.json(c["result"])
