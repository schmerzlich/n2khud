# n2khud.spec  # V0.1
# Was gefixt wurde:
# - Spezifikationsdatei aus deinem PyInstaller-Kommando abgeleitet.
# - Ressourcen- und unp4k-Verzeichnisse werden korrekt eingebunden.
#
# Was funktioniert:
# - Erstellt Onedir-Build mit Konsole, Icon, allen Hidden Imports.

# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('resources', 'resources'),
        ('unp4k-suite-v3.13.21', 'unp4k-suite-v3.13.21'),
    ],
    hiddenimports=[
        'tkinter',
        'queue',
        're',
        'codecs',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='n2khud',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    icon='resources/app.ico'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='n2khud'
)
