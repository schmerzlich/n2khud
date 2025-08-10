# n2khud.spec  # V0.2
# Was gefixt wurde:
# - Entfernt: Bundling der unp4k-Suite (senkt VT-False-Positives).
# - Beibehalten: onedir, keine UPX/strip, Version-Infos.

import os
from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT
from PyInstaller.building.api import TOC, Tree
from PyInstaller.utils.win32.versioninfo import VSVersionInfo, StringStruct, StringTable, VarStruct, VarFileInfo, StringFileInfo, FixedFileInfo

block_cipher = None

version_info = VSVersionInfo(
    ffi=FixedFileInfo(
        filevers=(1, 0, 0, 0),
        prodvers=(1, 0, 0, 0),
        mask=0x3f,
        flags=0x0,
        OS=0x40004,
        fileType=0x1,
        subtype=0x0,
        date=(0, 0)
    ),
    kids=[
        StringFileInfo([
            StringTable('040904B0', [
                StringStruct('CompanyName', 'n2k'),
                StringStruct('FileDescription', 'n2khud – Star Citizen global.ini Editor'),
                StringStruct('FileVersion', '1.0.0.0'),
                StringStruct('InternalName', 'n2khud'),
                StringStruct('LegalCopyright', '© 2025 n2k'),
                StringStruct('OriginalFilename', 'n2khud.exe'),
                StringStruct('ProductName', 'n2khud'),
                StringStruct('ProductVersion', '1.0.0.0'),
            ])
        ]),
        VarFileInfo([VarStruct('Translation', [0x0409, 0x04B0])])
    ]
)

datas = TOC()
datas += Tree('resources', prefix='resources')  # Icon etc.

hiddenimports = ['tkinter', 'queue', 're', 'codecs']

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    exclude_binaries=True,
    name='n2khud',
    icon='resources/app.ico',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,
    version=version_info,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    name='n2khud'
)
