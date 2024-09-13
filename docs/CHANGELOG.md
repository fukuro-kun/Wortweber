# Changelog

Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/),
und dieses Projekt folgt der [Semantischen Versionierung](https://semver.org/lang/de/).

## [0.12.0] - 2024-09-13
### Changed
- Umfangreiches Refactoring zur Zentralisierung der Konfigurationseinstellungen in `config.py`
- Verbesserte Modularität und Wartbarkeit des Codes durch Nutzung zentraler Konfigurationsvariablen

### Improved
- Optimierte Struktur für einfachere zukünftige Anpassungen und Erweiterungen
- Verbesserte Konsistenz bei der Verwendung von Konfigurationseinstellungen im gesamten Projekt

### Fixed
- Behebung potenzieller Inkonsistenzen bei der Verwendung von Standardwerten

## [0.11.3] - 2024-09-13
   ### Fixed
   - Verbesserungen und Stabilisierung basierend auf Version 0.11.1
   - Aktualisierte Dokumentation zur Reflektion der neuesten Änderungen

   ### Changed
   - Zusammenführung der Dokumentationsänderungen aus verschiedenen Entwicklungszweigen

## [0.11.1] - 2024-09-13
### Fixed
- Korrektur von Stabilitätsproblemen bei der Audioaufnahme und -verarbeitung
- Behebung von Fehlern bei der Anzeige von Transkriptionen im GUI

### Improved
- Verbesserung der Zuverlässigkeit des Audioaufnahmeprozesses
- Optimierung der Fehlerprotokolle für eine bessere Diagnose von Problemen

### Note
- Diese Version stellt eine stabile Verbesserung gegenüber früheren Versionen dar und wird als aktuell empfohlene Version betrachtet.
- Aufgrund von Problemen in der nachfolgenden Version 0.11.2 wird empfohlen, bei dieser Version zu bleiben, bis eine neuere stabile Version veröffentlicht wird.


## [0.11.0] - 2024-09-12
### Added
- Implementierung der verzögerten Verarbeitung von Audioaufnahmen während des Modellladens
- Neue Methode zum Speichern und Wiederherstellen der Fensterposition und -größe
- Funktion zum Speichern manueller Textänderungen im Transkriptionsfenster

### Changed
- Umfangreiches Refactoring der GUI-Struktur:
  - Aufteilung der `wortweber_gui.py` in mehrere spezialisierte Module
  - Einführung separater Klassen für MainWindow, TranscriptionPanel, OptionsPanel, StatusPanel
  - Implementierung eines ThemeManagers für verbesserte Theme-Verwaltung
  - Erstellung eines dedizierten InputProcessors für Eingabehandlung
  - Einführung eines SettingsManagers für zentralisierte Einstellungsverwaltung
- Optimierte Handhabung des Eingabemodus zwischen Neustarts
- Verbesserte Fehlerbehandlung beim Laden des Whisper-Modells
- Aktualisierte GUI-Logik für konsistentere Benutzererfahrung

### Fixed
- Problem mit dem Zurücksetzen des Eingabemodus beim Neustart behoben
- Abstürze beim Beenden der Anwendung durch verbesserte Ressourcenfreigabe behoben
- Korrektur der Persistenz von Benutzereinstellungen über Sitzungen hinweg

### Improved
- Erhöhte Modularität und Wartbarkeit des GUI-Codes
- Verbesserte Trennung von Belangen innerhalb der GUI-Komponenten
- Erhöhte Stabilität der GUI-Funktionalität
- Verbesserte Benutzerfeedback-Mechanismen für Modellladestatus

## [0.10.0] - 2024-09-11
### Added
- Funktion zum Speichern und Laden von Benutzereinstellungen
- Automatisches Speichern der Fenstergröße und des Textfensterinhalts
- Wiederherstellung der letzten Einstellungen beim Programmstart

## [0.9.0] - 2024-09-11
### Changed
- Abschluss des Frontend-Backend-Refactorings
- Verbesserte Modularität und Wartbarkeit des Codes

## [0.8.2] - 2024-09-11
### Changed
- Verschoben `text_operations.py` in `backend/text_processor.py` für eine konsistentere Struktur
- Aktualisierte Importe in anderen Dateien, die `text_operations` verwenden

### Removed
- Entfernte die leere Datei `src/text_operations.py`

### Added
- Erweiterte Dokumentation zur neuen Struktur der Textoperationen im Backend

## [0.8.0] - 2024-09-11
### Changed
- Umfassendes Refactoring: Trennung von Frontend und Backend
- Verbesserung der Codestruktur und Modularität
- Anpassung der GUI an die neue Struktur

### Added
- Neue Backend-Struktur mit separaten Modulen für AudioProcessor, Transcriber und WordweberBackend
- Verbesserte Fehlerbehandlung und Logging
- Erweiterte Dokumentation zur neuen Projektstruktur

### Fixed
- Behebung von Problemen bei der Audioaufnahme und -verarbeitung
- Korrektur der Texthervorhebung und des Kontextmenüs gemäß ursprünglichen Spezifikationen

## [0.7.1] - 2024-09-11
### Added
- Option zum Ein-/Ausschalten des automatischen Kopierens in die Zwischenablage

## [0.7.0] - 2024-09-11
### Added
- Neue Zwischenablage-Option für die Texteingabe an der Systemcursor-Position
- Benutzerdefiniertes Eingabefeld für die Verzögerung bei zeichenweiser Eingabe

### Changed
- Verbesserte Benutzeroberfläche mit dynamischer Aktivierung/Deaktivierung von Verzögerungsoptionen

### Fixed
- Behebung eines Fehlers bei der Verwendung der Zwischenablagefunktion mit pynput

## [0.6.0] - 2024-09-11
### Changed
- Umfassendes Code-Refactoring zur Verbesserung der Struktur und Lesbarkeit
- Einführung von Klassen für bessere Kapselung: WordweberState, AudioProcessor, Transcriber, und WordweberGUI
- Verbesserte Fehlerbehandlung in kritischen Funktionen
- Hinzufügung ausführlicher Docstrings zu allen Klassen und Methoden
- Überarbeitung der Konfigurationsdatei mit Einführung von HIGHLIGHT_DURATION

### Added
- Neue Typ-Annotationen zur Verbesserung der Code-Qualität und Wartbarkeit
- Explizite Typüberprüfungen zur Behandlung potenzieller None-Werte

### Fixed
- Behebung von Problemen mit der asynchronen Modellladung
- Korrektur der Audiodatenverarbeitung für konsistentere Ergebnisse

## [0.5.1] - 2024-09-11
### Changed
- Korrigierte Beschreibung der Audioaufnahme und -verarbeitung in der Entwicklerdokumentation
- Implementierung der semantischen Versionierung

## [0.5.0] - 2024-09-10
### Added
- Dropdown-Menü zur Auswahl verschiedener Whisper-Modelle
- Anzeige der Transkriptionszeit für jede Aufnahme
- "Alles kopieren (Zwischenablage)" Button zur einfachen Übernahme des gesamten Transkriptionstexts
- Kontextmenü für das Transkriptionsfeld mit Optionen zum Ausschneiden, Kopieren, Einfügen und Löschen
- Eigene Implementierung für die Konvertierung von Zahlwörtern zu Ziffern und umgekehrt

### Changed
- Entfernung der Abhängigkeit von num2words
- Verbesserte Cursor-Sichtbarkeit im Transkriptionsfeld
- Neuer transkribierter Text wird nun an der Cursorposition eingefügt
- Asynchrones Laden des Whisper-Modells mit Ladeanzeige
- Entfernung des zusätzlichen Zeilenumbruchs am Ende des eingefügten Texts
- Temporäre Hervorhebung (2 Sekunden) des neu eingefügten Texts
- Verbessertes visuelles Feedback für das Whisper-Modell Dropdown-Menü
- Klarerer Text für den "Alles kopieren" Button
- Verbesserte Ladereihenfolge der GUI-Elemente für eine konsistentere Darstellung beim Start
- Entfernung unerwünschter Rahmen um bestimmte GUI-Elemente
- Feinabstimmung des visuellen Stils für eine einheitlichere Erscheinung
- Verbesserte GUI-Layout-Struktur für platzsparendere Anordnung
- Sprachauswahl und Modellauswahl nun oben links
- Anweisungen, Timer und Statusanzeigen oben rechts platziert

## [0.4.0] - 2024-09-10
### Changed
- Projekt umbenannt zu "Wortweber"
- Aktualisierte Dokumentation und Codebase, um den neuen Namen zu reflektieren

### Added
- Sprachauswahl-Funktionalität für Deutsch und Englisch
- Aktualisierte Konfigurationsdatei mit Spracheinstellungen
- DEVELOPMENT.md für umfassende Projektdokumentation hinzugefügt

## [0.3.0] - 2024-09-10
### Added
- Implementierung der Echtzeit-Transkription mit OpenAI Whisper
- GUI mit Tkinter für einfache Bedienung
- Push-to-Talk-Funktionalität mit F12-Taste
- Sprachauswahl (Deutsch/Englisch) in der Benutzeroberfläche

### Changed
- Optimierung der Audioaufnahme und -verarbeitung
- Verbesserung der Transkriptionsgenauigkeit

### Fixed
- Behebung von Problemen mit der ALSA-Audioschnittstelle

## [0.2.0] - 2024-09-10
### Added
- Grundlegende Audioaufnahmefunktionalität
- Integration des Whisper-Modells für Transkription
- Einfache Benutzeroberfläche zur Anzeige der Transkription

## [0.1.0] - 2024-09-09
### Added
- Initialisierung des Projekts
- Grundlegende Projektstruktur und Abhängigkeiten
