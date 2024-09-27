# Wortweber: Entwicklungsdokumentation

## 1. Projektübersicht
Wortweber ist eine Python-basierte Anwendung zur Echtzeit-Sprachtranskription mit KI, die nun durch ein leistungsfähiges Plugin-System erweitert wurde. Das Projekt nutzt das OpenAI Whisper-Modell für die Spracherkennung und bietet eine benutzerfreundliche grafische Oberfläche mit Push-to-Talk-Funktionalität und Plugin-Unterstützung.

## 2. Aktuelle Entwicklungsschwerpunkte
- Optimierung und Erweiterung des neu implementierten Plugin-Systems
- Verbesserung der Benutzeroberfläche für Plugin-Verwaltung und -Konfiguration
- Erweiterung der Plugin-API und -Dokumentation für Drittentwickler
- Entwicklung zusätzlicher Beispiel-Plugins zur Demonstration der Systemfähigkeiten
- Verbesserung der Audiogeräteauswahl und -verwaltung

## 3. Nächste geplante Features
1. Erweiterte Dokumentation für Drittentwickler
2. Erweiterung der Plugin-Schnittstellen für tiefere Integration in die Kernfunktionalität
3. Überarbeitung der GUI und Tooltips überall

## 4. Hauptfunktionen
1. Echtzeit-Audioaufnahme mit Push-to-Talk
2. KI-basierte Transkription mit verschiedenen Whisper-Modellen
3. Mehrsprachige Unterstützung (aktuell Deutsch/Englisch)
4. Plugin-System für erweiterbare Funktionalität
5. Textverarbeitungsoptionen (inkl. Zahlwort-Konvertierung)
6. Anpassbare Benutzeroberfläche mit Theming-Unterstützung
7. Einstellungsverwaltung inkl. Plugin-Konfigurationen

## 5. Projektstruktur
```
Wortweber/
├── docs/
│   ├── CHANGELOG.md
│   ├── DEVELOPMENT.md
│   ├── PLUGINSYSTEM.md
│   ├── REFACTORING_NOTES.md
│   └── TODO.md
├── logs/
│   └── wortweber.log
├── plugins/
│   ├── README.md
│   └── text_transformer.py
├── src/
│   ├── backend/
│   │   ├── __init__.py
│   │   ├── audio_processor.py
│   │   ├── text_processor.py
│   │   ├── wortweber_backend.py
│   │   ├── wortweber_transcriber.py
│   │   └── wortweber_utils.py
│   ├── frontend/
│   │   ├── __init__.py
│   │   ├── audio_options_panel.py
│   │   ├── context_menu.py
│   │   ├── input_processor.py
│   │   ├── main_window.py
│   │   ├── options_panel.py
│   │   ├── options_window.py
│   │   ├── plugin_management_window.py
│   │   ├── settings_manager.py
│   │   ├── shortcut_panel.py
│   │   ├── status_panel.py
│   │   ├── theme_manager.py
│   │   ├── transcription_panel.py
│   │   └── wortweber_gui.py
│   ├── plugin_system/
│   │   ├── __init__.py
│   │   ├── plugin_interface.py
│   │   ├── plugin_loader.py
│   │   └── plugin_manager.py
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
│   │   ├── test_text_processor.py
│   │   └── test_transcription.py
│   ├── frontend/
│   │   ├── test_main_window.py
│   │   ├── test_options_panel.py
│   │   ├── test_status_panel.py
│   │   ├── test_transcription_panel.py
│   │   └── test_wortweber_gui.py
│   ├── utils/
│   │   └── test_text_processing.py
│   ├── __init__.py
│   ├── base_test.py
│   ├── test_config.py
│   ├── test_error_handling.py
│   ├── test_parallel_transcription.py
│   └── test_sequential_transcription.py
├── .env
├── .gitignore
├── install_and_test.sh
├── LICENSE
├── NOTICE
├── pyrightconfig.json
├── README.md
├── requirements.txt
├── run_tests.py
├── THIRD_PARTY_LICENSES.md
├── user_settings.json
├── VERSION
└── wortweber.sh
```

## 6. Installation und Einrichtung
1. Repository klonen: `git clone https://github.com/fukuro-kun/Wortweber.git`
2. In das Projektverzeichnis wechseln: `cd Wortweber`
3. Installationsskript ausführen: `bash install_and_test.sh`
4. Anwendung starten: `python src/wortweber.py`

## Plugin-System

### Aktive vs. Aktivierte Plugins
Das Plugin-System unterscheidet nun zwischen "aktiven" und "für den Start aktivierten" Plugins:
- Aktive Plugins: Plugins, die derzeit in der laufenden Sitzung aktiv sind.
- Für den Start aktivierte Plugins: Plugins, die beim nächsten Start der Anwendung automatisch aktiviert werden.

Diese Unterscheidung ermöglicht eine flexiblere Verwaltung von Plugins und verhindert unerwartetes Verhalten beim Neustart der Anwendung.

### Verbesserte Einstellungsverwaltung
Die `SettingsManager`-Klasse wurde optimiert, um eine bessere Synchronisation zwischen dem internen Zustand und den gespeicherten Einstellungen zu gewährleisten. Die `sync_settings_from_file`-Methode stellt sicher, dass immer die aktuellsten Einstellungen verwendet werden.

### Plugin-Entwicklung
Entwickler von Plugins sollten beachten:
- Plugins müssen die `AbstractPlugin`-Schnittstelle implementieren.
- Die `activate` und `deactivate` Methoden sollten robust implementiert werden, um einen reibungslosen Übergang zwischen den Zuständen zu gewährleisten.
- Plugin-Einstellungen werden automatisch vom `SettingsManager` verwaltet.

[Weitere Details zur API-Dokumentation werden in zukünftigen Updates hinzugefügt.]

## 7. Beitrag zum Projekt und Entwicklungsworkflow für Contributors
Wir freuen uns über Beiträge zur Verbesserung von Wortweber. Hier ist der empfohlene Workflow für externe Contributors:

1. Forken Sie das Repository auf GitHub.
2. Klonen Sie Ihr geforktes Repository: `git clone https://github.com/IHR_USERNAME/Wortweber.git`
3. Erstellen Sie einen neuen Branch für Ihr Feature oder Ihren Bugfix:
   `git checkout -b feature/neue-funktion` oder `git checkout -b fix/bug-beschreibung`
4. Machen Sie Ihre Änderungen und committen Sie diese mit aussagekräftigen Commit-Nachrichten.
5. Pushen Sie Ihren Branch zu Ihrem Fork: `git push origin feature/neue-funktion`
6. Erstellen Sie einen Pull Request vom Branch Ihres Forks zum `main` Branch des Haupt-Repositories.

Bitte beachten Sie folgende Richtlinien:
- Halten Sie sich an die bestehenden Code-Konventionen und den Stil des Projekts.
- Schreiben Sie Tests für neue Funktionen oder Bugfixes.
- Aktualisieren Sie die Dokumentation, wenn Sie Änderungen an der Funktionalität vornehmen.
- Vergewissern Sie sich, dass alle Tests bestehen, bevor Sie einen Pull Request einreichen.
- Bei der Entwicklung neuer Features berücksichtigen Sie bitte die Plugin-Architektur
- Testen Sie Ihre Änderungen gründlich mit verschiedenen Plugin-Konfigurationen

Wir werden Ihren Pull Request überprüfen und gegebenenfalls Feedback geben. Vielen Dank für Ihren Beitrag!

## 8. Codekonventionen und Kommentierungsrichtlinien
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

## 9. Fehlerbehandlung und Logging
- Zentrale Fehlerbehandlung in `src/utils/error_handling.py`
- Verwendung des `@handle_exceptions` Decorators für alle öffentlichen Methoden
- Konsistente Logging-Levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Log-Datei: `wortweber.log` im Projekthauptverzeichnis

## 10. Testabdeckung
- Unittest-Framework für Backend- und Integrationstests
- Parallelisierte Tests für effiziente Ausführung
- Testdaten im `tests/test_data/` Verzeichnis
- Führen Sie Tests mit `python run_tests.py` aus

## 11. Versionierung
- Semantische Versionierung (MAJOR.MINOR.PATCH)
- VERSION-Datei im Hauptverzeichnis für aktuelle Versionsnummer
- Git-Tags für jede Version: `v0.x.x`

## 12. Technische Details
- Python 3.11
- OpenAI Whisper (Version 20231117)
- PyAudio für Audioaufnahme
- Tkinter für GUI
- NumPy und SciPy für Signalverarbeitung
- pynput für Tastatureingabe-Simulation
- ttkthemes für erweiterte GUI-Themes

## 13. Entwicklungsworkflow für Hauptentwickler
1. Arbeiten auf dem `main`-Branch für kleinere Änderungen
2. Erstellen von Feature-Branches für größere Funktionen: `git checkout -b feature/neue-funktion`
3. Regelmäßige Commits mit aussagekräftigen Nachrichten
4. Vor dem Merge in `main`, Rebase durchführen: `git rebase main`
5. Merge in `main` mit `--no-ff` Flag: `git checkout main && git merge --no-ff feature/neue-funktion`
6. Für Releases, annotierte Tags erstellen: `git tag -a v0.x.x -m "Version 0.x.x"`

## 14. Wichtige Hinweise
- ALSA-Warnungen können in den meisten Fällen ignoriert werden
- Bei Audiogeräte-Problemen DEVICE_INDEX in config.py anpassen
- Regelmäßige Überprüfung auf Sicherheitsupdates für Abhängigkeiten
- Stellen Sie bei der Verwendung und Integration von Bibliotheken die Kompatibilität mit der GPLv3 sicher
- Achten Sie besonders auf die korrekte Verwendung von pynput als dynamisch verlinkte Bibliothek gemäß LGPL

## 15. Lizenzierung
Wortweber ist unter der GNU General Public License v3.0 (GPLv3) lizenziert. Dies hat wichtige Auswirkungen auf die Entwicklung und Verteilung des Projekts:

- Alle Änderungen und Erweiterungen des Codes müssen ebenfalls unter der GPLv3 oder einer kompatiblen Lizenz veröffentlicht werden.
- Bei der Verteilung des Programms (in Quell- oder Binärform) muss der vollständige Quellcode mitgeliefert oder zugänglich gemacht werden.
- Die Verwendung von Bibliotheken muss sorgfältig geprüft werden, um Lizenzkompatibilität sicherzustellen.
- Besondere Aufmerksamkeit gilt der Verwendung von pynput (LGPL), das als dynamisch verlinkte Bibliothek genutzt wird.

Entwickler sollten sich mit den Bedingungen der GPLv3 vertraut machen und sicherstellen, dass alle Beiträge und Änderungen konform sind.

## 16. Kontakt
Bei Fragen oder Problemen ein Issue auf GitHub erstellen oder sich an den Projektbetreuer wenden.

## 17. Historie

### Version 0.24.0 (aktuell)
- Implementierung eines umfassenden Plugin-Systems
- Einführung des PluginManager und PluginLoader
- Integration der Plugin-Verwaltung in die GUI
- Erstellung des ersten Beispiel-Plugins (TextTransformer)

### Version 0.23.2
- Verbesserung des Layouts im OptionsPanel
- Optimierung der Positionierung des Shortcut-Fensters

### Version 0.23.0
- Implementierung einer auswählbaren Shortcut-Taste für die Push-to-Talk-Funktion
- Einführung des ShortcutPanels in den erweiterten Optionen

### Version 0.22.0
- Implementierung einer detaillierten Statusleiste
- Verbesserte Zeitmessung für Aufnahme- und Transkriptionsdauer

### Version 0.21.7
- Implementierung der Audiogeräteauswahl überarbeitet
- Verbesserte Fehlerbehandlung und Logging für Audiogerätewechsel
- Einführung einer zentralen Wortweber-Klasse für besseres Ressourcenmanagement

### Version 0.18.0
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
