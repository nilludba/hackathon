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
    "CN": ["china", "volksrepublik china", "prc"],
    "IN": ["indien", "india"],
    "RS": ["serbien", "serbia"],
    "UA": ["ukraine"],
    "BA": ["bosnien", "bosnia"],
    "KR": ["südkorea", "korea", "south korea"],
    "VN": ["vietnam", "viet nam"],
    "US": ["usa", "vereinigte staaten", "united states"],
    "GB": ["vereinigtes königreich", "united kingdom", "großbritannien", "uk"],
}

# header keyword -> field
HEADER_KEYS = [
    ("description", ["beschreibung", "description", "warenbezeichnung", "artikel", "bezeichnung"]),
    ("cn", ["kn-code", "kn code", "kn", "hs", "cn code", "zolltarif", "taric", "warennummer"]),
    ("origin", ["ursprung", "origin", "herkunft", "ursprungsland"]),
    ("net_mass_kg", ["netto kg", "nettogewicht", "net weight", "netto", "net kg", "net mass"]),
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


def normalize_origin(s):
    s = (s or "").strip()
    m = re.search(r"\(([A-Z]{2})\)", s)
    if m:
        return m.group(1)
    if re.fullmatch(r"[A-Za-z]{2}", s):
        return s.upper()
    words = " " + re.sub(r"[^\wäöüß]+", " ", s.lower()).strip() + " "
    for iso, names in COUNTRIES.items():
        if any(f" {n} " in words for n in names):
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
    doc_type = "order" if re.search(r"Auftragsbestätigung|Order Confirmation|Proforma", text, re.I) else "invoice"
    return date, number, supplier, doc_type


def _map_header(row):
    cells = [re.sub(r"\s+", " ", (c or "").replace("\n", " ")).strip().lower() for c in row]
    mapping = {}
    for field, keys in HEADER_KEYS:
        for i, c in enumerate(cells):
            if i in mapping.values():
                continue
            if any(c.startswith(k) or f" {k}" in f" {c}" for k in keys):
                mapping[field] = i
                break
    return mapping if {"description", "net_mass_kg"} <= mapping.keys() else None


def _lines_from_table(table, meta):
    lines, mapping = [], None
    for row in table:
        if mapping is None:
            mapping = _map_header(row)
            continue
        get = lambda f: (row[mapping[f]] or "").strip() if f in mapping and mapping[f] < len(row) else ""
        desc = re.sub(r"\s+", " ", get("description"))
        mass = parse_number(get("net_mass_kg"))
        if not desc or mass is None or re.match(r"(summe|total|gesamt)", desc, re.I):
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
    if not lines:
        raise ExtractionError(f"{name}: no line-item table found")
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
