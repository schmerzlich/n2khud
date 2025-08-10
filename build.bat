@echo off
setlocal
title n2khud — clean onedir build

rem --- Pfade ---
set ROOT=%~dp0
set VENV=%ROOT%.venv
set DIST=%ROOT%dist\n2khud
set BUILD=%ROOT%build

echo === Clean old outputs ===
if exist "%DIST%" rmdir /s /q "%DIST%"
if exist "%BUILD%" rmdir /s /q "%BUILD%"

echo === Ensure venv ===
if not exist "%VENV%\Scripts\python.exe" (
  py -3 -m venv "%VENV%" || goto :err
)
call "%VENV%\Scripts\activate.bat"

echo === Install deps ===
python -m pip install -U pip wheel || goto :err
python -m pip install -U pyinstaller || goto :err

echo === Build onedir ===
pyinstaller --noconfirm --clean --onedir ^
  --name n2khud ^
  --icon resources\app.ico ^
  --add-data "resources;resources" ^
  --hidden-import tkinter --hidden-import queue --hidden-import re --hidden-import codecs ^
  main.py || goto :err

echo === Prune dist folder ===
rem Spezifikation, Batch-Skripte, Logs aus Distro entfernen (falls irgendwie hineingeraten)
del /q "%DIST%\*.spec" 2>nul
del /q "%DIST%\*.bat"  2>nul
del /q "%DIST%\*.log"  2>nul
del /q "%DIST%\log.log" 2>nul

rem Sicherstellen, dass KEIN unp4k versehentlich drin liegt
rmdir /s /q "%DIST%\unp4k-suite-v3.13.21" 2>nul
del /q "%DIST%\unp4k.exe" 2>nul
del /q "%DIST%\unforge.exe" 2>nul
del /q "%DIST%\unp4k.gui.exe" 2>nul

echo.
echo === DONE ===
echo Distro: "%DIST%"
echo Hinweis: Nutzer muss "unp4k-suite-v3.13.21" neben "%DIST%" bzw. neben n2khud.exe ablegen.
echo.
goto :eof

:err
echo Build failed. Aborting.
exit /b 1
