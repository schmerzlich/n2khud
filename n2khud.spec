# n2khud.spec  # V0.1
# Fixes:
# - Removed any bundling of 'unp4k-suite-v3.13.21' (keine Add-Data/Tree dafür).
# - Only 'resources' included as datas.
# Works:
# - onedir build with icon; Tkinter GUI.

import sys
from PyInstaller.utils.hooks import collect_submodules
from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

hidden = [
    "tkinter",
    "queue",
    "re",
    "codecs",
]
# Falls PyInstaller etwas von Tkinter verpasst:
hidden += collect_submodules("tkinter")

datas = collect_data_files("resources", includes=["resources/*"], excludes=[])

a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hidden,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Windowed App (keine Konsole). Für Konsole: console=True setzen.
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="n2khud",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon="resources/app.ico",
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="n2khud",
)
