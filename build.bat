@echo off
setlocal ENABLEDELAYEDEXPANSION

REM === build.bat — V0.1 ===
REM Einstellungen
set APPNAME=n2khud
set ICON=resources\app.ico
set RES=resources
set UNP4K_DIR=unp4k-suite-v3.13.21
set PY=py -3.11
set CONSOLE=no  REM yes|no

echo === Clean ===
if exist build rd /s /q build
if exist dist\%APPNAME% rd /s /q dist\%APPNAME%
if exist %APPNAME%.spec del %APPNAME%.spec

echo === PyInstaller installieren (falls nötig) ===
%PY% -m pip install -U pip wheel >nul 2>&1
%PY% -m pip show pyinstaller >nul 2>&1 || %PY% -m pip install pyinstaller

echo === Build ===
set CONSOLE_FLAG=--noconsole
if /I "%CONSOLE%"=="yes" set CONSOLE_FLAG=--console

%PY% -m PyInstaller ^
  --onedir ^
  --noconfirm ^
  %CONSOLE_FLAG% ^
  --name %APPNAME% ^
  --icon=%ICON% ^
  --add-data "%RES%;%RES%" ^
  --hidden-import=tkinter ^
  --hidden-import=queue ^
  --hidden-import=re ^
  --hidden-import=codecs ^
  main.py

if errorlevel 1 (
  echo Build failed.
  exit /b 1
)

echo === Externe unp4k-Suite bereitstellen ===
if exist "%UNP4K_DIR%" (
  xcopy "%UNP4K_DIR%" "dist\%APPNAME%\%UNP4K_DIR%" /E /I /Y >nul
) else (
  echo Hinweis: "%UNP4K_DIR%" wurde nicht gefunden. Bitte manuell neben die EXE legen.
)

echo === Fertig ===
echo Dist: .\dist\%APPNAME%\
endlocal
