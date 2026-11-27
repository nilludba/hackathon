"""Supplier letter (DE/EN) and PDF report. Pure text assembly; no figures are computed here."""

import unicodedata
from datetime import date

from fpdf import FPDF

LETTER = {
    "de": {
        "subject": "Anfrage: tatsächliche eingebettete Emissionen (CBAM, Verordnung (EU) 2023/956)",
        "greeting": "Sehr geehrte Damen und Herren,",
        "intro": ("wir importieren Ihre unten genannten Waren in die EU. Sie fallen unter das CO2-Grenzausgleichs"
                  "system (CBAM). Für unsere CBAM-Erklärung benötigen wir die tatsächlichen eingebetteten Emissionen "
                  "statt der Standardwerte der Europäischen Kommission."),
        "goods": "Betroffene Lieferungen:",
        "ask": "Bitte senden Sie uns je Ware bzw. Anlage:",
        "items": [
            "direkte und indirekte spezifische eingebettete Emissionen (t CO2e je t Ware),",
            "Produktionsweg und Name/Standort der Anlage (Anlagenkennung, falls vorhanden),",
            "den Bericht der Prüfstelle (akkreditierte Verifizierung der Emissionsdaten),",
            "gegebenenfalls im Ursprungsland gezahlte CO2-Preise.",
        ],
        "template": ("Am einfachsten ist die Kommunikationsvorlage der Europäischen Kommission für Anlagenbetreiber "
                     "(taxation-customs.ec.europa.eu, Rubrik CBAM)."),
        "deadline": "Wir bitten um Antwort bis {deadline}. Vielen Dank für Ihre Unterstützung.",
        "closing": "Mit freundlichen Grüßen",
    },
    "en": {
        "subject": "Request: actual embedded emissions (CBAM, Regulation (EU) 2023/956)",
        "greeting": "Dear Sir or Madam,",
        "intro": ("we import the goods listed below into the EU. They are covered by the Carbon Border Adjustment "
                  "Mechanism (CBAM). For our CBAM declaration we need the actual embedded emissions instead of "
                  "the European Commission's default values."),
        "goods": "Deliveries concerned:",
        "ask": "Please send us, per good and installation:",
        "items": [
            "direct and indirect specific embedded emissions (t CO2e per t of goods),",
            "production route and name/location of the installation (installation ID, if available),",
            "the verification report of an accredited verifier,",
            "any carbon price paid in the country of origin.",
        ],
        "template": ("The easiest way is the European Commission's communication template for operators "
                     "(taxation-customs.ec.europa.eu, CBAM section)."),
        "deadline": "We kindly ask for your reply by {deadline}. Thank you for your support.",
        "closing": "Kind regards",
    },
}


def supplier_letter(supplier, lines, importer, lang="de", deadline=None):
    """Letter text asking one supplier for actual emission data on its CBAM goods."""
    t = LETTER[lang]
    goods = [l for l in lines if l.get("cbam") and l.get("supplier") == supplier]
    rows = [f"- {l['description']} — KN/CN {l['cn']}, {l['net_mass_kg'] / 1000:g} t, {l['date']}"
            + (f", {l['invoice']}" if isinstance(l.get("invoice"), str) else "") for l in goods]
    return "\n".join([
        f"{t['subject']}", "", f"An/To: {supplier}", f"Von/From: {importer}", "",
        t["greeting"], "", t["intro"], "", t["goods"], *rows, "", t["ask"],
        *[f"- {i}" for i in t["items"]], "", t["template"], "",
        t["deadline"].format(deadline=deadline or "—"), "", t["closing"], importer,
    ])


def _latin1(text):
    """Core PDF fonts are Latin-1 only: map other characters (Ş, ₂, —) to the nearest ASCII."""
    text = str(text).replace("€", "EUR").replace("—", "-").replace("–", "-").replace("₂", "2")
    out = []
    for ch in text:
        try:
            ch.encode("latin-1")
            out.append(ch)
        except UnicodeEncodeError:
            out.append(unicodedata.normalize("NFKD", ch).encode("ascii", "ignore").decode() or "?")
    return "".join(out)


def report_pdf(importer, year, status, lines, cost=None, today=None):
    """PDF report: threshold status, Annex I verdict per line, cost with formula and source."""
    pdf = FPDF()
    pdf.set_auto_page_break(True, margin=15)
    pdf.add_page()
    w = pdf.epw

    def text(s, size=10, style="", h=5):
        pdf.set_font("Helvetica", style, size)
        pdf.multi_cell(w, h, _latin1(s), new_x="LMARGIN", new_y="NEXT")

    text("CBAM-Lotse - Bericht", 16, "B", 8)
    text(f"{importer} · Kalenderjahr {year} · erstellt am {(today or date.today()).isoformat()}", 9)
    pdf.ln(3)

    text("1. 50-Tonnen-Schwelle", 12, "B", 7)
    verdict = {"exempt": "unter der Schwelle - befreit",
               "near": "über 80 % der Schwelle",
               "over": "Schwelle überschritten - Zulassung als CBAM-Anmelder nötig"}[status["status"]]
    text(f"{status['total_t']:.1f} t von 50 t CBAM-Waren ({status['share']:.0%}): {verdict}.")
    if status.get("forecast_crossing"):
        text(f"Prognose beim bisherigen Tempo: Schwelle erreicht am {status['forecast_crossing']}.")
    text("Quelle: Verordnung (EU) 2025/2083 (CBAM-Omnibus), https://eur-lex.europa.eu/eli/reg/2025/2083/oj", 8)
    pdf.ln(3)

    text("2. Waren und Anhang I", 12, "B", 7)
    with pdf.table(col_widths=(40, 18, 12, 10, 12, 18), text_align="LEFT", line_height=5) as table:
        pdf.set_font("Helvetica", "", 8)
        table.row(["Ware", "KN", "t", "Land", "CBAM", "Anhang I"])
        for l in lines:
            cb = {True: "ja", False: "nein"}.get(l.get("cbam"), "unklar")
            table.row([_latin1(x) for x in (l.get("description", ""), l["cn"] if isinstance(l.get("cn"), str) else "-",
                                             f"{l['net_mass_kg'] / 1000:g}", l.get("origin", ""), cb,
                                             l.get("annex_entry") or "-")])
    text("Quelle: Anhang I der Verordnung (EU) 2023/956, https://eur-lex.europa.eu/eli/reg/2023/956/oj", 8)
    pdf.ln(3)

    if cost:
        text("3. Emissionen und Kosten (Standardwerte)", 12, "B", 7)
        lo, hi = cost["penalty_range_eur"]
        text(f"Graue Emissionen: {cost['total_emissions_t']:.1f} t CO2e · Zertifikate: EUR {cost['certificate_cost_eur']:,.0f}"
             f" · Strafe ohne Zulassung: EUR {lo:,.0f} - {hi:,.0f}")
        for r in cost["lines"]:
            text(f"- {r['description']}: {r['formula']} = EUR {r['certificate_eur']:,.0f}", 8)
        if cost["missing_default_value"]:
            text(f"{len(cost['missing_default_value'])} Zeile(n) ohne Standardwert - nicht geschätzt.", 8)
        text("Quellen: Standardwerte DVO (EU) 2025/2621 inkl. Aufschlag; Zertifikatspreis des Einfuhrquartals, "
             "Europäische Kommission; Strafe 3-5 x EUR 100 je t CO2e (Art. 26 Abs. 2a).", 8)
        pdf.ln(3)

    text("Hinweis", 10, "B", 6)
    text("Automatisch erstellte Ersteinschätzung, keine Rechtsberatung. Zuständig in Österreich: "
         "Amt für nationale Emissionshandelsangelegenheiten (AnEH), cbam@bmf.gv.at.", 8)
    return bytes(pdf.output())
