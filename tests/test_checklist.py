"""The English checklist must stay in step with the German original."""

import re
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"


def shape(name):
    text = (DATA / name).read_text(encoding="utf-8")
    return (re.findall(r"^## (\d+)\.", text, re.M), text.count("- [ ]"), sorted(re.findall(r"https?://\S+", text)),
            sorted(re.findall(r"\b(?:Y\d{3}|\d{1,2}\.\d{1,2}\.20\d\d)\b", text)))


def test_english_checklist_matches_german():
    de, en = shape("declarant_checklist.md"), shape("declarant_checklist_en.md")
    assert de[0] == en[0] == ["1", "2", "3", "4", "5"]  # numbered sections
    assert de[1] == en[1]  # same number of checkbox items
    assert de[2] == en[2]  # same sources
    assert de[3] == en[3]  # same TARIC codes and dates
