# pipeline.py  # V1.3
# Was gefixt wurde:
# - unp4k wird niemals aus _internal / _MEIPASS ausgeführt. Falls vorhanden, wird es
#   in einen externen Ordner (neben der EXE) kopiert und nur von dort verwendet.
# - SHA-256-Integritätscheck für unp4k.exe / unforge.exe / unp4k.gui.exe.
#
# Was funktioniert:
# - Analyze/Generate unverändert, Logging/Timer intakt.
# - Schreiben nach LIVE\...\german_(germany)\global.ini + user.cfg-Update.
# - Optionale Bereinigung von LIVE\Data.

import os
import sys
import shutil
import hashlib
from datetime import datetime
from tkinter import messagebox

from utils import find_file_case_insensitive, backup_file
from ini_parser import (
    load_items,
    read_text,
    write_text,
    build_modified_ini,
    build_attribute_catalog,
)
from unp4k_handler import run_unp4k
from user_cfg import ensure_language_cfg

# --- Erwartete Hashes der unp4k-Suite-Komponenten (laut Ihrer VT-Ausgabe) ---
_EXPECTED_SHA256 = {
    "unp4k.exe":      "a4b40d8a741ad50a1757ce82bb552a773aa62a386b82a7028c751272608aac2f",
    "unforge.exe":    "754301144e5a92621bcf31c3531e9b13b4f402355d66b386e5799ee0f2a6dd3f",
    "unp4k.gui.exe":  "c74a5324290f8a909fa7da933789e86098d5093bf92f4dbed3ace3dfcd7e8438",
}

# --- Konsolen-Adapter ---
class _NullConsole:
    def section(self, msg): print(f"[STEP] {msg}")
    def ok(self, msg):      print(f"[OK] {msg}")
    def info(self, msg):    print(f"[INFO] {msg}")
    def error(self, msg):   print(f"[ERROR] {msg}")
    def log(self, msg):     print(f"[LOG] {msg}")

def _get(gui, name, default=None):
    try:
        if hasattr(gui, name):
            return getattr(gui, name)
        return gui.get(name, default)
    except Exception:
        return default

def _fail(gui, msg):
    c = _get(gui, "console") or _NullConsole()
    try:
        c.error(msg)
    finally:
        try:
            messagebox.showerror("Fehler", msg)
        except Exception:
            pass

class _TeeConsole:
    def __init__(self, console, log_path):
        self._c = console or _NullConsole()
        self._log_path = log_path

    def _write_file(self, level, msg):
        try:
            ts = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            with open(self._log_path, "a", encoding="utf-8") as f:
                f.write(f"[{ts}] [{level}] {msg}\n")
        except Exception:
            pass

    def section(self, msg):
        self._c.section(msg); self._write_file("STEP", f"— {msg} —")
    def ok(self, msg):
        self._c.ok(msg); self._write_file("OK", msg)
    def info(self, msg):
        self._c.info(msg); self._write_file("INFO", msg)
    def error(self, msg):
        self._c.error(msg); self._write_file("ERROR", msg)
    def log(self, msg):
        self._c.log(msg); self._write_file("LOG", msg)

# --- Pfad-Helfer ---
def _dev_dir():
    return os.path.abspath(os.path.dirname(__file__))

def _exe_dir():
    try:
        return os.path.dirname(sys.executable)
    except Exception:
        return None

def _app_dir():
    return _exe_dir() or _dev_dir()

def _meipass_dir():
    return getattr(sys, "_MEIPASS", None)

def _resolve_live_dir(game_dir: str):
    if not game_dir:
        return None, None
    g = os.path.abspath(game_dir)
    cand = os.path.join(g, "Data.p4k")
    if os.path.isfile(cand): return g, cand
    live = os.path.join(g, "LIVE")
    cand = os.path.join(live, "Data.p4k")
    if os.path.isfile(cand): return live, cand
    pu = os.path.join(g, "PU")
    cand = os.path.join(pu, "Data.p4k")
    if os.path.isfile(cand): return pu, cand
    return None, None

# --- unp4k: nie intern ausführen; extern bereitstellen + prüfen ---
_UNP4K_DIRNAME = "unp4k-suite-v3.13.21"

def _sha256_of(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def _verify_unp4k_suite(dir_path: str, c: _TeeConsole) -> bool:
    ok_all = True
    for fn, expected in _EXPECTED_SHA256.items():
        p = os.path.join(dir_path, fn)
        if not os.path.isfile(p):
            c.error(f"Fehlt: {p}")
            ok_all = False
            continue
        got = _sha256_of(p)
        c.info(f"Gefundener SHA256: {got}")
        c.info(f"Erwartet:        {expected}")
        if got.lower() != expected.lower():
            c.error(f"Hash-Mismatch bei {fn}")
            ok_all = False
    return ok_all

def _copytree(src, dst):
    if os.path.isdir(dst):
        return
    shutil.copytree(src, dst)

def _find_or_materialize_unp4k(c: _TeeConsole) -> str | None:
    """
    Bevorzugt externen Ordner neben EXE/Script.
    Falls nur in _MEIPASS/_internal vorhanden -> nach außen kopieren.
    Gibt finalen externen Pfad zurück oder None bei Fehler.
    """
    base = _app_dir()
    external = os.path.join(base, _UNP4K_DIRNAME)
    if os.path.isdir(external):
        return external

    # Liegt es versehentlich im Bundle?
    mei = _meipass_dir()
    candidates_internal = []
    if mei:
        candidates_internal += [
            os.path.join(mei, _UNP4K_DIRNAME),
            os.path.join(mei, "_internal", _UNP4K_DIRNAME),
        ]
    # Manche onedir-Builds legen _internal direkt neben EXE ab
    exedir = _exe_dir()
    if exedir:
        candidates_internal += [
            os.path.join(exedir, "_internal", _UNP4K_DIRNAME),
        ]

    for src in candidates_internal:
        if os.path.isdir(src):
            try:
                c.info(f"Finde gebündeltes unp4k unter: {src}")
                c.info(f"Kopiere nach extern: {external}")
                _copytree(src, external)
                return external
            except Exception as e:
                c.error(f"Konnte unp4k nicht nach außen kopieren: {e}")
                return None

    # Letzter Versuch: DEV-Nachbar (beim Entwickeln)
    dev_alt = os.path.join(_dev_dir(), _UNP4K_DIRNAME)
    if os.path.isdir(dev_alt):
        return dev_alt

    return None

# --- Haupt-Pipeline ---
def run_pipeline(gui, game_dir, unp4k_dir=None, settings=None):
    base_dir = _app_dir()
    log_path = os.path.join(base_dir, "log.log")
    c = _TeeConsole(_get(gui, "console") or _NullConsole(), log_path)
    settings = settings or {}
    try:
        live_dir, p4k = _resolve_live_dir(game_dir)
        if not live_dir or not p4k:
            return _fail(gui, "Bitte gültigen Star Citizen Ordner wählen (LIVE/PU oder dessen Parent).")

        # unp4k extern sicherstellen + verifizieren
        suite_dir = unp4k_dir or _find_or_materialize_unp4k(c)
        if not suite_dir or not os.path.isdir(suite_dir):
            return _fail(gui, f"unp4k-Ordner nicht gefunden oder nicht extern bereitstellbar:\n{suite_dir or '(None)'}")

        c.section("Integrity")
        c.info(f"Unp4k dir: {suite_dir}")
        if not _verify_unp4k_suite(suite_dir, c):
            return _fail(gui, "Integritätsprüfung der unp4k-Suite fehlgeschlagen.")

        c.section("Extraction")
        c.info(f"Using Data.p4k: {p4k}")

        ok, out = run_unp4k(suite_dir, p4k, "*.ini")
        for ln in (out or "").splitlines():
            c.info(ln)
        if not ok:
            c.error("unp4k reported an error.")
            return _fail(gui, "Extraction failed.")
        c.ok("Extraction complete.")

        c.section("Locate Files")
        eng_ini = os.path.join(suite_dir, "Data", "Localization", "english", "global.ini")
        if not os.path.isfile(eng_ini):
            eng_ini = find_file_case_insensitive(os.path.join(suite_dir, "Data", "Localization"), "global.ini")
            if not eng_ini:
                return _fail(gui, "English global.ini not found in unp4k output.")
        c.ok(f"Found: {eng_ini}")

        c.section("Parse & Catalog")
        items, raw_text, enc = load_items(eng_ini)
        all_cats = sorted({it.get("category") for it in items if it.get("category")})
        c.ok(f"{len(items)} items recognized across {len(all_cats)} categories.")
        c.info(f"Used encoding: {enc}")

        set_parsed = _get(gui, "set_parsed_data")
        if callable(set_parsed):
            catalog = build_attribute_catalog(items)  # <-- NEU
            set_parsed(items, raw_text, catalog)      # <-- catalog statt {}
            c.section("Update GUI"); c.ok("Filter UI updated.")

        c.section("Ready"); c.ok("Choose attributes and click 'Generate'.")
    except Exception as e:
        _fail(gui, str(e))

def _get_analyzed_raw(gui):
    get_parsed = _get(gui, "get_parsed_data")
    if callable(get_parsed):
        data = get_parsed()
        if data and isinstance(data, (tuple, list)) and len(data) >= 2:
            return data[1]
    return None

def _load_eng_ini_text_fallback():
    suite_dir = os.path.join(_app_dir(), _UNP4K_DIRNAME)
    eng_ini = os.path.join(suite_dir, "Data", "Localization", "english", "global.ini")
    if os.path.isfile(eng_ini):
        txt, _ = read_text(eng_ini)
        return txt
    loc_dir = os.path.join(suite_dir, "Data", "Localization")
    found = find_file_case_insensitive(loc_dir, "global.ini") if os.path.isdir(loc_dir) else None
    if found and os.path.isfile(found):
        txt, _ = read_text(found)
        return txt
    return None

def generate_from_gui(gui, game_dir, settings):
    base_dir = _app_dir()
    log_path = os.path.join(base_dir, "log.log")
    c = _TeeConsole(_get(gui, "console") or _NullConsole(), log_path)

    try:
        live_dir, _p4k = _resolve_live_dir(game_dir)
        if not live_dir:
            return _fail(gui, "Bitte gültigen Star Citizen Ordner wählen (LIVE/PU oder dessen Parent).")

        c.section("Generate")
        c.info("Generating global.ini from selected attributes…")

        raw_text = _get_analyzed_raw(gui) or _load_eng_ini_text_fallback()
        if not raw_text:
            return _fail(gui, "Quell‑INI nicht verfügbar. Bitte erneut 'Analyze' ausführen.")

        merged_text = build_modified_ini(raw_text, settings)

        # 1) Kopie im App-Ordner
        merged_path = os.path.join(base_dir, "global_merged.ini")
        write_text(merged_path, merged_text, encoding="utf-8-sig")
        c.ok(f"Merged written: {merged_path}")

        # 2) Ausgabe im LIVE-Verzeichnis
        out_dir = os.path.join(live_dir, "Data", "Localization", "german_(germany)")
        os.makedirs(out_dir, exist_ok=True)
        out_file = os.path.join(out_dir, "global.ini")
        backup_file(out_file)
        write_text(out_file, merged_text, encoding="utf-8-sig")
        c.ok(f"Written: {out_file}")

        # user.cfg aktualisieren
        c.section("user.cfg")
        ensure_language_cfg(live_dir, "german_(germany)", "english")
        c.ok("user.cfg updated.")

        if settings and settings.get("cleanup_after_write"):
            data_dir = os.path.join(live_dir, "Data")
            if os.path.isdir(data_dir):
                shutil.rmtree(data_dir, ignore_errors=True)
                c.ok("Temporary Data folder removed.")

        c.section("Done"); c.ok("All set.")
        c.ok("Finish — Exit program")
    except Exception as e:
        _fail(gui, str(e))
