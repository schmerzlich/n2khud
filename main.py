# main.py  # V1.1
# Was gefixt wurde:
# - Frühes DLL-Hardening (Windows) via dll_hardening.apply().
# Was funktioniert:
# - Unveränderte GUI-Funktionalität, DPI-Awareness, Konfig speichern.

import os
import sys
import tkinter as tk
from tkinter import messagebox

# --- DLL-Hardening so früh wie möglich ---
try:
    import dll_hardening
    dll_hardening.apply()
except Exception:
    pass

from gui_components import build_gui
from config_manager import load_config, save_config


def center_window(win, w: int, h: int):
    win.update_idletasks()
    sw = win.winfo_screenwidth()
    sh = win.winfo_screenheight()
    x = max(0, (sw - w) // 2)
    y = max(0, (sh - h) // 3)
    win.geometry(f"{w}x{h}+{x}+{y}")

def try_set_icon(win):
    app_dir = os.path.abspath(os.path.dirname(__file__))
    ico_path = os.path.join(app_dir, "resources", "app.ico")
    png_path = os.path.join(app_dir, "resources", "app.png")
    try:
        if os.path.isfile(ico_path):
            win.iconbitmap(ico_path)
        elif os.path.isfile(png_path):
            img = tk.PhotoImage(file=png_path)
            win.iconphoto(True, img)
    except Exception:
        pass

def main():
    root = tk.Tk()
    root.title("n2khud – Star Citizen global.ini Editor")
    try_set_icon(root)
    center_window(root, 1000, 760)
    root.minsize(820, 600)

    config = load_config()
    gui = build_gui(root, config)

    def on_close():
        try:
            if isinstance(gui, dict):
                if "get_game_dir" in gui and callable(gui["get_game_dir"]):
                    config["game_dir"] = gui["get_game_dir"]() or ""
            save_config(config)
        except Exception as e:
            messagebox.showwarning("Warning", f"Could not save configuration:\n{e}")
        finally:
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()

if __name__ == "__main__":
    if sys.platform.startswith("win"):
        try:
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass
    main()
