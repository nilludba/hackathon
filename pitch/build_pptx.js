const pptxgen = require("pptxgenjs");
const { applyTheme } = require(process.env.APPLY_THEME || "./apply_theme.js");

const THEME = { name: "CBAM-Lotse", headFontFace: "Arial", bodyFontFace: "Calibri",
  colors: { dk1: "16222F", lt1: "FBFAF6", dk2: "1F3346", lt2: "F2EFE8", accent1: "B4501E", accent2: "2C6B45",
            accent3: "4A5563", accent4: "BFCCD8", accent5: "28405A", accent6: "D9D3C7", hlink: "B4501E", folHlink: "7A3A17" } };
const HEX = THEME.colors;
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = "CBAM-Lotse — Pitch"; pres.author = "Darmen & Matvey";
const C = pres.SchemeColor;
const W = 13.333, M = 0.8, CW = W - 2 * M;

function layout(name, bg, eyebrowColor, titleColor) {
  pres.defineSlideMaster({ title: name, background: { color: bg }, objects: [
    { placeholder: { options: { name: "eyebrow", type: "body", x: M, y: 0.55, w: CW, h: 0.4, fontSize: 14, bold: true,
        charSpacing: 3, color: eyebrowColor, margin: 0, valign: "top" }, text: "" } },
    { placeholder: { options: { name: "title", type: "title", x: M, y: 0.95, w: CW, h: 1.3, fontSize: 36, bold: true,
        color: titleColor, margin: 0, valign: "top", align: "left", fontFace: "Arial" }, text: "" } },
  ]});
}
layout("LIGHT", HEX.lt2, C.accent1, C.text1);
layout("DARK", HEX.dk2, "E8956A", C.background1);
layout("ACCENT", HEX.accent1, "FBE3D3", C.background1);

const T = (s, text, o) => s.addText(text, { isTextBox: true, margin: 0, valign: "top", ...o });
function card(s, x, y, w, h, dark) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.12,
    fill: { color: dark ? C.accent5 : C.background1 }, line: { color: dark ? "3A5672" : C.accent6, width: 1 } });
}
function head(s, eyebrow, title) {
  s.addText(eyebrow.toUpperCase(), { placeholder: "eyebrow" });
  s.addText(title, { placeholder: "title" });
}

// 1 cover
pres.addSection({ title: "Problem" });
let s = pres.addSlide({ masterName: "DARK", sectionTitle: "Problem" });
T(s, "AAU HACKATHON 2026 · THE $15-AN-HOUR EXPERT", { x: M, y: 1.2, w: CW, h: 0.4, fontSize: 14, bold: true, charSpacing: 3, color: "E8956A" });
T(s, "CBAM-Lotse", { x: M, y: 1.8, w: CW, h: 1.4, fontSize: 66, bold: true, color: C.background1, fontFace: "Arial" });
T(s, "Know your tonnes before the next order. An assistant that turns a small importer’s invoices into a CBAM decision they can check.",
  { x: M, y: 3.4, w: 10.5, h: 1.4, fontSize: 22, color: C.accent4 });
T(s, "Darmen & Matvey · Universität Klagenfurt", { x: M, y: 6.4, w: CW, h: 0.4, fontSize: 14, color: C.accent4 });
s.addNotes("Hi, we are Darmen and Matvey. CBAM-Lotse helps a small metal workshop deal with the EU’s new carbon border duty without a customs lawyer.");

// helper: 3 stat cards
function cards3(s, y, h, items, dark) {
  const gap = 0.35, w = (CW - 2 * gap) / 3;
  items.forEach((it, i) => {
    const x = M + i * (w + gap);
    card(s, x, y, w, h, dark);
    let yy = y + 0.3;
    if (it.label) { T(s, it.label, { x: x + 0.3, y: yy, w: w - 0.6, h: 0.3, fontSize: 12, bold: true, charSpacing: 2, color: dark ? "E8956A" : C.accent1 }); yy += 0.4; }
    if (it.big) { T(s, it.big, { x: x + 0.3, y: yy, w: w - 0.6, h: 0.8, fontSize: 36, bold: true, fontFace: "Arial", color: it.rust ? C.accent1 : (dark ? C.background1 : C.text1) }); yy += 0.85; }
    if (it.h) { T(s, it.h, { x: x + 0.3, y: yy, w: w - 0.6, h: 0.8, fontSize: 20, bold: true, fontFace: "Arial", color: dark ? C.background1 : C.text1 }); yy += 0.95; }
    T(s, it.body, { x: x + 0.3, y: yy, w: w - 0.6, h: y + h - yy - 0.2, fontSize: 16, color: dark ? C.accent4 : C.accent3 });
  });
}

// 2 problem
s = pres.addSlide({ masterName: "LIGHT", sectionTitle: "Problem" });
head(s, "The problem", "Since 1 January 2026, steel and aluminium imports carry a CO₂ price");
cards3(s, 2.6, 2.6, [
  { big: "182,000", body: "EU importers are exempt — but only while they stay under 50 t a year." },
  { big: "50 t", body: "Cross it once and every tonne of the year counts, not just the excess." },
  { big: "€300–500", rust: true, body: "fine per tonne of CO₂ for importing above 50 t without authorisation." }]);
T(s, "Sources: European Commission, 20.10.2025 (Omnibus, Reg. (EU) 2025/2083); Art. 26(2a) Reg. (EU) 2023/956.", { x: M, y: 6.75, w: CW, h: 0.3, fontSize: 11, color: C.accent3 });
s.addNotes("Ninety percent of importers are exempt. Nobody tells them when they stop being exempt. That is the gap.");

// 3 user
pres.addSection({ title: "Tool" });
s = pres.addSlide({ masterName: "LIGHT", sectionTitle: "Tool" });
head(s, "Our user", "Herr Gruber runs a 15-person metal workshop in Klagenfurt");
cards3(s, 2.6, 3.4, [
  { label: "HIS JOB", h: "Buy steel and aluminium", body: "Beams and screws from Türkiye, aluminium profiles from China. Importing is daily work." },
  { label: "NOT HIS JOB", h: "Customs and climate law", body: "No customs lawyer, no CBAM expert. The Commission’s free tool only answers “is this code on the list?”." },
  { label: "HIS DECISION", h: "Order or wait?", body: "Will the next delivery push him over 50 t — and what does each choice cost?" }]);
s.addNotes("A real professional task that needs expertise he doesn’t have. That’s exactly the challenge brief.");

// 4 flow
s = pres.addSlide({ masterName: "DARK", sectionTitle: "Tool" });
head(s, "Live demo", "Three steps from invoices to an answer");
cards3(s, 2.4, 2.9, [
  { label: "1 · UPLOAD", h: "4 PDFs", body: "3 invoices and 1 order confirmation. The tool finds 6 lines, CN codes, net mass, origin." },
  { label: "2 · CHECK", h: "4 CBAM goods", body: "Each matched to its Annex I entry. Nails without a code: it suggests 7317 00 and asks." },
  { label: "3 · DECIDE", h: "41 of 50 t", body: "“The order from China pushes you to 53 t.” Three options with euros, letter and report." }], true);
s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: M, y: 5.75, w: CW, h: 0.3, rectRadius: 0.15, fill: { color: C.accent6 }, line: { type: "none" } });
s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: M, y: 5.75, w: CW * 0.82, h: 0.3, rectRadius: 0.15, fill: { color: C.accent1 }, line: { type: "none" }, objectName: "progress 41 of 50 t" });
T(s, "41.0 t imported in 2026 · 82 % of the 50 t threshold · planned order +12.0 t", { x: M, y: 6.25, w: CW, h: 0.4, fontSize: 14, color: C.accent4 });
s.addNotes("Switch to the app now: Demo, read demo PDFs. Point at the result card, the order warning and the decision table.");

// 5 decision
s = pres.addSlide({ masterName: "LIGHT", sectionTitle: "Tool" });
head(s, "The decision", "One order from China decides what 2026 costs");
const hdr = (t) => ({ text: t, options: { bold: true, fontSize: 12, color: C.accent3, charSpacing: 2 } });
const eur = (t, col) => ({ text: t, options: { bold: true, fontSize: 20, fontFace: "Arial", color: col } });
s.addTable([
  [hdr("OPTION"), hdr("WHAT HAPPENS IN 2026"), hdr("COST")],
  ["A · Plan delivery for January", "Stays at 41 t, still exempt", eur("€0 (exempt)", C.accent2)],
  ["B · Apply for authorisation first", "53 t, certificates for all 241 t CO₂e", eur("≈ €19,057", C.text1)],
  ["C · Ask supplier for real data", "Lower factor than the EU default", eur("less than B", C.text1)],
  ["Do nothing", "53 t without authorisation", eur("€72k–121k fine", C.accent1)],
], { x: M, y: 2.4, w: CW, colW: [4.2, 5.2, 2.333], fontSize: 16, color: C.text1, fontFace: "Calibri",
     border: { type: "solid", color: HEX.accent6, pt: 1 }, rowH: 0.75, valign: "middle", margin: [0, 0.15, 0, 0.15] });
T(s, "Computed by CBAM-Lotse on the demo invoices: EU default values incl. 2026 mark-up, certificate price of the import quarter.", { x: M, y: 6.75, w: CW, h: 0.3, fontSize: 11, color: C.accent3 });
s.addNotes("Option A means planning the delivery date, not splitting shipments to dodge the threshold. That is ruled out by anti-avoidance rules, and the app says so.");

// 6 trust (creativity)
pres.addSection({ title: "Criteria" });
s = pres.addSlide({ masterName: "ACCENT", sectionTitle: "Criteria" });
head(s, "Creativity of the solution", "The AI reads and explains. The law and the maths are tested code");
[["No invented numbers", "Annex I, threshold and cost are rules checked by over 130 automated tests, runnable from the app."],
 ["Every number has a source", "Click a value: formula, EU default value table, EUR-Lex article."],
 ["Warns before, not after", "Order confirmations count as planned imports — the warning comes before the goods arrive."]].forEach(([h, b], i) => {
  const w = (CW - 0.7) / 3, x = M + i * (w + 0.35);
  T(s, h, { x, y: 3.0, w, h: 0.6, fontSize: 22, bold: true, fontFace: "Arial", color: C.background1 });
  T(s, b, { x, y: 3.95, w, h: 1.8, fontSize: 16, color: "FBE3D3" });
});
s.addNotes("Language models make up numbers. We don’t let ours: it only extracts data from invoices and explains results.");

// 7 interaction
s = pres.addSlide({ masterName: "LIGHT", sectionTitle: "Criteria" });
head(s, "Quality of user interaction", "Built for someone who has never heard of a CN code");
[["One-sentence answer", "“Careful: 41 of 50 t.” Result first, details later."],
 ["No typing codes", "Upload PDFs. Missing code? A suggestion and one click to accept."],
 ["“What if?”", "Extra order or other country: new status and cost at once."],
 ["His language", "German, English, Russian. Plain words, no legal jargon."]].forEach(([h, b], i) => {
  const w = (CW - 0.35) / 2, x = M + (i % 2) * (w + 0.35), y = 2.4 + Math.floor(i / 2) * 2.0;
  card(s, x, y, w, 1.7, false);
  T(s, h, { x: x + 0.3, y: y + 0.3, w: w - 0.6, h: 0.5, fontSize: 20, bold: true, fontFace: "Arial", color: C.text1 });
  T(s, b, { x: x + 0.3, y: y + 0.85, w: w - 0.6, h: 0.7, fontSize: 16, color: C.accent3 });
});
s.addNotes("Show the CN suggestion, the What-if tab and the language switch if time allows.");

// 8 impact
s = pres.addSlide({ masterName: "LIGHT", sectionTitle: "Criteria" });
head(s, "Problem fit & practical impact", "A real duty, a real decision, an outcome anyone can check");
cards3(s, 2.4, 2.3, [
  { big: "~200,000", body: "EU importers of CBAM goods; 182,000 stay exempt only while they track their tonnes." },
  { big: "€0 vs €72k", body: "What one order can mean for a 15-person workshop — seen before ordering." },
  { big: "3 files", body: "Report with sources, supplier letter, AnEH application checklist." }]);
T(s, "“[Quote from interview — e.g. Metallbau, Kärnten]”", { x: M, y: 5.1, w: CW / 2 - 0.2, h: 1.0, fontSize: 20, italic: true, fontFace: "Arial", color: C.text1 });
T(s, "“[Quote from interview — e.g. freight forwarder]”", { x: M + CW / 2 + 0.2, y: 5.1, w: CW / 2 - 0.2, h: 1.0, fontSize: 20, italic: true, fontFace: "Arial", color: C.text1 });
s.addNotes("Placeholders: replace with two quotes from the validation calls, with the person’s role.");

// 9 close
s = pres.addSlide({ masterName: "DARK", sectionTitle: "Criteria" });
T(s, "CBAM-LOTSE", { x: M, y: 1.2, w: CW, h: 0.4, fontSize: 14, bold: true, charSpacing: 3, color: "E8956A" });
T(s, "Upload your invoices. Know your tonnes. Decide before the next order.", { x: M, y: 1.8, w: 11, h: 2.4, fontSize: 44, bold: true, fontFace: "Arial", color: C.background1 });
T(s, "Try it: cbam-lotse.streamlit.app", { x: M, y: 5.3, w: CW / 2, h: 0.4, fontSize: 18, color: C.accent4 });
T(s, "Code: github.com/nilludba/hackathon", { x: M + CW / 2, y: 5.3, w: CW / 2, h: 0.4, fontSize: 18, color: C.accent4 });
T(s, "First assessment, not legal advice. Competent authority in Austria: AnEH, cbam@bmf.gv.at.", { x: M, y: 6.3, w: CW, h: 0.4, fontSize: 12, color: C.accent4 });
s.addNotes("Thank you. Questions?");

(async () => {
  await pres.writeFile({ fileName: "CBAM-Lotse_Pitch.pptx" });
  await applyTheme("CBAM-Lotse_Pitch.pptx", THEME);
  console.log("ok");
})();
