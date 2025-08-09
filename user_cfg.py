# user_cfg.py  # V1.6.1
# Was gefixt wurde:
# - Klarstellung: Erwartet LIVE-Ordner als sc_dir (Kompatibilität bleibt).
# - UTF-8 Ausgabe mit Newline am Ende.
# Was funktioniert:
# - Idempotentes Setzen/Aktualisieren von g_language / g_languageAudio.

import os

def ensure_language_cfg(sc_dir, lang_text="german_(germany)", lang_audio="english"):
    """
    Setzt/aktualisiert g_language und g_languageAudio in user.cfg (idempotent).
    Erwartet i.d.R. den LIVE-Ordner als sc_dir.
    """
    user_cfg_path = os.path.join(sc_dir, "user.cfg")
    lines = []
    if os.path.isfile(user_cfg_path):
        with open(user_cfg_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.read().splitlines()

    def upsert(key, val):
        key_l = key.lower()
        for i, ln in enumerate(lines):
            if ln.strip().lower().startswith(key_l):
                lines[i] = f"{key} = {val}"
                return
        lines.append(f"{key} = {val}")

    upsert("g_language", lang_text)
    upsert("g_languageAudio", lang_audio)

    with open(user_cfg_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
