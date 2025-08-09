# gui_components.py — V1.3
# Was gefixt wurde:
# - Doppelte „Generate“-/„Generating…“-Logs entfernt: Nur noch Pipeline loggt.
# - Voll kompatibel mit StatusConsole (Timer/Lock).
#
# Was funktioniert:
# - Analyze/Generate im Thread, Live‑Timer während Generate.
# - Generate-Button: während Lauf disabled, danach wieder grün (Ready/Finish).

import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from collections import Counter

from status_console import StatusConsole
from pipeline import run_pipeline, generate_from_gui
from category_map import CATEGORIES, PRIORITY

TARGET_WIDTH = 820
MIN_WIDTH = 780

def sort_categories(categories):
    prio_index = {k: i for i, k in enumerate(PRIORITY)}
    return sorted([c for c in categories if c in prio_index], key=lambda c: prio_index[c])

class ScrollableFrame(ttk.Frame):
    def __init__(self, parent, height=260, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0, height=height)
        self.vsb = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.inner = ttk.Frame(self.canvas)
        self.inner.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.vsb.grid(row=0, column=1, sticky="ns")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

def _ensure_target_width(root):
    try:
        root.update_idletasks()
        cur_h = max(600, root.winfo_height() or 720)
        root.minsize(MIN_WIDTH, 600)
        root.geometry(f"{TARGET_WIDTH}x{cur_h}")
    except Exception:
        pass

def build_gui(root, config):
    # --- Top ---
    folder_frame = tk.Frame(root); folder_frame.pack(fill="x", padx=8, pady=(6, 4))

    tk.Label(folder_frame, text="Game dir - Set Live or PU folder:").grid(row=0, column=0, padx=(2, 2), pady=2, sticky="w")
    folder_var = tk.StringVar(value=config.get("game_dir", ""))
    entry = tk.Entry(folder_frame, textvariable=folder_var)
    entry.grid(row=0, column=1, padx=(2, 2), pady=2, sticky="ew")

    def browse_folder():
        path = filedialog.askdirectory(title="Choose Star Citizen folder (LIVE)")
        if path:
            folder_var.set(path)
    browse_btn = tk.Button(folder_frame, text="Browse", command=browse_folder)
    browse_btn.grid(row=0, column=2, padx=(2, 0), pady=2, sticky="e")

    var_cleanup = tk.BooleanVar(value=False)
    tk.Checkbutton(folder_frame, text="Remove temp Data folder", variable=var_cleanup)\
        .grid(row=1, column=0, padx=(2, 2), pady=(0, 2), sticky="w")

    analyze_btn = tk.Button(folder_frame, text="Analyze", state="disabled", bg="lightgray")
    analyze_btn.grid(row=1, column=1, padx=(2, 2), pady=(0, 2), sticky="e")

    generate_btn = tk.Button(folder_frame, text="Generate global.ini", state="disabled")
    generate_btn.grid(row=1, column=2, padx=(2, 0), pady=(0, 2), sticky="e")

    folder_frame.columnconfigure(1, weight=1)

    # --- Filters ---
    filters_group = ttk.LabelFrame(root, text="Attribute selection by category")
    filters_group.pack(fill="both", expand=False, padx=8, pady=(0, 8))
    filters_scroll = ScrollableFrame(filters_group, height=260)
    filters_scroll.pack(fill="both", expand=True, padx=2, pady=2)
    for c in range(2):
        filters_scroll.inner.grid_columnconfigure(c, weight=1)

    filter_vars = {}
    def clear_filters_ui():
        for w in list(filters_scroll.inner.winfo_children()):
            w.destroy()
        for c in range(2):
            filters_scroll.inner.grid_columnconfigure(c, weight=1)

    # --- Abbreviations & Format ---
    abbr_group = ttk.LabelFrame(root, text="Abbreviations & Format (Bracket Rules)")
    abbr_group.pack(fill="x", expand=False, padx=8, pady=(0, 8))

    _abbr_vars = {
        "Military": tk.StringVar(value="Mil"),
        "Civilian": tk.StringVar(value="Civ"),
        "Competition": tk.StringVar(value="Cmp"),
        "Industrial": tk.StringVar(value="Ind"),
        "Stealth": tk.StringVar(value="Stl"),
    }

    ttk.Label(abbr_group, text="Role-Mapping:").grid(row=0, column=0, sticky="w", padx=2, pady=(4, 2))
    role_frame = ttk.Frame(abbr_group); role_frame.grid(row=1, column=0, columnspan=12, sticky="ew", padx=2)
    for i, rname in enumerate(_abbr_vars.keys()):
        cell = ttk.Frame(role_frame); cell.grid(row=0, column=i, padx=2, pady=2, sticky="w")
        ttk.Label(cell, text=f"{rname} →").grid(row=0, column=0, sticky="e", padx=(0, 2))
        ttk.Entry(cell, textvariable=_abbr_vars[rname], width=8).grid(row=0, column=1, sticky="w")

    ttk.Separator(abbr_group).grid(row=2, column=0, columnspan=12, sticky="ew", pady=4)

    bar = ttk.Frame(abbr_group); bar.grid(row=3, column=0, columnspan=12, sticky="ew", padx=2, pady=(0, 2))
    var_size_prefix = tk.StringVar(value="S")
    var_size_pad = tk.IntVar(value=2)
    order_options = ("role", "size", "grade")
    var_order_1 = tk.StringVar(value="role")
    var_order_2 = tk.StringVar(value="size")
    var_order_3 = tk.StringVar(value="grade")

    ttk.Label(bar, text="Size prefix:").grid(row=0, column=0, sticky="e", padx=(0, 2))
    ttk.Entry(bar, textvariable=var_size_prefix, width=6).grid(row=0, column=1, sticky="w", padx=(0, 8))
    ttk.Label(bar, text="Pad:").grid(row=0, column=2, sticky="e", padx=(0, 2))
    ttk.Spinbox(bar, from_=0, to=4, width=4, textvariable=var_size_pad).grid(row=0, column=3, sticky="w", padx=(0, 8))
    ttk.Label(bar, text="Order:").grid(row=0, column=4, sticky="e", padx=(0, 2))
    ttk.Combobox(bar, width=9, values=order_options, textvariable=var_order_1, state="readonly").grid(row=0, column=5, padx=(0, 2))
    ttk.Combobox(bar, width=9, values=order_options, textvariable=var_order_2, state="readonly").grid(row=0, column=6, padx=(0, 2))
    ttk.Combobox(bar, width=9, values=order_options, textvariable=var_order_3, state="readonly").grid(row=0, column=7, padx=(0, 2))

    # --- Console ---
    console_frame = tk.Frame(root); console_frame.pack(fill="both", expand=True, padx=8, pady=(0, 8))
    console = StatusConsole(console_frame); console.pack(fill="both", expand=True)
    console.attach_generate_button(generate_btn)

    class GuiBridge:
        def __init__(self):
            self.console = console
            self._parsed = None
        def set_parsed_data(self, items, raw_text, catalog):
            self._parsed = (items, raw_text, catalog)
            clear_filters_ui()
            counts = Counter(it.get("category") for it in items if it.get("category"))
            cats_sorted = sort_categories(list(catalog.keys()))
            for idx, cat in enumerate(cats_sorted):
                attrs = catalog.get(cat, [])
                title = f"{CATEGORIES.get(cat, {}).get('title', cat)}  ({counts.get(cat, 0)} items)"
                box = ttk.LabelFrame(filters_scroll.inner, text=title)
                r, c = divmod(idx, 2)
                box.grid(row=r, column=c, sticky="nsew", padx=8, pady=6)
                filter_vars.setdefault(cat, {})
                grid = ttk.Frame(box); grid.pack(fill="x", padx=4, pady=(0, 2))
                if attrs:
                    for i, a in enumerate(attrs):
                        var = tk.BooleanVar(value=True)
                        filter_vars[cat][a] = var
                        tk.Checkbutton(grid, text=a.title(), variable=var, anchor="w")\
                            .grid(row=i // 3, column=i % 3, sticky="w", padx=6, pady=2)
                else:
                    tk.Label(grid, text="(No attributes detected)", fg="gray")\
                        .grid(row=0, column=0, sticky="w", padx=6, pady=2)
            generate_btn.config(state="normal")
        def get_parsed_data(self):
            return self._parsed
        def get_filter_config(self):
            sel = {}
            for cat, d in filter_vars.items():
                chosen = {a for a, v in d.items() if v.get()}
                if chosen:
                    sel[cat] = chosen
            return sel

    gui_bridge = GuiBridge()

    def settings():
        return {
            "filters_selected": gui_bridge.get_filter_config(),
            "abbr_map": {k: (v.get().strip() or default) for k, v, default in [
                ("Military", _abbr_vars["Military"], "Mil"),
                ("Civilian", _abbr_vars["Civilian"], "Civ"),
                ("Competition", _abbr_vars["Competition"], "Cmp"),
                ("Industrial", _abbr_vars["Industrial"], "Ind"),
                ("Stealth", _abbr_vars["Stealth"], "Stl"),
            ]},
            "formatting": {
                "size_prefix": var_size_prefix.get(),
                "size_pad": int(var_size_pad.get()),
                "order": [var_order_1.get(), var_order_2.get(), var_order_3.get()],
            },
            "cleanup_after_write": bool(var_cleanup.get()),
        }

    def on_folder_change(*_):
        path = folder_var.get()
        if path and os.path.isdir(path):
            analyze_btn.config(state="normal", bg="green")
        else:
            analyze_btn.config(state="disabled", bg="lightgray")
            generate_btn.config(state="disabled")
    folder_var.trace_add("write", on_folder_change); on_folder_change()

    def do_analyze():
        game_dir = folder_var.get().strip()
        if not os.path.isdir(game_dir):
            messagebox.showerror("Error", "Please choose a valid game directory."); return
        analyze_btn.config(state="disabled", bg="lightgray")
        generate_btn.config(state="disabled")
        # GUI-eigene Logzeile ist ok; Pipeline beginnt mit „Extraction“
        console.section("GUI"); console.log(f"Analyze with game directory: {game_dir}")
        threading.Thread(
            target=lambda: run_pipeline(gui_bridge, game_dir, None, settings() | {"mode": "analyze"}),
            daemon=True
        ).start()
    analyze_btn.config(command=do_analyze)

    def do_generate():
        game_dir = folder_var.get().strip()
        if not os.path.isdir(game_dir):
            messagebox.showerror("Error", "Please choose a valid game directory."); return
        # WICHTIG: Kein eigenes „Generate“-Logging mehr, nur Button sperren.
        generate_btn.config(state="disabled")
        threading.Thread(
            target=lambda: generate_from_gui(gui_bridge, game_dir, settings()),
            daemon=True
        ).start()
    generate_btn.config(command=do_generate)

    _ensure_target_width(root)
    return {"get_game_dir": lambda: folder_var.get().strip()}
