"""CBAM-Lotse — Streamlit UI. Run: streamlit run app.py"""

import os
from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st

from cbam.agent import answer
from cbam.annex import check_annex_i, load_annex
from cbam.cost import estimate_cost, load_default_values, load_prices
from cbam.documents import report_pdf, supplier_letter
from cbam.extract import read_documents
from cbam.threshold import THRESHOLD_T, threshold_status
from i18n import LANGS, tr

ROOT = Path(__file__).resolve().parent
DEMO_CSV = ROOT / "demo" / "purchases_2026.csv"
DEMO_PDFS = sorted((ROOT / "demo").glob("*.pdf"))
CHECKLIST = ROOT / "data" / "declarant_checklist.md"
COLUMNS = ["description", "cn", "net_mass_kg", "origin", "date", "supplier"]

OMNIBUS_URL = "https://eur-lex.europa.eu/eli/reg/2025/2083/oj"
CBAM_REG_URL = "https://eur-lex.europa.eu/eli/reg/2023/956/oj"
PRICE_URL = "https://taxation-customs.ec.europa.eu/carbon-border-adjustment-mechanism/price-cbam-certificates_en"
STATUS_COLOR = {"exempt": "#2E7D4F", "near": "#B7791F", "over": "#B42318"}

st.set_page_config(page_title="CBAM-Lotse", page_icon="🏭", layout="centered")
st.markdown("""
<style>
.block-container { padding-top: 2rem; max-width: 880px; }
.hero { background: #FFFFFF; border: 1px solid #E4DED2; border-radius: 14px; padding: 22px 26px; margin: 8px 0 18px; }
.hero .kicker { font-size: .8rem; letter-spacing: .08em; text-transform: uppercase; color: #6B6457; }
.hero .title { font-size: 1.7rem; font-weight: 700; line-height: 1.25; margin: 4px 0 6px; }
.hero .sub { font-size: 1.05rem; color: #3D3A33; }
.step { font-size: .8rem; letter-spacing: .08em; text-transform: uppercase; color: #A8451A; font-weight: 700; margin-top: 1.2rem; }
.option { background: #FFFFFF; border: 1px solid #E4DED2; border-radius: 12px; padding: 14px 16px; height: 100%; }
.option b { display: block; margin-bottom: 4px; }
</style>""", unsafe_allow_html=True)


def try_load(loader):
    try:
        return loader()
    except FileNotFoundError:
        return None


annex = try_load(load_annex)
default_values = try_load(load_default_values)
prices = try_load(load_prices)

# Sidebar: settings that apply to the whole page
with st.sidebar:
    L = LANGS[st.radio("Sprache / Language / Язык", list(LANGS), key="ui_lang")]


def _(text, **kw):
    return tr(text, L, **kw)


with st.sidebar:
    importer = st.text_input(_("Ihr Unternehmen"), "Metallbau Gruber GmbH")
    st.divider()
    st.markdown(_("**So funktioniert es**\n\n1. Rechnungen hochladen oder Demo laden\n2. Ergebnis lesen: Betrifft mich CBAM?\n3. Nächsten Schritt wählen und Dokumente herunterladen"))
    st.caption(_("Ersteinschätzung, keine Rechtsberatung. Zuständig in Österreich: AnEH, cbam@bmf.gv.at."))

st.title("🏭 CBAM-Lotse")
st.markdown(_("Betrifft mich CBAM? Prüfung Ihrer Stahl- und Aluminiumimporte gegen Anhang I und die 50-Tonnen-Schwelle — jede Zahl mit Quelle."))
with st.expander(_("Was ist CBAM? (30 Sekunden)")):
    st.markdown(_("Seit 1. Jänner 2026 kostet die Einfuhr von Stahl, Aluminium, Zement, Dünger, Strom und Wasserstoff in die EU einen CO₂-Preis. Wer mehr als **50 Tonnen** solcher Waren pro Jahr einführt, braucht vorher eine Zulassung. Ohne Zulassung drohen **€ 300–500 Strafe je Tonne CO₂**. Ob eine Ware zählt, entscheidet ihr Zolltarif-Code (KN-Code)."))

if annex is None:
    st.error(_("data/annex_i.json fehlt — ohne Anhang I ist keine Prüfung möglich."))
    st.stop()

# Step 1: input
st.markdown(f"<div class='step'>{_('Schritt 1')}</div>", unsafe_allow_html=True)
st.subheader(_("Ihre Einkäufe"))
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


tab_demo, tab_pdf, tab_csv = st.tabs(["▶ " + _("Demo ausprobieren"), _("Rechnungen (PDF) hochladen"), _("CSV hochladen")])
with tab_demo:
    st.write(_("Metallbau Gruber GmbH (Beispiel): Träger und Schrauben aus der Türkei, Alu-Profile aus China, Ventile."))
    if DEMO_PDFS and st.button(_("Demo-PDFs einlesen ({n} Dokumente)", n=len(DEMO_PDFS)), type="primary"):
        st.session_state["demo"] = "pdf"
    if st.session_state.get("demo") == "pdf":
        lines = use_documents([(p, p.name) for p in DEMO_PDFS])
    elif st.session_state.get("demo") == "csv" and DEMO_CSV.exists():
        lines = pd.read_csv(DEMO_CSV, dtype={"cn": str})
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
    if DEMO_CSV.exists() and st.button(_("Demo-Rechnungen laden (CSV)")):
        st.session_state["demo"] = "csv"
        st.rerun()

if lines is None:
    st.info(_("Laden Sie die Demo oder Ihre Rechnungen — das Ergebnis erscheint dann hier."))
    st.stop()

missing_cols = [c for c in COLUMNS if c not in lines.columns]
if missing_cols:
    st.error(_("Fehlende Spalten: ") + ", ".join(missing_cols))
    st.stop()

with st.expander(_("Erkannte Positionen prüfen und korrigieren ({n})", n=len(lines))):
    st.caption(_("Bitte KN-Codes und Gewichte prüfen — Sie können jede Zelle korrigieren."))
    lines = st.data_editor(lines[COLUMNS + [c for c in lines.columns if c not in COLUMNS]], num_rows="dynamic",
                           width="stretch", column_config={
                               "description": _("Ware"), "cn": _("KN-Code"), "net_mass_kg": _("Nettomasse (kg)"),
                               "origin": _("Land"), "date": _("Datum"), "supplier": _("Lieferant")})

records = []
for row in lines.to_dict("records"):
    try:
        verdict = check_annex_i(row["cn"])
    except (ValueError, TypeError):
        verdict = {"cbam": None, "sector": None, "annex_entry": None, "description": None, "source": None}
    records.append({**row, **{k: verdict[k] for k in ("cbam", "sector", "annex_entry", "source")},
                    "annex_description": verdict["description"]})
result = pd.DataFrame(records)

years = sorted({str(d)[:4] for d in result["date"]}, reverse=True)
year = years[0] if len(years) == 1 else st.selectbox(_("Kalenderjahr"), years)
status = threshold_status([r for r in records if r["cbam"]], int(year),
                          today=date.today() if int(year) == date.today().year else None)


def _is_cbam(cn):
    try:
        return check_annex_i(cn)["cbam"]
    except (ValueError, TypeError):
        return False


planned_cbam = [l for l in planned_lines if str(l.get("date", "")).startswith(year) and _is_cbam(l.get("cn"))]
planned_t = sum(l["net_mass_kg"] for l in planned_cbam) / 1000
cost = None
if default_values is not None and prices is not None:
    cost = estimate_cost([r for r in records if r["cbam"] and str(r["date"]).startswith(year)], prices, default_values)

# Step 2: the answer, in one sentence
st.markdown(f"<div class='step'>{_('Schritt 2')}</div>", unsafe_allow_html=True)
st.subheader(_("Ihr Ergebnis"))
t = status["total_t"]
headline = {
    "exempt": _("Sie sind befreit: {t:.1f} t von 50 t", t=t),
    "near": _("Achtung: {t:.1f} t von 50 t — knapp unter der Schwelle", t=t),
    "over": _("Schwelle überschritten: {t:.1f} t von 50 t", t=t),
}[status["status"]]
sub = {
    "exempt": _("Sie müssen derzeit nichts zahlen. Geben Sie die Befreiung in der Zollanmeldung an und behalten Sie die Menge im Blick."),
    "near": _("Noch {left:.1f} t, dann brauchen Sie eine Zulassung als CBAM-Anmelder — sonst drohen hohe Strafen.", left=max(THRESHOLD_T - t, 0)),
    "over": _("Sie brauchen den Status als zugelassener CBAM-Anmelder. Ohne Zulassung drohen hohe Strafen."),
}[status["status"]]
if planned_t and t + planned_t > THRESHOLD_T >= t:
    sub += " " + _("Ihre geplanten Lieferungen ({p:.1f} t) würden die Schwelle überschreiten.", p=planned_t)
color = STATUS_COLOR[status["status"]]
st.markdown(f"<div class='hero' style='border-left:8px solid {color}'><div class='kicker'>{importer} · {year}</div>"
            f"<div class='title' style='color:{color}'>{headline}</div><div class='sub'>{sub}</div></div>",
            unsafe_allow_html=True)
st.progress(min(t / THRESHOLD_T, 1.0), text=_("{t:.1f} t von {max:.0f} t CBAM-Waren im Jahr {year}", t=t, max=THRESHOLD_T, year=year))
if status["forecast_crossing"]:
    st.caption(_("Prognose beim bisherigen Tempo: Schwelle erreicht am **{d}**.", d=status["forecast_crossing"]))
if cost:
    lo, hi = cost["penalty_range_eur"]
    m1, m2, m3 = st.columns(3)
    m1.metric(_("Graue Emissionen"), f"{cost['total_emissions_t']:.0f} t CO₂e")
    m2.metric(_("Zertifikate (Quartalspreise)"), f"€ {cost['certificate_cost_eur']:,.0f}")
    m3.metric(_("Strafe ohne Zulassung"), f"€ {lo / 1000:,.0f}–{hi / 1000:,.0f} k")

# Step 3: details and actions
st.markdown(f"<div class='step'>{_('Schritt 3')}</div>", unsafe_allow_html=True)
st.subheader(_("Was jetzt?"))
t_act, t_goods, t_cost, t_ask = st.tabs([_("✅ Nächste Schritte"), _("📦 Waren"), _("💶 Kosten"), _("💬 Fragen")])

with t_act:
    a, b, c = st.columns(3)
    a.markdown(f"<div class='option'><b>{_('A · Unter 50 t bleiben')}</b>"
               f"{_('Noch **{t:.1f} t** bis zur Schwelle. Käufe planen und dokumentieren.', t=max(THRESHOLD_T - t, 0)).replace('**', '')}</div>",
               unsafe_allow_html=True)
    b.markdown(f"<div class='option'><b>{_('B · Zulassung beantragen')}</b>"
               f"{_('Antrag als zugelassener CBAM-Anmelder beim AnEH (cbam@bmf.gv.at), bevor die Schwelle überschritten wird.')}</div>",
               unsafe_allow_html=True)
    c.markdown(f"<div class='option'><b>{_('C · Lieferant fragen')}</b>"
               f"{_('Echte Emissionsdaten beim Lieferanten anfordern — oft niedriger als die Standardwerte.')}</div>",
               unsafe_allow_html=True)
    if CHECKLIST.exists():
        with st.expander(_("Checkliste Antrag")):
            st.markdown(CHECKLIST.read_text(encoding="utf-8"))

    st.markdown("#### " + _("Dokumente"))
    pdf = report_pdf(importer, year, status, records, cost)
    st.download_button("📄 " + _("Bericht herunterladen (PDF)"), pdf, file_name=f"CBAM_Bericht_{year}.pdf",
                       mime="application/pdf", type="primary")
    suppliers = sorted({r["supplier"] for r in records if r["cbam"] and isinstance(r.get("supplier"), str)})
    if suppliers:
        s1, s2 = st.columns([3, 1])
        supplier = s1.selectbox(_("Brief an Lieferanten (Anfrage echter Emissionsdaten)"), suppliers)
        lang = s2.radio(_("Sprache des Briefs"), ["de", "en"], horizontal=True)
        letter = supplier_letter(supplier, records, importer, lang)
        with st.expander(_("Brief")):
            st.text_area(_("Brief"), letter, height=320, label_visibility="collapsed")
        st.download_button("✉ " + _("Brief herunterladen (.txt)"), letter, file_name=f"CBAM_Anfrage_{supplier[:20]}.txt")

with t_goods:
    yes = result[result["cbam"] == True]  # noqa: E712 (cbam may be None)
    no = result[result["cbam"] == False]  # noqa: E712
    unclear = result[result["cbam"].isna()]
    st.markdown(_("**{y}** CBAM-Ware(n) · **{n}** nicht betroffen · **{u}** unklar", y=len(yes), n=len(no), u=len(unclear)))
    if len(unclear):
        st.warning(_("{n} Zeile(n) ohne gültigen KN-Code — bitte oben ergänzen.", n=len(unclear)))
    view = result[["description", "cn", "net_mass_kg", "origin", "cbam", "annex_description", "source"]].copy()
    view["net_mass_kg"] = view["net_mass_kg"] / 1000
    st.dataframe(view, width="stretch", hide_index=True, column_config={
        "description": _("Ware"), "cn": _("KN-Code"),
        "net_mass_kg": st.column_config.NumberColumn(_("Menge (t)"), format="%.1f"),
        "origin": _("Land"), "cbam": st.column_config.CheckboxColumn(_("CBAM-Ware")),
        "annex_description": _("Anhang I"), "source": st.column_config.LinkColumn(_("Quelle"), display_text="EUR-Lex")})
    st.caption(_("Quelle: [Verordnung (EU) 2025/2083 (CBAM-Omnibus)]({o}), Anhang I der [Verordnung (EU) 2023/956]({r}).",
                 o=OMNIBUS_URL, r=CBAM_REG_URL))

with t_cost:
    if cost is None:
        st.info(_("Standardwerte oder Zertifikatspreise fehlen noch (data/default_values.csv, data/cbam_prices.json)."))
    else:
        st.markdown(_("So rechnen wir: **Menge × Standardwert der EU (t CO₂ je t Ware) × Zertifikatspreis des Quartals**."))
        if cost["lines"]:
            st.dataframe(pd.DataFrame(cost["lines"])[["description", "origin", "formula", "emissions_t", "certificate_eur"]],
                         width="stretch", hide_index=True, column_config={
                             "description": _("Ware"), "origin": _("Land"), "formula": _("Rechnung"),
                             "emissions_t": st.column_config.NumberColumn("t CO₂e", format="%.1f"),
                             "certificate_eur": st.column_config.NumberColumn("€", format="%.0f")})
        if cost["missing_default_value"]:
            st.warning(_("{n} Zeile(n) ohne Standardwert für Herkunftsland/KN — nicht geschätzt.", n=len(cost["missing_default_value"])))
        st.caption(_("Standardwerte inkl. Aufschlag des Jahres (DVO (EU) 2025/2621). Zertifikatspreis des Einfuhrquartals: [Europäische Kommission]({u}). Strafe: 3–5 × € 100 je fehlendem Zertifikat, auf alle Emissionen des Jahres (Art. 26 Abs. 2a, vor Indexierung).", u=PRICE_URL))

with t_ask:
    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
    except Exception:  # no secrets.toml locally
        api_key = None
    api_key = api_key or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        st.caption(_("KI-Assistent aus (kein GEMINI_API_KEY) — Sie erhalten eine feste Zusammenfassung."))
    with st.form("ask", clear_on_submit=True):
        question = st.text_input(_("Ihre Frage"), placeholder=_("z. B. Was passiert, wenn ich im Herbst noch 20 t Profile kaufe?"))
        sent = st.form_submit_button(_("Fragen"))
    if sent and question:
        ctx = {"lines": records, "year": int(year), "values": default_values, "prices": prices}
        with st.spinner(_("Der Lotse rechnet …")):
            text, calls = answer(question, ctx, api_key=api_key,
                                 language={"de": "Deutsch", "en": "Englisch", "ru": "Russisch"}[L])
        st.chat_message("user").write(question)
        st.chat_message("assistant").write(text)
        for call in calls:
            with st.expander(f"{_('Werkzeug')}: {call['name']}({call['args'] or ''})"):
                st.json(call["result"])
