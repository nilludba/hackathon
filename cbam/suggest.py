"""Suggest a CN code when an invoice line has none.

Deterministic keyword rules (German/English descriptions + material), no AI and no guessing
beyond the heading level. The user always confirms; the app shows the suggestion as a proposal
and links to the official tariff for checking.
"""

import re

from cbam.annex import check_annex_i

TARIC_URL = "https://ec.europa.eu/taxation_customs/dds2/taric/taric_consultation.jsp?Lang=de"

ALU = r"\balu\b|alumin|en aw"
STEEL = r"stahl|eisen|steel|iron|s235|s355|verzinkt|galvani|inox|edelstahl"

# (pattern on description, material: "alu" | "steel" | None, cn, German label, confidence)
RULES = [
    (r"drahtstift|nagel|nägel|\bnails?\b|reißnagel", None, "7317 00", "Nägel, Drahtstifte, Krampen aus Eisen oder Stahl", "hoch"),
    (r"schraube|bolzen|mutter|unterleg|niete?|\bscrews?\b|\bbolts?\b|\bnuts?\b|washer|rivet", "alu", "7616 10 00",
     "Schrauben, Bolzen, Muttern … aus Aluminium", "hoch"),
    (r"schraube|bolzen|mutter|unterleg|niete?|\bscrews?\b|\bbolts?\b|\bnuts?\b|washer|rivet", None, "7318",
     "Schrauben, Bolzen, Muttern … aus Eisen oder Stahl", "hoch"),
    (r"kugelh[aä]hn|ventil|absperr|\bvalves?\b|armatur", None, "8481", "Armaturen, Hähne, Ventile", "mittel"),
    (r"treppe|geländer|podest|tor\b|türen?\b|fenster|konstruktion|gerüst|structure|staircase|railing", "alu", "7610",
     "Konstruktionen und Konstruktionsteile aus Aluminium", "mittel"),
    (r"treppe|geländer|podest|tor\b|türen?\b|fenster|konstruktion|gerüst|structure|staircase|railing", None, "7308",
     "Konstruktionen und Konstruktionsteile aus Eisen oder Stahl", "mittel"),
    (r"profil|stange|stab|\bbars?\b|\brods?\b|profiles?|strangpress|extru", "alu", "7604",
     "Stangen (Stäbe) und Profile aus Aluminium", "hoch"),
    (r"\bhe[abm]\b|\bhe[abm][ -]?\d|\bipe\b|\bipe[ -]?\d|\bupn?\b|träger|winkel|t-profil|u-profil|\bbeams?\b|girder|angle", None, "7216",
     "Profile aus Eisen oder nicht legiertem Stahl (Träger, Winkel)", "mittel"),
    (r"rohr|\btubes?\b|\bpipes?\b|hohlprofil", "alu", "7608", "Rohre aus Aluminium", "mittel"),
    (r"rohr|\btubes?\b|\bpipes?\b|hohlprofil", None, "7306", "Andere Rohre und Hohlprofile aus Eisen oder Stahl", "niedrig"),
    (r"folie|\bfoil\b", "alu", "7607", "Folien und dünne Bänder aus Aluminium", "mittel"),
    (r"blech|\bsheets?\b|\bplates?\b|band\b|coil", "alu", "7606", "Bleche und Bänder aus Aluminium (> 0,2 mm)", "mittel"),
    (r"blech|\bsheets?\b|\bplates?\b|coil", None, "7208", "Flachgewalzte Erzeugnisse aus Stahl (warmgewalzt) — Breite/Behandlung prüfen", "niedrig"),
    (r"draht(?!stift)|\bwire\b", "alu", "7605", "Draht aus Aluminium", "mittel"),
    (r"draht(?!stift)|\bwire\b", None, "7217", "Draht aus Eisen oder nicht legiertem Stahl", "niedrig"),
    (r"zement|cement", None, "2523 29 00", "Portlandzement (grau) — Zementart prüfen", "niedrig"),
]


def material(description):
    d = description.lower()
    if re.search(ALU, d):
        return "alu"
    if re.search(STEEL, d):
        return "steel"
    return None


def suggest_cn(description):
    """Return up to 2 suggestions: [{cn, label, confidence, cbam, sector}] (empty if nothing fits)."""
    if not isinstance(description, str) or not description.strip():
        return []
    d, mat = description.lower(), material(description)
    out, seen = [], set()
    for pattern, needs, cn, label, conf in RULES:
        if needs == "alu" and mat != "alu":
            continue
        if needs is None and mat == "alu" and any(r[1] == "alu" and re.search(r[0], d) for r in RULES):
            continue  # an aluminium-specific rule exists for this word
        if re.search(pattern, d) and cn not in seen:
            verdict = check_annex_i(cn)
            out.append({"cn": cn, "label": label, "confidence": conf,
                        "cbam": verdict["cbam"], "sector": verdict["sector"]})
            seen.add(cn)
        if len(out) == 2:
            break
    return out
