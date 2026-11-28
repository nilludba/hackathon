# Jury questions and answers (criteria: Creativity · User interaction · Problem fit)

Short answers, max 2 sentences each. Numbers: `demo/demo_script.md`, sources: `data/market_facts.md`.

## Creativity of the solution

**"Isn't this just ChatGPT with a PDF upload?"**
No. The AI only reads invoices and explains; Annex I, the 50 t threshold and every euro are computed by deterministic code with over 130 tests — you can run them from the sidebar.

**"What is new compared to existing CBAM tools?"**
Existing SME tools (e.g. CbamTrack from €79/month, CBAM Desk from €145/month) help you *report* once you are in scope. We help the importer *below or near* 50 t: read invoices, watch the threshold and warn before the order that pushes you over.

**"What if the AI misreads a CN code?"**
The extraction is rule-based (pdfplumber), not guessed; if a code is missing the app proposes one from the description, shows its confidence and the user confirms with one click. Everything after that is tested code.

## Quality of user interaction

**"Who is the user and can he really use it?"**
A workshop owner with no customs knowledge: result in one sentence first ("Careful: 41 of 50 t"), three steps, PDFs instead of codes, plain language, German/English/Russian.

**"How does he know the number is right?"**
Every line shows its formula (tonnes × EU default value × quarter price) and links to the Commission's table and EUR-Lex.

**"What does he walk away with?"**
Three files: a PDF report with sources, a letter to the supplier asking for real emission data, and the AnEH application checklist.

## Problem fit & practical impact

**"How big is the problem?"**
About 200,000 EU importers of CBAM goods; 182,000 are exempt only as long as they stay under 50 t (European Commission). Above it, without authorisation, the fine is €300–500 per tonne of CO₂ on the whole year.

**"Did you talk to real users?"**
[Validation quotes — fill in after the calls.]

**"What is the practical impact for Herr Gruber?"**
One order decides between €0, about €19,000 of certificates or a €72,000–121,000 fine — and he sees it before ordering, not after customs.

**"Isn't option A (deliver in January) just dodging the law?"**
Planning a real delivery date is legal; artificially splitting shipments to stay under 50 t is not, and the app says so.

**"Why Austria?"**
Customs authority, application process and language are national; we built the AnEH checklist from the BMF guide. The rules themselves are EU-wide, so other countries need only a new checklist.

## Limits — say them before the jury does

- First assessment, not legal advice; the AnEH and the customs office decide.
- Default values only (no actual installation emissions); all 74 countries of the EC table plus "Other countries and territories" for the rest (Annex I, Impl. Reg. 2025/2621), iron/steel and aluminium only.
- Scanned PDFs without a text layer are not read yet.
- Q4 2026 certificate price is not published yet: Q3 is used and marked "estimate".

## Presentation-day checklist (Sunday 29.11)

- [ ] 07:30 open the hosted app on the presentation laptop **and** a phone; click "Demo-PDFs einlesen" once (warms the cache)
- [ ] Backup: run locally (`streamlit run app.py`, see README) — works without internet except the AI chat
- [ ] Backup 2: screen recording of the demo flow (Darmen, after deploy) on the laptop desktop
- [ ] Slides: `pitch/CBAM Helper_Pitch.pptx`; fill in the 2 quotes and the Streamlit link
- [ ] Language switch on **English** for the jury, German for the demo data is fine
- [ ] Gemini key set in Streamlit secrets; if the AI fails, the app shows the fixed summary — do not demo the chat as the main feature
- [ ] 09:45 submit: README with run instructions + link
