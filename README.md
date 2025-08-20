# n2khud – Star Citizen global.ini Editor  
*English version below*

---

## Übersicht

**n2khud** ist ein Desktop-Tool für Windows, mit dem die `global.ini` von Star Citizen extrahiert, analysiert und angepasst werden kann.  
Es fügt ausschließlich Klammerinhalte hinter Item-Namen hinzu (z. B. `Avalanche (Mil S02 A)`), um wichtige Attribute wie Klasse, Größe und Grade anzuzeigen und kompakt darzustellen.

---

## Hauptfunktionen

- **Automatisches Entpacken** der `global.ini` aus `Data.p4k` via **unp4k** (extern).
- **Analyse** und **Kategorisierung** aller Items in logische Gruppen.
- **GUI** zur Attributauswahl (Class, Size, Grade) pro Kategorie (z.B.: vehicle components).
- **Benutzerdefinierte Abkürzungen** für Rollen (Mil, Civ, Cmp, Ind, Stl).
- **Formatregeln** für Klammern (Reihenfolge, Size-Prefix, Padding).
- **Direkter Export** der modifizierten `global.ini` in das deutsche Sprachverzeichnis von Star Citizen.
- **Automatische Aktualisierung** der `user.cfg`.
- **Protokollierung** aller Schritte in `log.log`.
- **Optionales Aufräumen** des temporären `Data`-Ordners.

---

## Voraussetzungen

- Windows 10/11  
- Installiertes Star Citizen  
- Schreibrechte im Spielverzeichnis  
- **unp4k v3.13.21** (muss separat heruntergeladen werden)  

---

## Installation

1. **n2khud herunterladen und entpacken**  
   Lade `n2khud_v1_2_2.zip` von der Release-Seite herunter und entpacke den Inhalt in einen Ordner deiner Wahl.

2. **unp4k-Suite herunterladen**  
   Lade die **unp4k v3.13.21** ZIP-Datei hier herunter:  
   🔗 [https://github.com/dolkensp/unp4k/releases/tag/v3.13.21](https://github.com/dolkensp/unp4k/releases/tag/v3.13.21)

3. **unp4k Archiv neben n2khud.exe legen**
4. Wichtig: Entpacke den Ordner `unp4k-suite-v3.13.21` aus dem Download und platziere ihn **im gleichen Verzeichnis** wie `n2khud.exe`.

5. **Starten**  
   Doppelklicke `n2khud.exe`. Beim ersten Start wird die Integrität der `unp4k`-Dateien geprüft.

---

## Nutzung

1. Spielverzeichnis wählen (Verzeichnis `LIVE`- oder `PU`).  
2. "Revmove temp Data folder" anhaken, falls gewünscht. 
3. **Analyze** klicken.  
4. Attribute auswählen.  
5. Abkürzungen & Format einstellen.  
6. **Generate** klicken.  
7. Optional: temporären `Data`-Ordner löschen lassen.

---

## Deinstallation

Um **n2khud** vollständig zu entfernen:  

1. **Star Citizen-Daten anpassen**  
   - Lösche im `LIVE`- oder `PU`-Verzeichnis den Ordner:  
     ```
     Data\Localization\german_(germany)
     ```  
     (Falls vorhanden, ist dies der von n2khud erzeugte Sprachordner.)  
   - Lösche im `LIVE`- oder `PU`-Verzeichnis den Ordner `Data`, falls er nur von n2khud angelegt wurde und nicht mehr benötigt wird.

2. **user.cfg zurücksetzen oder entfernen**  
   - Datei `user.cfg` im `LIVE`-Ordner öffnen und die beiden Zeilen entfernen:  
     ```
     g_language = german_(germany)
     g_languageAudio = english
     ```  
     oder alternativ die gesamte Datei löschen.

3. **Programmdateien entfernen**  
   - Lösche den Ordner, in dem `n2khud.exe` liegt.  
   - Lösche den Ordner `unp4k-suite-v3.13.21`, sofern er nur für n2khud genutzt wird.

---

## Haftungsausschluss / Disclaimer

**Star Citizen** und alle zugehörigen geistigen Eigentumsrechte, Inhalte und Markenzeichen sind Eigentum von Cloud Imperium Games Corporation und deren Tochtergesellschaften.

Dieses Tool ist ein **inoffizielles Fanprojekt** und steht in keiner Verbindung zu Cloud Imperium Games oder deren verbundenen Unternehmen.

Alle Inhalte, die nicht vom Tool-Host oder dessen Nutzern stammen, sind Eigentum ihrer jeweiligen Rechteinhaber.

Offizielle Star Citizen Webseite: [https://robertsspaceindustries.com/](https://robertsspaceindustries.com/)

---

## Lizenz – MIT License

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

---

## Danksagungen (Third-Party Acknowledgements)

Dieses Projekt verwendet das Tool **unp4k** zum Extrahieren von Dateien aus Star Citizen's `Data.p4k`.  
GitHub-Repository: [https://github.com/dolkensp/unp4k](https://github.com/dolkensp/unp4k)  

---

# English version

---

## Overview

**n2khud** is a Windows desktop tool to extract, analyze, and modify the `global.ini` file of Star Citizen.  
It only adds bracketed parts after item names (e.g., `Avalanche (Mil S02 A)`) to compactly display key attributes such as class, size, and grade.

---

## Key Features

- **Automatic extraction** of `global.ini` from `Data.p4k` via **unp4k** (external).
- **Analysis** and **categorization** of all items.
- **GUI** attribute selection per category.
- **Custom abbreviations** for roles (Mil, Civ, Cmp, Ind, Stl).
- **Bracket formatting rules**.
- **Direct export** of modified `global.ini` into German localization folder.
- **Automatic update** of `user.cfg`.
- **Logging** of all steps.
- **Optional cleanup** of the temporary `Data` folder.

---

## Requirements

- Windows 10/11  
- Installed Star Citizen  
- Write permissions in the game directory  
- **unp4k v3.13.21** (must be downloaded separately)  

---

## Installation

1. **Download and extract n2khud**  
   Download `n2khud_v1_2_2.zip` from the release page and extract it to a folder of your choice.

2. **Download unp4k suite**  
   Download **unp4k v3.13.21** ZIP from here:  
   🔗 [https://github.com/dolkensp/unp4k/releases/tag/v3.13.21](https://github.com/dolkensp/unp4k/releases/tag/v3.13.21)

3. **Place unp4k archive next to n2khud.exe**
4. Important: Extract the `unp4k-suite-v3.13.21` folder from the download and place it **in the same directory** as `n2khud.exe`.

5. **Run**  
   Double-click `n2khud.exe`. On first start, the integrity of the `unp4k` files will be verified.

---

## Usage

1. Select the game directory (Direcory `LIVE`- or `PU`).
2. Check "Remove temp Data folder" if wanted.
3. Click **Analyze**.  
4. Select attributes.  
5. Adjust abbreviations & format.  
6. Click **Generate**.  
7. Optionally delete the temporary `Data` folder.

---

## Uninstallation

To completely remove **n2khud**:  

1. **Clean up Star Citizen data**  
   - Delete the folder:  
     ```
     Data\Localization\german_(germany)
     ```  
     inside the `LIVE` or `PU` directory (if it was created by n2khud).  
   - Delete the `Data` folder inside `LIVE` or `PU` if it was only created by n2khud and is no longer needed.

2. **Reset or remove user.cfg**  
   - Open `user.cfg` inside the `LIVE` folder and remove the two lines:  
     ```
     g_language = german_(germany)
     g_languageAudio = english
     ```  
     or delete the entire file.

3. **Remove program files**  
   - Delete the folder containing `n2khud.exe`.  
   - Delete the folder `unp4k-suite-v3.13.21` if it was only used for n2khud.

---

## Disclaimer

**Star Citizen** and all associated intellectual property, content, and trademarks are owned by Cloud Imperium Games Corporation and its subsidiaries.

This tool is an **unofficial fan project** and is not affiliated with Cloud Imperium Games or any of its affiliated companies.

All content not created by the tool’s host or its users remains the property of their respective owners.

Official Star Citizen website: [https://robertsspaceindustries.com/](https://robertsspaceindustries.com/)

---

## Lizenz – MIT License

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

---

## Third-Party Acknowledgements

This project uses the **unp4k** tool for extracting files from Star Citizen's `Data.p4k` archives.  
GitHub repository: [https://github.com/dolkensp/unp4k](https://github.com/dolkensp/unp4k)  
