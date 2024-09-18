# Wortweber: Entwicklungsdokumentation

## Projektübersicht
Wortweber ist ein Python-basiertes Einzelentwickler-Projekt zur Echtzeit-Transkription von Sprache in Text. Es nutzt das OpenAI Whisper-Modell für die Spracherkennung und bietet eine benutzerfreundliche grafische Oberfläche mit Push-to-Talk-Funktionalität.

## Projektstruktur
```
Wortweber/
├── src/
│   ├── backend/
│   │   ├── __init__.py
│   │   ├── audio_processor.py
│   │   ├── wortweber_transcriber.py
│   │   ├── text_processor.py
│   │   ├── wortweber_backend.py
│   │   └── wortweber_utils.py
│   ├── frontend/
│   │   ├── __init__.py
│   │   ├── wortweber_gui.py
│   │   ├── main_window.py
│   │   ├── transcription_panel.py
│   │   ├── options_panel.py
│   │   ├── status_panel.py
│   │   ├── theme_manager.py
│   │   ├── input_processor.py
│   │   ├── settings_manager.py
│   │   ├── context_menu.py
│   │   └── options_window.py
│   ├── utils/
│   │   └── error_handling.py
│   ├── __init__.py
│   ├── config.py
│   └── wortweber.py
├── tests/
│   ├── backend/
│   │   ├── __init__.py
│   │   ├── test_audio_processor.py
│   │   ├── test_audio_recording.py
│   │   └── test_transcription.py
│   ├── test_data/
│   │   └── speech_sample.wav
│   ├── __init__.py
│   ├── base_test.py
│   ├── test_config.py
│   ├── test_parallel_transcription.py
│   └── test_sequential_transcription.py
├── docs/
│   ├── README.md
│   ├── CHANGELOG.md
│   ├── DEVELOPMENT.md
│   ├── REFACTORING_NOTES.md
│   └── TODO.md
├── LICENSE
├── NOTICE
├── THIRD_PARTY_LICENSES.md
├── requirements.txt
├── install_and_test.sh
├── VERSION
├── run_tests.py
└── .gitignore
```

## Hauptfunktionen
1. Echtzeit-Audioaufnahme mit Push-to-Talk (F12-Taste)
2. Transkription mit verschiedenen Whisper-Modellen (tiny, base, small, medium, large)
3. Sprachauswahl (Deutsch/Englisch)
4. Automatisches Kopieren der Transkription in die Zwischenablage
5. Anzeige der Transkriptionszeit
6. Kontextmenü für Textbearbeitung
7. Zahlwort-zu-Ziffer und Ziffer-zu-Zahlwort Konvertierung
8. Verschiedene Eingabemodi: Textfenster, Systemcursor-Position mit Verzögerungsoptionen
9. Theme-Auswahl für die GUI
10. Speichern und Laden von Benutzereinstellungen

## Technische Details
- Python 3.11
- OpenAI Whisper (Version 20231117)
- PyAudio für Audioaufnahme
- Tkinter für GUI
- NumPy und SciPy für Signalverarbeitung
- pynput für Tastatureingabe-Simulation
- ttkthemes für erweiterte GUI-Themes

## Lizenzierung
Wortweber ist unter der GNU General Public License v3.0 (GPLv3) lizenziert. Dies hat wichtige Auswirkungen auf die Entwicklung und Verteilung des Projekts:

- Alle Änderungen und Erweiterungen des Codes müssen ebenfalls unter der GPLv3 oder einer kompatiblen Lizenz veröffentlicht werden.
- Bei der Verteilung des Programms (in Quell- oder Binärform) muss der vollständige Quellcode mitgeliefert oder zugänglich gemacht werden.
- Die Verwendung von Bibliotheken muss sorgfältig geprüft werden, um Lizenzkompatibilität sicherzustellen.
- Besondere Aufmerksamkeit gilt der Verwendung von pynput (LGPL), das als dynamisch verlinkte Bibliothek genutzt wird.

Entwickler sollten sich mit den Bedingungen der GPLv3 vertraut machen und sicherstellen, dass alle Beiträge und Änderungen konform sind.

## Entwicklungsworkflow
1. Arbeiten auf dem `main`-Branch für kleinere Änderungen
2. Erstellen von Feature-Branches für größere Funktionen: `git checkout -b feature/neue-funktion`
3. Regelmäßige Commits mit aussagekräftigen Nachrichten
4. Vor dem Merge in `main`, Rebase durchführen: `git rebase main`
5. Merge in `main` mit `--no-ff` Flag: `git checkout main && git merge --no-ff feature/neue-funktion`
6. Für Releases, annotierte Tags erstellen: `git tag -a v0.x.x -m "Version 0.x.x"`

## Installation und Einrichtung
1. Repository klonen: `git clone https://github.com/fukuro-kun/Wortweber.git`
2. In das Projektverzeichnis wechseln: `cd Wortweber`
3. Installationsskript ausführen: `bash install_and_test.sh`
4. Anwendung starten: `python src/wortweber.py`

## Fehlerbehandlung und Logging
- Zentrale Fehlerbehandlung in `src/utils/error_handling.py`
- Verwendung des `@handle_exceptions` Decorators für alle öffentlichen Methoden
- Konsistente Logging-Levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Log-Datei: `wortweber.log` im Projekthauptverzeichnis

## Testabdeckung
- Unittest-Framework für Backend- und Integrationstests
- Parallelisierte Tests für effiziente Ausführung
- Testdaten im `tests/test_data/` Verzeichnis

## Codekonventionen und Kommentierungsrichtlinien
- PEP 8 Stilrichtlinien strikt befolgen
- Docstrings für alle Klassen und öffentlichen Methoden:
  - Kurze Beschreibung der Funktionalität
  - Parameter und Rückgabewerte dokumentieren
  - Beispiele für komplexe Funktionen hinzufügen
- Inline-Kommentare für komplexe Logik:
  - Erklären Sie das "Warum", nicht nur das "Was"
  - Kommentare aktuell halten bei Code-Änderungen
- Copyright-Informationen am Anfang jeder Datei
- Gruppierung von Importen:
  1. Standardbibliotheken
  2. Drittanbieterbibliotheken
  3. Projektspezifische Module
- Verwendung von absoluten Importen für bessere Lesbarkeit
- Am Ende jeder Datei einen Abschnitt "Zusätzliche Erklärungen" für besonders komplexe Konzepte hinzufügen
- Bei Codeänderungen bestehende Kommentare erhalten und bei Bedarf aktualisieren
- Kommentare in deutscher Sprache verfassen

## Versionierung
- Semantische Versionierung (MAJOR.MINOR.PATCH)
- VERSION-Datei im Hauptverzeichnis für aktuelle Versionsnummer
- Git-Tags für jede Version: `v0.x.x`

## Wichtige Hinweise
- ALSA-Warnungen können in den meisten Fällen ignoriert werden
- Bei Audiogeräte-Problemen DEVICE_INDEX in config.py anpassen
- Regelmäßige Überprüfung auf Sicherheitsupdates für Abhängigkeiten
- Stellen Sie bei der Verwendung und Integration von Bibliotheken die Kompatibilität mit der GPLv3 sicher
- Achten Sie besonders auf die korrekte Verwendung von pynput als dynamisch verlinkte Bibliothek gemäß LGPL

## Beitrag zum Projekt
1. Fork des Repositories auf GitHub
2. Feature-Branch erstellen: `git checkout -b feature/neue-funktion`
3. Änderungen committen: `git commit -am 'Füge neue Funktion hinzu'`
4. Zum Branch pushen: `git push origin feature/neue-funktion`
5. Pull Request erstellen

## Kontakt
Bei Fragen oder Problemen ein Issue auf GitHub erstellen oder sich an den Projektbetreuer wenden.

## Historie

### Version 0.21.2
- Wechsel der Projektlizenz von Apache License 2.0 zu GNU General Public License v3.0 (GPLv3)
- Aktualisierung aller Quelldateien mit dem neuen GPLv3-Lizenztext
- Anpassung der Projektdokumentation zur Reflexion der neuen Lizenzbestimmungen

### Version 0.18.0 (aktuell)
- Implementierung einer einheitlichen Fehlerbehandlungs- und Logging-Strategie
- Einführung des `@handle_exceptions` Decorators
- Zentralisierung der Logging-Konfiguration

### Version 0.17.3
- Verbesserung der Ressourcenverwaltung in AudioProcessor
- Erhöhung der Typsicherheit im Transcriber

### Version 0.17.1
- Implementierung von Farbvorschau-Funktionalität
- Optimierung der Farbauswahl-Performance

### Version 0.17.0
- Einführung benutzerdefinierter Farbauswahl für erhöhte Personalisierung
- Integration des tkcolorpicker für Farbauswahl

### Version 0.16.1
- Verbesserung der Testausführungslogik
- Einführung von Kurzformen für Kommandozeilenoptionen bei Tests

### Version 0.16.0
- Implementierung von parallelen Transkriptionstests
- Einführung von GPU-Ressourcenüberprüfung

### Version 0.15.1
- Behebung von Gerätekompatibilitätsproblemen
- Optimierung der Audiovorverarbeitung

### Version 0.15.0
- Implementierung der Testaufnahme-Funktion
- Erweiterung der Tests für AudioProcessor

### Version 0.14.0
- Umfassende Kommentierung des gesamten Quellcodes
- Einführung einheitlicher Kommentierungsrichtlinien

### Version 0.13.0 - 0.11.0
- Implementierung des Optionsmenüs mit Textgrößenanpassung
- Umfangreiches GUI-Refactoring zur Verbesserung der Modularität
- Einführung von Klassen für MainWindow, TranscriptionPanel, OptionsPanel, StatusPanel
- Implementierung eines ThemeManagers und SettingsManagers

### Version 0.10.0 - 0.1.0
- Implementierung der Echtzeit-Transkription mit OpenAI Whisper
- Entwicklung der grundlegenden GUI mit Tkinter
- Einführung der Push-to-Talk-Funktionalität
- Implementierung verschiedener Eingabemodi und Verzögerungsoptionen
- Initialisierung des Projekts und Aufbau der Grundstruktur
