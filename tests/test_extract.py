from pathlib import Path

import pytest

from cbam.annex import check_annex_i
from cbam.extract import (ExtractionError, extract_lines, normalize_cn_text, normalize_origin,
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
    ("Indien", "IN"), ("Atlantis", None),
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


def test_unsupported_type(tmp_path):
    f = tmp_path / "x.docx"
    f.write_text("x")
    with pytest.raises(ExtractionError):
        extract_lines(f)
