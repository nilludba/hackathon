"""CBAM-Lotse agent: Gemini answers questions in German, but every number comes from our tools.

The LLM never decides legal questions or computes figures itself. It calls
check_cn / threshold / cost, which wrap the tested deterministic functions.
Without GEMINI_API_KEY the app still works: `answer()` falls back to a fixed summary.
"""

import json
import urllib.request

from cbam.annex import check_annex_i
from cbam.cost import estimate_cost
from cbam.threshold import threshold_status

MODEL = "gemini-2.5-flash"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
MAX_STEPS = 5

SYSTEM = (
    "Du bist CBAM-Lotse, ein Assistent für kleine österreichische Importeure von Stahl und Aluminium. "
    "Antworte auf Deutsch, kurz und klar, für Nicht-Juristen. "
    "Nenne Zahlen NUR aus Tool-Ergebnissen, nie aus dem Gedächtnis, und gib die Quelle an. "
    "Für KN-Codes rufe check_cn auf, für die 50-Tonnen-Schwelle threshold, für Kosten und Strafen cost. "
    "Wenn ein Tool etwas nicht weiß, sag das. Du gibst keine Rechtsberatung; verweise bei Zweifeln auf "
    "das Amt für nationale Emissionshandelsangelegenheiten (AnEH, cbam@bmf.gv.at)."
)

TOOLS = [{"function_declarations": [
    {"name": "check_cn",
     "description": "Prüft, ob ein KN-Code (Zolltarifnummer) unter Anhang I der CBAM-Verordnung fällt.",
     "parameters": {"type": "object", "properties": {"cn": {"type": "string"}}, "required": ["cn"]}},
    {"name": "threshold",
     "description": "Summe der CBAM-Waren im Jahr, Anteil an der 50-t-Schwelle, Status und Prognose.",
     "parameters": {"type": "object", "properties": {}}},
    {"name": "cost",
     "description": "Graue Emissionen, Kosten der CBAM-Zertifikate und Strafrahmen ohne Zulassung.",
     "parameters": {"type": "object", "properties": {}}},
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


def _post(body, api_key):
    req = urllib.request.Request(URL, data=json.dumps(body).encode(), method="POST",
                                 headers={"Content-Type": "application/json", "x-goog-api-key": api_key})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp)


def fallback_answer(ctx, reason="kein GEMINI_API_KEY gesetzt"):
    """Deterministic summary used when no API key is set or the API fails."""
    s = run_tool("threshold", {}, ctx)
    text = f"Im Jahr {ctx['year']} haben Sie {s['total_t']:.1f} t CBAM-Waren importiert ({s['share']:.0%} der 50-t-Schwelle). "
    text += {"exempt": "Sie sind derzeit befreit.",
             "near": "Sie liegen nahe an der Schwelle.",
             "over": "Die Schwelle ist überschritten — Sie brauchen die Zulassung als CBAM-Anmelder."}[s["status"]]
    return text + f" (KI-Assistent nicht verfügbar: {reason}.)"


def answer(question, ctx, api_key=None, post=_post):
    """Answer a user question with Gemini tool calling. Returns (text, list of tool calls made)."""
    if not api_key:
        return fallback_answer(ctx), []
    contents = [{"role": "user", "parts": [{"text": question}]}]
    calls = []
    for _ in range(MAX_STEPS):
        body = {"system_instruction": {"parts": [{"text": SYSTEM}]}, "contents": contents, "tools": TOOLS}
        try:
            content = post(body, api_key)["candidates"][0]["content"]
        except Exception:  # network, quota or malformed reply: the app must keep working
            return fallback_answer(ctx, "Gemini-API nicht erreichbar"), calls
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
    return fallback_answer(ctx, "zu viele Tool-Aufrufe"), calls
