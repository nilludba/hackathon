"""CBAM Helper — Streamlit UI. Run: streamlit run app.py"""

import html
import io
import os
from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st

import importlib

import cbam.agent
import cbam.cost
import cbam.extract

# Streamlit Cloud keeps imported modules (and their lru caches) across a git pull;
# reload them if they predate this app.py
_stale_cost = not hasattr(cbam.cost, "OTHER")
if _stale_cost:
    importlib.reload(cbam.cost)
if _stale_cost or not hasattr(cbam.extract, "parse_mass") or not hasattr(cbam.agent, "extract_document"):
    importlib.reload(cbam.extract)
    importlib.reload(cbam.agent)
# data/default_values.csv may have changed without a code change: reload it when its size differs
_dv = cbam.cost.DATA_DIR / "default_values.csv"
if cbam.cost.load_default_values.cache_info().currsize and len(cbam.cost.load_default_values()) != sum(1 for _ in open(_dv, encoding="utf-8")) - 1:
    cbam.cost.load_default_values.cache_clear()
from cbam.agent import answer, extract_document
from cbam.annex import check_annex_i, load_annex
from cbam.cost import estimate_cost, load_default_values, load_prices
from cbam.documents import report_pdf, supplier_letter
from cbam.extract import read_documents
from cbam.suggest import TARIC_URL, suggest_cn
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
STATUS_COLOR = {"exempt": "#248A3D", "near": "#BF4800", "over": "#D70015"}

st.set_page_config(page_title="CBAM Helper", page_icon="◼", layout="centered", initial_sidebar_state="collapsed")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Color+Emoji&display=swap');
html, body, .stApp, button, input, textarea, select, p, li, label {
  font-family: 'Inter', 'Noto Color Emoji', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif;
  -webkit-font-smoothing: antialiased; }
header[data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"], footer, #MainMenu,
section[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"] { display: none !important; }
.block-container { max-width: 980px; padding-top: 1.2rem; padding-bottom: 5rem; }
h1, h2, h3, h4 { letter-spacing: -0.022em; color: #1D1D1F; }
.nav { font-weight: 600; font-size: 1.05rem; letter-spacing: -0.01em; color: #1D1D1F; }
.hero-t { text-align: center; font-size: clamp(2.6rem, 6.5vw, 4.4rem); font-weight: 700; letter-spacing: -0.035em;
  line-height: 1.04; margin: 3.2rem 0 1rem; color: #1D1D1F; }
.hero-s { text-align: center; font-size: clamp(1.1rem, 2.3vw, 1.4rem); color: #6E6E73; line-height: 1.42;
  max-width: 640px; margin: 0 auto 2.2rem; }
.feat { text-align: center; padding: 1.4rem .4rem; }
.feat .k { font-size: 2.3rem; font-weight: 700; letter-spacing: -0.035em; color: #1D1D1F; }
.feat .d { color: #6E6E73; font-size: .98rem; line-height: 1.42; margin-top: .2rem; }
.section { font-size: clamp(1.9rem, 4.2vw, 2.7rem); font-weight: 700; letter-spacing: -0.032em; line-height: 1.1;
  margin: 4.2rem 0 1.2rem; color: #1D1D1F; }
.section small { display: block; font-size: .95rem; font-weight: 600; color: #86868B; letter-spacing: 0; margin-bottom: .45rem; }
.stButton > button, .stDownloadButton > button, .stFormSubmitButton > button {
  border-radius: 4px; min-height: 40px; padding: .5rem 1.6rem; font-size: .9rem; font-weight: 500; letter-spacing: .01em;
  border: none; background: rgba(23,26,32,.06); color: #171A20; transition: background .25s ease; }
.stButton > button:hover, .stDownloadButton > button:hover, .stFormSubmitButton > button:hover { background: rgba(23,26,32,.12); color: #171A20; }
[data-testid="stButtonGroup"] button { border-radius: 4px; }
button[data-testid="stBaseButton-primary"] { background: #3E6AE1; border: none; color: #FFFFFF; }
button[data-testid="stBaseButton-primary"]:hover { background: #3457B1; color: #FFFFFF; }
.hero-card { background: var(--glass); border: 1px solid rgba(255,255,255,.7); box-shadow: var(--lift); backdrop-filter: blur(18px) saturate(160%); border-radius: 24px; padding: 2.3rem 2.3rem 2rem; margin: .4rem 0 1.1rem; }
.hero-card .kicker { font-size: .88rem; color: #6E6E73; font-weight: 500; }
.hero-card .title { font-size: clamp(1.7rem, 3.8vw, 2.6rem); font-weight: 700; letter-spacing: -0.032em; line-height: 1.1; margin: .45rem 0 .7rem; }
.hero-card .sub { font-size: 1.12rem; color: #424245; line-height: 1.45; }
.option { background: var(--glass); border: 1px solid rgba(255,255,255,.7); box-shadow: var(--lift); backdrop-filter: blur(18px) saturate(160%); border-radius: 20px; padding: 1.4rem; min-height: 158px; color: #424245; line-height: 1.45; }
.option b { display: block; font-size: 1.06rem; margin-bottom: .4rem; color: #1D1D1F; }
div[data-testid="stColumn"] > div:has(.option) { height: 100%; }
div[data-testid="stMetric"] { background: var(--glass); border: 1px solid rgba(255,255,255,.7); box-shadow: var(--lift); backdrop-filter: blur(18px) saturate(160%); border-radius: 20px; padding: 1.1rem 1.3rem; }
div[data-testid="stMetricValue"] { font-size: 1.9rem; font-weight: 600; letter-spacing: -0.025em; }
div[data-testid="stMetricLabel"] p { color: #6E6E73; }
.tbar { position: relative; height: 14px; border-radius: 7px; background: #E8E8ED; margin: 26px 0 10px; }
.tbar .imp { position: absolute; left: 0; top: 0; height: 14px; border-radius: 7px; }
.tbar .plan { position: absolute; top: 0; height: 14px; border-radius: 0 7px 7px 0;
  background: repeating-linear-gradient(45deg, #D70015 0 5px, #F9D0D5 5px 10px); }
.tbar .lim { position: absolute; top: -7px; width: 2px; height: 28px; background: #1D1D1F; border-radius: 1px; }
.tbar .lim span { position: absolute; top: -21px; left: -12px; font-size: .78rem; font-weight: 600; color: #1D1D1F; white-space: nowrap; }
.tlegend { display: flex; gap: 22px; flex-wrap: wrap; font-size: .86rem; color: #6E6E73; margin-bottom: 18px; }
.tlegend i { display: inline-block; width: 10px; height: 10px; border-radius: 5px; margin-right: 7px; }
.tlegend i.hatch { background: repeating-linear-gradient(45deg, #D70015 0 3px, #F9D0D5 3px 6px); }
[data-baseweb="tab-list"] { gap: 1.8rem; }
[data-baseweb="tab"] p { font-weight: 500; font-size: 1rem; }
[data-testid="stExpander"] details { border: 1px solid rgba(255,255,255,.7); background: var(--glass); backdrop-filter: blur(18px); border-radius: 14px; }
[data-testid="stExpander"] summary, [data-testid="stExpander"] summary:hover, [data-testid="stExpander"] summary:focus,
[data-testid="stExpander"] summary:focus-visible, [data-testid="stExpander"] details[open] > summary {
  background: transparent !important; color: #1D1D1F !important; }
[data-testid="stExpander"] summary p, [data-testid="stExpander"] summary:hover p,
[data-testid="stExpander"] details[open] > summary p { color: #1D1D1F !important; }
[data-testid="stExpander"] summary svg { color: #1D1D1F !important; fill: #1D1D1F !important; }
[data-testid="stFileUploaderDropzone"] { background: var(--glass); backdrop-filter: blur(18px); border: 1px dashed #C7C7CC; border-radius: 18px; }
.foot { color: #86868B; font-size: .8rem; text-align: center; margin-top: 4.5rem; line-height: 1.6; }
.cta-trust { text-align: center; color: #424245; font-size: .88rem; margin-top: .7rem; }
.next-step { background: #FFFFFF; border: 1px solid rgba(29,29,31,.1); border-left: 6px solid var(--c); border-radius: 14px;
  padding: 1.1rem 1.3rem; margin: 1.4rem 0 .6rem; }
.next-step .lbl { font-size: .8rem; font-weight: 600; letter-spacing: .04em; text-transform: uppercase; color: #6E6E73; }
.next-step b { display: block; font-size: 1.15rem; margin: .25rem 0 .3rem; color: #1D1D1F; }
.next-step span { color: #424245; line-height: 1.45; }
/* Motion and detail */
:root { --glass: rgba(255,255,255,.72); --lift: 0 10px 30px rgba(17,17,26,.06); }
.stApp { background: #F7F8FB; }
@keyframes drift { 0% { background-position: 0% 0%; } 100% { background-position: 100% 100%; } }
.chip { display: inline-block; padding: .3rem .8rem; border-radius: 980px; font-size: .85rem; font-weight: 600; margin: .55rem 0 .2rem; }
.nums { display: flex; align-items: baseline; flex-wrap: wrap; gap: .5rem .8rem; margin: .5rem 0 .8rem; }
.nums .big { font-size: clamp(2.4rem, 6vw, 3.6rem); font-weight: 700; letter-spacing: -0.04em; line-height: 1; color: #1D1D1F; }
.nums .of { font-size: 1.3rem; color: #86868B; font-weight: 500; }
.nums .arrow { font-size: 1.8rem; color: #86868B; }
.nums .over { align-self: center; padding: .35rem .8rem; border-radius: 980px; background: #D70015; color: #FFFFFF; font-weight: 600; font-size: .95rem;
  animation: pop .5s .9s both; }
@keyframes pop { from { opacity: 0; transform: scale(.8); } to { opacity: 1; transform: none; } }
.tbar .zone { position: absolute; top: 0; right: 0; height: 14px; border-radius: 0 7px 7px 0;
  background: repeating-linear-gradient(-45deg, rgba(215,0,21,.10) 0 6px, rgba(215,0,21,.04) 6px 12px); }
@keyframes rise { from { opacity: 0; transform: translateY(18px); } to { opacity: 1; transform: none; } }
@keyframes grow { from { transform: scaleX(0); } to { transform: scaleX(1); } }
@keyframes shine { to { background-position: 200% center; } }
@keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(0,113,227,.45); } 70% { box-shadow: 0 0 0 9px rgba(0,113,227,0); } 100% { box-shadow: 0 0 0 0 rgba(0,113,227,0); } }
.pill { display: table; margin: 2.4rem auto 0; padding: .38rem .95rem; border-radius: 980px; background: rgba(245,245,247,.85);
  border: 1px solid #E8E8ED; font-size: .85rem; font-weight: 500; color: #1D1D1F; animation: rise .7s both; }
.pill .dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #0071E3; margin-right: .55rem;
  vertical-align: 1px; animation: pulse 2.2s infinite; }
.hero-t { margin-top: 1.1rem; animation: rise .8s .06s both; }
.hero-s { animation: rise .8s .16s both; }
.feat { animation: rise .8s both; }
.section, .hero-card { animation: rise .7s both; }
.hero-card { position: relative; overflow: hidden; box-shadow: 0 1px 0 rgba(0,0,0,.02); }
.hero-card::before { content: ""; position: absolute; left: 0; top: 0; bottom: 0; width: 6px; background: var(--c, #0071E3); }
div[data-testid="stMetric"], .option { transition: transform .25s ease, box-shadow .25s ease; animation: rise .7s .12s both; }
div[data-testid="stMetric"]:hover, .option:hover { transform: translateY(-3px); box-shadow: 0 14px 34px rgba(0,0,0,.08); }
.tbar .imp, .tbar .plan { transform-origin: left center; animation: grow 1.1s cubic-bezier(.2,.8,.2,1) both; }
.tbar .plan { animation-delay: .85s; }
[data-testid="InputInstructions"] { display: none; }
@media (max-width: 640px) {  /* phone: logo + language on one line, links on the next; Streamlit would stack all five */
  .st-key-topnav [data-testid="stHorizontalBlock"] { flex-direction: row !important; flex-wrap: wrap !important; gap: .1rem 1.1rem !important; }
  .st-key-topnav [data-testid="stColumn"] { width: auto !important; flex: 0 0 auto !important; min-width: 0 !important; order: 2; }
  .st-key-topnav [data-testid="stColumn"]:first-child { flex: 1 0 46% !important; order: 0; }
  .st-key-topnav [data-testid="stColumn"]:last-child { order: 1; }
  .st-key-topnav [data-testid="stButtonGroup"] button { padding: .15rem .55rem; min-height: 32px; }
  .st-key-topnav [data-testid="stButtonGroup"] button p, .st-key-topnav button[data-testid="stBaseButton-tertiary"] p { font-size: .9rem; }
  .pill { margin-top: 1rem; }
  .hero-t { margin-top: 1.2rem !important; }
  .section { margin-top: 2.6rem; }
  .hero-card { padding: 1.6rem 1.4rem 1.4rem; }
}
button[data-testid="stBaseButton-tertiary"] { background: transparent !important; min-height: auto; padding: .25rem .1rem;
  color: #171A20 !important; font-weight: 500; }
button[data-testid="stBaseButton-tertiary"]:hover { color: #3E6AE1 !important; }
.st-key-nav_logo button { transition: transform .2s ease; transform-origin: left center; }
.st-key-nav_logo button p { font-size: 1.1rem; font-weight: 700; letter-spacing: -0.01em; }
.st-key-nav_logo button:hover { transform: scale(1.08); color: #171A20 !important; }
@media (prefers-reduced-motion: reduce) { *, *::before { animation: none !important; transition: none !important; } }
</style>""", unsafe_allow_html=True)


def try_load(loader):
    try:
        return loader()
    except FileNotFoundError:
        return None


annex = try_load(load_annex)
default_values = try_load(load_default_values)
prices = try_load(load_prices)

# Top bar: wordmark · Home · Prüfen · Fragen & Antworten · language
# One URL per page (/, /tool, /faq), so the browser's back button returns to the previous page
PAGES = {k: st.Page(lambda: None, title="CBAM Helper", url_path=k, default=k == "home")
         for k in ("home", "tool", "faq")}
_current = st.navigation(list(PAGES.values()), position="hidden")
page = next(k for k, p in PAGES.items() if p is _current or p.url_path == _current.url_path)


def go(key):
    st.switch_page(PAGES[key])


with st.container(key="topnav"):
    nav = st.columns([2.1, .8, .9, 1.9, 1.5], vertical_alignment="center")
if nav[0].button("CBAM Helper", type="tertiary", key="nav_logo"):  # wordmark = home link
    go("home")
nav_r = nav[4]
FLAGS = {"DE": "🇦🇹 DE", "EN": "🇬🇧 EN"}  # Austrian German, British English
L = LANGS[nav_r.segmented_control("Sprache", list(LANGS), default=list(LANGS)[0], key="ui_lang",
                                  format_func=lambda k: FLAGS.get(k, k),
                                  label_visibility="collapsed") or list(LANGS)[0]]


def _loc(s):
    """Number separators for the UI language: 1,234.5 (en) · 1.234,5 (de)."""
    if L == "en":
        return s
    return s.replace(",", "\0").replace(".", ",").replace("\0", ".")


class _Num(float):
    def __format__(self, spec):
        return _loc(format(float(self), spec))


def n(x, spec=",.1f"):
    return _loc(format(x, spec))


def eur(x):
    return "€ " + n(x, ",.0f")


def _(text, **kw):
    kw = {k: _Num(v) if isinstance(v, float) else v for k, v in kw.items()}
    return tr(text, L, **kw)


for col, key, label in ((nav[1], "home", "Home"), (nav[2], "tool", "Prüfen"), (nav[3], "faq", "Fragen & Antworten")):
    if col.button(_(label), type="tertiary", key=f"nav_{key}"):
        go(key)
st.markdown(f"<style>.st-key-nav_{page} button p {{ font-weight: 700; border-bottom: 2px solid #171A20; }}</style>",
            unsafe_allow_html=True)


def faq():
    for q, a in (
        ("Was ist CBAM?", "Seit 1. Jänner 2026 kostet die Einfuhr von Stahl, Aluminium, Zement, Dünger, Strom und Wasserstoff in die EU einen CO₂-Preis. Wer mehr als **50 Tonnen** solcher Waren pro Jahr einführt, braucht vorher eine Zulassung. Ohne Zulassung drohen **€ 300–500 Strafe je Tonne CO₂**. Ob eine Ware zählt, entscheidet ihr Zolltarif-Code (KN-Code)."),
        ("Betrifft mich das?", "Ja, wenn Sie pro Kalenderjahr mehr als 50 t Waren aus Anhang I einführen — z. B. Träger, Rohre, Schrauben aus Stahl oder Profile aus Aluminium. Alle CBAM-Waren des Jahres werden zusammengezählt. Für Strom und Wasserstoff gibt es keine Schwelle."),
        ("Was kostet es?", "Pro Tonne Ware: Standardwert der EU (t CO₂ je t Ware) × Preis eines CBAM-Zertifikats des Einfuhrquartals. Zertifikate für Einfuhren 2026 werden ab 1. Februar 2027 verkauft, die erste Jahreserklärung ist bis 30. September 2027 fällig."),
        ("Was passiert ohne Zulassung?", "Wer über 50 t kommt, ohne zugelassener CBAM-Anmelder zu sein, zahlt das 3- bis 5-Fache der Strafe von € 100 je fehlendem Zertifikat — auf alle Emissionen des Jahres, nicht nur auf die Menge über 50 t."),
        ("Wie beantrage ich die Zulassung?", "In Österreich beim Amt für den nationalen Emissionszertifikatehandel (AnEH), cbam@bmf.gv.at, über das CBAM-Register der EU — bevor Sie die Schwelle überschreiten. Die Checkliste dafür finden Sie unter „Prüfen“ → „Nächste Schritte“."),
        ("Woher kommen die Zahlen?", "Aus Anhang I der Verordnung (EU) 2023/956, dem CBAM-Omnibus (EU) 2025/2083, den Standardwerten der DVO (EU) 2025/2621 und den Zertifikatspreisen der Europäischen Kommission. Die KI liest nur Rechnungen und erklärt — gerechnet wird mit geprüftem Code."),
        ("Werden meine Rechnungen gespeichert?", "Nein, wir legen sie in keiner Datenbank ab; sie werden nur für die Berechnung verarbeitet. Stellen Sie der KI eine Frage, werden Ihre Positionen dafür an Google Gemini gesendet."),
        ("Ist das Rechtsberatung?", "Nein. CBAM Helper ist eine Ersteinschätzung und bereitet Unterlagen vor. Die Entscheidung treffen Sie bzw. die Behörde."),
    ):
        with st.expander(_(q)):
            st.markdown(_(a))


def section(step, title):
    st.markdown(f"<div class='section'><small>{step}</small>{title}</div>", unsafe_allow_html=True)


def footer():
    st.markdown(f"<div class='foot'>{_('Ersteinschätzung, keine Rechtsberatung. Zuständig in Österreich: AnEH, cbam@bmf.gv.at.')}"
                f"<br>{_('Quellen: Verordnung (EU) 2023/956, (EU) 2025/2083, DVO (EU) 2025/2621, Europäische Kommission.')}</div>",
                unsafe_allow_html=True)
    with st.expander(_("Wie prüfen wir uns selbst?")):
        st.markdown(_("Die KI liest nur und erklärt. Anhang I, Schwelle und Kosten rechnet geprüfter Code. Sie können die automatischen Tests hier selbst laufen lassen."))
        if st.button(_("Tests ausführen")):
            import subprocess
            import sys
            run = subprocess.run([sys.executable, "-m", "pytest", "-q", "--no-header", "-p", "no:cacheprovider"],
                                 cwd=ROOT, capture_output=True, text=True, timeout=120)
            summary = (run.stdout.strip().splitlines() or ["?"])[-1]
            (st.success if run.returncode == 0 else st.error)(summary)


DEMO_IMPORTER = "Metallbau Gruber GmbH"
importer = st.session_state.setdefault("importer", DEMO_IMPORTER)


def start_demo():
    st.session_state.update(demo="pdf", importer=DEMO_IMPORTER, cn_fixes={})


def start_own():
    """'Eigene Rechnungen prüfen': empty tool, no example data and no example company."""
    st.session_state.update(demo=None, importer="", cn_fixes={})


def own_files_changed():
    """Own upload replaces the demo for good: removing the file later must not bring the example back."""
    if st.session_state.get("uploads"):
        st.session_state["demo"] = None
        st.session_state["cn_fixes"] = {}
        if st.session_state.get("importer", DEMO_IMPORTER) == DEMO_IMPORTER:
            st.session_state["importer"] = ""

INTRO_CSS = """<style>
.stApp { background: #F7F8FB !important; animation: none !important; }
.nav, .hero-t { color: #1D1D1F; }
.hero-t { margin-top: 4.5rem; font-size: clamp(3rem, 8.5vw, 5.8rem); }
.hero-s, .feat .d, .foot, .demo-note { color: #424245 !important; }
.pill { background: rgba(255,255,255,.85); border-color: rgba(29,29,31,.12); color: #1D1D1F; backdrop-filter: blur(12px); }
[data-testid="stExpander"] details { background: rgba(255,255,255,.8); border-color: rgba(29,29,31,.1); }
[data-testid="stExpander"] summary, [data-testid="stExpander"] p, [data-testid="stExpander"] li { color: #1D1D1F; }
[data-testid="stButtonGroup"] button { background: #FFFFFF; color: #1D1D1F; border-color: rgba(29,29,31,.15); }
[data-testid="stButtonGroup"] button p { color: #1D1D1F; }
button[data-testid="stBaseButton-primary"] { min-height: 44px; }
.stButton > button:not([data-testid="stBaseButton-primary"]) { background: rgba(23,26,32,.06); color: #171A20; }
</style>"""


def hero():
    st.markdown(f"<div class='pill'><span class='dot'></span>{_('CBAM-Pflicht seit 1. Jänner 2026')}</div>"
                f"<div class='hero-t'>{_('Betrifft mich CBAM?')}</div>"
                f"<div class='hero-s'>{_('Laden Sie Ihre Rechnungen. In einer Minute wissen Sie, ob die CO₂-Grenzabgabe der EU Sie trifft, was sie kostet und was jetzt zu tun ist.')}</div>",
                unsafe_allow_html=True)


BAND_CSS = """<style>
.st-key-band_how, .st-key-band_faq { padding: 1rem 0 3.5rem; clip-path: inset(0 -100vmax); }
.st-key-band_how { background: #F2F3F5; box-shadow: 0 0 0 100vmax #F2F3F5; margin-top: 4rem; }
.st-key-band_faq { background: #FFFFFF; box-shadow: 0 0 0 100vmax #FFFFFF; }
.st-key-band_faq .section, .st-key-band_faq .section small { color: #1D1D1F; }
.st-key-band_faq [data-testid="stExpander"] details { background: #F7F8FB; border: 1px solid rgba(29,29,31,.1); }
.st-key-band_faq [data-testid="stExpander"] p, .st-key-band_faq [data-testid="stExpander"] li,
.st-key-band_faq .foot { color: #1D1D1F !important; }
.steps { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; align-items: stretch; }
@media (max-width: 640px) { .steps { grid-template-columns: 1fr; } }
.step-card { background: #FFFFFF; border-radius: 4px; padding: 1.6rem 1.4rem; min-height: 170px; }
.step-card .no { font-size: .85rem; font-weight: 600; color: #3E6AE1; }
.step-card b { display: block; font-size: 1.15rem; margin: .35rem 0 .4rem; color: #171A20; }
.step-card span { color: #5C5E62; line-height: 1.45; }
.block-container { padding-bottom: 0; }
</style>"""

if page == "faq":
    section(_("Hilfe"), _("Fragen & Antworten"))
    faq()
    footer()
    st.stop()

# Home: landing page; the tool opens with "Los geht's" or "Prüfen"
if page == "home":
    st.markdown(INTRO_CSS, unsafe_allow_html=True)
    hero()
    _pad_l, own, demo, _pad_r = st.columns([0.5, 1, 1, 0.5])
    if own.button(_("Eigene Rechnungen prüfen"), type="primary", width="stretch", key="cta_own"):
        start_own()
        go("tool")
    if demo.button(_("Beispiel ansehen – 30 Sekunden"), width="stretch", key="cta_demo"):
        start_demo()
        st.session_state["scroll_to_result"] = True
        go("tool")
    st.markdown(f"<div class='cta-trust'>{_('Kostenlos · ohne Anmeldung · Ihre Rechnungen werden nicht gespeichert')}</div>",
                unsafe_allow_html=True)
    st.markdown("<div style='height:2.5rem'></div>", unsafe_allow_html=True)
    f1, f2, f3 = st.columns(3)
    for i, (col, k, d) in enumerate(((f1, "50 t", _("pro Jahr. Darunter sind Sie befreit, darüber brauchen Sie eine Zulassung.")),
                                     (f2, "€ 300–500", _("Strafe je Tonne CO₂ ohne Zulassung — auf alle Emissionen des Jahres.")),
                                     (f3, _("1 Minute"), _("von der Rechnung zur Entscheidung. Jede Zahl mit Quelle.")))):
        col.markdown(f"<div class='feat' style='animation-delay:{.35 + .12 * i:.2f}s'><div class='k'>{k}</div>"
                     f"<div class='d'>{d}</div></div>", unsafe_allow_html=True)
    st.markdown(BAND_CSS, unsafe_allow_html=True)
    with st.container(key="band_how"):
        section(_("In drei Schritten"), _("So funktioniert's"))
        cards = "".join(f"<div class='step-card'><div class='no'>{no}</div><b>{title}</b><span>{text}</span></div>" for no, title, text in (
                ("01", _("Rechnungen hochladen"), _("PDF oder CSV — oder erst das Beispiel ansehen. Codes, Gewichte und Herkunft werden erkannt.")),
                ("02", _("Ergebnis lesen"), _("Welche Waren zählen, wie nah Sie an 50 t sind und was es kosten würde.")),
                ("03", _("Entscheiden"), _("Unter 50 t bleiben, Zulassung beantragen oder echte Daten beim Lieferanten anfragen — mit fertigen Dokumenten."))))
        st.markdown(f"<div class='steps'>{cards}</div>", unsafe_allow_html=True)
    with st.container(key="band_faq"):
        section(_("Hilfe"), _("Fragen & Antworten"))
        faq()
        footer()
    st.stop()

section(_("Schritt 1"), _("Ihre Einkäufe"))

if annex is None:
    st.error(_("data/annex_i.json fehlt — ohne Anhang I ist keine Prüfung möglich."))
    st.stop()

lines = None
planned_lines = []  # order confirmations: planned imports, never counted as imported


def gemini_key():
    try:
        key = st.secrets.get("GEMINI_API_KEY")
    except Exception:  # no secrets.toml locally
        key = None
    return key or os.environ.get("GEMINI_API_KEY")


@st.cache_data(show_spinner=False)
def _read_ai(data, name):
    """Fallback for PDFs our parser cannot read (scans, photos, unusual layouts)."""
    return extract_document(data, name, gemini_key())


# Part of the cache key: an updated parser must not serve results cached by the old one
PARSER_VERSION = __import__("hashlib").sha1(Path(cbam.extract.__file__).read_bytes()).hexdigest()


@st.cache_data(show_spinner=False)
def _read(blobs, parser_version=None):
    """Parse each document once; Streamlit reruns the script on every click."""
    return read_documents([(io.BytesIO(data), name) for data, name in blobs])


def use_documents(blobs):
    """blobs: list of (bytes, file name), PDF or CSV. Returns invoice lines as DataFrame (or None)."""
    global planned_lines
    imported, planned_lines, errors = _read(tuple(blobs), PARSER_VERSION)
    planned_lines = list(planned_lines)
    imported = list(imported)
    failed = {e.split(":")[0]: e for e in errors}
    # Parsed, but no position has a weight: the layout fooled the parser - let the AI try as well
    weak = {name for _d, name in blobs if name.lower().endswith(".pdf")
            and (ls := [l for l in imported + planned_lines if l.get("file") == name])
            and all(l.get("net_mass_kg") is None for l in ls)}
    if weak and gemini_key():
        for data, name in blobs:
            if name not in weak:
                continue
            try:
                with st.spinner(_("{f} wird mit KI gelesen …", f=name)):
                    ai = _read_ai(data, name)
            except Exception:
                continue
            if any(l.get("net_mass_kg") for l in ai):
                imported = [l for l in imported if l.get("file") != name]
                planned_lines = [l for l in planned_lines if l.get("file") != name]
                st.info(_("{f}: per KI gelesen — bitte Codes und Gewichte unten prüfen.", f=name))
                for l in ai:
                    (planned_lines if l["doc_type"] == "order" else imported).append(l)
    if failed and gemini_key():
        for data, name in blobs:
            if name in failed and name.lower().endswith(".pdf"):
                try:
                    with st.spinner(_("{f} wird mit KI gelesen …", f=name)):
                        ai = _read_ai(data, name)
                except Exception as e:  # API down or quota: keep the parser's message
                    failed[name] += f" · KI: {type(e).__name__}"
                    continue
                if ai:
                    del failed[name]
                    st.info(_("{f}: per KI gelesen — bitte Codes und Gewichte unten prüfen.", f=name))
                    for l in ai:
                        (planned_lines if l["doc_type"] == "order" else imported).append(l)
    for e in failed.values():
        st.warning(_("{f}: konnte nicht gelesen werden. Bitte als CSV hochladen oder Positionen unten von Hand eintragen.",
                     f=e.split(":")[0]) + f" ({e.split(':', 1)[-1].strip()})")
    st.caption(_("{n} Dokument(e) gelesen: {inv} Rechnungszeile(n), {plan} geplante Zeile(n) aus Auftragsbestätigungen.",
                 n=len(blobs), inv=len(imported), plan=len(planned_lines)))
    return pd.DataFrame(imported) if imported else None


uploads = st.file_uploader(_("Eigene Rechnungen hochladen — PDF oder CSV"), type=["pdf", "csv"], accept_multiple_files=True,
                           key="uploads", on_change=own_files_changed, help=_("Auftragsbestätigungen zählen als geplante Einfuhr, nicht als bereits eingeführt. CSV-Spalten: ") + ", ".join(COLUMNS))
if uploads:
    lines = use_documents([(f.getvalue(), f.name) for f in uploads])
elif st.session_state.get("demo") == "pdf":
    lines = use_documents([(p.read_bytes(), p.name) for p in DEMO_PDFS])

if lines is None:
    st.info(_("Laden Sie Ihre Rechnungen hoch — das Ergebnis erscheint dann hier."))
    footer()
    st.stop()

missing_cols = [c for c in COLUMNS if c not in lines.columns]
if missing_cols:
    st.error(_("Fehlende Spalten: ") + ", ".join(missing_cols))
    st.stop()



def _valid_cn(cn):
    try:
        check_annex_i(cn)
        return True
    except (ValueError, TypeError):
        return False


# Lines without a CN code: propose one (deterministic rules), the user confirms with one click.
lines = lines.reset_index(drop=True)
fixes = st.session_state.setdefault("cn_fixes", {})
for i, desc in fixes.items():
    if i < len(lines) and lines.loc[i, "description"] == desc[0]:
        lines.loc[i, "cn"] = desc[1]
for i, row in lines.iterrows():
    if _valid_cn(row["cn"]):
        continue
    with st.container(border=True):
        st.markdown(_("**Kein KN-Code** bei „{d}“", d=row["description"]))
        options = suggest_cn(row["description"])
        if not options:
            st.caption(_("Kein Vorschlag möglich — bitte Code in der Tabelle unten eintragen ([Zolltarif TARIC]({u})).", u=TARIC_URL))
        for k, s in enumerate(options):
            verdict = _("CBAM-Ware") if s["cbam"] else _("keine CBAM-Ware")
            col1, col2 = st.columns([4, 1])
            col1.markdown(_("Vorschlag: **{cn}** — {label} · {v} · Sicherheit: {c}",
                            cn=s["cn"], label=_(s["label"]), v=verdict, c=_(s["confidence"])))
            if col2.button(_("Übernehmen"), key=f"fix_{i}_{k}"):
                fixes[i] = (row["description"], s["cn"])
                st.rerun()
        if options:
            st.caption(_("Vorschlag nach Warenbeschreibung, bitte prüfen ([Zolltarif TARIC]({u})).", u=TARIC_URL))

with st.expander(_("Erkannte Positionen prüfen und korrigieren ({n})", n=len(lines))):
    st.caption(_("Bitte KN-Codes und Gewichte prüfen — Sie können jede Zelle korrigieren."))
    lines = st.data_editor(lines[COLUMNS + [c for c in lines.columns if c not in COLUMNS]], num_rows="dynamic",
                           width="stretch", column_config={
                               "description": _("Ware"), "cn": _("KN-Code"), "net_mass_kg": _("Nettomasse (kg)"),
                               "origin": _("Land"), "date": _("Datum"), "supplier": _("Lieferant")})

# Rows from uploads or hand edits may lack a weight or date; NaN must not reach the logic or the AI.
lines = lines.copy()
lines["net_mass_kg"] = pd.to_numeric(lines["net_mass_kg"], errors="coerce")
lines["date"] = pd.to_datetime(lines["date"], errors="coerce").dt.strftime("%Y-%m-%d")
incomplete = lines["net_mass_kg"].isna() | lines["date"].isna()
if incomplete.any():
    st.warning(_("{n} Zeile(n) ohne Gewicht oder Datum werden nicht gezählt — bitte oben ergänzen.", n=int(incomplete.sum())))
lines = lines[~incomplete].astype(object).where(lines[~incomplete].notna(), None)
if lines.empty:
    st.stop()

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
cost = after = None
total_after = status["total_t"] + planned_t
crosses = planned_t > 0 and total_after > THRESHOLD_T >= status["total_t"]
if default_values is not None and prices is not None:
    year_cbam = [r for r in records if r["cbam"] and str(r["date"]).startswith(year)]
    cost = estimate_cost(year_cbam, prices, default_values)
    planned_records = [{**l, "cbam": True, "sector": check_annex_i(l["cn"])["sector"]} for l in planned_cbam]
    after = estimate_cost(year_cbam + planned_records, prices, default_values) if planned_records else cost

# Step 2: the answer, in one sentence
section(_("Schritt 2"), _("Ihr Ergebnis"))
t = status["total_t"]
sub = {
    "exempt": _("Sie müssen derzeit nichts zahlen. Geben Sie die Befreiung in der Zollanmeldung an und behalten Sie die Menge im Blick."),
    "near": _("Noch {left:.1f} t, dann brauchen Sie eine Zulassung als CBAM-Anmelder — sonst drohen hohe Strafen.", left=max(THRESHOLD_T - t, 0)),
    "over": _("Sie brauchen den Status als zugelassener CBAM-Anmelder. Ohne Zulassung drohen hohe Strafen."),
}[status["status"]]
chip = {"exempt": _("Befreit"), "near": _("Knapp unter dem Limit"), "over": _("Limit überschritten")}[status["status"]]
if crosses:
    chip = _("Geplante Lieferung überschreitet das Limit")
    sub = _("Heute sind Sie mit {t:.1f} t noch befreit. Die bestätigte Bestellung über {p:.1f} t würde die Schwelle überschreiten — entscheiden Sie vorher (Schritt 3).", t=t, p=planned_t)
color = STATUS_COLOR["over" if crosses else status["status"]]
end_t = total_after if planned_t else t
nums = f"<span class='big'>{n(t)} t</span><span class='of'>/ 50 t</span>"
if planned_t:
    nums += f"<span class='arrow'>→</span><span class='big' style='color:{STATUS_COLOR['over'] if end_t > THRESHOLD_T else '#1D1D1F'}'>{n(end_t)} t</span>"
if end_t > THRESHOLD_T:
    nums += f"<span class='over'>{_('+{o:.1f} t über dem Limit', o=end_t - THRESHOLD_T)}</span>"
st.markdown(f"<div class='hero-card' style='--c:{color}'><div class='kicker'>{html.escape(importer or _("Ihr Unternehmen"))} · {year}</div>"
            f"<span class='chip' style='color:{color};background:{color}1A'>{chip}</span>"
            f"<div class='nums'>{nums}</div><div class='sub'>{sub}</div></div>",
            unsafe_allow_html=True)
# Threshold bar: imported (solid) + planned (hatched), 50 t marker
scale = max(THRESHOLD_T * 1.2, total_after * 1.05)
w_imp, w_plan, x_lim = t / scale * 100, planned_t / scale * 100, THRESHOLD_T / scale * 100
bar_color = STATUS_COLOR["over" if t > THRESHOLD_T else ("near" if t >= 0.8 * THRESHOLD_T else "exempt")]
st.markdown(
    f"<div class='tbar' role='img' aria-label='{html.escape(_('{t:.1f} t von {max:.0f} t CBAM-Waren im Jahr {year}', t=t, max=THRESHOLD_T, year=year))}'>"
    f"<div class='zone' style='left:{x_lim:.1f}%'></div>"
    f"<div class='imp' style='width:{w_imp:.1f}%;background:{bar_color}'></div>"
    f"<div class='plan' style='left:{w_imp:.1f}%;width:{w_plan:.1f}%'></div>"
    f"<div class='lim' style='left:{x_lim:.1f}%'><span>50 t</span></div></div>"
    f"<div class='tlegend'><span><i style='background:{bar_color}'></i>{_('Eingeführt {year}: {t:.1f} t', year=year, t=t)}</span>"
    + (f"<span><i class='hatch'></i>{_('Geplant: {p:.1f} t', p=planned_t)}</span>" if planned_t else "")
    + "</div>", unsafe_allow_html=True)
if status["forecast_crossing"]:
    st.caption(_("Prognose beim bisherigen Tempo: Schwelle erreicht am **{d}**.", d=status["forecast_crossing"]))
def money(c, v):
    """No EU default value for some lines: never show their share as € 0."""
    if not c["missing_default_value"]:
        return eur(v)
    return _("nicht berechenbar") if not c["lines"] else _("mind. {v}", v=eur(v))


def krange(c, lo, hi):
    if not c["missing_default_value"]:
        return f"€ {n(lo / 1000, ',.0f')}–{n(hi / 1000, ',.0f')} k"
    return _("nicht berechenbar") if not c["lines"] else _("mind. {v}", v=f"€ {n(lo / 1000, ',.0f')} k")


if cost and cost["missing_default_value"]:
    st.caption(_("Für einige Positionen ({c}) gibt es keinen EU-Standardwert (nur Eisen/Stahl und Aluminium sind hinterlegt). Die Menge zählt für die 50-t-Schwelle, die Kosten können wir dafür nicht schätzen.",
                 c=", ".join(sorted({str(l.get("origin") or "?") for l in cost["missing_default_value"]}))))
if cost:
    over_now = t > THRESHOLD_T
    m1, m2, m3 = st.columns(3)
    m1.metric(_("Heute zu zahlen"), money(cost, cost["certificate_cost_eur"]) if over_now else _("€ 0 (befreit)"),
              help=_("Zertifikate für alle CBAM-Waren des Jahres, sobald Sie über 50 t liegen."))
    if crosses:
        lo, hi = after["penalty_range_eur"]
        m2.metric(_("Nach der Lieferung: Zertifikate"), money(after, after["certificate_cost_eur"]),
                  help=_("Mit Zulassung: Menge × EU-Standardwert × Zertifikatspreis des Quartals, für alle Waren des Jahres."))
        m3.metric(_("Nach der Lieferung ohne Zulassung"), krange(after, lo, hi),
                  help=_("Strafe 3–5 × € 100 je fehlendem Zertifikat (Art. 26 Abs. 2a)."))
    else:
        lo, hi = cost["penalty_range_eur"]
        m2.metric(_("Graue Emissionen"), (_("nicht berechenbar") if cost["missing_default_value"] and not cost["lines"]
                                          else ("≥ " if cost["missing_default_value"] else "") + f"{n(cost['total_emissions_t'], ',.0f')} t CO₂e"))
        m3.metric(_("Falls über 50 t: Zertifikate") if not over_now else _("Strafe ohne Zulassung"),
                  money(cost, cost["certificate_cost_eur"]) if not over_now else krange(cost, lo, hi))

# One primary next step, depending on the situation
cbam_suppliers = sorted({r["supplier"] for r in records if r["cbam"] and isinstance(r.get("supplier"), str)})


@st.dialog(_("Checkliste für die Zulassung"), width="large")
def checklist_dialog():
    st.markdown(CHECKLIST.read_text(encoding="utf-8"))


@st.dialog(_("Brief an Ihren Lieferanten"), width="large")
def letter_dialog():
    sup = st.selectbox(_("Lieferant"), cbam_suppliers)
    lg = st.radio(_("Sprache des Briefs"), ["de", "en"], horizontal=True, key="dlg_lang")
    txt = supplier_letter(sup, records, importer or _("Ihr Unternehmen"), lg)
    st.text_area(_("Brief"), txt, height=300, label_visibility="collapsed")
    st.download_button(_("Brief herunterladen (.txt)"), txt, file_name=f"CBAM_Anfrage_{sup[:20]}.txt", type="primary")


if crosses or t > THRESHOLD_T:
    ns_title = _("Zulassung beantragen, bevor die Ware kommt")
    ns_text = _("Ohne Zulassung drohen Strafen auf alle Emissionen des Jahres. Die Checkliste zeigt Schritt für Schritt, was das AnEH braucht.")
    ns_kind = "checklist" if CHECKLIST.exists() else "report"
elif status["status"] == "near" and cbam_suppliers:
    ns_title = _("Lieferanten nach echten Emissionsdaten fragen")
    ns_text = _("Sie sind knapp unter 50 t. Echte Daten sind oft niedriger als die EU-Standardwerte — der fertige Brief spart Ihnen die Formulierung.")
    ns_kind = "letter"
else:
    ns_title = _("Befreiung dokumentieren")
    ns_text = _("Laden Sie den Bericht mit Quellen herunter — so können Sie jederzeit belegen, warum Sie befreit sind.")
    ns_kind = "report"
st.markdown(f"<div class='next-step' style='--c:{STATUS_COLOR['over' if crosses or t > THRESHOLD_T else status['status']]}'>"
            f"<div class='lbl'>{_('Ihr nächster Schritt')}</div><b>{ns_title}</b><span>{ns_text}</span></div>",
            unsafe_allow_html=True)
ns_col, _ns_pad = st.columns([1, 1.4])
if ns_kind == "checklist":
    if ns_col.button(_("Checkliste öffnen"), type="primary", width="stretch", key="ns_checklist"):
        checklist_dialog()
elif ns_kind == "letter":
    if ns_col.button(_("Brief erstellen"), type="primary", width="stretch", key="ns_letter"):
        letter_dialog()
else:
    ns_col.download_button(_("Bericht herunterladen (PDF)"), report_pdf(importer or _("Ihr Unternehmen"), year, status, records, cost),
                           file_name=f"CBAM_Bericht_{year}.pdf", mime="application/pdf", type="primary",
                           width="stretch", key="ns_report")

if st.session_state.pop("scroll_to_result", False):  # came from "Beispiel ansehen": jump to the answer
    import streamlit.components.v1 as components
    components.html("<script>const d=window.parent.document;const el=d.querySelector('.hero-card');"
                    "if(el){el.scrollIntoView({behavior:'smooth',block:'start'});}</script>", height=0)

# Step 3: details and actions
section(_("Schritt 3"), _("Was jetzt?"))
t_act, t_goods, t_cost, t_what, t_ask = st.tabs([_("Nächste Schritte"), _("Waren"), _("Kosten"),
                                                 _("Was wäre wenn"), _("Fragen")])

with t_act:
    a, b, c = st.columns(3)
    a.markdown(f"<div class='option'><b>{_('A · Unter 50 t bleiben')}</b>"
               f"{_('Noch **{t:.1f} t** bis zur Schwelle. Käufe planen und dokumentieren.', t=float(max(THRESHOLD_T - t, 0))).replace('**', '')}</div>",
               unsafe_allow_html=True)
    b.markdown(f"<div class='option'><b>{_('B · Zulassung beantragen')}</b>"
               f"{_('Antrag als zugelassener CBAM-Anmelder beim AnEH (cbam@bmf.gv.at), bevor die Schwelle überschritten wird.')}</div>",
               unsafe_allow_html=True)
    c.markdown(f"<div class='option'><b>{_('C · Lieferant fragen')}</b>"
               f"{_('Echte Emissionsdaten beim Lieferanten anfordern — oft niedriger als die Standardwerte.')}</div>",
               unsafe_allow_html=True)
    if cost is not None and (planned_t or status["status"] != "exempt"):
        now_eur = _("€ 0 (befreit)") if t <= THRESHOLD_T else money(cost, cost["certificate_cost_eur"])
        rows = [{_("Szenario"): _("Ohne geplante Lieferung"), _("Menge"): f"{n(t)} t", _("Kosten im Jahr"): now_eur}]
        if planned_t:
            rows.append({_("Szenario"): _("Mit geplanter Lieferung und Zulassung"), _("Menge"): f"{n(total_after)} t",
                         _("Kosten im Jahr"): (money(after, after["certificate_cost_eur"]) if total_after > THRESHOLD_T
                                               else _("€ 0 (befreit)"))})
        if total_after > THRESHOLD_T:
            lo_a, hi_a = after["penalty_range_eur"]
            rows.append({_("Szenario"): _("Über 50 t ohne Zulassung"), _("Menge"): f"{n(total_after)} t",
                         _("Kosten im Jahr"): (f"{eur(lo_a)} – {eur(hi_a)}" if not after["missing_default_value"]
                                               else money(after, lo_a))})
        st.markdown("#### " + _("Was kostet welche Entscheidung?"))
        st.table(pd.DataFrame(rows))
        st.caption(_("Wird die Schwelle überschritten, zählen alle CBAM-Waren des Jahres, nicht nur die Menge über 50 t. Lieferung später planen ist zulässig; Lieferungen künstlich aufzuteilen, um unter 50 t zu bleiben, ist es nicht."))
    if CHECKLIST.exists():
        with st.expander(_("Checkliste Antrag")):
            st.markdown(CHECKLIST.read_text(encoding="utf-8"))

    st.markdown("#### " + _("Dokumente"))
    importer = st.text_input(_("Ihr Unternehmen"), key="importer")
    pdf = report_pdf(importer or _("Ihr Unternehmen"), year, status, records, cost)
    st.download_button(_("Bericht herunterladen (PDF)"), pdf, file_name=f"CBAM_Bericht_{year}.pdf",
                       mime="application/pdf")
    suppliers = sorted({r["supplier"] for r in records if r["cbam"] and isinstance(r.get("supplier"), str)})
    if suppliers:
        s1, s2 = st.columns([3, 1])
        supplier = s1.selectbox(_("Brief an Lieferanten (Anfrage echter Emissionsdaten)"), suppliers)
        lang = s2.radio(_("Sprache des Briefs"), ["de", "en"], horizontal=True)
        letter = supplier_letter(supplier, records, importer or _("Ihr Unternehmen"), lang)
        with st.expander(_("Brief")):
            st.text_area(_("Brief"), letter, height=320, label_visibility="collapsed")
        st.download_button(_("Brief herunterladen (.txt)"), letter, file_name=f"CBAM_Anfrage_{supplier[:20]}.txt")

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
            st.dataframe(pd.DataFrame(cost["lines"])[["description", "origin", "formula", "emissions_t", "certificate_eur",
                                                      "factor_source"]],
                         width="stretch", hide_index=True, column_config={
                             "description": _("Ware"), "origin": _("Land"), "formula": _("Rechnung"),
                             "emissions_t": st.column_config.NumberColumn("t CO₂e", format="%.1f"),
                             "certificate_eur": st.column_config.NumberColumn("€", format="%.0f"),
                             "factor_source": st.column_config.LinkColumn(_("Standardwert"), display_text=_("EU-Tabelle"))})
        if cost["missing_default_value"]:
            st.warning(_("{n} Zeile(n) ohne Standardwert für Herkunftsland/KN — nicht geschätzt.", n=len(cost["missing_default_value"])))
        st.caption(_("Standardwerte inkl. Aufschlag des Jahres (DVO (EU) 2025/2621). Zertifikatspreis des Einfuhrquartals: [Europäische Kommission]({u}). Strafe: 3–5 × € 100 je fehlendem Zertifikat, auf alle Emissionen des Jahres (Art. 26 Abs. 2a, vor Indexierung).", u=PRICE_URL))

with t_what:
    st.markdown(_("Was passiert mit einer zusätzlichen Bestellung? Und was kostet dieselbe Ware aus einem anderen Land?"))
    if cost is None:
        st.info(_("Standardwerte oder Zertifikatspreise fehlen noch (data/default_values.csv, data/cbam_prices.json)."))
    else:
        w1, w2, w3 = st.columns([2, 1, 1])
        w_cn = w1.text_input(_("KN-Code der Ware"), "7604 29 90")
        w_t = w2.number_input(_("Menge (t)"), min_value=0.0, value=10.0, step=1.0)
        countries = sorted({v["country_iso"] for v in default_values})
        w_country = w3.selectbox(_("Herkunft"), countries, index=countries.index("CN") if "CN" in countries else 0)
        try:
            w_verdict = check_annex_i(w_cn)
        except (ValueError, TypeError):
            w_verdict = None
        if w_verdict is None:
            st.warning(_("Bitte einen gültigen KN-Code eingeben (mindestens 4 Ziffern)."))
        elif not w_verdict["cbam"]:
            st.success(_("Keine CBAM-Ware — zählt nicht zur 50-t-Schwelle."))
        else:
            w_date = f"{year}-12-01" if int(year) != date.today().year else date.today().isoformat()
            base = t + planned_t
            new_t = base + w_t
            line = {"cn": w_cn, "net_mass_kg": w_t * 1000, "date": w_date, "cbam": True, "sector": w_verdict["sector"],
                    "description": w_verdict["description"]}
            msg = _("Danach: **{n:.1f} t** von 50 t (bisher {b:.1f} t inkl. geplanter Lieferungen).", n=new_t, b=base)
            (st.error if new_t > THRESHOLD_T else st.success)(
                msg + " " + (_("Schwelle überschritten — Zulassung nötig.") if new_t > THRESHOLD_T else _("Weiter befreit.")))
            comp = []
            for ctry in countries:
                c = estimate_cost([{**line, "origin": ctry}], prices, default_values)
                if c["lines"]:
                    r = c["lines"][0]
                    comp.append({_("Herkunft"): ctry, _("t CO₂ je t Ware"): n(r["factor_tco2_per_t"], ",.3f"),
                                 "t CO₂e": n(r["emissions_t"]), _("Zertifikate"): eur(r["certificate_eur"])})
            if comp:
                st.markdown(_("Dieselbe Menge aus verschiedenen Ländern (EU-Standardwerte, Preis des Einfuhrquartals):"))
                st.table(pd.DataFrame(comp))
                st.caption(_("Zahlen gelten, wenn Sie über 50 t liegen. Echte Lieferantendaten können niedriger sein (Option C)."))
            else:
                st.info(_("Für diesen KN-Code gibt es in unseren Daten keinen Standardwert."))

with t_ask:
    api_key = gemini_key()
    if not api_key:
        st.caption(_("KI-Assistent aus (kein GEMINI_API_KEY) — Sie erhalten eine feste Zusammenfassung."))
    with st.form("ask", clear_on_submit=True):
        question = st.text_input(_("Ihre Frage"), placeholder=_("z. B. Was passiert, wenn ich im Herbst noch 20 t Profile kaufe?"))
        sent = st.form_submit_button(_("Fragen"))
    history = st.session_state.setdefault("chat", [])  # every click reruns the script; keep the answers
    if sent and question:
        ctx = {"lines": records, "year": int(year), "values": default_values, "prices": prices}
        with st.spinner(_("CBAM Helper rechnet …")):
            text, calls = answer(question, ctx, api_key=api_key,
                                 language={"de": "Deutsch", "en": "Englisch"}[L])
        history.append((question, text, calls))
    for question, text, calls in reversed(history):
        st.chat_message("user").write(question)
        st.chat_message("assistant").write(text)
        for call in calls:
            with st.expander(f"{_('Werkzeug')}: {call['name']}({call['args'] or ''})"):
                st.json(call["result"])

footer()
