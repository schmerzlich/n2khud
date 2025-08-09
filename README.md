n2khud – Star Citizen global.ini Editor

(English version below / Englische Version siehe unten)

Übersicht

n2khud ist ein Desktop-Tool für Windows, mit dem die global.ini von Star Citizen extrahiert, analysiert und angepasst werden kann.Es ändert ausschließlich die Klammerinhalte hinter Item-Namen (z. B. (Military - Size 2) → (Mil S02)), um wichtige Attribute wie Klasse, Größe und Grade kompakt darzustellen.

Hauptfunktionen

Automatisches Entpacken der global.ini aus Data.p4k via unp4k.

Analyse und Kategorisierung aller Items in logische Gruppen.

GUI zur Attributauswahl (Class, Size, Grade) pro Kategorie.

Benutzerdefinierte Abkürzungen für Rollen (Mil, Civ, Cmp, Ind, Stl).

Formatregeln für Klammern (Reihenfolge, Size-Prefix, Padding).

Direkter Export der modifizierten global.ini in das deutsche Sprachverzeichnis von Star Citizen.

Automatische Aktualisierung der user.cfg.

Protokollierung aller Schritte in log.log.

Optionales Aufräumen des temporären Data-Ordners.

Voraussetzungen

Windows 10/11

Installiertes Star Citizen

Schreibrechte im Spielverzeichnis

unp4k.exe im Unterordner unp4k-suite-v3.13.21 neben der Anwendung

Installation

ZIP-Datei entpacken.

Sicherstellen, dass der Ordner unp4k-suite-v3.13.21 mit unp4k.exe im gleichen Verzeichnis wie n2khud.exe liegt.

Optional: config.json anpassen.

Nutzung

Spielverzeichnis wählen.

Analyze klicken.

Attribute auswählen.

Abkürzungen & Format einstellen.

Generate klicken.

Optional: Temporären Data-Ordner löschen lassen.

Lizenz – MIT License

Copyright (c) 2025 schmrzlch

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Third-Party Acknowledgements

This project uses the unp4k tool for extracting files from Star Citizen's Data.p4k archives.GitHub repository: https://github.com/dolkensp/unp4k

English version

Overview

n2khud is a Windows desktop tool to extract, analyze, and modify the global.ini file of Star Citizen.It only changes the bracketed parts after item names (e.g., (Military - Size 2) → (Mil S02)) to compactly display key attributes such as class, size, and grade.

Key Features

Automatic extraction of global.ini from Data.p4k via unp4k.

Analysis and categorization of all items.

GUI attribute selection per category.

Custom abbreviations for roles (Mil, Civ, Cmp, Ind, Stl).

Bracket formatting rules.

Direct export of modified global.ini into German localization folder.

Automatic update of user.cfg.

Logging of all steps.

Optional cleanup of the temporary Data folder.

License – MIT License

Copyright (c) 2025 schmrzlch

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Third-Party Acknowledgements

This project uses the unp4k tool for extracting files from Star Citizen's Data.p4k archives.GitHub repository: https://github.com/dolkensp/unp4k

