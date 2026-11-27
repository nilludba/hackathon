from datetime import date

from cbam.documents import _latin1, report_pdf, supplier_letter

LINES = [
    {"description": "Schrauben", "cn": "7318 15 88", "net_mass_kg": 2600, "origin": "TR", "date": "2026-02-12",
     "supplier": "Anadolu Çelik A.Ş.", "invoice": "EXP-1", "cbam": True, "annex_entry": "7318"},
    {"description": "Kugelhähne", "cn": "8481 80 85", "net_mass_kg": 450, "origin": "CN", "date": "2026-05-20",
     "supplier": "Anadolu Çelik A.Ş.", "cbam": False, "annex_entry": None},
    {"description": "Drahtstifte", "cn": None, "net_mass_kg": 380, "origin": "TR", "date": "2026-09-08",
     "supplier": "X", "cbam": None, "annex_entry": None},
]
STATUS = {"status": "near", "total_t": 41.0, "share": 0.82, "forecast_crossing": "2026-12-01"}
COST = {"lines": [{"description": "Schrauben", "formula": "2.6 t x 5.973 tCO2e/t x EUR 75.36", "certificate_eur": 1170.3}],
        "missing_default_value": [], "total_emissions_t": 15.5, "certificate_cost_eur": 1170.3,
        "penalty_range_eur": (4650.0, 7750.0)}


def test_letter_lists_only_cbam_goods_of_that_supplier():
    text = supplier_letter("Anadolu Çelik A.Ş.", LINES, "Metallbau Gruber GmbH", "de", "15.01.2027")
    assert "7318 15 88" in text and "2.6 t" in text and "EXP-1" in text
    assert "8481" not in text and "15.01.2027" in text and "Sehr geehrte" in text


def test_letter_english():
    assert "Dear Sir or Madam" in supplier_letter("Anadolu Çelik A.Ş.", LINES, "Gruber", "en")


def test_report_is_pdf_with_non_latin_names():
    pdf = report_pdf("Metallbau Gruber GmbH", 2026, STATUS, LINES, COST, today=date(2026, 11, 28))
    assert pdf.startswith(b"%PDF") and len(pdf) > 1000


def test_latin1_mapping():
    assert _latin1("Çelik A.Ş. — CO₂ €") == "Çelik A.S. - CO2 EUR"
