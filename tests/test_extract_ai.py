import json

from cbam.agent import extract_document


def fake_post(reply):
    def post(body, api_key):
        assert body["contents"][0]["parts"][0]["inline_data"]["mime_type"] == "application/pdf"
        return {"candidates": [{"content": {"parts": [{"text": json.dumps(reply)}]}}]}
    return post


def test_ai_reading_is_normalised_to_the_parser_schema():
    reply = {"doc_type": "invoice", "invoice": "X-1", "date": "2026-03-04", "supplier": "Demo Ltd",
             "lines": [{"description": "Steel coils", "cn": "72083900", "net_mass_kg": 24500, "origin": "ua"},
                       {"description": "Bolts", "cn": None, "net_mass_kg": "1,2 t", "origin": "China"},
                       {"description": "", "cn": "7318", "net_mass_kg": 1}]}
    lines = extract_document(b"%PDF-", "scan.pdf", "key", post=fake_post(reply))
    assert [(l["cn"], l["net_mass_kg"], l["origin"]) for l in lines] == [("7208 39 00", 24500.0, "UA"),
                                                                          (None, 1200.0, "CN")]
    assert lines[0]["invoice"] == "X-1" and lines[0]["date"] == "2026-03-04" and lines[0]["read_by"] == "ai"


def test_ai_order_confirmation_and_german_date():
    reply = {"doc_type": "order", "date": "20.11.2026", "lines": [{"description": "Profile", "net_mass_kg": 500}]}
    (l,) = extract_document(b"%PDF-", "oc.pdf", "key", post=fake_post(reply))
    assert l["doc_type"] == "order" and l["date"] == "2026-11-20" and l["invoice"] == "oc.pdf"
