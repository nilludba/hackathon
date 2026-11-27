# CBAM-Lotse

AI agent that helps small Austrian importers of steel and aluminium handle the EU
Carbon Border Adjustment Mechanism (CBAM): it reads import invoices, checks every
CN code against Annex I of Regulation (EU) 2023/956, tracks the 50-tonne annual
exemption threshold introduced by the CBAM Omnibus (Regulation (EU) 2025/2083),
estimates certificate cost and penalty risk, and drafts the supplier request and a
report in which every number links to its legal source.

Built at the AAU Hackathon, Klagenfurt, 27–29 November 2026
(University Challenge "The $15-an-Hour Expert").

## Principle

The language model extracts data from invoices and explains results. Every legal
decision (is this a CBAM good? is the threshold crossed?) and every calculation is
deterministic Python code covered by tests. Numbers come only from the files in
`data/`, each with a `source` link.

## Project layout

```
app.py              Streamlit user interface (German)
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

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest
```

Start the web app:

```bash
streamlit run app.py
```

The AI assistant (section 6) uses the Google Gemini API. It is optional: without a key the app still runs
and shows a fixed summary. To turn it on, set the key yourself, never commit it:

```bash
export GEMINI_API_KEY=...                       # or .streamlit/secrets.toml: GEMINI_API_KEY = "..."
```

The model only calls our tools (`check_cn`, `threshold`, `cost`); every number in its answer comes from them.
The hosted demo link will be added here.

## Disclaimer

CBAM-Lotse is a pre-check and document-preparation tool, not legal advice. The
importer and the competent authority (in Austria: Amt für den nationalen
Emissionszertifikatehandel, AnEH) remain responsible for the final decision.
