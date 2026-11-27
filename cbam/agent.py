"""CBAM-Lotse agent: Gemini answers questions in the chosen language, but every number comes from our tools.

The LLM never decides legal questions or computes figures itself. It calls
check_cn / threshold / cost, which wrap the tested deterministic functions.
Without GEMINI_API_KEY the app still works: `answer()` falls back to a fixed summary.
"""

import json
import logging
import math
import urllib.error
import urllib.request

from cbam.annex import check_annex_i
from cbam.cost import estimate_cost
from cbam.threshold import threshold_status

# Newest first; a model Google retired or limited answers 404 and the next one is tried.
# See https://ai.google.dev/gemini-api/docs/deprecations
MODELS = ("gemini-3.8-flash", "gemini-3.6-flash", "gemini-3.5-flash-lite")
URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
MAX_STEPS = 5

SYSTEM = (
    "Du bist CBAM-Lotse, ein Assistent für kleine österreichische Importeure von Stahl und Aluminium. "
    "Antworte auf Deutsch, kurz und klar, für Nicht-Juristen. "
    "Nenne Zahlen NUR aus Tool-Ergebnissen, nie aus dem Gedächtnis, und gib die Quelle an. "
    "Für KN-Codes rufe check_cn auf, für die 50-Tonnen-Schwelle threshold, für Kosten und Strafen cost. "
    "Wenn ein Tool etwas nicht weiß, sag das. Du gibst keine Rechtsberatung; verweise bei Zweifeln auf "
    "das Amt für den nationalen Emissionszertifikatehandel (AnEH, cbam@bmf.gv.at)."
)

TOOLS = [{"function_declarations": [
    {"name": "check_cn",
     "description": "Prüft, ob ein KN-Code (Zolltarifnummer) unter Anhang I der CBAM-Verordnung fällt.",
     "parameters": {"type": "object", "properties": {"cn": {"type": "string"}}, "required": ["cn"]}},
    {"name": "threshold",
     "description": "Summe der CBAM-Waren im Jahr, Anteil an der 50-t-Schwelle, Status und Prognose."},
    {"name": "cost",
     "description": "Graue Emissionen, Kosten der CBAM-Zertifikate und Strafrahmen ohne Zulassung."},
]}]


def run_tool(name, args, ctx):
    """Execute one tool call against the current import lines. ctx: lines, year, prices, values."""
    cbam_lines = [r for r in ctx["lines"] if r.get("cbam")]
    if name == "check_cn":
        try:
            return check_annex_i(args.get("cn", ""))
        except ValueError as e:
            return {"error": str(e)}
    if name == "threshold":
        return threshold_status(cbam_lines, ctx["year"])
    if name == "cost":
        if ctx.get("values") is None or ctx.get("prices") is None:
            return {"error": "Standardwerte oder Zertifikatspreis fehlen."}
        year_lines = [r for r in cbam_lines if str(r.get("date", "")).startswith(str(ctx["year"]))]
        return estimate_cost(year_lines, ctx["prices"], ctx["values"])
    return {"error": f"Unbekanntes Tool: {name}"}


def _json_safe(x):
    """NaN/inf are not valid JSON; the API rejects them. Map them to null, other odd types to str."""
    if isinstance(x, dict):
        return {k: _json_safe(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_json_safe(v) for v in x]
    if isinstance(x, float) and not math.isfinite(x):
        return None
    return x if x is None or isinstance(x, (str, int, float, bool)) else str(x)


def _post(body, api_key):
    data = json.dumps(_json_safe(body), allow_nan=False).encode()
    for i, model in enumerate(MODELS):
        req = urllib.request.Request(URL.format(model=model), data=data, method="POST",
                                     headers={"Content-Type": "application/json", "x-goog-api-key": api_key})
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as e:
            if e.code != 404 or i == len(MODELS) - 1:
                raise


FALLBACK = {
    "Deutsch": ("Im Jahr {year} haben Sie {t:.1f} t CBAM-Waren importiert ({share:.0%} der 50-t-Schwelle). ",
                {"exempt": "Sie sind derzeit befreit.", "near": "Sie liegen nahe an der Schwelle.",
                 "over": "Die Schwelle ist überschritten — Sie brauchen die Zulassung als CBAM-Anmelder."},
                " (KI-Assistent nicht verfügbar: {r}.)",
                {"no_key": "kein GEMINI_API_KEY gesetzt", "api": "Gemini-API nicht erreichbar", "steps": "zu viele Tool-Aufrufe"}),
    "Englisch": ("In {year} you imported {t:.1f} t of CBAM goods ({share:.0%} of the 50 t threshold). ",
                 {"exempt": "You are currently exempt.", "near": "You are close to the threshold.",
                  "over": "The threshold is exceeded — you need authorisation as a CBAM declarant."},
                 " (AI assistant unavailable: {r}.)",
                 {"no_key": "no GEMINI_API_KEY set", "api": "Gemini API not reachable", "steps": "too many tool calls"}),
    "Russisch": ("В {year} году вы ввезли {t:.1f} t товаров CBAM ({share:.0%} от порога 50 t). ",
                 {"exempt": "Сейчас вы освобождены.", "near": "Вы близко к порогу.",
                  "over": "Порог превышен — нужен статус уполномоченного декларанта CBAM."},
                 " (ИИ-помощник недоступен: {r}.)",
                 {"no_key": "не задан GEMINI_API_KEY", "api": "Gemini API недоступен", "steps": "слишком много вызовов инструментов"}),
}


def fallback_answer(ctx, reason="no_key", language="Deutsch", detail=""):
    """Deterministic summary used when no API key is set or the API fails."""
    head, verdicts, tail, reasons = FALLBACK.get(language, FALLBACK["Deutsch"])
    s = run_tool("threshold", {}, ctx)
    return (head.format(year=ctx["year"], t=s["total_t"], share=s["share"]) + verdicts[s["status"]]
            + tail.format(r=reasons[reason] + (f" — {detail}" if detail else "")))


def answer(question, ctx, api_key=None, post=_post, language="Deutsch"):
    """Answer a user question with Gemini tool calling. Returns (text, list of tool calls made)."""
    if not api_key:
        return fallback_answer(ctx, "no_key", language), []
    contents = [{"role": "user", "parts": [{"text": question}]}]
    calls = []
    for _ in range(MAX_STEPS):
        body = {"system_instruction": {"parts": [{"text": SYSTEM.replace("Antworte auf Deutsch", f"Antworte auf {language}")}]}, "contents": contents, "tools": TOOLS}
        try:
            content = post(body, api_key)["candidates"][0]["content"]
        except urllib.error.HTTPError as e:  # bad key, quota, bad request: show the code, log Google's message
            logging.warning("Gemini HTTP %s: %s", e.code, e.read()[:1000].decode("utf-8", "replace"))
            return fallback_answer(ctx, "api", language, f"HTTP {e.code}"), calls
        except Exception as e:  # network or malformed reply: the app must keep working
            logging.warning("Gemini call failed: %r", e)
            return fallback_answer(ctx, "api", language, type(e).__name__), calls
        parts = content.get("parts", [])
        fcalls = [p["functionCall"] for p in parts if "functionCall" in p]
        if not fcalls:
            return "".join(p.get("text", "") for p in parts).strip(), calls
        contents.append(content)  # keep the model turn verbatim (Gemini 2.5 needs its thought signatures)
        responses = []
        for fc in fcalls:
            result = run_tool(fc["name"], fc.get("args", {}), ctx)
            calls.append({"name": fc["name"], "args": fc.get("args", {}), "result": result})
            responses.append({"functionResponse": {"name": fc["name"], "response": {"result": result}}})
        contents.append({"role": "user", "parts": responses})
    return fallback_answer(ctx, "steps", language), calls
