"""Extra fictional invoices for testing the site with other data than the Gruber demo.

Three importers, one per result state:
  A_befreit/  Fensterbau Moser KG, Graz       ->  4,2 t CBAM goods  (exempt  -> "Bericht herunterladen")
  B_knapp/    Stahlhandel Wieser GmbH, Villach -> 43,5 t           (near    -> "Brief erstellen")
  C_ueber/    Alu-Fassaden Berger GmbH, Linz   -> 63,0 t           (over    -> "Checkliste öffnen")
All companies, addresses and numbers are invented.
Run:  python demo/make_test_invoices.py
"""

from pathlib import Path

import make_demo_invoices as base

OUT = Path(__file__).resolve().parent / "test_invoices"
base.ORIGIN_NAME.update({"IN": "Indien (IN)"})

SUPPLIERS = {
    "IN": ("Pune Demo Metals Pvt. Ltd.", "Plot 14, MIDC Chakan, Pune 410501, Maharashtra, Indien"),
    "CN": ("Tianjin Demo Steel Pipe Co., Ltd.", "No. 5 Demo Avenue, Binhai New Area, Tianjin, China"),
    "TR": ("Ege Demo Sac Sanayi A.Ş.", "Atatürk OSB 10007 Sok. No. 3, 35620 Çiğli/İzmir, Türkei"),
    "CN_AL": ("Foshan Demo Aluminium Plate Co., Ltd.", "No. 21 Demo Road, Nanhai District, Foshan, Guangdong, China"),
}


def inv(file, number, date, sup, lines, kind="Handelsrechnung / Commercial Invoice", incoterm="DAP Österreich"):
    name, addr = SUPPLIERS[sup]
    return {"file": file, "kind": kind, "number": number, "date": date, "supplier": name,
            "supplier_address": addr, "incoterm": incoterm, "currency": "EUR", "lines": lines}


SETS = {
    "A_befreit": ("Fensterbau Moser KG, Conrad-von-Hötzendorf-Straße 88, 8010 Graz, Österreich, UID ATU00000001", [
        inv("A1_Moser_IN.pdf", "PDM/26/0091", "14.04.2026", "IN", [
            ("Fensterbeschläge aus Aluminium, eloxiert", "7616 99 10", "IN", "3.000 Stk", 2400.0, 9600.00),
            ("Holzschrauben 5x50, Stahl verzinkt", "7318 12 90", "IN", "120 Karton", 1800.0, 2160.00),
            ("Scharniere aus Messing", "8302 10 00", "IN", "800 Stk", 600.0, 3200.00),
        ]),
    ]),
    "B_knapp": ("Stahlhandel Wieser GmbH, Italiener Straße 41, 9500 Villach, Österreich, UID ATU00000002", [
        inv("B1_Wieser_CN.pdf", "TJDS-2026-0217", "09.03.2026", "CN", [
            ("Geschweißte Stahlrohre, rund, 48,3x3,2 mm, verzinkt", "7306 30 77", "CN", "6.000 m", 18000.0, 21600.00),
        ], incoterm="CIF Koper"),
        inv("B2_Wieser_IN.pdf", "PDM/26/0233", "17.06.2026", "IN", [
            ("Walzdraht 8 mm, S235, in Ringen", "7213 91 10", "IN", "7 Ringe", 14000.0, 9100.00),
            ("Kabelbinder aus Kunststoff, schwarz", None, "IN", "50 Karton", 250.0, 400.00),
        ], incoterm="CIF Triest"),
        inv("B3_Wieser_TR.pdf", "EGS-26-1102", "06.10.2026", "TR", [
            ("Bandverzinktes Feinblech 1,0 mm, Coils", "7210 49 00", "TR", "3 Coils", 11500.0, 10350.00),
        ]),
    ]),
    "C_ueber": ("Alu-Fassaden Berger GmbH, Wiener Straße 150, 4020 Linz, Österreich, UID ATU00000003", [
        inv("C1_Berger_CN.pdf", "FSAP-26-0045", "22.04.2026", "CN_AL", [
            ("Aluminiumbleche 3 mm, EN AW-5754, für Fassadenpaneele", "7606 12 99", "CN", "28 Paletten", 28000.0, 92400.00),
        ], incoterm="CIF Koper"),
        inv("C2_Berger_IN.pdf", "PDM/26/0310", "11.08.2026", "IN", [
            ("Aluminium in Rohform, nicht legiert, Masseln", "7601 10 00", "IN", "22 Bündel", 22000.0, 55000.00),
        ], incoterm="CIF Triest"),
        inv("C3_Berger_TR.pdf", "EGS-26-1290", "03.11.2026", "TR", [
            ("Unterkonstruktion Fassade, Stahlprofile geschweißt, feuerverzinkt", "7308 90 98", "TR", "40 Stk", 13000.0, 28600.00),
        ]),
    ]),
}

if __name__ == "__main__":
    regular, bold = base.font()
    for folder, (buyer, invoices) in SETS.items():
        base.OUT, base.BUYER = OUT / folder, buyer
        base.OUT.mkdir(parents=True, exist_ok=True)
        for i in invoices:
            base.make_pdf(i, regular, bold)
    print("test invoices written to", OUT)
