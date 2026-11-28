"""Invoice PDF / purchase CSV -> invoice lines.

Each line is a dict:
    {"description", "cn", "net_mass_kg", "origin", "date", "supplier", "invoice", "doc_type", "file"}
`invoice` is the invoice number (falls back to the file name if none is printed).
`cn` is None when the document carries no code (the agent then proposes one and the
user confirms). `origin` is ISO-2. `doc_type` is "invoice" or "order" (an order
confirmation is a planned import and must not be counted as already imported).

Text-based PDFs are read with pdfplumber tables. Scanned PDFs yield no lines and
`extract_lines` raises ExtractionError so the agent can fall back to a vision model.
"""

import csv
import re
from datetime import datetime
from pathlib import Path

import pdfplumber


class ExtractionError(ValueError):
    pass


COUNTRIES = {
    "TR": ["türkei", "turkei", "türkiye", "turkiye", "turkey"],
    "CN": ["china", "volksrepublik china", "prc", "people s republic of china"],
    "IN": ["indien", "india"],
    "RS": ["serbien", "serbia"],
    "UA": ["ukraine"],
    "BA": ["bosnien", "bosnien und herzegowina", "bosnia", "bosnia and herzegovina"],
    "KR": ["südkorea", "suedkorea", "republik korea", "korea", "south korea", "republic of korea"],
    "VN": ["vietnam", "viet nam"],
    "US": ["usa", "vereinigte staaten", "united states", "united states of america"],
    "GB": ["vereinigtes königreich", "united kingdom", "großbritannien", "grossbritannien", "england", "uk"],
    "AZ": ["aserbaidschan", "azerbaijan"],
    "KZ": ["kasachstan", "kazakhstan"],
    "GE": ["georgien", "georgia"],
    "AM": ["armenien", "armenia"],
    "UZ": ["usbekistan", "uzbekistan"],
    "RU": ["russland", "russische föderation", "russia", "russian federation"],
    "BY": ["belarus", "weißrussland", "weissrussland"],
    "MD": ["moldau", "moldawien", "moldova"],
    "MK": ["nordmazedonien", "mazedonien", "north macedonia", "macedonia"],
    "AL": ["albanien", "albania"],
    "ME": ["montenegro"],
    "XK": ["kosovo"],
    "CH": ["schweiz", "switzerland"],
    "NO": ["norwegen", "norway"],
    "IS": ["island", "iceland"],
    "LI": ["liechtenstein"],
    "EG": ["ägypten", "aegypten", "egypt"],
    "MA": ["marokko", "morocco"],
    "DZ": ["algerien", "algeria"],
    "TN": ["tunesien", "tunisia"],
    "ZA": ["südafrika", "suedafrika", "south africa"],
    "MZ": ["mosambik", "mozambique"],
    "NG": ["nigeria"],
    "AE": ["vereinigte arabische emirate", "united arab emirates", "vae", "uae"],
    "SA": ["saudi arabien", "saudi-arabien", "saudi arabia"],
    "QA": ["katar", "qatar"],
    "BH": ["bahrain"],
    "OM": ["oman"],
    "IR": ["iran"],
    "IL": ["israel"],
    "JO": ["jordanien", "jordan"],
    "PK": ["pakistan"],
    "BD": ["bangladesch", "bangladesh"],
    "TH": ["thailand"],
    "MY": ["malaysia"],
    "ID": ["indonesien", "indonesia"],
    "PH": ["philippinen", "philippines"],
    "TW": ["taiwan"],
    "JP": ["japan"],
    "HK": ["hongkong", "hong kong"],
    "SG": ["singapur", "singapore"],
    "AU": ["australien", "australia"],
    "NZ": ["neuseeland", "new zealand"],
    "CA": ["kanada", "canada"],
    "MX": ["mexiko", "mexico"],
    "BR": ["brasilien", "brazil"],
    "AR": ["argentinien", "argentina"],
    "CL": ["chile"],
    "PE": ["peru"],
    "CO": ["kolumbien", "colombia"],
    "VE": ["venezuela"],
}

# header keyword -> field
HEADER_KEYS = [
    ("description", ["beschreibung", "warenbeschreibung", "description", "goods", "warenbezeichnung", "artikel",
                     "bezeichnung", "produkt", "product", "item", "ware", "leistung"]),
    ("cn", ["kn-code", "kn code", "kn", "hs", "hs-code", "hs code", "cn code", "cn-code", "cn", "zolltarif", "taric",
            "warennummer", "tarifnummer", "statistische warennummer", "commodity code", "customs code"]),
    ("origin", ["ursprung", "origin", "herkunft", "ursprungsland", "country of origin", "coo", "land"]),
    ("net_mass_kg", ["netto kg", "nettogewicht", "net weight", "netto", "net kg", "net mass", "nettomasse", "eigenmasse",
                     "gewicht", "weight", "masse", "kg", "tonnage"]),
    ("qty", ["menge", "quantity", "qty", "anzahl", "liefermenge", "amount"]),
]

# Fallback for invoices whose table has no ruling lines: columns from text positions
TEXT_TABLES = [
    {"vertical_strategy": "text", "horizontal_strategy": "text", "snap_tolerance": 4, "join_tolerance": 4,
     "intersection_tolerance": 4, "text_x_tolerance": 2},
    {"vertical_strategy": "text", "horizontal_strategy": "text", "snap_tolerance": 4, "join_tolerance": 4,
     "intersection_tolerance": 4, "text_x_tolerance": 2, "min_words_vertical": 2, "min_words_horizontal": 1},
]


def parse_number(s):
    """'10.200,0' -> 10200.0 ; '10,200.5' -> 10200.5 ; '380' -> 380.0 ; '' -> None."""
    s = re.sub(r"[^\d,.\-]", "", str(s or ""))
    if not s:
        return None
    if "," in s and "." in s:
        if s.rfind(",") > s.rfind("."):          # German: 1.234,5
            s = s.replace(".", "").replace(",", ".")
        else:                                     # English: 1,234.5
            s = s.replace(",", "")
    elif "," in s:
        head, _, tail = s.rpartition(",")
        s = s.replace(",", "") if len(tail) == 3 and head else s.replace(",", ".")
    elif s.count(".") > 1 or (s.count(".") == 1 and len(s.split(".")[1]) == 3 and s.split(".")[0]):
        s = s.replace(".", "")                    # 1.234 / 1.234.567 as thousands separators
    try:
        return float(s)
    except ValueError:                            # "-", "1.2.3" etc.: no usable number
        return None


UNIT_RE = re.compile(r"(\d[\d.,\s]*\d|\d)\s*(kg|kgs|kilogramm|kilogram|t|to|tonnen|tonne|tons|mt|lbs|lb|pounds?)\b", re.I)
LB_KG = 0.45359237


def _unit_factor(unit):
    u = unit.lower()
    return 1.0 if u.startswith("k") else LB_KG if u.startswith(("lb", "pound")) else 1000.0


def parse_mass(cell, weight_column=False, column_factor=1.0):
    """Mass in kg from a cell: '60.000 kg' -> 60000, '12,5 t' -> 12500, '50 lbs' -> 22.7.
    A plain number counts only in a weight column (unit from its header, kg if none);
    '46 Stk' never counts."""
    m = UNIT_RE.search(str(cell or ""))
    if m:
        v = parse_number(m.group(1).replace(" ", ""))
        if v is not None:
            return round(v * _unit_factor(m.group(2)), 3)
    if weight_column and not re.search(r"[a-zA-Z]{2,}", str(cell or "").replace("kg", "")):
        v = parse_number(cell)
        return None if v is None else round(v * column_factor, 3)
    return None


def normalize_origin(s):
    s = (s or "").strip()
    m = re.search(r"\(([A-Z]{2})\)", s)
    if m:
        return m.group(1)
    if re.fullmatch(r"[A-Za-z]{2}", s):  # a cell holding only the code: "TR", "cn"
        return s.upper()
    words = " " + re.sub(r"[^\wäöüß]+", " ", s.lower()).strip() + " "
    for iso, names in COUNTRIES.items():
        if any(f" {re.sub(r'[^\wäöüß]+', ' ', n)} " in words for n in names):
            return iso
    return None


def normalize_cn_text(s):
    digits = re.sub(r"\D", "", str(s or ""))
    if len(digits) < 4:
        return None
    groups = [digits[:4]] + [digits[i:i + 2] for i in range(4, min(len(digits), 10), 2)]
    return " ".join(groups)


def parse_date(s):
    for fmt in ("%d.%m.%Y", "%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(s.strip(), fmt).date().isoformat()
        except ValueError:
            pass
    return None


def _header_fields(text):
    date = number = supplier = None
    # (?<![\w-]) and \b keep "Lieferdatum", "UID-Nr.", "Lieferanten-Nr." from matching
    m = re.search(r"(?<![\w-])(?:Rechnungsdatum|Invoice date|Datum|Date)\b[^:\n]*:\s*([\d./-]{8,10})", text, re.I)
    if m:
        date = parse_date(m.group(1))
    m = (re.search(r"(?:Rechnungsnummer|Rechnungs-Nr\.?|Invoice No\.?)\s*[:#]\s*(\S+)", text, re.I)
         or re.search(r"(?<![\w-])(?:Nr\.|No\.)(?:\s*/\s*(?:Nr\.|No\.))?\s*:\s*(\S+)", text, re.I))
    if m:
        number = m.group(1)
    m = re.search(r"(?<![\w-])(?:Lieferant|Seller|Supplier|Verkäufer)\b[^:\n]*:\s*(.+)", text, re.I)
    supplier = m.group(1).strip() if m else (text.strip().splitlines() or [None])[0]
    if supplier:  # first line often also holds the document title: "Kaspia Metall MMC RECHNUNG"
        supplier = re.sub(r"\s+(HANDELSRECHNUNG|RECHNUNG|COMMERCIAL INVOICE|INVOICE|PROFORMA.*|AUFTRAGSBESTÄTIGUNG)\s*$",
                          "", supplier, flags=re.I).strip() or supplier
    doc_type = "order" if re.search(r"Auftragsbestätigung|Order Confirmation|Proforma", text, re.I) else "invoice"
    return date, number, supplier, doc_type


def _doc_origin(text):
    """'Ursprungsland Aserbaidschan', 'Country of origin: China', 'Warenursprung: TR' -> ISO-2."""
    m = re.search(r"\bof\s+((?:[A-Z][\w'-]*\s){0,3}[A-Z][\w'-]*)\s+origin\b", text)  # "... of United States origin"
    if m and normalize_origin(m.group(1)):
        return normalize_origin(m.group(1))
    for m in re.finditer(r"(?:Ursprungsland|Warenursprung|Ursprung|Country of origin|Origin)\s*[:]?\s*([^\n,;.]{2,40})", text, re.I):
        words = m.group(1).split()
        # "Origin: TR ..." -> first word if it is a capital ISO code; never "... origin to be displayed"
        iso = None if re.fullmatch(r"[a-z]{2}", m.group(1).strip()) else normalize_origin(m.group(1))
        if not iso and words and re.fullmatch(r"[A-Z]{2}", words[0]):
            iso = words[0]
        if iso:
            return iso
    return None


def _doc_mass(text):
    m = re.search(r"(?:Nettogewicht|Net weight|Nettomasse|Gesamtgewicht netto)\s*[:]?\s*([\d.,\s]+\s*(?:kg|t)\b)", text, re.I)
    return parse_mass(m.group(1)) if m else None


def _map_header(row):
    cells = [re.sub(r"\s+", " ", (c or "").replace("\n", " ")).strip().lower() for c in row]
    mapping = {}
    for field, keys in HEADER_KEYS:  # keys in priority order: "Goods description" beats "Item"
        for k in keys:
            hit = next((i for i, c in enumerate(cells) if i not in mapping.values()
                        and (c.startswith(k) or f" {k}" in f" {c}" or (len(k) > 5 and k in c))), None)
            if hit is not None:
                mapping[field] = hit
                break
    return mapping if "description" in mapping and ({"net_mass_kg", "qty"} & mapping.keys()) else None


def _header_unit_factor(cell):
    """'Weight / Lbs' -> lb, 'Netto (t)' / 'Weight MT' -> t, else kg."""
    c = " " + re.sub(r"[^a-z]+", " ", (cell or "").lower()) + " "
    if " lb " in c or " lbs " in c or " pounds " in c:
        return LB_KG
    if any(f" {u} " in c for u in ("t", "to", "mt", "tonnen", "tonnes", "tons")):
        return 1000.0
    return 1.0


def _split_row(row, mapping):
    """Tables without lines between rows: pdfplumber returns one row whose cells hold all
    positions, one per text line. Split it when the CN column holds several codes."""
    cn_cell = (row[mapping["cn"]] or "") if "cn" in mapping and mapping["cn"] < len(row) else ""
    k = sum(1 for part in cn_cell.split("\n") if len(re.sub(r"\D", "", part)) >= 4)
    if k < 2:
        return [row]
    cols = [(c or "").split("\n") for c in row]
    return [[parts[j] if len(parts) == k else "" for parts in cols] for j in range(k)]


def _lines_from_table(table, meta):
    lines, mapping, factor = [], None, 1.0
    pending = []
    for row in table:
        if mapping is None:
            mapping = _map_header(row)
            if mapping and "net_mass_kg" in mapping:
                factor = _header_unit_factor(row[mapping["net_mass_kg"]])
            continue
        pending += _split_row(row, mapping)
    for row in pending:
        get = lambda f: (row[mapping[f]] or "").strip() if f in mapping and mapping[f] < len(row) else ""
        desc = re.sub(r"\s+", " ", get("description"))
        mass = parse_mass(get("net_mass_kg"), weight_column=True, column_factor=factor) if "net_mass_kg" in mapping else None
        if mass is None and "qty" in mapping:
            mass = parse_mass(get("qty"))
        if not desc or re.match(r"(zwischen)?(summe|total|gesamt|subtotal)", desc, re.I):
            continue
        if mass is None and not normalize_cn_text(get("cn")):
            continue
        lines.append({
            "description": desc,
            "cn": normalize_cn_text(get("cn")),
            "net_mass_kg": mass,
            "origin": normalize_origin(get("origin")),
            **meta,
        })
    return lines


def extract_pdf(path, name=None):
    """`path` may be a file path or a binary file-like object (then pass `name`)."""
    name = name or Path(getattr(path, "name", str(path))).name
    with pdfplumber.open(path) as pdf:
        text = "\n".join(p.extract_text() or "" for p in pdf.pages)
        if not text.strip():
            raise ExtractionError(f"{name}: no text layer (scanned PDF?) - use vision fallback")
        date, number, supplier, doc_type = _header_fields(text)
        meta = {"date": date, "supplier": supplier, "invoice": number or name,
                "doc_type": doc_type, "file": name}
        lines = []
        for page in pdf.pages:
            for table in page.extract_tables():
                lines += _lines_from_table(table, meta)
        for settings in TEXT_TABLES:  # no ruled table found: columns from text positions
            if lines:
                break
            for page in pdf.pages:
                for table in page.extract_tables(settings):
                    lines += _lines_from_table(table, meta)
        if not lines:  # no table at all: one line of text per position (CN code + mass with unit)
            lines = _lines_from_text(text, meta)
    origin, doc_mass = _doc_origin(text), _doc_mass(text)
    for l in lines:
        l["origin"] = l["origin"] or origin
    if len(lines) == 1 and lines[0]["net_mass_kg"] is None:
        lines[0]["net_mass_kg"] = doc_mass
    if not lines:
        raise ExtractionError(f"{name}: no line-item table found")
    return lines


CN_RE = re.compile(r"(?<![\d.,])(\d{4}\s?\d{2}(?:\s?\d{2})?(?:\s?\d{2})?)(?![\d.,])")


def _lines_from_text(text, meta):
    """Last resort for PDFs without any detectable table: a text line with a CN code
    and a mass with unit ('... 7208 39 00 ... 60.000 kg ...') is one position."""
    lines = []
    for raw in text.splitlines():
        cn_m, mass_m = CN_RE.search(raw), UNIT_RE.search(raw)
        if not cn_m or not mass_m or mass_m.start() < cn_m.start():
            continue
        desc = re.sub(r"^\s*\d{1,3}[.)]?\s+", "", raw[:cn_m.start()]).strip(" -|:")
        if not desc or re.match(r"(zwischen)?(summe|total|gesamt)", desc, re.I):
            continue
        lines.append({"description": desc, "cn": normalize_cn_text(cn_m.group(1)),
                      "net_mass_kg": parse_mass(mass_m.group(0)),
                      "origin": normalize_origin(raw[cn_m.end():mass_m.start()]), **meta})
    return lines


CSV_ALIASES = {
    "description": ["description", "beschreibung", "warenbezeichnung"],
    "cn": ["cn", "kn", "kn-code", "hs", "cn_code"],
    "net_mass_kg": ["net_mass_kg", "netto_kg", "nettogewicht", "net_weight_kg", "netto kg"],
    "origin": ["origin", "ursprung", "country_of_origin"],
    "date": ["date", "datum", "invoice_date"],
    "supplier": ["supplier", "lieferant", "seller"],
    "invoice": ["invoice", "rechnung", "invoice_no", "rechnungsnummer"],
}


def extract_csv(path, name=None):
    """`path` may be a file path or a binary file-like object (then pass `name`)."""
    if hasattr(path, "read"):
        raw = path.read()
        raw = raw.decode("utf-8-sig") if isinstance(raw, bytes) else raw
    else:
        raw = Path(path).read_text(encoding="utf-8-sig")
    name = name or Path(getattr(path, "name", str(path))).name
    dialect = csv.Sniffer().sniff(raw.splitlines()[0], delimiters=",;\t")
    reader = csv.DictReader(raw.splitlines(), dialect=dialect)
    cols = {c.strip().lower(): c for c in reader.fieldnames}
    pick = {f: next((cols[a] for a in al if a in cols), None) for f, al in CSV_ALIASES.items()}
    if not pick["description"] or not pick["net_mass_kg"]:
        raise ExtractionError(f"{name}: needs at least description and net mass columns")
    lines = []
    for r in reader:
        g = lambda f: (r.get(pick[f]) or "").strip() if pick[f] else ""
        mass = parse_number(g("net_mass_kg"))
        if mass is None:
            continue
        lines.append({
            "description": g("description"),
            "cn": normalize_cn_text(g("cn")),
            "net_mass_kg": mass,
            "origin": normalize_origin(g("origin")),
            "date": parse_date(g("date")) if g("date") else None,
            "supplier": g("supplier") or None,
            "invoice": g("invoice") or name,
            "doc_type": "invoice",
            "file": name,
        })
    return lines


def extract_lines(path, name=None):
    """PDF or CSV (path or uploaded file object) -> list of invoice lines."""
    name = name or getattr(path, "name", str(path))
    suffix = Path(name).suffix.lower()
    if suffix == ".pdf":
        return extract_pdf(path, Path(name).name)
    if suffix in (".csv", ".txt"):
        return extract_csv(path, Path(name).name)
    raise ExtractionError(f"unsupported file type: {suffix}")


def read_documents(files):
    """Read several uploaded documents.

    `files` is a list of (path_or_file_object, name). Returns (imported, planned, errors):
    invoice lines, order-confirmation lines (planned imports, not yet imported) and
    error messages for documents that could not be read.
    """
    imported, planned, errors = [], [], []
    for f, name in files:
        try:
            for line in extract_lines(f, name=name):
                (planned if line.get("doc_type") == "order" else imported).append(line)
        except ExtractionError as e:
            errors.append(str(e))
        except Exception as e:  # broken or encrypted file: report, do not crash the UI
            errors.append(f"{name}: Datei nicht lesbar ({type(e).__name__})")
    return imported, planned, errors
