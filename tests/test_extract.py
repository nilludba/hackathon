from pathlib import Path

import pytest

from cbam.annex import check_annex_i
from cbam.extract import (ExtractionError, extract_lines, extract_pdf, normalize_cn_text, normalize_origin,
                          parse_number)

DEMO = Path(__file__).resolve().parent.parent / "demo"


@pytest.mark.parametrize("s, v", [
    ("10.200,0", 10200.0), ("380,0", 380.0), ("1,234.5", 1234.5), ("18,400", 18400.0),
    ("2.600", 2600.0), ("1.5", 1.5), ("12 000 kg", 12000.0), ("", None),
])
def test_parse_number(s, v):
    assert parse_number(s) == v


@pytest.mark.parametrize("s, iso", [
    ("Türkei (TR)", "TR"), ("Turkey", "TR"), ("cn", "CN"), ("Volksrepublik China", "CN"),
    ("Indien", "IN"), ("Atlantis", None), ("Ukraine", "UA"), ("Made in UK", "GB"),
    ("Indiana, USA", "US"), ("Atlantis", None), ("Russland", "RU"), ("Aserbaidschan", "AZ"),
])
def test_normalize_origin(s, iso):
    assert normalize_origin(s) == iso


def test_normalize_cn_text():
    assert normalize_cn_text("73181588") == "7318 15 88"
    assert normalize_cn_text("7604.29.90") == "7604 29 90"
    assert normalize_cn_text("") is None


def test_invoice_01():
    lines = extract_lines(DEMO / "invoice_01_TR.pdf")
    assert [l["cn"] for l in lines] == ["7216 33 10", "7318 15 88"]
    assert [l["net_mass_kg"] for l in lines] == [18400.0, 2600.0]
    assert {l["origin"] for l in lines} == {"TR"}
    assert lines[0]["date"] == "2026-02-12"
    assert lines[0]["supplier"].startswith("Anadolu Demo")
    assert lines[0]["doc_type"] == "invoice"
    assert lines[0]["invoice"] == "EXP-2026-0147"          # number, not the file path
    assert lines[0]["file"] == "invoice_01_TR.pdf"


def test_uploaded_file_object():
    with open(DEMO / "invoice_02_CN.pdf", "rb") as f:
        lines = extract_lines(f, name="upload.pdf")
    assert lines[0]["invoice"] == "NBHX-26-0388" and lines[0]["file"] == "upload.pdf"
    with open(DEMO / "purchases_2026.csv", "rb") as f:
        assert len(extract_lines(f, name="p.csv")) == 6


def test_missing_code_stays_none():
    lines = extract_lines(DEMO / "invoice_03_TR.pdf")
    assert lines[1]["cn"] is None
    assert lines[1]["description"].startswith("Drahtstifte")
    assert "Stahlkonstruktionsteile" in lines[0]["description"]   # multi-line cell joined


def test_order_confirmation_is_marked_planned():
    lines = extract_lines(DEMO / "order_04_CN.pdf")
    assert lines[0]["doc_type"] == "order" and lines[0]["net_mass_kg"] == 12000.0


def test_demo_story_41_tonnes():
    lines = []
    for f in ["invoice_01_TR.pdf", "invoice_02_CN.pdf", "invoice_03_TR.pdf"]:
        lines += extract_lines(DEMO / f)
    assert len(lines) == 6
    cbam = [l for l in lines if l["cn"] and check_annex_i(l["cn"])["cbam"]]
    assert len(cbam) == 4
    assert sum(l["net_mass_kg"] for l in cbam) / 1000 == pytest.approx(41.0)


def test_csv_matches_pdfs():
    csv_lines = extract_lines(DEMO / "purchases_2026.csv")
    assert len(csv_lines) == 6
    assert sum(l["net_mass_kg"] for l in csv_lines) == pytest.approx(41830.0)
    assert csv_lines[5]["cn"] is None
    assert csv_lines[0]["invoice"] == "EXP-2026-0147"


def test_unsupported_type(tmp_path):
    f = tmp_path / "x.docx"
    f.write_text("x")
    with pytest.raises(ExtractionError):
        extract_lines(f)


def test_read_documents_splits_orders_and_collects_errors(tmp_path):
    bad = tmp_path / "scan.pdf"
    bad.write_bytes(b"not a pdf")
    files = [(DEMO / f, f) for f in ["invoice_01_TR.pdf", "invoice_02_CN.pdf", "invoice_03_TR.pdf", "order_04_CN.pdf"]]
    from cbam.extract import read_documents
    imported, planned, errors = read_documents(files + [(DEMO / "missing.docx", "x.docx"), (bad, "scan.pdf")])
    assert len(imported) == 6 and len(planned) == 1
    assert planned[0]["net_mass_kg"] == 12000.0
    assert len(errors) == 2


def test_parse_number_rejects_non_numbers():
    from cbam.extract import parse_number
    assert parse_number("-") is None and parse_number("--") is None


def test_header_ignores_uid_supplier_no_and_delivery_date():
    from cbam.extract import _header_fields
    text = ("ACME GmbH\nUID-Nr.: ATU123\nLieferanten-Nr.: 4711\nLieferdatum: 30.01.2026\n"
            "Rechnungsnummer: R-77\nDatum: 01.02.2026\nLieferant: Çelik A.Ş.\n")
    date, number, supplier, _ = _header_fields(text)
    assert (date, number, supplier) == ("2026-02-01", "R-77", "Çelik A.Ş.")


FIX = Path(__file__).resolve().parent / "fixtures"


def test_invoice_without_ruling_lines_english():
    lines = extract_lines(FIX / "invoice_no_grid_en.pdf")
    assert [(l["cn"], l["net_mass_kg"], l["origin"]) for l in lines] == [
        ("7208 39 00", 24500.0, "IN"), ("7606 12", 3200.5, "CN"), ("9401 30", 300.0, "CN")]
    assert lines[0]["invoice"] == "INV-77812" and lines[0]["date"] == "2026-03-05"
    assert lines[0]["supplier"] == "Demo Steel Exports Pvt Ltd"


def test_invoice_without_ruling_lines_single_row_weight_column():
    lines = extract_lines(FIX / "invoice_no_grid_de_one_line.pdf")
    assert len(lines) == 1 and lines[0]["net_mass_kg"] == 1200.0 and lines[0]["cn"] is None


# Layouts seen in real invoices: weight only in "Menge"/"Quantity" with a unit, no table at all,
# country names outside the old list, origin only in the document header.
def test_weight_in_quantity_column_and_origin_azerbaijan():
    (l,) = extract_pdf(FIX / "invoice_quantity_kg_azerbaijan.pdf")
    assert (l["cn"], l["net_mass_kg"], l["origin"], l["invoice"]) == ("7208 39 00", 60000.0, "AZ", "KME-2026-184")
    assert l["supplier"] == "Kaspia Metall Export MMC"


def test_quantity_in_tonnes_and_goods_description_beats_item_column():
    lines = extract_pdf(FIX / "invoice_quantity_tonnes.pdf")
    assert lines[0]["description"].startswith("Aluminium plates") and lines[0]["net_mass_kg"] == 12500.0
    assert lines[0]["origin"] == "VN" and lines[1]["net_mass_kg"] is None  # "40 pcs" is not a mass


def test_invoice_without_any_table_is_read_line_by_line():
    lines = extract_pdf(FIX / "invoice_text_only_en.pdf")
    assert [(l["cn"], l["net_mass_kg"], l["origin"]) for l in lines] == [
        ("7208 51 20", 24500.0, "UA"), ("7213 91 10", 8200.0, "UA")]


@pytest.mark.parametrize("cell,kg", [("60.000 kg", 60000.0), ("12,5 t", 12500.0), ("8,200 kg", 8200.0),
                                     ("46 Stk", None), ("1.5 to", 1500.0)])
def test_parse_mass_units(cell, kg):
    from cbam.extract import parse_mass
    assert parse_mass(cell) == kg
