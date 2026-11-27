# CBAM Helper

AI agent that helps small Austrian importers of steel and aluminium handle the EU
Carbon Border Adjustment Mechanism (CBAM): it reads import invoices, checks every
CN code against Annex I of Regulation (EU) 2023/956, tracks the 50-tonne annual
exemption threshold introduced by the CBAM Omnibus (Regulation (EU) 2025/2083),
estimates certificate cost and penalty risk, and drafts the supplier request and a
report in which every number links to its legal source.

**Live demo: https://cbam-helfer.streamlit.app/?embed=true** — click "Demo starten" (DE/EN switch top right).

Built at the AAU Hackathon, Klagenfurt, 27–29 November 2026
(University Challenge "The $15-an-Hour Expert").

## Principle

The language model extracts data from invoices and explains results. Every legal
decision (is this a CBAM good? is the threshold crossed?) and every calculation is
deterministic Python code covered by tests. Numbers come only from the files in
`data/`, each with a `source` link.

## Project layout

```
app.py              Streamlit user interface (DE/EN, texts in i18n.py)
cbam/agent.py       Gemini agent: tool calling over the deterministic functions
cbam/annex.py       check_annex_i: CN code -> CBAM good or not
cbam/threshold.py   50 t threshold status and forecast
cbam/cost.py        embedded emissions, certificate cost, penalty scenario
cbam/extract.py     invoice PDF/CSV -> lines
cbam/documents.py   supplier letter (DE/EN) and PDF report
data/               annex_i.json, default_values.csv, cbam_prices.json
demo/               demo invoices for "Metallbau Gruber GmbH"
tests/              pytest suite
```

## Run locally (about 2 minutes)

Needs Python 3.11+ and git.

**Windows (PowerShell)**

```powershell
git clone https://github.com/nilludba/hackathon
cd hackathon
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m streamlit run app.py
```

**macOS / Linux**

```bash
git clone https://github.com/nilludba/hackathon
cd hackathon
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/streamlit run app.py
```

The app opens at http://localhost:8501. Click **"Demo starten"** to run the full flow on the
demo company. The DE/EN switch is at the top right.

Tests: `.venv/bin/pytest` (Windows: `.venv\Scripts\python -m pytest`).

### Optional: AI assistant

The "Questions" tab uses the Google Gemini API. Without a key the app still works and answers with a
fixed summary. To turn it on, set the key in your shell (never commit it):

```bash
export GEMINI_API_KEY=...          # PowerShell: $env:GEMINI_API_KEY="..."
```

or put `GEMINI_API_KEY = "..."` into `.streamlit/secrets.toml`. The model only calls our tools
(`check_cn`, `threshold`, `cost`); every number in its answer comes from them.

## Disclaimer

CBAM Helper is a pre-check and document-preparation tool, not legal advice. The
importer and the competent authority (in Austria: Amt für den nationalen
Emissionszertifikatehandel, AnEH) remain responsible for the final decision.
