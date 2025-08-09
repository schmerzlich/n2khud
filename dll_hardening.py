# dll_hardening.py  # V0.1
# Was gefixt wurde:
# - Erzwingt sichere DLL-Suchpfade (Windows).
# Was funktioniert:
# - Beschränkt das Laden von DLLs auf System32 + App-Ordner; keine Wirkung auf macOS/Linux.

import os, sys

def apply():
    if not sys.platform.startswith("win"):
        return
    app_dir = os.path.abspath(os.path.dirname(__file__))
    try:
        # Python 3.8+: bevorzugt
        if hasattr(os, "add_dll_directory"):
            os.add_dll_directory(app_dir)

        import ctypes
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

        LOAD_LIBRARY_SEARCH_DEFAULT_DIRS = 0x00000400
        LOAD_LIBRARY_SEARCH_SYSTEM32     = 0x00000800

        kernel32.SetDefaultDllDirectories(
            LOAD_LIBRARY_SEARCH_DEFAULT_DIRS | LOAD_LIBRARY_SEARCH_SYSTEM32
        )

        AddDllDirectory = getattr(kernel32, "AddDllDirectory", None)
        if AddDllDirectory:
            AddDllDirectory(ctypes.c_wchar_p(app_dir))
    except Exception:
        # Fallback: keine App-Beendigung bei älteren Systemen
        pass
