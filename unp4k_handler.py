# unp4k_handler.py  # V1.7
# Was gefixt wurde:
# - SHA256-Integritätsprüfung für unp4k.exe hinzugefügt.
# - Script verweigert Ausführung, wenn der Hash nicht mit dem bekannten Wert übereinstimmt.
# Was funktioniert:
# - unp4k.exe wird nur ausgeführt, wenn sie exakt dem erwarteten Hash entspricht.
# - Erfolgs-/Fehlerausgabe bleibt wie gehabt.

import subprocess, os, hashlib

# Erwarteter SHA256-Hash der unp4k.exe (Beispielwert – anpassen!)
EXPECTED_SHA256 = "a4b40d8a741ad50a1757ce82bb552a773aa62a386b82a7028c751272608aac2f"

def _file_sha256(path, buf_size=65536):
    """Berechnet den SHA256-Hash einer Datei."""
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            data = f.read(buf_size)
            if not data:
                break
            sha256.update(data)
    return sha256.hexdigest()

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

    # Hash-Prüfung
    actual_hash = _file_sha256(unp4k_exe)
    if actual_hash.lower() != EXPECTED_SHA256.lower():
        return False, (
            f"Integritätsprüfung fehlgeschlagen!\n"
            f"Gefundener SHA256: {actual_hash}\n"
            f"Erwartet: {EXPECTED_SHA256}"
        )

    cmd = [unp4k_exe, p4k_path, pattern]
    try:
        proc = subprocess.run(cmd, cwd=work_dir, capture_output=True, text=True)
        out = (proc.stdout or "") + (("\n" + proc.stderr) if proc.stderr else "")
        ok = (proc.returncode == 0)
        return ok, out.strip()
    except Exception as e:
        return False, f"Fehler beim Start von unp4k: {e}"
