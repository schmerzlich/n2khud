# ini_parser.py  # V1.9.3
# Was gefixt wurde:
# - read_text() heilt verwaiste 0xA0-Bytes im Roh-Stream (-> C2 A0) und probiert
#   danach erneut UTF-8-SIG, bevor auf Latin-1 (replace) zurückgefallen wird.
# - V1.9.2-Verbesserung bleibt: Originale Whitespaces um '=' werden bewahrt.
#
# Was funktioniert:
# - Analyze: Items/Kategorien + Attributkatalog für die GUI.
# - Generate: Einheitliche Klammern (role/size/grade) gemäß GUI-Regeln.
# - Keine „Â“-Artefakte mehr durch Latin-1-Fallback bei UTF‑8‑BOM-Quellen.

import codecs
import re
from datetime import datetime
from collections import Counter

from filter_engine_strict import (
    parse_all,
    parse_kv_lines,
    shorten_class,
    format_size as _format_size_engine,
    categorize as _categorize_engine,
)

# --- Engine -> GUI Kategorien ---
_CAT_MAP = {
    "vehicle_components":            "ship_components",
    "vehicle_weapons":               "ship_guns",
    "personal_weapons":              "personal_weapons",
    "personal_weapon_attachments":   "weapon_attachments",
    "vehicle_mining_components":     "mining_components",
    "mining_attachments":            "mining_attachments",
}
def _map_category(cat): return _CAT_MAP.get(cat, cat)

# --- IO ---
def read_text(path):
    """
    Liest eine INI als Text ein.
    Strategie:
      1) Direkt UTF-8 mit BOM (utf-8-sig) versuchen.
      2) Bei UnicodeDecodeError Rohbytes laden, verwaiste 0xA0 -> C2 A0 heilen,
         erneut utf-8-sig versuchen.
      3) Falls weiterhin fehlerhaft, Latin-1 mit errors='replace'.
    """
    # 1) Schnellpfad UTF-8-SIG
    try:
        with codecs.open(path, "r", encoding="utf-8-sig") as f:
            return f.read(), "utf-8-sig"
    except UnicodeDecodeError:
        pass

    # 2) Byte-Heilung: einzelne 0xA0 in gültige UTF-8-NBSP (C2 A0) umwandeln
    with open(path, "rb") as fb:
        raw = fb.read()

    healed = bytearray()
    prev = None
    for b in raw:
        if b == 0xA0 and prev != 0xC2:
            healed.append(0xC2)
            healed.append(0xA0)
            prev = 0xA0
        else:
            healed.append(b)
            prev = b

    try:
        text = healed.decode("utf-8-sig")
        return text, "utf-8-sig(healed)"
    except UnicodeDecodeError:
        # 3) Letzter Ausweg: Latin-1 (mit Ersatzzeichen)
        return raw.decode("latin-1", errors="replace"), "latin-1"

def write_text(path, txt, encoding="utf-8-sig"):
    with codecs.open(path, "w", encoding=encoding) as f:
        f.write(txt)

# --- Analyze: Items laden + Katalog aufbauen ---
def load_items(path):
    raw_text, enc = read_text(path)
    _, pairs = parse_all(raw_text)

    items = []
    for p in pairs:
        name_key = p["name_key"]
        name_val = p["name_val"]
        desc_val = p.get("desc_val")
        engine_cat = _categorize_engine(desc_val, name_val)
        gui_cat = _map_category(engine_cat)
        items.append({
            "key": name_key,
            "val": name_val,
            "desc": desc_val,
            "name": name_val,
            "base": name_key,
            "category": gui_cat,
        })
    return items, raw_text, enc

def build_attribute_catalog(items):
    """Welche Attribute existieren in welcher Kategorie? (class/size/grade)"""
    all_cats = set(it.get("category") for it in items if it.get("category"))
    found = {cat: set() for cat in all_cats}

    for it in items:
        cat = it.get("category")
        if not cat:
            continue
        d = parse_kv_lines(it.get("desc") or "")
        cls  = shorten_class(d.get("class"))
        size = _format_size_engine(d.get("size"))
        grd  = d.get("grade")
        if cls:  found[cat].add("class")
        if size: found[cat].add("size")
        if grd:  found[cat].add("grade")

    catalog = {}
    for cat in all_cats:
        catalog[cat] = sorted(found[cat]) if found[cat] else ["class", "size", "grade"]
    return catalog

# --- Merge-/Format-Hilfen ---
_TRAIL_PAREN_RE = re.compile(r"\s*\(([^()]*)\)\s*$")
# Für formatgetreues Überschreiben (Gruppen: lead, key, wsL, "=", wsR, val)
_KEY_LINE_FMT_RE = re.compile(r'^(\s*)([^=\s]+)(\s*)=(\s*)(.*)$')

def _get_fmt_settings(settings: dict):
    fmt = (settings or {}).get("formatting", {}) or {}
    size_prefix = fmt.get("size_prefix", "S")
    try:
        size_pad = int(fmt.get("size_pad", 2))
    except Exception:
        size_pad = 2
    order = fmt.get("order", ["role", "size", "grade"])
    valid = ["role", "size", "grade"]
    order = [o for o in order if o in valid] or ["role", "size", "grade"]
    return size_prefix, size_pad, order

def _abbr_role(settings: dict, cls_short: str | None) -> str | None:
    if not cls_short:
        return None
    m = (settings or {}).get("abbr_map", {}) or {}
    rev = {"Mil":"Military","Civ":"Civilian","Cmp":"Competition","Ind":"Industrial","Stl":"Stealth"}
    if cls_short in rev and rev[cls_short] in m and m[rev[cls_short]]:
        return m[rev[cls_short]].strip()
    return cls_short

def _format_size_with(settings: dict, size_raw: str | None) -> str | None:
    if size_raw is None:
        return None
    size_prefix, size_pad, _ = _get_fmt_settings(settings)
    s = _format_size_engine(size_raw)  # "S02" o.ä.
    if not s:
        return None
    m = re.search(r'(\d+)', s)
    if not m:
        return None
    num = int(m.group(1))
    return f"{size_prefix}{num:0{size_pad}d}"

def _build_bracket(desc_text: str, settings: dict, gui_cat: str, filters_selected: dict) -> str | None:
    d = parse_kv_lines(desc_text or "")
    role = _abbr_role(settings, shorten_class(d.get("class")))
    size = _format_size_with(settings, d.get("size"))
    grade = (d.get("grade") or "").strip() or None

    chosen = set(filters_selected.get(gui_cat, set())) if filters_selected else {"class","size","grade"}
    parts_map = {
        "role":  role if "class" in chosen else None,
        "size":  size if "size"  in chosen else None,
        "grade": grade if "grade" in chosen else None,
    }
    _, _, order = _get_fmt_settings(settings)
    parts = [parts_map[k] for k in order if parts_map.get(k)]
    if not parts:
        return None
    return "(" + " ".join(parts) + ")"

def _apply_trailing_bracket(name_val: str, bracket: str | None) -> str:
    if not bracket:
        return name_val
    if _TRAIL_PAREN_RE.search(name_val or ""):
        return _TRAIL_PAREN_RE.sub(" " + bracket, name_val).strip()
    return (name_val + " " + bracket).strip()

def build_modified_ini(raw_text: str, settings: dict) -> str:
    """
    Modifiziert item_Name*-Zeilen anhand der GUI-Einstellungen.
    - Header-Block als Marker (einmalig).
    - Für jedes Name/Desc-Paar: End-Klammer normiert hinzufügen/ersetzen.
    - Bewahrt originalen Whitespace um '='.
    """
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = (
        f"; === n2khud merged ===\n"
        f"; Generated: {ts}\n"
        f"; Rule: order={(settings or {}).get('formatting',{}).get('order',['role','size','grade'])}, "
        f"size_prefix/size_pad={(settings or {}).get('formatting',{}).get('size_prefix','S')}/"
        f"{(settings or {}).get('formatting',{}).get('size_pad',2)}\n"
    )
    body = raw_text
    if not raw_text.lstrip().startswith("; === n2khud merged ==="):
        body = (("\n" + raw_text) if not raw_text.startswith("\n") else raw_text)
        body = header + body

    _, pairs = parse_all(body)
    filters_selected = (settings or {}).get("filters_selected", {}) or {}

    rename = {}
    for p in pairs:
        name_key = p["name_key"]
        name_val = p["name_val"]
        desc_val = p.get("desc_val")

        eng_cat = _categorize_engine(desc_val, name_val)
        gui_cat = _map_category(eng_cat)

        bracket = _build_bracket(desc_val, settings, gui_cat, filters_selected)
        if not bracket:
            continue
        new_name = _apply_trailing_bracket(name_val, bracket)
        if new_name != name_val:
            rename[name_key] = new_name

    if not rename:
        return body

    out_lines = []
    for ln in body.splitlines():
        m = re.match(r'^(\s*)([^=\s]+)(\s*)=(\s*)(.*)$', ln)
        if not m:
            out_lines.append(ln); continue
        lead, key, wsL, wsR, val = m.groups()
        if key in rename:
            out_lines.append(f"{lead}{key}{wsL}={wsR}{rename[key]}")
        else:
            out_lines.append(ln)
    return "\n".join(out_lines)
