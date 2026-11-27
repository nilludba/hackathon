import json
from pathlib import Path

import pytest

import cbam.annex
from cbam.agent import answer, run_tool

ENTRIES = json.loads((Path(__file__).parent / "fixtures" / "annex_sample.json").read_text(encoding="utf-8"))
VALUES = [{"country_iso": "TR", "cn": "7318", "total_tco2_per_t": 2.5, "source": "test"}]
CTX = {
    "year": 2026, "prices": 80.0, "values": VALUES,
    "lines": [
        {"cbam": True, "sector": "iron_steel", "cn": "7318 15 88", "origin": "TR", "net_mass_kg": 45_000, "date": "2026-03-01"},
        {"cbam": False, "sector": None, "cn": "8481 80 85", "origin": "CN", "net_mass_kg": 9_000, "date": "2026-04-01"},
    ],
}


@pytest.fixture(autouse=True)
def fixture_annex(monkeypatch):
    monkeypatch.setattr(cbam.annex, "load_annex", lambda path=None: ENTRIES)


def test_no_key_gives_deterministic_answer():
    text, calls = answer("Betrifft mich CBAM?", CTX)
    assert "45.0 t" in text and "nahe an der Schwelle" in text and calls == []


def test_tools_use_deterministic_logic():
    assert run_tool("check_cn", {"cn": "7604 29 10"}, CTX)["cbam"] is True
    assert run_tool("threshold", {}, CTX)["total_t"] == 45.0
    assert run_tool("cost", {}, CTX)["total_emissions_t"] == pytest.approx(112.5)
    assert "error" in run_tool("check_cn", {"cn": "x"}, CTX)


def test_tool_calling_loop():
    replies = iter([
        {"candidates": [{"content": {"role": "model", "parts": [{"functionCall": {"name": "threshold", "args": {}}}]}}]},
        {"candidates": [{"content": {"role": "model", "parts": [{"text": "Sie haben 45 t importiert."}]}}]},
    ])
    sent = []

    def fake_post(body, key):
        sent.append(body)
        return next(replies)

    text, calls = answer("Wie viel?", CTX, api_key="test", post=fake_post)
    assert text == "Sie haben 45 t importiert."
    assert calls[0]["name"] == "threshold" and calls[0]["result"]["total_t"] == 45.0
    # second request carries the model's call and our function response
    assert sent[1]["contents"][-1]["parts"][0]["functionResponse"]["name"] == "threshold"


def test_api_error_falls_back():
    def broken(body, key):
        raise OSError("quota")
    text, _ = answer("?", CTX, api_key="test", post=broken)
    assert "45.0 t" in text and "nicht erreichbar" in text
