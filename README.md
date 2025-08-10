# n2khud – Star Citizen global.ini Editor  
*English version below*

---

## Übersicht

**n2khud** ist ein Desktop-Tool für Windows, mit dem die `global.ini` von Star Citizen extrahiert, analysiert und angepasst werden kann.  
Es fügt ausschließlich die Klammerinhalte hinter Item-Namen hinzu (z. B. `Avalanche (Mil S02 A)`), um wichtige Attribute wie Klasse, Größe und Grade kompakt darzustellen.

---

## Hauptfunktionen

- **Automatisches Entpacken** der `global.ini` aus `Data.p4k` via **unp4k** (extern).
- **Analyse** und **Kategorisierung** aller Items in logische Gruppen.
- **GUI** zur Attributauswahl (Class, Size, Grade) pro Kategorie.
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
   Lade `n2khud_v1_2_0.zip` von der Release-Seite herunter und entpacke den Inhalt in einen Ordner deiner Wahl.

2. **unp4k-Suite herunterladen**  
   Lade die **unp4k v3.13.21** ZIP-Datei hier herunter:  
   🔗 [https://github.com/dolkensp/unp4k/releases/tag/v3.13.21](https://github.com/dolkensp/unp4k/releases/tag/v3.13.21)

3. **unp4k neben n2khud.exe legen**  
   Entpacke den Ordner `unp4k-suite-v3.13.21` aus dem Download und platziere ihn **im gleichen Verzeichnis** wie `n2khud.exe`.

4. **Starten**  
   Doppelklicke `n2khud.exe`. Beim ersten Start wird die Integrität der `unp4k`-Dateien geprüft.

---

## Nutzung

1. Spielverzeichnis wählen.  
2. **Analyze** klicken.  
3. Attribute auswählen.  
4. Abkürzungen & Format einstellen.  
5. **Generate** klicken.  
6. Optional: temporären `Data`-Ordner löschen lassen.

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

## Lizenz – MIT License

Copyright (c) 2025 schmrzlch

[... Lizenztext unverändert beibehalten ...]

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
   Download `n2khud_v1_2_0.zip` from the release page and extract it to a folder of your choice.

2. **Download unp4k suite**  
   Download **unp4k v3.13.21** ZIP from here:  
   🔗 [https://github.com/dolkensp/unp4k/releases/tag/v3.13.21](https://github.com/dolkensp/unp4k/releases/tag/v3.13.21)

3. **Place unp4k next to n2khud.exe**  
   Extract the `unp4k-suite-v3.13.21` folder from the download and place it **in the same directory** as `n2khud.exe`.

4. **Run**  
   Double-click `n2khud.exe`. On first start, the integrity of the `unp4k` files will be verified.

---

## Usage

1. Select the game directory.  
2. Click **Analyze**.  
3. Select attributes.  
4. Adjust abbreviations & format.  
5. Click **Generate**.  
6. Optionally delete the temporary `Data` folder.

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

## License – MIT License

Copyright (c) 2025 schmrzlch

[... license text unchanged ...]

---

## Third-Party Acknowledgements

This project uses the **unp4k** tool for extracting files from Star Citizen's `Data.p4k` archives.  
GitHub repository: [https://github.com/dolkensp/unp4k](https://github.com/dolkensp/unp4k)  
