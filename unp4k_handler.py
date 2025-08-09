# unp4k_handler.py  # V1.6.2
# Was gefixt wurde:
# - unp4k-Konsole startet unter Windows minimiert (SW_SHOWMINNOACTIVE).
#   Fallback: Falls Minimize nicht verfügbar, ohne Fenster (CREATE_NO_WINDOW).
#
# Was funktioniert:
# - Start von unp4k.exe im Arbeitsverzeichnis (cwd=work_dir).
# - Rückgabe als Tupel (ok: bool, output: str), kombinierte Stdout/Stderr.
# - Plattformneutraler Betrieb; Spezialbehandlung nur auf Windows.

import subprocess, os

def run_unp4k(work_dir, p4k_path, pattern="*.ini"):
    """
    Führt unp4k im angegebenen Arbeitsordner aus und gibt (ok: bool, output: str) zurück.
    ok == True bei Returncode 0.
    """
    unp4k_exe = os.path.join(work_dir, "unp4k.exe")
    if not os.path.isfile(unp4k_exe):
        return False, f"unp4k.exe nicht gefunden unter {unp4k_exe}"
    if not os.path.isfile(p4k_path):
        return False, f"Data.p4k nicht gefunden unter {p4k_path}"

    cmd = [unp4k_exe, p4k_path, pattern]

    try:
        creationflags = 0
        startupinfo = None

        if os.name == "nt":
            # Bevorzugt: neues Konsolenfenster, minimiert (stört die GUI nicht).
            creationflags = getattr(subprocess, "CREATE_NEW_CONSOLE", 0)
            try:
                si = subprocess.STARTUPINFO()
                si.dwFlags |= getattr(subprocess, "STARTF_USESHOWWINDOW", 0x00000001)
                si.wShowWindow = 7  # SW_SHOWMINNOACTIVE
                startupinfo = si
            except Exception:
                # Fallback: gar kein Fenster anzeigen (verhindert Überdeckung sicher)
                creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)

        proc = subprocess.run(
            cmd,
            cwd=work_dir,
            capture_output=True,
            text=True,
            creationflags=creationflags,
            startupinfo=startupinfo
        )

        out = (proc.stdout or "")
        if proc.stderr:
            out = (out + ("\n" if out else "")) + proc.stderr

        ok = (proc.returncode == 0)
        return ok, (out.strip() if out else "")
    except Exception as e:
        return False, f"Fehler beim Start von unp4k: {e}"
