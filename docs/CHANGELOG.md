# Changelog

Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/),
und dieses Projekt folgt der [Semantischen Versionierung](https://semver.org/lang/de/).

## [0.29.5] - 2024-01-16

### Verbessert
- Umfassende Dokumentation des Whisper-Transkriptionssystems
- Optimierte Code-Kommentare im Transcriber-Modul

### Technisch
- Konsolidierung der OpenAI Whisper-Implementation
- Verbesserte Ressourcenverwaltung für GPU/CPU-Nutzung
- Optimierte Speicherfreigabe für CUDA-Ressourcen

### Dokumentation
- Detaillierte Entwickler-Dokumentation für das Transkriptionssystem
- Ausführliche Erklärungen zur Whisper-Modell-Architektur
- Verbesserte API-Dokumentation der Transcriber-Klasse

## [0.29.4] - 2024-11-15
### Geändert
- Grundlegende Überarbeitung des Plugin-Management-Systems
- Strikte Trennung zwischen Laufzeit-Status und Start-Konfiguration von Plugins
- Implementierung von sofortigem Speichern für Plugin-Einstellungen

### Verbessert
- Ausführlichere Dokumentation der Plugin-Management-Methoden
- Detaillierteres Logging für Plugin-Status-Änderungen
- Klarere Fehlermeldungen bei Plugin-Aktivierung/-Deaktivierung

### Technisch
- Refaktorierung der Plugin-Manager-Klasse für bessere Wartbarkeit
- Optimierung der Persistenz von Plugin-Einstellungen
- Verbesserung der Thread-Sicherheit bei Plugin-Status-Änderungen

## [0.29.3] - 2024-10-02
### Geändert
- Aktualisierung der Dokumentation zur Reflektion der Änderungen im Einstellungsmanagement
- Verbesserung der Erklärungen zu RLock, set_setting_instant und verzögerter Speicherung in der Entwicklerdokumentation
### Verbessert
- Klarere Beschreibung der Best Practices für die Verwendung des aktualisierten Einstellungsmanagements

## [0.29.2] - 2024-10-02
### Geändert
- Implementierung von RLock zur Vermeidung von Deadlocks bei Einstellungsänderungen
- Optimierung der Speichervorgänge für Einstellungen
- Restrukturierung und Vereinfachung der TODO-Liste für bessere Übersichtlichkeit und Priorisierung

### Behoben
- Behebung eines Deadlock-Problems beim Ändern des Ausgabemodus

### Dokumentation
- Aktualisierung der TODO-Liste mit klarer Priorisierung in drei Kategorien (Hohe, Mittlere, Niedrige Priorität)
- Hinzufügung neuer Aufgaben zur Überprüfung der Stabilität und Performanz nach RLock-Implementierung

## [0.29.1] - 2024-10-02
### Behoben
- Korrektur der Speicherung von Plugin-Einstellungen und Aktivierungsstatus
- Verbesserung der Konsistenz zwischen `enabled_plugins` und `active_plugins`

### Verbessert
- Optimierung der Plugin-Aktivierungslogik
- Erweiterung des Logging-Systems für bessere Fehlerdiagnose

## [0.29.0] - 2024-09-29
### Hinzugefügt
- Erweiterte UI-Funktionalitäten für Plugins (Menüeinträge, Kontextmenüs, Plugin-Leiste)
- Verbesserte Event-System-Integration für Plugins
- Neue Best Practices für UI-Integration und Event-Handling
- Umfassendes Plugin-Beispiel zur Demonstration neuer Funktionalitäten

### Geändert
- Aktualisierung der Plugin-Entwicklungsdokumentation (PLUGINSYSTEM.md)
- Erweiterung der AbstractPlugin-Klasse um neue UI-bezogene Methoden
- Anpassung des PluginManagers zur Unterstützung erweiterter UI-Funktionen

### In Bearbeitung
- Implementierung des Ollama-LLM-Chat-Plugins als Testfall

## [0.28.0] - 2024-09-29
### Hinzugefügt
- Erweiterung des Plugin-Systems mit verbesserter UI-Integration
- Dynamische Plugin-Leiste im Hauptfenster
- Erweiterte Menüeinträge für Plugins
- Verbesserte Event-Kommunikation zwischen PluginManager und GUI
- Ollama-LLM-Chat-Plugin als Beispielimplementierung

### Geändert
- Überarbeiteter PluginManager mit Event-basierter Kommunikation
- Anpassungen in WordweberGUI für bessere Plugin-Integration
- Aktualisierte AbstractPlugin-Klasse mit erweiterten Methoden
- Changelog auf Deutsch vereinheitlicht

### Behoben
- Problem mit dem Speichern von Plugin-Einstellungen
- Inkonsistenzen bei der Anzeige von Plugin-UI-Elementen

## [0.27.1] - 2024-09-27
### Hinzugefügt
- Mermaid-Diagramm zur Visualisierung des Plugin-Lebenszyklus in PLUGINSYSTEM.md

### Verbessert
- Erweiterte Erklärung des Plugin-Lebenszyklus in der Dokumentation

## [0.27.0] - 2024-09-27
### Hinzugefügt
- Umfassende Dokumentation des Plugin-Systems
- Erweiterte Funktionalität für Plugin-Validierung in PluginLoader

### Geändert
- Verbesserte Fehlerbehandlung und Logging in PluginManager
- Aktualisierte Beschreibungen für Event-System und Einstellungsverwaltung

### Dokumentation
- Neue PLUGINSYSTEM.md mit detaillierter Beschreibung des Plugin-Systems
- Neue GLOSSAR.md mit Plugin-spezifischen Begriffen
- Verbesserte Codebeispiele und Erklärungen in der Dokumentation

## [0.26.1] - 2024-09-27
### Behoben
- Behebung des Problems mit doppelten Log-Einträgen bei Audioaufnahmen

## [0.26.0] - 2024-09-27
### Hinzugefügt
- Erweitertes Plugin-System mit Unterstützung für Abhängigkeiten
- Neue Methoden in AbstractPlugin: on_update(), get_config_ui(), und register_events()
- Möglichkeit zum Neuladen einzelner Plugins
- Automatische Auflösung von Plugin-Abhängigkeiten

### Geändert
- Verbesserte Struktur des PluginManagers für erweiterte Funktionalität
- Optimierte Fehlerbehandlung und Logging für Plugins

## [0.25.0] - 2024-09-27
### Hinzugefügt
- Umfassende Dokumentation des Wortweber Plugin-Systems
- Detaillierte Beschreibung der Plugin-Architektur und -Entwicklung
- Ausführliche API-Referenz für das Plugin-System
- Umfangreicher Glossar mit Querverweisen und Beispielreferenzen
- Kapitel über zukünftige Entwicklungen des Plugin-Systems

### Verbessert
- Strukturierung und Konsistenz der gesamten Projektdokumentation
- Codebeispiele zur Veranschaulichung von Plugin-Konzepten

## [0.24.6] - 2023-09-27
### Geändert
- Verbesserte Logging-Struktur für erhöhte Übersichtlichkeit
- Reduzierte redundante Logs, insbesondere bei Einstellungen und Plugin-Informationen
- Anpassung des Incognito-Modus-Loggings für konsistentere Ausgaben
### Behoben
- Korrektur der Anwendung des Incognito-Modus beim Logging

## [0.24.5] - 2024-09-26
### Geändert
- Verbesserte Konsistenz im Plugin-Management-System
- Optimierte Unterscheidung zwischen aktiven und für den Start aktivierten Plugins
- Erhöhte Zuverlässigkeit der Einstellungsverwaltung

### Behoben
- Behebung von Inkonsistenzen bei der Plugin-Aktivierung und -Deaktivierung
- Verbesserung der Synchronisation zwischen internem Zustand und gespeicherten Einstellungen

## [0.24.4] - 2024-09-24
### Geändert
- Optimiertes Logging für Textauswahl-Änderungen, um die Logmenge zu reduzieren und die Übersichtlichkeit zu verbessern.

## [0.24.3] - 2024-09-24
### Behoben
- Verbesserte Handhabung der Fenstergeometrie-Speicherung für alle Fenster.
### Geändert
- Reduzierung der Log-Ausgaben für routinemäßige Operationen.
- Anpassung der Logging-Levels für verschiedene Komponenten zur Verbesserung der Übersichtlichkeit.

## [0.24.2] - 2024-09-24
### Behoben
- Korrekte Speicherung der Fenstergeometrie für das Plugin-Verwaltungsfenster implementiert.

## [0.24.1] - 2024-09-24
### Behoben
- Zuverlässige Speicherung und Wiederherstellung der Fenstergeometrie implementiert
- Regelmäßige Aktualisierung der Fenstergeometrie während der Laufzeit eingeführt

### Geändert
- Entfernung des veralteten `window_size`-Eintrags aus den Einstellungen
- Verbessertes Logging für Fenstergeometrie-bezogene Aktionen

## [0.24.0] - 2024-09-21
### Hinzugefügt
- Implementierung eines umfassenden Plugin-Systems für Wortweber
- Neue `PluginManager`-Klasse zur Verwaltung von Plugins
- `PluginLoader` für dynamisches Laden von Plugins
- Abstrakte `AbstractPlugin`-Schnittstelle für die Entwicklung von Plugins
- Neues Plugin-Verwaltungsfenster (`PluginManagementWindow`) für Benutzerinteraktion
- Funktionalität zum Aktivieren, Deaktivieren und Konfigurieren von Plugins über die GUI
- Integration des Plugin-Systems in den Haupttextverarbeitungsprozess
- Beispiel-Plugin "TextTransformer" zur Demonstration der Plugin-Funktionalität

### Geändert
- Umfassende Überarbeitung der Kernarchitektur zur Unterstützung von Plugins
- Erweiterung des `SettingsManager` zur Verwaltung von Plugin-spezifischen Einstellungen
- Anpassung der Hauptanwendungslogik in `WordweberGUI` und `WordweberBackend` für Plugin-Integration
- Erweiterung des Menüsystems um einen Plugin-Verwaltungseintrag

### Verbessert
- Erhebliche Steigerung der Erweiterbarkeit und Anpassbarkeit der Anwendung
- Verbesserte Modularität durch klare Trennung von Kern- und Plugin-Funktionalitäten
- Erweiterte Fehlerbehandlung und Logging für robustere Plugin-Interaktionen

## [0.23.2] - 2024-09-20
### Geändert
- Verbesserung des Layouts im OptionsPanel für eine konsistentere Darstellung
- Optimierung der Positionierung des Shortcut-Fensters

### Verbessert
- Erhöhte Flexibilität des Layouts bei verschiedenen Fenstergrößen
- Verbesserte visuelle Konsistenz zwischen Shortcut-Anzeige und Statusleiste

### Behoben
- Korrektur von Layout-Problemen im MainWindow

## [0.23.1] - 2024-09-20
### Verbessert
- Optimierung der Shortcut-Setzungsfunktionalität
- Behebung von Bugs im Zusammenhang mit der Shortcut-Implementierung

### Geändert
- Verfeinerung der Benutzeroberfläche für die Shortcut-Einstellungen
- Verbesserte Fehlerbehandlung bei der Shortcut-Konfiguration

### Behoben
- Diverse Bugfixes im Zusammenhang mit der Shortcut-Funktionalität

## [0.23.0] - 2024-09-20
### Hinzugefügt
- Implementierung einer auswählbaren Shortcut-Taste für die Push-to-Talk-Funktion
- Neues ShortcutPanel in den erweiterten Optionen zur Anpassung des Push-to-Talk-Shortcuts
- Dynamische Aktualisierung des Shortcuts im InputProcessor

### Geändert
- Überarbeitung des OptionsWindow zur Integration des neuen ShortcutPanels
- Anpassung der Konfigurationsdatei zur Unterstützung des anpassbaren Shortcuts
- Verbesserung der Flexibilität des InputProcessors für verschiedene Tastentypen

### Verbessert
- Erhöhte Benutzerfreundlichkeit durch einfache Anpassung des Push-to-Talk-Shortcuts
- Verbesserte Fehlerbehandlung und Logging für Shortcut-bezogene Operationen

## [0.22.3] - 2024-09-20
### Geändert
- AudioProcessor-Tests aktualisiert, um die Verwendung des SettingsManager zu berücksichtigen
- Entfernung der librosa-Abhängigkeit in den Tests, ersetzt durch scipy.signal für Audio-Resampling
### Behoben
- Fehler in AudioProcessor-Tests aufgrund fehlender SettingsManager-Initialisierung behoben

## [0.22.2] - 2024-09-20
### Geändert
- Verbesserung des Layouts im OptionsPanel für eine übersichtlichere Darstellung
- Optimierung der Verzögerungsoptionen im erweiterten Optionsmenü

### Behoben
- Korrektur von Fehlern im Zusammenhang mit den Verzögerungseinstellungen
- Behebung des fehlenden Zwischenablage-Punktes im Optionsmenü

### Verbessert
- Erhöhte Konsistenz bei der Verwaltung von Verzögerungseinstellungen

## [0.22.1] - 2024-09-20
### Geändert
- Optimierung des Layouts im OptionsPanel für eine kompaktere Darstellung
- Anpassung der Standardfenstergröße auf 900x700 Pixel

### Verbessert
- Effizientere Platznutzung in der Benutzeroberfläche

## [0.22.0] - 2024-09-19
### Hinzugefügt
- Implementierung einer detaillierten Statusleiste mit Anzeige von Modellstatus, Ausgabemodus, Aufnahme- und Transkriptionszeit
- Zeitmessung für Aufnahme- und Transkriptionsdauer
- Verbesserte Fehlerbehandlung und Benutzerrückmeldungen

### Geändert
- Überarbeitung der GUI-Struktur für bessere Integration der Statusleiste
- Optimierung der Aufnahme- und Transkriptionsprozesse
- Anpassung der Benutzeroberfläche für verbesserte Übersichtlichkeit

### Verbessert
- Erhöhte Konsistenz bei Statusaktualisierungen über alle Komponenten hinweg
- Optimierte Ressourcenverwaltung in kritischen Komponenten

## [0.21.8] - 2024-09-19
### Hinzugefügt
- Verbesserte Persistenz der Audiogeräteauswahl
- Aktualisierte UI für Audiogeräteoptionen im Einstellungsfenster
- Rückgängig-Funktion für Audiogeräteänderungen

### Geändert
- Optimierte Initialisierung des AudioProcessors
- Verbesserte Fehlerbehandlung bei der Audiogeräteverwaltung
- Umfassende Überarbeitung und Straffung der TODO-Liste
- Neustrukturierung der DEVELOPMENT.md für verbesserte Übersichtlichkeit

### Behoben
- Problem mit inkonsistenter Anzeige des ausgewählten Audiogeräts im Optionsfenster
- Fehler bei der Speicherung und dem Laden der Audiogeräteeinstellungen

### Verbessert
- Klarere Struktur und Fokussierung auf Kernaufgaben in der Entwicklungsplanung
- Optimierte Dokumentation für neue und erfahrene Entwickler

## [0.21.7] - 2024-09-18
### Verbessert
- Implementierung der Audiogeräteauswahl überarbeitet
- Verbesserte Fehlerbehandlung und Logging für Audiogerätewechsel
- Einführung einer zentralen Wortweber-Klasse für besseres Ressourcenmanagement

### Geändert
- `AudioProcessor` Klasse um robustere Gerätemanagement-Funktionen erweitert
- `SettingsManager` um zusätzliche Logging-Funktionen ergänzt
- Hauptanwendungslogik in `wortweber.py` für verbesserte Übersichtlichkeit restrukturiert

## [0.21.6] - 2024-09-18
### Verbessert
- Implementierung der Audiogeräteauswahl überarbeitet
- Robustere Handhabung von Audiogerätewechseln
- Verbesserte Fehlerbehandlung bei Audiogeräteproblemen

### Geändert
- `AudioProcessor` Klasse um bessere Gerätemanagement-Funktionen erweitert
- `WordweberBackend` an neue `AudioProcessor` Struktur angepasst
- `AudioOptionsPanel` UI für sofortige Aktualisierung bei Gerätewechsel verbessert

### Behoben
- Problem mit nicht sofort wirksamen Audiogerätewechseln behoben
- Fehler bei der Anzeige des aktuell verwendeten Audiogeräts korrigiert

## [0.21.5] - 2024-09-18
### Hinzugefügt
- Implementierung eines Audiogeräte-Auswahlmenüs im Optionsfenster
- Anzeige des aktuell verwendeten Audiogeräts im Optionsfenster

### Verbessert
- Verbesserte Logik zur Aktualisierung des Audiogeräts im Backend
- Erhöhte Robustheit bei der Auswahl nicht verfügbarer Audiogeräte

## [0.21.4] - 2024-09-18
### Hinzugefügt
- Integration von xclip als Systemabhängigkeit für verbesserte Zwischenablagenfunktionalität
- Erweitertes Installationsprozess mit automatischer xclip-Installation
- Zusätzliche Fehlerbehebungshinweise für Pyperclip-bezogene Probleme

### Geändert
- Aktualisierung der Installationsanleitung in der README mit detaillierteren Schritten
- Verbesserung des `install_and_test.sh`-Skripts für robustere Installation

### Verbessert
- Verbesserte Benutzerfreundlichkeit durch klarere Installationsanweisungen
- Erhöhte Stabilität der Zwischenablagenfunktionen unter Linux

## [0.21.3] - 2024-09-18
### Geändert
- README.md überarbeitet, um den experimentellen Status des Projekts klarer darzustellen
- Projektbeschreibung auf GitHub angepasst für realistischere Darstellung

## [0.21.2] - 2024-09-18
### Geändert
- Projektlizenz von Apache License 2.0 zu GNU General Public License v3.0 (GPLv3) geändert
- Alle Quelldateien mit dem neuen GPLv3-Lizenztext aktualisiert
- README.md aktualisiert, um die neue Lizenz zu reflektieren
- NOTICE-Datei aktualisiert mit Informationen zum Lizenzwechsel
- Entwicklerdokumentation (DEVELOPMENT.md) aktualisiert mit Hinweisen zur GPLv3-Konformität

### Hinzugefügt
- Zusätzlicher Hinweis zur Verwendung von pynput (LGPL) in relevanten Dateien

### Aktualisiert
- requirements.txt mit Lizenzinformationen für alle Abhängigkeiten ergänzt

## [0.21.1] - 2024-09-17
### Behoben
- Korrektur der Zahlwort-zu-Ziffer-Konvertierung für Sonderfälle wie 10000001
- Verbesserung der Inline-Kommentierung in der ziffern_zu_zahlwoerter Funktion
- Behebung von Inkonsistenzen bei der Verwendung von "ein" vs. "eins"

### Verbessert
- Erhöhte Lesbarkeit und Verständlichkeit des Codes durch präzisere Inline-Kommentare

## [0.21.0] - 2024-09-17
### Verbessert
- Verbesserte Zahlwort-zu-Ziffer-Konvertierung für komplexe deutsche Zahlwörter
- Korrekte Beibehaltung von Nicht-Zahlwörtern im verarbeiteten Text
- Optimierte Akkumulation von Zahlenwerten in der TextProcessor-Klasse

### Geändert
- Überarbeitung der `accumulate_numbers`-Methode für präzisere Textverarbeitung
- Anpassung der `parse_german_number`-Funktion zur Verarbeitung von Ziffern und Zahlwörtern

## [0.20.4] - 2024-09-17
### Hinzugefügt
- Re-Implementierung der `digits_to_words` Funktion für die Konvertierung von Ziffern zu Zahlwörtern
- Farbige Ausgabe für Testergebnisse in der `test_words_to_digits` Funktion
### Verbessert
- Vervollständigung der bidirektionalen Zahlwort-Ziffer-Konvertierung
- Verbesserte Lesbarkeit der Testausgabe durch Farbkodierung (Grün für korrekte, Rot für inkorrekte Ergebnisse)

## [0.20.3] - 2024-09-17
### Behoben
- Korrektur der Verarbeitung von großen Zahlwörtern wie "zwei Millionen"
- Behebung von Problemen bei der Akkumulation von Zahlwörtern
- Verbesserung der Erkennung von Zahlwörtern unabhängig von Groß-/Kleinschreibung

### Verbessert
- Erhöhte Genauigkeit bei der Umwandlung komplexer Zahlwörter in numerische Werte

## [0.20.2] - 2024-09-16
### Geändert
- Vereinfachung und Fokussierung der GUI-Tests
- Verbesserung der Testabdeckung für Backend-Komponenten

### Entfernt
- Komplexe Button-Funktionalitätstests zugunsten einfacherer Konfigurationstests

### Verbessert
- Erhöhte Testgeschwindigkeit und -zuverlässigkeit

## [0.20.1] - 2024-09-15
### Behoben
- Verbesserte Behandlung von zusammengesetzten deutschen Zahlwörtern
- Korrigierte Umwandlung von "eine Million" und ähnlichen Fällen
- Optimierte Leerzeichenbehandlung bei der Umwandlung von Ziffern zu Worten

### Geändert
- Erweiterte Debugausgaben für bessere Nachvollziehbarkeit der Zahlenkonvertierung
- Markierte kritische Stellen im Code für deutsche Zahlenbehandlung

## [0.20.0] - 2024-09-15
### Hinzugefügt
- Verbesserte Zahlwort-zu-Ziffer und Ziffer-zu-Zahlwort Konvertierung für Deutsch und Englisch
- Separate Parsing-Funktionen für deutsche und englische Zahlwörter
- Umfangreiche neue GUI-Tests zur Verbesserung der Testabdeckung

### Geändert
- Optimierte Behandlung von "ein" und "eine" in deutschen Zahlwörtern
- Verbesserte Leerzeichenbehandlung bei Ziffer-zu-Zahlwort-Konvertierung
- Erweiterte Teststruktur für GUI-Komponenten

### Verbessert
- Erweiterte Wörterbücher für umfassendere Zahlwortabdeckung
- Verfeinerte Spracherkennungsfunktion für genauere Ergebnisse
- Erhöhte Robustheit der GUI durch verbesserte Testabdeckung

## [0.19.0] - 2024-09-15
### Hinzugefügt
- Implementierung des Incognito-Modus für erhöhten Datenschutz
- Erweitertes Logging-System mit Berücksichtigung des Incognito-Modus

### Geändert
- Überarbeitung der Logging-Logik in allen relevanten Modulen
- Anpassung der Benutzeroberfläche für Incognito-Modus-Einstellungen

### Verbessert
- Verbesserte Datenschutzmaßnahmen durch selektives Logging
- Erweiterte Debugging-Möglichkeiten im nicht-Incognito-Modus

## [0.18.1] - 2024-09-14
### Hinzugefügt
- Neues `wortweber.sh` Skript für einfacheren Start der Anwendung
- Automatische Erstellung von `wortweber.sh` im Installations- und Testskript

### Geändert
- Verbesserte Installation und Einrichtung durch Aktualisierung von `install_and_test.sh`
- Aktualisierte README mit klaren Anweisungen für beide Startmethoden

### Verbessert
- Optimierte Projektstruktur für konsistente Ausführung in verschiedenen Szenarien
- Verbesserte Benutzerfreundlichkeit durch vereinfachten Startprozess

## [0.18.0] - 2024-09-14
### Hinzugefügt
- Implementierung einer einheitlichen Fehlerbehandlungs- und Logging-Strategie im gesamten Projekt
- Neue Datei `src/utils/error_handling.py` für zentrale Fehlerbehandlung und Logging-Konfiguration
- `@handle_exceptions` Decorator für konsistente Fehlerbehandlung in allen Modulen

### Geändert
- Ersetzung von Print-Statements durch strukturiertes Logging in allen Modulen
- Anpassung aller Backend- und Frontend-Dateien zur Nutzung der neuen Fehlerbehandlung und des Loggings
- Aktualisierung der Hauptdatei `src/wortweber.py` zur Verwendung der neuen Fehlerbehandlung

### Verbessert
- Verbesserte Fehlerdiagnose und Debugging-Möglichkeiten durch detailliertes Logging
- Erhöhte Codequalität und Konsistenz durch einheitliche Fehlerbehandlung

## [0.17.3] - 2024-09-14
### Behoben
- Behebung von Problemen mit der PyAudio-Instanz in AudioProcessor
- Korrektur der Typannotationen in Transcriber für verbesserte Typsicherheit

### Geändert
- Ersetzung von Print-Statements durch Logging in Transcriber für bessere Fehlerdiagnose
- Optimierung der Ressourcenverwaltung in AudioProcessor

### Verbessert
- Verbesserte Fehlerbehandlung und Logging in kritischen Audiokomponenten
- Erhöhte Zuverlässigkeit der Transkriptionsfunktion


## [0.17.1] - 2024-09-14
### Hinzugefügt
- Fenstergröße- und Positionsspeicherung für das Optionsfenster
- Erweiterte Rückgängig-Funktionalität im Optionsfenster für alle Einstellungen einschließlich Farben

### Geändert
- Verbesserte Farbaktualisierungsmechanismen in der gesamten GUI
- Änderung der Standardschriftart zu "Nimbus Mono L"

### Verbessert
- Implementierung der Einzelinstanz-Funktionalität für das Optionsfenster
- Optimierte Benutzerinteraktion im Optionsfenster

## [0.17.0] - 2024-09-14
### Hinzugefügt
- Implementierung eines Farbauswahldialogs für benutzerdefinierte Textfarben
- Neue Funktionen zur Anpassung von Textfarbe, Texthintergrund, Auswahlfarbe und Auswahlhintergrund
- Integration des tkcolorpicker für erweiterte Farbauswahl

### Geändert
- Überarbeitung des ThemeManagers für verbesserte Farbverwaltung
- Anpassung der WordweberGUI für die Unterstützung benutzerdefinierter Farben
- Erweiterung des TranscriptionPanels zur Anwendung der benutzerdefinierten Farben

### Verbessert
- Verbesserte Benutzerfreundlichkeit durch individuelle Farbanpassungen
- Optimierte Speicherung und Wiederherstellung von Farbeinstellungen

## [0.16.1] - 2024-09-14
### Behoben
- Korrektur der Testausführungslogik in `run_tests.py`
- Behebung von Problemen mit sequentiellen Transkriptionstests

### Hinzugefügt
- Neue Kommandozeilenoptionen für Testausführung: -p/--parallel, -s/--sequential, -a/--all
- Verbesserte Dokumentation und Kommentare in `run_tests.py`

### Geändert
- Optimierte Struktur für flexiblere Testausführung

## [0.16.0] - 2024-09-14
### Hinzugefügt
- Implementierung von parallelen Transkriptionstests
- Neue Utility-Funktionen für GPU-Ressourcenüberprüfung
- Erweiterte Konfigurationsoptionen für Tests

### Geändert
- Umfassende Überarbeitung der Teststruktur
- Verbesserung der Testausgabe mit farbiger Darstellung
- Aktualisierung der run_tests.py für flexiblere Testausführung

### Verbessert
- Optimierte Ressourcennutzung bei parallelen Tests
- Verbesserte Lesbarkeit und Wartbarkeit des Testcodes

## [0.15.1] - 2024-09-13
### Behoben
- Behebung von Gerätekompatibilitätsproblemen bei der Transkription
- Korrektur der Audiovorverarbeitung für konsistente Eingaben in das Whisper-Modell

### Geändert
- Verbesserung der Modellinitialisierung mit expliziter Gerätezuweisung
- Optimierung der Mel-Spektrogramm-Erstellung und -Verarbeitung

### Hinzugefügt
- Erweiterte Fehlerprotokolle für bessere Diagnose von Transkriptionsproblemen
- Implementierung robusterer Fehlerbehandlung in kritischen Audiokomponenten

### Verbessert
- Verbesserte Integration der Whisper-Bibliotheksfunktionen für optimale Kompatibilität
- Erhöhte Zuverlässigkeit der Transkriptionsfunktion

## [0.15.0] - 2024-09-13
### Hinzugefügt
- Implementierung der Audioaufnahme-Funktion für Testaufnahmen
- Erweiterung der Tests für AudioProcessor und Audioaufnahme
- Hinzufügung von Testdaten (speech_sample.wav) für realistische Audiotests

### Geändert
- Verbesserung der Fehlerbehandlung in AudioProcessor
- Optimierung der Resampling-Funktionalität für bessere Audioqualität

### Verbessert
- Erhöhte Testabdeckung für kritische Audiofunktionen
- Verbesserte Modularität der Audioverarbeitungskomponenten

## [0.14.0] - 2024-09-13
### Hinzugefügt
- Umfassende Kommentierung des gesamten Quellcodes
- Detaillierte Inline-Kommentare und Docstrings für alle Funktionen und Klassen
- Zusätzliche Erklärungen für komplexe Code-Abschnitte

### Verbessert
- Verbesserte Lesbarkeit und Verständlichkeit des Codes
- Erweiterte Dokumentation zur Unterstützung neuer Entwickler

## [0.13.1] - 2024-09-13
### Hinzugefügt
- Implementierung der Textgrößenspeicherung
- Zentralisierung der Standardwerte in `config.py`

### Geändert
- Verbesserte Handhabung von Standardwerten in `SettingsManager`

### Behoben
- Bugfix in `SettingsManager.get_setting()` Methode für korrekte Handhabung von Standardwerten

## [0.13.0] - 2024-09-13
### Hinzugefügt
- Implementierung des Optionsmenüs mit Textgrößenanpassung
- Verbesserung des Zwischenablage-Loggings

### Geändert
- Restrukturierung der GUI-Komponenten für bessere Modularität

## [0.12.0] - 2024-09-13
### Geändert
- Umfassendes Code-Refactoring zur Verbesserung der Struktur und Lesbarkeit
- Einführung von Klassen für bessere Kapselung: WordweberState, AudioProcessor, Transcriber, und WordweberGUI
- Verbesserte Fehlerbehandlung in kritischen Funktionen
- Hinzufügung ausführlicher Docstrings zu allen Klassen und Methoden
- Überarbeitung der Konfigurationsdatei mit Einführung von HIGHLIGHT_DURATION

### Hinzugefügt
- Neue Typ-Annotationen zur Verbesserung der Code-Qualität und Wartbarkeit
- Explizite Typüberprüfungen zur Behandlung potenzieller None-Werte

### Behoben
- Behebung von Problemen mit der asynchronen Modellladung
- Korrektur der Audiodatenverarbeitung für konsistentere Ergebnisse

## [0.11.3] - 2024-09-13
   ### Behoben
   - Verbesserungen und Stabilisierung basierend auf Version 0.11.1
   - Aktualisierte Dokumentation zur Reflektion der neuesten Änderungen

   ### Geändert
   - Zusammenführung der Dokumentationsänderungen aus verschiedenen Entwicklungszweigen

## [0.11.1] - 2024-09-13
### Behoben
- Korrektur von Stabilitätsproblemen bei der Audioaufnahme und -verarbeitung
- Behebung von Fehlern bei der Anzeige von Transkriptionen im GUI

### Verbessert
- Verbesserung der Zuverlässigkeit des Audioaufnahmeprozesses
- Optimierung der Fehlerprotokolle für eine bessere Diagnose von Problemen

### Hinweis
- Diese Version stellt eine stabile Verbesserung gegenüber früheren Versionen dar und wird als aktuell empfohlene Version betrachtet.
- Aufgrund von Problemen in der nachfolgenden Version 0.11.2 wird empfohlen, bei dieser Version zu bleiben, bis eine neuere stabile Version veröffentlicht wird.


## [0.11.0] - 2024-09-12
### Hinzugefügt
- Implementierung der verzögerten Verarbeitung von Audioaufnahmen während des Modellladens
- Neue Methode zum Speichern und Wiederherstellen der Fensterposition und -größe
- Funktion zum Speichern manueller Textänderungen im Transkriptionsfenster

### Geändert
- Umfangreiches Refactoring der GUI-Struktur:
  - Aufteilung der `wortweber_gui.py` in mehrere spezialisierte Module
  - Einführung separater Klassen für MainWindow, TranscriptionPanel, OptionsPanel, StatusPanel
  - Implementierung eines ThemeManagers für verbesserte Theme-Verwaltung
  - Erstellung eines dedizierten InputProcessors für Eingabehandlung
  - Einführung eines SettingsManagers für zentralisierte Einstellungsverwaltung
- Optimierte Handhabung des Eingabemodus zwischen Neustarts
- Verbesserte Fehlerbehandlung beim Laden des Whisper-Modells
- Aktualisierte GUI-Logik für konsistentere Benutzererfahrung

### Behoben
- Problem mit dem Zurücksetzen des Eingabemodus beim Neustart behoben
- Abstürze beim Beenden der Anwendung durch verbesserte Ressourcenfreigabe behoben
- Korrektur der Persistenz von Benutzereinstellungen über Sitzungen hinweg

### Verbessert
- Erhöhte Modularität und Wartbarkeit des GUI-Codes
- Verbesserte Trennung von Belangen innerhalb der GUI-Komponenten
- Erhöhte Stabilität der GUI-Funktionalität
- Verbesserte Benutzerfeedback-Mechanismen für Modellladestatus

## [0.10.0] - 2024-09-11
### Hinzugefügt
- Funktion zum Speichern und Laden von Benutzereinstellungen
- Automatisches Speichern der Fenstergröße und des Textfensterinhalts
- Wiederherstellung der letzten Einstellungen beim Programmstart

## [0.9.0] - 2024-09-11
### Geändert
- Abschluss des Frontend-Backend-Refactorings
- Verbesserte Modularität und Wartbarkeit des Codes

## [0.8.2] - 2024-09-11
### Geändert
- Verschoben `text_operations.py` in `backend/text_processor.py` für eine konsistentere Struktur
- Aktualisierte Importe in anderen Dateien, die `text_operations` verwenden

### Entfernt
- Entfernte die leere Datei `src/text_operations.py`

### Hinzugefügt
- Erweiterte Dokumentation zur neuen Struktur der Textoperationen im Backend

## [0.8.0] - 2024-09-11
### Geändert
- Umfassendes Refactoring: Trennung von Frontend und Backend
- Verbesserung der Codestruktur und Modularität
- Anpassung der GUI an die neue Struktur

### Hinzugefügt
- Neue Backend-Struktur mit separaten Modulen für AudioProcessor, Transcriber und WordweberBackend
- Verbesserte Fehlerbehandlung und Logging
- Erweiterte Dokumentation zur neuen Projektstruktur

### Behoben
- Behebung von Problemen bei der Audioaufnahme und -verarbeitung
- Korrektur der Texthervorhebung und des Kontextmenüs gemäß ursprünglichen Spezifikationen

## [0.7.1] - 2024-09-11
### Hinzugefügt
- Option zum Ein-/Ausschalten des automatischen Kopierens in die Zwischenablage

## [0.7.0] - 2024-09-11
### Hinzugefügt
- Neue Zwischenablage-Option für die Texteingabe an der Systemcursor-Position
- Benutzerdefiniertes Eingabefeld für die Verzögerung bei zeichenweiser Eingabe

### Geändert
- Verbesserte Benutzeroberfläche mit dynamischer Aktivierung/Deaktivierung von Verzögerungsoptionen

### Behoben
- Behebung eines Fehlers bei der Verwendung der Zwischenablagefunktion mit pynput

## [0.6.0] - 2024-09-11
### Geändert
- Umfassendes Code-Refactoring zur Verbesserung der Struktur und Lesbarkeit
- Einführung von Klassen für bessere Kapselung: WordweberState, AudioProcessor, Transcriber, und WordweberGUI
- Verbesserte Fehlerbehandlung in kritischen Funktionen
- Hinzufügung ausführlicher Docstrings zu allen Klassen und Methoden
- Überarbeitung der Konfigurationsdatei mit Einführung von HIGHLIGHT_DURATION

### Hinzugefügt
- Neue Typ-Annotationen zur Verbesserung der Code-Qualität und Wartbarkeit
- Explizite Typüberprüfungen zur Behandlung potenzieller None-Werte

### Behoben
- Behebung von Problemen mit der asynchronen Modellladung
- Korrektur der Audiodatenverarbeitung für konsistentere Ergebnisse

## [0.5.1] - 2024-09-11
### Geändert
- Korrigierte Beschreibung der Audioaufnahme und -verarbeitung in der Entwicklerdokumentation
- Implementierung der semantischen Versionierung

## [0.5.0] - 2024-09-10
### Hinzugefügt
- Dropdown-Menü zur Auswahl verschiedener Whisper-Modelle
- Anzeige der Transkriptionszeit für jede Aufnahme
- "Alles kopieren (Zwischenablage)" Button zur einfachen Übernahme des gesamten Transkriptionstexts
- Kontextmenü für das Transkriptionsfeld mit Optionen zum Ausschneiden, Kopieren, Einfügen und Löschen
- Eigene Implementierung für die Konvertierung von Zahlwörtern zu Ziffern und umgekehrt

### Geändert
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
### Geändert
- Projekt umbenannt zu "Wortweber"
- Aktualisierte Dokumentation und Codebase, um den neuen Namen zu reflektieren

### Hinzugefügt
- Sprachauswahl-Funktionalität für Deutsch und Englisch
- Aktualisierte Konfigurationsdatei mit Spracheinstellungen
- DEVELOPMENT.md für umfassende Projektdokumentation hinzugefügt

## [0.3.0] - 2024-09-10
### Hinzugefügt
- Implementierung der Echtzeit-Transkription mit OpenAI Whisper
- GUI mit Tkinter für einfache Bedienung
- Push-to-Talk-Funktionalität mit F12-Taste
- Sprachauswahl (Deutsch/Englisch) in der Benutzeroberfläche

### Geändert
- Optimierung der Audioaufnahme und -verarbeitung
- Verbesserung der Transkriptionsgenauigkeit

### Behoben
- Behebung von Problemen mit der ALSA-Audioschnittstelle

## [0.2.0] - 2024-09-10
### Hinzugefügt
- Grundlegende Audioaufnahmefunktionalität
- Integration des Whisper-Modells für Transkription
- Einfache Benutzeroberfläche zur Anzeige der Transkription

## [0.1.0] - 2024-09-09
### Hinzugefügt
- Initialisierung des Projekts
- Grundlegende Projektstruktur und Abhängigkeiten
