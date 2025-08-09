# config_manager.py — V1.1
import json
import os
import sys

APP_DIR = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))
RESOURCES_DIR = os.path.join(APP_DIR, "resources")

# Nutzerpfad für beschreibbare Konfig
_APPDATA = os.environ.get("APPDATA") or os.path.expanduser("~\\AppData\\Roaming")
CONFIG_DIR = os.path.join(_APPDATA, "n2khud")
os.makedirs(CONFIG_DIR, exist_ok=True)
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

DEFAULTS_FILE = os.path.join(RESOURCES_DIR, "defaults.json")

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return load_defaults()

def load_defaults():
    with open(DEFAULTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
