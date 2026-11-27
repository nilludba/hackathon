# Demo script and slide numbers (3 minutes)

Jury criteria (updated 27.11 23:25): **Creativity of solution · Quality of user interaction · Problem fit & practical impact** (10 each).

All numbers below were computed with the project code (`read_documents` → `check_annex_i` →
`threshold_status` → `estimate_cost`) on the four demo PDFs in `demo/`. Re-run after data changes:
`python demo/compute_demo_numbers.py`.

## Key numbers

| | Value |
|---|---|
| Documents read | 4 (3 invoices, 1 order confirmation) |
| Invoice lines found | 6, of which **4 CBAM goods**, 1 non-CBAM (valves 8481), 1 without code (nails → user confirms) |
| CBAM goods imported in 2026 | **41.0 t of 50 t (82 %)** → status "near" |
| Embedded emissions (default values incl. 2026 mark-up) | **176.8 t CO₂e** |
| Certificate cost **if** obliged | **€ 13,753** (each line at its quarter's price: Q1 € 75.36, Q2 € 75.28, Q3 € 82.32) |
| Planned order (12 t aluminium profiles from China, delivery week 50) | 41 t + 12 t = **53 t > 50 t** |
| After the order: emissions / certificates | **241.3 t CO₂e / € 19,057** (Q4 price not yet published → Q3 used, marked "Schätzung") |
| After the order **without** authorisation: penalty | **€ 72,379 – € 120,631** (€ 300–500 per missing certificate, Art. 26(2a)) |

Line by line (formula shown in the app):

| Invoice | Goods | CN | Origin | t | tCO₂e/t (2026) | Price | € |
|---|---|---|---|---|---|---|---|
| EXP-2026-0147 | HEB beams | 7216 33 10 | TR | 18.4 | 2.541 | 75.36 | 3,523 |
| EXP-2026-0147 | Screws M16 | 7318 15 88 | TR | 2.6 | 5.973 | 75.36 | 1,170 |
| NBHX-26-0388 | Aluminium profiles | 7604 29 90 | CN | 9.8 | 5.369 | 75.28 | 3,961 |
| EXP-2026-0512 | Steel stair stringers | 7308 90 59 | TR | 10.2 | 6.072 | 82.32 | 5,098 |

## The decision (slide "What Herr Gruber decides")

Today he is exempt and pays **€ 0**. The one order from China changes that:

| Option | What happens in 2026 | Cost |
|---|---|---|
| **A** Deliver in January 2027 instead of week 50 | stays at 41 t → still exempt | € 0 for 2026 (the 12 t count for 2027) |
| **B** Apply for authorisation now, then import | 53 t, declaration by 30.09.2027 | ≈ € 19,057 certificates + admin |
| **C** Ask the supplier for real emission data | lower factor than the default value → lower cost | depends on supplier data |
| (do nothing) | 53 t without authorisation | € 72k – 121k penalty |

Careful wording for option A: a real business decision to deliver later is fine; artificially splitting
shipments to stay below 50 t is what the anti-avoidance rules target. Say "plan the delivery date",
not "split to dodge".

## 3-minute flow

1. **0:00–0:30 Problem.** "Since 1 January 2026 every company importing steel or aluminium into the EU has a new duty. 182,000 importers are exempt — but only as long as they stay under 50 tonnes a year. Cross it unnoticed and the fine is € 300–500 per tonne of CO₂ for the whole year."
2. **0:30–2:00 Live demo.** Herr Gruber, Metallbau in Klagenfurt, 15 employees. Upload 4 PDFs (tab "Rechnungen (PDF) hochladen" or "Demo-PDFs einlesen") → 6 lines, 4 CBAM goods, each with its Annex I entry → **41 of 50 t** → the order confirmation: **"this delivery pushes you to 53 t"** → three options with euros → supplier letter + PDF report.
3. **2:00–2:30 Trust.** Click a number → formula, default value from the Commission's Excel, EUR-Lex link. "The AI reads and explains; every legal decision is tested code — over 110 automated tests."
4. **2:30–3:00 Problem fit & impact.** Who has this problem: ~200,000 EU importers of CBAM goods, 182,000 of them exempt only while below 50 t (Commission) — mostly SMEs like Herr Gruber. Impact in the demo: one order decides between **€ 0**, **€ 19k** of certificates or a **€ 72k–121k** fine — and he sees it *before* ordering. Validation quotes from Kärnten go here (interviews pending).

## How the demo shows each criterion

| Criterion | Show on stage |
|---|---|
| Creativity | AI only reads invoices and explains; law and maths are tested code — no hallucinated numbers. The order confirmation is checked *before* the goods arrive. |
| Quality of user interaction | One sentence result on top, 3 steps, PDF upload instead of typing CN codes, plain-language explanation, DE/EN/RU, every number clickable → formula + source. Nails without a code: the app asks instead of guessing. |
| Problem fit & practical impact | Real professional task (customs/climate law) for a non-expert; verifiable outcome: report + supplier letter + AnEH checklist; € 0 vs € 19k vs € 72–121k decision. |

(Competitor prices for questions only: SME tools from € 79/month (CbamTrack), € 145/month (CBAM Desk) — see `data/market_facts.md`.)

## Slide one-liners

- Problem: "90 % are exempt. Nobody tells them when they stop being exempt."
- Solution: "Upload your invoices. Know your tonnes. Decide before the next order."
- Proof: "Every number has a source. Every rule is a test."
- Validation quotes: _pending — interviews planned at the end._

Sources for market and law figures: `data/market_facts.md`, `data/declarant_checklist.md`.
