# filter_engine_strict.py  # V1.6.1
# Was gefixt wurde:
# - Entpacken von escapen Zeilenumbrüchen ("\n", "\r\n") vor dem KV-Parsing.
# - Robustere Säuberung (NBSP/Â\xa0), Trimmen, Normalisierung von Keys ("item type" etc.).
# - KV-Parser liest jetzt pro Zeile exakt ein "k: v", statt an der ersten Stelle abzuschneiden.
# Was funktioniert:
# - Aus desc-Texten wie "Manufacturer: ...\nItem Type: ...\nClass: ..." werden korrekte Dicts.
# - Kürzungen/Formatierungen (Class->Mil/Civ/...) & Size->S02 bleiben intakt.
# - Kategorisierung wie gehabt.

import re

# --- Regex ---
_KEY_RE  = re.compile(r'^\s*([^=\s]+)\s*=\s*(.*)\s*$')
_NAME_RE = re.compile(r'^(item_Name[^=]*)$', re.I)
_DESC_RE = re.compile(r'^(item_Desc[^=]*)$', re.I)

def read_text(path):
    import codecs
    try:
        with codecs.open(path, "r", encoding="utf-8-sig") as f:
            return f.read()
    except UnicodeDecodeError:
        with codecs.open(path, "r", encoding="latin-1", errors="replace") as f:
            return f.read()

# === Normalisierung/Varianten (wie dein Script) ===
def normalize_key(key: str) -> str:
    key = key.lower()
    if key.endswith("_scitem"):
        key = key[:-7]
    key = key.replace('_', '').replace('-', '').replace(' ', '')
    return key

def generate_desc_key_variants(name_key: str):
    base = name_key[len('item_Name'):]  # z.B. '_POWR_ACOM_S01_StarHeart_SCItem'
    variants = []
    variants.append('item_Desc'  + base)   # ohne Unterstrich
    variants.append('item_Desc_' + base)   # mit Unterstrich
    if base.lower().endswith('_scitem'):
        base2 = base[:-7]
        variants.append('item_Desc'  + base2)
        variants.append('item_Desc_' + base2)
    return variants

# === Hilfen zum Säubern / Unescaping ===
def _clean_text(s: str) -> str:
    if not s:
        return ""
    # Escapte Umbrüche in echte Zeilenumbrüche wandeln
    s = s.replace("\\r\\n", "\n").replace("\\n", "\n").replace("\r\n", "\n")
    # Häufige Encoding-Artefakte glätten
    s = s.replace("Â\xa0", " ").replace("\xa0", " ")
    # Trim über alle Zeilen
    s = "\n".join(line.strip() for line in s.split("\n"))
    return s.strip()

# === Striktes Attribut-Parsing: nur "k: v"-Zeilen ===
def parse_kv_lines(desc_text: str):
    d = {}
    if not desc_text:
        return d
    blob = _clean_text(desc_text)
    for ln in blob.split("\n"):
        if ":" not in ln:
            continue
        k, v = ln.split(":", 1)
        k = k.strip().lower()
        v = v.strip()
        if not k or not v:
            continue
        # Schlüssel glätten / vereinheitlichen
        k = k.replace("—", "-").replace("–", "-")
        k = k.replace("item  type", "item type")
        k = k.replace("attachment point", "attachment point")
        # Nur den letzten sinnvollen Wert behalten (idempotent)
        d[k] = v
    return d

def shorten_class(cls: str):
    if not cls:
        return None
    cls = cls.lower()
    mapping = {
        'military': 'Mil',
        'civilian': 'Civ',
        'industrial': 'Ind',
        'competition': 'Cmp',
        'stealth': 'Stl',
    }
    return mapping.get(cls, cls[:3].capitalize())

def format_size(size: str):
    if size is None:
        return None
    s = str(size).strip()
    # "Size: 1" / "Size: S1" / "Size: 16 cm" -> nur Zahl extrahieren
    m = re.search(r'(\d+)', s)
    if not m:
        return None
    try:
        num = int(m.group(1))
        return f"S{num:02d}"
    except:
        return None

def has_any_attribute_from_desc(desc_text: str):
    d = parse_kv_lines(desc_text)
    cls  = shorten_class(d.get('class'))
    size = format_size(d.get('size'))
    grd  = d.get('grade')
    return any([cls, size, grd])

# === Kategorien ===
CAT_VEH_COMPONENTS = "vehicle_components"
CAT_VEH_WEAPONS    = "vehicle_weapons"
CAT_PERS_WEAPONS   = "personal_weapons"
CAT_PERS_ATTACH    = "personal_weapon_attachments"
CAT_VEH_MINING     = "vehicle_mining_components"

RE_PERS_WEAP = re.compile(r'\b(pistol|rifle|shotgun|sniper|smg|lmg)\b', re.I)
RE_PERS_ATT  = re.compile(r'\b(scope|optic|suppressor|silencer|mag(?:azine)?|grip|sight|laser\s*sight|flashlight|underbarrel|stock|rail)\b', re.I)
RE_SHIP_GUNS = re.compile(r'\b(cannon|repeater|gatling|turret|missile|torpedo|bomb|gun|launcher)\b', re.I)
RE_MINING    = re.compile(r'\b(mining\s*(laser|head|gadget|attachment|consumable|module|arm))\b', re.I)
RE_COMPONENT = re.compile(r'\b(power|cool(?:er)?|shield|q(?:drv|fuel|int)|thr(?:uster)?|scanner|radar|powerplant|power plant|quantum\s*drive|cooling|avionics|life\s*support)\b', re.I)

def categorize(desc_text, name_text=""):
    blob = f"{_clean_text(desc_text) or ''} || {name_text or ''}"
    if RE_MINING.search(blob):    return CAT_VEH_MINING
    if RE_PERS_ATT.search(blob):  return CAT_PERS_ATTACH
    if RE_PERS_WEAP.search(blob): return CAT_PERS_WEAPONS
    if RE_SHIP_GUNS.search(blob): return CAT_VEH_WEAPONS
    if RE_COMPONENT.search(blob) or any(x in (blob.lower()) for x in ["size","class","grade"]):
        return CAT_VEH_COMPONENTS
    return CAT_VEH_COMPONENTS

# === Haupt-API ===
def parse_all(raw_or_path: str):
    """
    Liest die INI und bildet Paare (name_key, name_val, desc_val) über
    normalize_key() + generate_desc_key_variants() (streng wie dein Script).
    """
    raw = raw_or_path if "\n" in raw_or_path else read_text(raw_or_path)
    desc_index = {}
    name_lines = []

    for ln in raw.splitlines():
        m = _KEY_RE.match(ln)
        if not m:
            continue
        key, val = m.group(1), m.group(2)
        if _DESC_RE.match(key):
            desc_index[key.lower()] = val
        elif _NAME_RE.match(key):
            name_lines.append((key, val))

    pairs = []
    for name_key, name_val in name_lines:
        matched_desc_val = None
        for desc_key_variant in generate_desc_key_variants(name_key):
            norm_target = normalize_key(desc_key_variant)
            for cand_key_lc, cand_val in desc_index.items():
                if normalize_key(cand_key_lc) == norm_target:
                    matched_desc_val = cand_val
                    break
            if matched_desc_val:
                break
        pairs.append({
            "name_key": name_key,
            "name_val": name_val,
            "desc_val": matched_desc_val
        })
    return raw, pairs

def filter_pairs_with_attributes(pairs):
    out = []
    for p in pairs:
        if has_any_attribute_from_desc(p["desc_val"]):
            d = parse_kv_lines(p["desc_val"] or "")
            q = dict(p)
            q["class"] = shorten_class(d.get("class"))
            q["size"]  = format_size(d.get("size"))
            q["grade"] = d.get("grade")
            q["category"] = categorize(p["desc_val"], p["name_val"])
            out.append(q)
    return out
