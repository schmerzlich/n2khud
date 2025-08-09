:: ---- build.cmd (V0.1) ----
@echo off
setlocal

:: 1) Python wählen (bevorzugt 3.11)
for %%P in ("py -3.11" "py -3.10" "python" "py") do (
  call %%~P -c "import sys;print(sys.version)" >nul 2>nul && set "PYCMD=%%~P" & goto :found
)
echo Kein passendes Python gefunden. Bitte Python 3.11 installieren.
exit /b 1
:found

:: 2) venv anlegen (falls fehlt)
if not exist ".venv\Scripts\python.exe" (
  echo Erzeuge .venv …
  %PYCMD% -m venv .venv || exit /b 1
)

set VENV_PY=.venv\Scripts\python.exe
if not exist "%VENV_PY%" (
  echo Venv defekt: %VENV_PY% nicht gefunden.
  exit /b 1
)

:: 3) Pip/Tools
%VENV_PY% -m pip install -U pip || exit /b 1
%VENV_PY% -m pip install -U pyinstaller || exit /b 1

:: 4) Build
.\.venv\Scripts\pyinstaller.exe --clean --noconfirm n2khud.spec || exit /b 1

echo Fertig. Ausgabe: dist\n2khud\
endlocal
