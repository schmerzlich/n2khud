# category_map.py
"""
Categorization for Star Citizen items into six high-level buckets.
Hybrid logic:
1) Strong matches via item_Desc / item_Name (regex)
2) Prefix / token mapping from BASE (e.g., "pwr", "cool", "shld" …) derived from original prompt
3) Fallback: If Size/Grade/Class present and nothing else matches -> ship_components
"""

import re

PRIORITY = [
    "ship_components",
    "ship_guns",
    "personal_weapons",
    "weapon_attachments",
    "mining_components",
    "mining_attachments",
]

CATEGORIES = {
    "ship_components": {"title": "Ship & Vehicle Components"},
    "ship_guns": {"title": "Ship & Vehicle Weapons"},
    "personal_weapons": {"title": "Personal Weapons"},
    "weapon_attachments": {"title": "Weapon Attachments"},
    "mining_components": {"title": "Vehicle Mining Components"},
    "mining_attachments": {"title": "Vehicle Mining Attachments"},
}

# 1) DESC/NAME KEYWORDS (broad coverage)
REGEX_BY_CATEGORY = {
    "mining_attachments": [
        r"\bmining\s*gadget\b",
        r"\bmining\s*consumable\b",
        r"\bmining\s*attachment\b",
    ],
    "mining_components": [
        r"\bmining\s*laser\b",
        r"\bmining\s*head\b",
        r"\bmining\s*module\b",
        r"\bmining\s*arm\b",
        r"\bmining\b.*\b(laser|head|module|arm)\b",
    ],
    "ship_guns": [
        r"\b(laser|ballistic|plasma|tachyon)\s+(cannon|repeater)\b",
        r"\bgatling\b",
        r"\b(ship|vehicle)\s+(weapon|gun)\b",
        r"\bturret\b",
        r"\bsize\s*[1-9]\b.*\b(cannon|repeater|gatling|gun)\b",
        r"\bmissile\s*(rack|launcher)\b",
        r"\brotary\b",
        r"\bautocannon\b",
        r"\bscattergun\b",
        r"\btorpedo\b",
        r"\bbomb\b",
    ],
    "personal_weapons": [
        r"\bpistol\b",
        r"\brifle\b",
        r"\bshotgun\b",
        r"\bsniper(\s*rifle)?\b",
        r"\bsmg\b",
        r"\blmg\b",
        r"\bgrenade\s*launcher\b",
        r"\bsubmachine\s*gun\b",
        r"\bcarbine\b",
        r"\bpdw\b",
        r"\bsidearm\b",
    ],
    "weapon_attachments": [
        r"\bscope\b",
        r"\boptic(s)?\b",
        r"\bsuppressor\b",
        r"\bsilencer\b",
        r"\bmag(azine)?\b",
        r"\bgrip\b",
        r"\bbarrel\b",
        r"\bcompensator\b",
        r"\bsight\b",
        r"\bflash\s*hider\b",
        r"\bunderbarrel\b",
        r"\bstock\b",
        r"\brail\b",
        r"\battachment\b",
        r"\bholographic\b",
        r"\breflex\b",
        r"\biron\s*sight(s)?\b",
    ],
    "ship_components": [
        r"\bpower\s*plant\b",
        r"\bcooler\b",
        r"\bshield(\s*generator)?\b",
        r"\bquantum\s*drive\b|\bq\-?drive\b",
        r"\bradar\b",
        r"\bfuel\s*tank\b",
        r"\bfuel\s*intake\b",
        r"\bjump\s*drive\b",
        r"\bemp(\s*generator)?\b",
        r"\bscanner\b",
        r"\bcargo\s*grid\b",
        r"\bpower\s*regulator\b",
        r"\bavionics\b",
        r"\bpower\s*conduit\b",
        r"\bcooling\s*(unit|array|system)\b",
        r"\blife\s*support\b",
        r"\bbattery\b",
        r"\bcapacitor\b",
        r"\bheat\s*sink\b",
    ],
}
REGEX_BY_CATEGORY = {
    cat: [re.compile(p, re.IGNORECASE) for p in pats]
    for cat, pats in REGEX_BY_CATEGORY.items()
}

# 2) PREFIX/TOKEN MAPPING from BASE (case-insensitive)
TOKENS = {
    "ship_components": {
        "comp","pwr","power","cool","cooler","shld","shield","qdrv","quantum","radar",
        "fuel","emp","life","avionics","battery","capacitor","cap","heatsink","heat",
        "scanner","cargo","qdrive","q_drive","jumpdrive","jump_drive"
    },
    "ship_guns": {
        "cannon","repeater","gatling","turret","missile","rocket","torp","torpedo","bomb","gun","wpn"
    },
    "personal_weapons": {
        "pistol","smg","lmg","rifle","shotgun","sniper","carbine","pdw","sidearm"
    },
    "weapon_attachments": {
        "scope","optic","mag","grip","barrel","comp","sight","ubrl","stock","rail","suppressor","silencer"
    },
    "mining_components": {
        "mininglaser","mininghead","miningmodule","miningarm","mining_laser","mining_head","mining_module"
    },
    "mining_attachments": {
        "mininggadget","miningconsumable","miningattach","mining_attachment","gadget","consumable"
    },
}

FALLBACK_COMPONENT_CUES = [
    re.compile(r"\bsize\s*[1-9]\b", re.IGNORECASE),
    re.compile(r"\bgrade\s*[A-E]\b", re.IGNORECASE),
    re.compile(r"\bclass\s*[A-Za-z]+\b", re.IGNORECASE),
    re.compile(r"\bgenerator\b", re.IGNORECASE),
    re.compile(r"\bmodule\b", re.IGNORECASE),
    re.compile(r"\bavionics\b", re.IGNORECASE),
    re.compile(r"\blife\s*support\b", re.IGNORECASE),
]

def _split_tokens(base: str):
    parts = [p.lower() for p in re.split(r"[_\-\.]+", base) if p]
    joined = {"".join(parts)} if parts else set()
    return set(parts) | joined

def _match_desc_name(desc: str, name: str):
    blob = f"{desc or ''} || {name or ''}"
    for cat in ["mining_attachments","mining_components","ship_guns","personal_weapons","weapon_attachments","ship_components"]:
        for rx in REGEX_BY_CATEGORY[cat]:
            if rx.search(blob):
                return cat
    return None

def _match_tokens(base: str):
    toks = _split_tokens(base or "")
    for cat, token_set in TOKENS.items():
        if toks & token_set:
            return cat
    return None

def categorize_item(desc_text: str, name_text: str = "", base: str = ""):
    """Returns a category key or None."""
    # 1) Strong textual matches
    cat = _match_desc_name(desc_text, name_text)
    if cat:
        return cat
    # 2) BASE tokens/prefix
    cat = _match_tokens(base)
    if cat:
        return cat
    # 3) Fallback -> ship_components when typical component cues are present and not FPS/attachment/ship-gun
    blob = f"{desc_text or ''} || {name_text or ''}"
    if any(rx.search(blob) for rx in FALLBACK_COMPONENT_CUES):
        if not (re.search(r"\b(pistol|rifle|shotgun|sniper|smg|lmg)\b", blob, re.IGNORECASE) or
                re.search(r"\b(scope|optic|suppressor|mag(azine)?|grip|sight)\b", blob, re.IGNORECASE) or
                re.search(r"\b(cannon|repeater|gatling|turret|missile|torpedo|bomb|gun)\b", blob, re.IGNORECASE)):
            return "ship_components"
    return None
