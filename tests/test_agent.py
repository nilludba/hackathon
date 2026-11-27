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


def test_fallback_in_russian():
    text, _ = answer("?", CTX, language="Russisch")
    assert "45.0 t" in text and "близко к порогу" in text


def test_tool_schemas_have_no_empty_parameters():
    from cbam.agent import TOOLS
    for f in TOOLS[0]["function_declarations"]:
        assert "parameters" not in f or f["parameters"]["properties"]  # Gemini rejects empty OBJECT schemas


def test_request_body_is_valid_json_without_nan():
    import json
    from cbam.agent import _json_safe
    body = _json_safe({"a": float("nan"), "b": [1.5, float("inf")], "c": None})
    assert json.dumps(body, allow_nan=False) == '{"a": null, "b": [1.5, null], "c": null}'


def test_post_falls_back_to_next_model_on_404(monkeypatch):
    import io, urllib.error
    import cbam.agent as agent
    tried = []

    def fake_urlopen(req, timeout):
        tried.append(req.full_url)
        if len(tried) == 1:
            raise urllib.error.HTTPError(req.full_url, 404, "not found", {}, io.BytesIO(b"{}"))
        return io.BytesIO(b'{"ok": 1}')

    monkeypatch.setattr(agent.urllib.request, "urlopen", fake_urlopen)
    assert agent._post({"a": 1}, "k") == {"ok": 1}
    assert agent.MODELS[0] in tried[0] and agent.MODELS[1] in tried[1]


def test_post_falls_back_on_overload_but_not_on_bad_key(monkeypatch):
    import io, urllib.error
    import pytest
    import cbam.agent as agent
    codes = iter([503, 403])

    def fake_urlopen(req, timeout):
        raise urllib.error.HTTPError(req.full_url, next(codes), "x", {}, io.BytesIO(b"{}"))

    monkeypatch.setattr(agent.urllib.request, "urlopen", fake_urlopen)
    with pytest.raises(urllib.error.HTTPError) as e:
        agent._post({}, "k")
    assert e.value.code == 403  # 503 moved on to the next model, 403 (bad key) stops at once


def test_threshold_tool_forecast_is_never_in_the_past():
    from datetime import date
    ctx = {**CTX, "year": date.today().year,
           "lines": [{"cbam": True, "sector": "iron_steel", "cn": "7318", "origin": "TR", "net_mass_kg": 45_000,
                      "date": f"{date.today().year}-01-15"}]}
    f = run_tool("threshold", {}, ctx)["forecast_crossing"]
    assert f is None or f >= date.today().isoformat()
