# ---- status_console.py ----  V1.5
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from queue import Queue, Empty
import time
import re

_FINISH_RE = re.compile(r"finish\s*[—-]\s*exit\s*program", re.IGNORECASE)

class StatusConsole(tk.Frame):
    def __init__(self, master, poll_ms: int = 80, tick_ms: int = 100):
        super().__init__(master)

        # Stil für grünen Progressbar
        self._style = ttk.Style()
        try:
            self._style.configure(
                "green.Horizontal.TProgressbar",
                troughcolor="#1e1e1e",
                background="#2ecc71"
            )
        except Exception:
            pass

        # Kopfzeile: Status | Progress | Timer
        top = tk.Frame(self)
        top.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 4))
        self._step_title_var = tk.StringVar(value="—")
        self._timer_var = tk.StringVar(value="(00.000 s)")

        self._lbl_step = tk.Label(top, textvariable=self._step_title_var, anchor="w")
        self._lbl_step.grid(row=0, column=0, sticky="w", padx=(0, 6))

        self._progress = ttk.Progressbar(
            top, orient="horizontal", mode="determinate",
            style="green.Horizontal.TProgressbar", maximum=100, length=200
        )
        self._progress.grid(row=0, column=1, sticky="ew", padx=6)

        self._lbl_timer = tk.Label(top, textvariable=self._timer_var, anchor="e", fg="blue")
        self._lbl_timer.grid(row=0, column=2, sticky="e", padx=(6, 0))

        top.columnconfigure(1, weight=1)

        # Textkonsole
        self.text = tk.Text(self, height=12, state="disabled", wrap="word")
        self.scroll = tk.Scrollbar(self, command=self.text.yview)
        self.text.configure(yscrollcommand=self.scroll.set)
        self.text.grid(row=1, column=0, sticky="nsew")
        self.scroll.grid(row=1, column=1, sticky="ns")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Queue & Timer/Progress-Status
        self._q = Queue()
        self._poll_ms = poll_ms
        self._tick_ms = tick_ms
        self._step_start = None
        self._timer_running = False
        self._generate_btn = None

        # Fortschritts-Parameter
        self._secs_for_full = 40.0   # Zeit, in der 100 % erreicht wären
        self._stall_at = 97.0        # bis hierhin "faken", dann warten
        self._progress_value = 0.0

        # Generate-Lock (verhindert Neustarts während Generate)
        self._gen_lock_active = False

        self.after(self._poll_ms, self._drain_queue)
        self.after(self._tick_ms, self._tick)

    # Optional: Button anhängen, um ihn bei Ready/Finish zu aktivieren/färben
    def attach_generate_button(self, btn):
        self._generate_btn = btn

    @staticmethod
    def _fmt_elapsed(delta: float) -> str:
        delta = max(0.0, delta)
        secs = int(delta)
        msec = int(round((delta - secs) * 1000))
        return f"({secs:02d}.{msec:03d} s)"

    def _elapsed_str(self) -> str:
        if self._step_start is None:
            return "(00.000 s)"
        return self._fmt_elapsed(time.monotonic() - self._step_start)

    # --- Timer/Progress-Steuerung ---
    def _reset_progress(self):
        self._progress_value = 0.0
        try:
            self._progress['value'] = 0.0
        except Exception:
            pass

    def _complete_progress(self):
        self._progress_value = 100.0
        try:
            self._progress['value'] = 100.0
        except Exception:
            pass

    def _start_timer(self):
        self._step_start = time.monotonic()
        self._timer_running = True
        self._timer_var.set("(00.000 s)")
        self._reset_progress()
        # Bei neuem Schritt: Generate-Button neutral/deaktiviert
        if self._generate_btn:
            try:
                self._generate_btn.config(bg="", state="disabled")
            except Exception:
                pass

    def _freeze_timer(self):
        self._timer_running = False

    def _enable_generate_green(self):
        if self._generate_btn:
            try:
                self._generate_btn.config(bg="green", state="normal")
            except Exception:
                pass

    def _freeze_timer_and_enable_generate(self):
        self._freeze_timer()
        self._enable_generate_green()
        self._complete_progress()

    def _enqueue(self, msg: str, level: str):
        ts = datetime.now().strftime("%H:%M:%S")
        elapsed = self._elapsed_str()
        line = f"[{ts}] [{level}] {msg}  {elapsed}\n"
        self._q.put(line)

        text = (msg or "").strip()

        # Ready: Button grün, Timer einfrieren (wartet auf Klick)
        if level == "OK" and "Choose attributes and click 'Generate'." in text:
            self._freeze_timer_and_enable_generate()
            return

        # Finaler Stopp UND erneutes Freigeben des Generate-Buttons
        if level == "OK" and _FINISH_RE.search(text):
            self._freeze_timer()
            self._gen_lock_active = False
            self._enable_generate_green()
            self._complete_progress()
            return

    # Öffentliche API
    def log(self, msg: str, level: str = "INFO"):
        self._enqueue(msg, level)

    def section(self, title: str):
        t = (title or "").strip()
        tl = t.lower()

        # Neuer Abschnitt beendet den alten -> Progress auf 100 %
        if self._timer_running:
            self._complete_progress()

        # Beim ersten „Generate“: Timer starten & Lock aktivieren
        if "generate" in tl and not self._gen_lock_active:
            self._gen_lock_active = True
            self._start_timer()
            self._step_title_var.set("— Generate —")
            self._enqueue("— Generate —", "STEP")
            return

        # Solange Generate-Lock aktiv ist: keine Neustarts durch Sub-Schritte
        if self._gen_lock_active:
            self._enqueue(f"— {t} —", "STEP")
            return

        # Normalfall (Analyse etc.): Timer pro Abschnitt neu starten
        self._start_timer()
        self._step_title_var.set(f"— {t} —")
        self._enqueue(f"— {t} —", "STEP")

    def ok(self, msg: str):
        self._enqueue(msg, "OK")

    def error(self, msg: str):
        self._enqueue(msg, "ERROR")

    def info(self, msg: str):
        self._enqueue(msg, "INFO")

    # Interna
    def _drain_queue(self):
        try:
            while True:
                line = self._q.get_nowait()
                self.text.configure(state="normal")
                self.text.insert("end", line)
                self.text.see("end")
                self.text.configure(state="disabled")
        except Empty:
            pass
        finally:
            self.after(self._poll_ms, self._drain_queue)

    def _tick(self):
        # Timer
        if self._timer_running:
            self._timer_var.set(self._elapsed_str())
            # „Gefakter“ Fortschritt bis 97 %
            try:
                elapsed = time.monotonic() - (self._step_start or time.monotonic())
                pct = (elapsed / max(0.001, self._secs_for_full)) * 100.0
                pct = min(self._stall_at, pct)
                if pct > self._progress_value:
                    self._progress_value = pct
                    self._progress['value'] = pct
            except Exception:
                pass
        self.after(self._tick_ms, self._tick)
