"""Generate the fictional demo invoices of "Metallbau Gruber GmbH" (PDF + CSV).

All companies, addresses and numbers are invented for the hackathon demo.
Run:  python demo/make_demo_invoices.py
"""

import csv
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle

OUT = Path(__file__).resolve().parent
BUYER = "Metallbau Gruber GmbH, Industriestraße 12, 9020 Klagenfurt am Wörthersee, Österreich, UID ATU00000000"

INVOICES = [
    {
        "file": "invoice_01_TR.pdf", "kind": "Handelsrechnung / Commercial Invoice",
        "number": "EXP-2026-0147", "date": "12.02.2026",
        "supplier": "Anadolu Demo Profil Çelik A.Ş.",
        "supplier_address": "Organize Sanayi Bölgesi 4. Cadde No. 7, 41400 Gebze/Kocaeli, Türkei",
        "incoterm": "DAP Klagenfurt", "currency": "EUR",
        "lines": [
            ("HEB-Träger 200, S235JR, warmgewalzt", "7216 33 10", "TR", "46 Stk", 18400.0, 13800.00),
            ("Sechskantschrauben M16x60, 8.8, feuerverzinkt", "7318 15 88", "TR", "52 Karton", 2600.0, 6240.00),
        ],
    },
    {
        "file": "invoice_02_CN.pdf", "kind": "Commercial Invoice",
        "number": "NBHX-26-0388", "date": "20.05.2026",
        "supplier": "Ningbo Demo Aluminium Co., Ltd.",
        "supplier_address": "No. 88 Demo Road, Beilun District, Ningbo, Zhejiang, China",
        "incoterm": "CIF Koper", "currency": "EUR",
        "lines": [
            ("Aluminium-Strangpressprofile EN AW-6060 T66, eloxiert", "7604 29 90", "CN", "1.240 m", 9800.0, 34300.00),
            ("Kugelhähne DN25, Messing, für Geländerentwässerung", "8481 80 85", "CN", "300 Stk", 450.0, 2850.00),
        ],
    },
    {
        "file": "invoice_03_TR.pdf", "kind": "Handelsrechnung / Commercial Invoice",
        "number": "EXP-2026-0512", "date": "08.09.2026",
        "supplier": "Anadolu Demo Profil Çelik A.Ş.",
        "supplier_address": "Organize Sanayi Bölgesi 4. Cadde No. 7, 41400 Gebze/Kocaeli, Türkei",
        "incoterm": "DAP Klagenfurt", "currency": "EUR",
        "lines": [
            ("Treppenwangen und Podestträger, geschweißt, grundiert (Stahlkonstruktionsteile)", "7308 90 59", "TR", "24 Stk", 10200.0, 21420.00),
            ("Drahtstifte 3,1x80 mm, blank", None, "TR", "40 Karton", 380.0, 610.00),
        ],
    },
    {
        "file": "order_04_CN.pdf", "kind": "Auftragsbestätigung / Order Confirmation",
        "number": "NBHX-OC-26-0611", "date": "20.11.2026",
        "supplier": "Ningbo Demo Aluminium Co., Ltd.",
        "supplier_address": "No. 88 Demo Road, Beilun District, Ningbo, Zhejiang, China",
        "incoterm": "CIF Koper, Lieferung KW 50/2026", "currency": "EUR",
        "lines": [
            ("Aluminium-Strangpressprofile EN AW-6063 T5, pulverbeschichtet RAL 7016", "7604 29 90", "CN", "1.520 m", 12000.0, 43200.00),
        ],
    },
]

ORIGIN_NAME = {"TR": "Türkei (TR)", "CN": "China (CN)"}


def de_num(x, dec=1):
    s = f"{x:,.{dec}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def font():
    path = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    if path.exists():
        pdfmetrics.registerFont(TTFont("DejaVu", str(path)))
        pdfmetrics.registerFont(TTFont("DejaVu-Bold", str(path.with_name("DejaVuSans-Bold.ttf"))))
        return "DejaVu", "DejaVu-Bold"
    return "Helvetica", "Helvetica-Bold"


def make_pdf(inv, regular, bold):
    st = ParagraphStyle("n", fontName=regular, fontSize=9, leading=12)
    hd = ParagraphStyle("h", fontName=bold, fontSize=15, leading=19)
    small = ParagraphStyle("s", fontName=regular, fontSize=7, leading=9, textColor=colors.grey)
    doc = SimpleDocTemplate(str(OUT / inv["file"]), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
                            topMargin=16 * mm, bottomMargin=16 * mm, title=f"{inv['kind']} {inv['number']}")
    story = [
        Paragraph(inv["supplier"], hd),
        Paragraph(inv["supplier_address"], st),
        Spacer(1, 8 * mm),
        Paragraph(f"<font name='{bold}'>{inv['kind']}</font>", ParagraphStyle("k", parent=st, fontSize=12, leading=15)),
        Spacer(1, 3 * mm),
        Paragraph(f"Nr. / No.: {inv['number']}", st),
        Paragraph(f"Datum / Date: {inv['date']}", st),
        Paragraph(f"Lieferant / Seller: {inv['supplier']}", st),
        Paragraph(f"Empfänger / Buyer: {BUYER}", st),
        Paragraph(f"Lieferbedingung / Incoterm: {inv['incoterm']}", st),
        Spacer(1, 6 * mm),
    ]
    head = ["Pos.", "Beschreibung / Description", "KN-Code / HS", "Ursprung / Origin", "Menge", "Netto kg", "Betrag EUR"]
    hst = ParagraphStyle("th", fontName=bold, fontSize=8, leading=10)
    rows = [[Paragraph(h, hst) for h in head]]
    for i, (desc, cn, origin, qty, kg, eur) in enumerate(inv["lines"], 1):
        rows.append([str(i), Paragraph(desc, st), cn or "", ORIGIN_NAME[origin], qty, de_num(kg), de_num(eur, 2)])
    total_kg = sum(l[4] for l in inv["lines"])
    total_eur = sum(l[5] for l in inv["lines"])
    rows.append(["", "Summe / Total", "", "", "", de_num(total_kg), de_num(total_eur, 2)])
    t = Table(rows, colWidths=[10 * mm, 58 * mm, 22 * mm, 24 * mm, 18 * mm, 20 * mm, 22 * mm], repeatRows=1)
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), regular), ("FONTNAME", (0, 0), (-1, 0), bold),
        ("FONTNAME", (0, -1), (-1, -1), bold), ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8EEF4")),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA7B4")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"), ("ALIGN", (5, 1), (-1, -1), "RIGHT"),
    ]))
    story += [t, Spacer(1, 6 * mm),
              Paragraph("Gewichte = Nettomasse in kg. Zahlungsziel 30 Tage netto.", st),
              Spacer(1, 30 * mm),
              Paragraph("Fiktive Demo-Rechnung – CBAM-Lotse, AAU Hackathon 2026. Alle Firmen und Daten sind erfunden.", small)]
    doc.build(story)


def make_csv():
    with open(OUT / "purchases_2026.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["description", "cn", "net_mass_kg", "origin", "date", "supplier", "invoice"])
        for inv in INVOICES:
            if inv["file"].startswith("order"):
                continue
            d, m, y = inv["date"].split(".")
            for desc, cn, origin, _, kg, _ in inv["lines"]:
                w.writerow([desc, cn or "", kg, origin, f"{y}-{m}-{d}", inv["supplier"], inv["number"]])


if __name__ == "__main__":
    regular, bold = font()
    for inv in INVOICES:
        make_pdf(inv, regular, bold)
    make_csv()
    print("demo files written to", OUT)
