"""CBAM covers goods originating in third countries - not EU origin, not Annex III (Art. 2, Annex III Reg. 2023/956)."""

import pytest

from cbam.annex import origin_exemption
from cbam.extract import extract_pdf, normalize_origin
from pathlib import Path

FIX = Path(__file__).resolve().parent / "fixtures"


@pytest.mark.parametrize("origin,reason", [("DE", "eu"), ("AT", "eu"), ("GR", "eu"), ("EL", "eu"), ("EU", "eu"), ("MC", "eu"),
                                           ("CH", "annex_iii"), ("NO", "annex_iii"), ("IS", "annex_iii"), ("LI", "annex_iii"),
                                           ("XB", "annex_iii"), ("XH", "annex_iii"), ("XV", "annex_iii"), ("XC", "annex_iii"),
                                           ("XL", "annex_iii"), ("CN", None), ("TR", None), ("GB", None), ("UA", None), (None, None)])
def test_origin_exemption(origin, reason):
    got = origin_exemption(origin)
    assert (got["reason"] if got else None) == reason


@pytest.mark.parametrize("text,iso", [("Deutschland", "DE"), ("Made in EU", "EU"), ("Livigno, Italien", "XV"),
                                      ("Ceuta (Spanien)", "XC"), ("Büsingen am Hochrhein", "XB"), ("Helgoland", "XH"),
                                      ("Schweiz", "CH"), ("UK", "GB"), ("Österreich", "AT")])
def test_country_and_territory_names(text, iso):
    assert normalize_origin(text) == iso


def test_swiss_trader_invoice_only_chinese_steel_is_cbam():
    # supplier in Switzerland; what counts is the origin of each line
    lines = extract_pdf(FIX / "invoice_swiss_trader_mixed_origins.pdf")
    origins = [l["origin"] for l in lines]
    assert origins == ["DE", "CH", "XV", "CN"]
    assert [origin_exemption(o) is None for o in origins] == [False, False, False, True]
