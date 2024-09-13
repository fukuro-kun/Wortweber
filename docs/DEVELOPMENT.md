# Wortweber: Entwicklungsdokumentation

## Projektübersicht
Wortweber ist ein Python-basiertes Einzelentwickler-Projekt mit KI-Unterstützung zur Echtzeit-Transkription von Sprache in Text. Es nutzt das OpenAI Whisper-Modell für die Spracherkennung und bietet eine benutzerfreundliche grafische Oberfläche mit Push-to-Talk-Funktionalität.

## Entwicklungsworkflow
- Direktes Arbeiten auf dem main-Branch
- Einfache Commit- und Push-Operationen
- Verwendung von Tags für Versionierung

## Git-Workflow
1. Änderungen vornehmen
2. Änderungen committen: `git add . && git commit -m "Beschreibende Nachricht"`
3. Änderungen pushen: `git push origin main`
4. Bei neuen Versionen: `git tag -a v0.x.x -m "Version 0.x.x" && git push origin v0.x.x`

## Hauptfunktionen
- Echtzeit-Audioaufnahme mit Push-to-Talk-Funktionalität (F12-Taste)
- Transkription in Deutsch und Englisch mit Sprachauswahl
- Benutzerfreundliche GUI mit Statusanzeigen und Timer
- Kopieren der Transkription in die Zwischenablage
- Kontextmenü für Textbearbeitung und Zahlwort-Konvertierung
- Auswahl verschiedener Whisper-Modelle

## Technische Details
- Programmiersprache: Python 3.11
- Hauptbibliotheken: OpenAI Whisper, PyAudio, Tkinter, NumPy, SciPy
- Audioformat: 16-bit PCM
- Audioaufnahme: Kontinuierliche Aufnahme in Chunks, gesammelt für einmalige Verarbeitung nach Beendigung der Aufnahme
- Unterstützte Eingabegeräte: Alle vom System erkannten Audiogeräte
- Whisper Modell: "small" (konfigurierbar)
- Eigene Implementierung für Zahlwort-zu-Ziffer und Ziffer-zu-Zahlwort Konvertierung

## Projektstruktur
- src/
  - backend/
    - __init__.py
    - audio_processor.py
    - transcriber.py
    - wortweber_backend.py
  - frontend/
    - __init__.py
    - wortweber_gui.py
  - __init__.py
  - config.py: Zentrale Konfigurationsdatei
  - wortweber.py: Hauptanwendung
  - text_operations.py: Funktionen für Textoperationen
- docs/
  - README.md: Allgemeine Projektinformationen
  - CHANGELOG.md: Änderungsprotokoll
  - DEVELOPMENT.md: Entwicklerdokumentation (dieses Dokument)
- tests/
  - backend/
    - __init__.py
    - test_audio_processor.py
  - __init__.py
  - Audioaufnahme_Testskript.py
- requirements.txt: Liste der Python-Abhängigkeiten
- install_and_test.sh: Installations- und Testskript
- VERSION: Aktuelle Versionsnummer des Projekts

## Installation und Nutzung
1. Klonen Sie das Repository: `git clone https://github.com/fukuro-kun/Wortweber.git`
2. Navigieren Sie zum Projektverzeichnis: `cd Wortweber`
3. Führen Sie das Installations- und Testskript aus: `./install_and_test.sh`
4. Aktivieren Sie die Conda-Umgebung: `conda activate wortweber`
5. Starten Sie die Anwendung: `python src/wortweber.py`

## Git-Workflow
1. Änderungen vornehmen
2. VERSION-Datei aktualisieren, falls nötig
3. Änderungen committen: `git add . && git commit -m "Beschreibende Nachricht"`
4. Änderungen pushen: `git push origin main`
5. Bei neuen Versionen:
   - Sicherstellen, dass die VERSION-Datei aktualisiert wurde
   - `git tag -a v$(cat VERSION) -m "Version $(cat VERSION)" && git push origin v$(cat VERSION)`

## Kommentierungsrichtlinien
Bei der jüngsten Überarbeitung wurden folgende Richtlinien für die Codekommentierung eingeführt:
1. Jede Datei beginnt mit einem Kommentarblock, der den Zweck und die Hauptfunktionen erklärt.
2. Alle Klassen und Funktionen haben Docstrings, die Parameter, Rückgabewerte und Seiteneffekte beschreiben.
3. Komplexe Codeabschnitte werden durch Inline-Kommentare erklärt.
4. Am Ende jeder Datei gibt es einen Abschnitt "Zusätzliche Erklärungen" für besonders komplexe Konzepte.
5. Copyright-Informationen wurden zu relevanten Dateien hinzugefügt.
Diese Richtlinien sollten bei zukünftigen Codeänderungen und -erweiterungen beibehalten werden.

## Versionierung
- Die aktuelle Version des Projekts wird in der VERSION-Datei im Hauptverzeichnis gespeichert.
- Bei jeder Änderung, die eine neue Version rechtfertigt, muss diese Datei aktualisiert werden.
- Das Format der Versionsnummer folgt der Semantischen Versionierung (MAJOR.MINOR.PATCH).
- Bei der Erstellung eines neuen Git-Tags sollte die Versionsnummer aus dieser Datei verwendet werden.

## Aktuelle Entwicklung (Version 0.11.1)

Mit Version 0.11.1 wurden wichtige Stabilitätsverbesserungen implementiert:

1. Audioaufnahme und -verarbeitung:
   - Verbesserte Fehlerbehandlung während des Aufnahmeprozesses
   - Optimierung für konsistentere Eingaben in das Whisper-Modell

2. GUI-Verbesserungen:
   - Behebung von Problemen bei der Anzeige von Transkriptionen im Textfenster

3. Allgemeine Stabilität:
   - Verbesserung der Fehlerprotokolle für eine effektivere Fehlerdiagnose
   - Optimierung des Ressourcenmanagements

Diese Version stellt einen stabilen Punkt in der Entwicklung dar und dient als Grundlage für zukünftige Verbesserungen.

### Hinweis zur Versionierung

Bei der Entwicklung der nachfolgenden Version 0.11.2 traten unerwartete Probleme auf. Als Konsequenz daraus wurden folgende Lehren für zukünftige Entwicklungen gezogen:

1. Verstärkte inkrementelle Entwicklung und Testing
2. Verbesserung der Testabdeckung, insbesondere für kritische Funktionen
3. Einrichtung einer Staging-Umgebung für gründlichere Tests vor Veröffentlichungen
4. Entwicklung eines klaren Rollback-Plans für problematische Releases
5. Detailliertere Dokumentation von Änderungen und deren erwarteten Auswirkungen

Diese Erkenntnisse werden in die zukünftige Entwicklungsstrategie einfließen, um die Stabilität und Zuverlässigkeit des Projekts weiter zu verbessern.

## Umfangreiches GUI-Refactoring (Version 0.11.0)

In Version 0.11.0 wurde ein umfassendes Refactoring der GUI-Komponente durchgeführt, um die Modularität, Wartbarkeit und Erweiterbarkeit des Codes zu verbessern. Die Hauptänderungen umfassen:

1. Aufteilung der GUI-Logik:
   - Die monolithische `wortweber_gui.py` wurde in mehrere spezialisierte Module aufgeteilt.
   - Neue Module: `main_window.py`, `transcription_panel.py`, `options_panel.py`, `status_panel.py`, `theme_manager.py`, `input_processor.py`, `settings_manager.py`

2. Einführung spezialisierter Klassen:
   - `MainWindow`: Verantwortlich für das Hauptfensterlayout und die Integration aller GUI-Komponenten.
   - `TranscriptionPanel`: Verwaltet den Transkriptionsbereich und zugehörige Funktionen.
   - `OptionsPanel`: Handhabt alle Benutzeroptionen und Einstellungen.
   - `StatusPanel`: Zeigt Statusmeldungen und Timer an.

3. Verbesserte Themenverwaltung:
   - Implementierung eines `ThemeManager` für zentralisierte Theme-Verwaltung und -Anwendung.

4. Zentralisierte Einstellungsverwaltung:
   - Einführung eines `SettingsManager` für das Laden, Speichern und Verwalten von Benutzereinstellungen.

5. Dedizierte Eingabeverarbeitung:
   - `InputProcessor` zur Handhabung von Tastatureingaben und Aufnahmesteuerung.

6. Verbesserte Fehlerbehandlung und Logging:
   - Implementierung robusterer Fehlerbehandlungsmechanismen in allen GUI-Komponenten.
   - Erweitertes Logging für bessere Nachvollziehbarkeit und Debugging.

Diese Änderungen verbessern die Codestruktur erheblich und erleichtern zukünftige Erweiterungen und Wartungsarbeiten.
Entwickler sollten sich mit der neuen Modulstruktur vertraut machen und die eingeführten Konventionen für zukünftige Entwicklungen beibehalten.


## Neue Features (Version 0.10.0)

- Implementierung der Speicherung und des Ladens von Benutzereinstellungen
- Automatisches Speichern der Fenstergröße und des Textfensterinhalts
- Wiederherstellung der letzten Einstellungen beim Programmstart

### Technische Details zur Einstellungsspeicherung

- Die Einstellungen werden in einer JSON-Datei (`user_settings.json`) im Hauptverzeichnis der Anwendung gespeichert.
- Beim Starten der Anwendung werden die gespeicherten Einstellungen geladen und angewendet.
- Bei Änderungen an den Einstellungen oder beim Beenden der Anwendung werden die aktuellen Einstellungen automatisch gespeichert.
- Fehlerbehandlung wurde implementiert, um Probleme beim Laden der Einstellungen zu behandeln.


## Restrukturierung der Textoperationen (Version 0.8.2)

Am 2024-09-13 wurden die Textoperationen restrukturiert, um die Projektstruktur zu verbessern und konsistenter zu machen:

1. Verschiebung von Funktionalitäten:
   - `text_operations.py` wurde in `backend/text_processor.py` verschoben
   - Alle Textverarbeitungsfunktionen sind nun im Backend-Verzeichnis

2. Aktualisierung von Imports:
   - Alle Dateien, die `text_operations` verwendeten, wurden aktualisiert, um die neue Struktur zu reflektieren

3. Entfernung redundanter Dateien:
   - Die leere Datei `src/text_operations.py` wurde entfernt

4. Dokumentation:
   - Aktualisierung der Projektdokumentation, um die neue Struktur der Textoperationen zu reflektieren


## Umfassendes Refactoring (Version 0.8.0)

Am 2024-09-12 wurde ein umfassendes Refactoring durchgeführt, um die Projektstruktur zu verbessern und die Trennung von Frontend und Backend zu implementieren. Die Hauptänderungen umfassen:

1. Neue Verzeichnisstruktur:
   - Einführung von `src/backend/` und `src/frontend/` Verzeichnissen
   - Aufteilung der Logik in separate Module

2. Backend-Struktur:
   - Implementierung von `AudioProcessor`, `Transcriber`, und `WordweberBackend` Klassen
   - Verbesserte Kapselung und Modularität

3. Frontend-Anpassungen:
   - Überarbeitung der `WordweberGUI` Klasse zur Nutzung des neuen Backends
   - Verbesserung der Benutzeroberfläche und Interaktionslogik

4. Fehlerbehandlung und Logging:
   - Einführung verbesserter Fehlerbehandlungsmechanismen
   - Erweitertes Logging für bessere Debuggingmöglichkeiten

5. Dokumentation:
   - Aktualisierung aller Docstrings und Kommentare
   - Erweiterung der Projektdokumentation zur Reflexion der neuen Struktur

Diese Änderungen zielen darauf ab, die Codebase modularer, wartbarer und erweiterbar zu machen.
Entwickler sollten sich mit der neuen Struktur vertraut machen und die eingeführten Konventionen
für zukünftige Entwicklungen beibehalten.

## Neue Features (Version 0.7.1)

- Eine neue Checkbox wurde hinzugefügt, um das automatische Kopieren in die Zwischenablage optional zu machen. Diese Funktion gibt den Benutzern mehr Kontrolle über die Handhabung der transkribierten Texte.

## Neue Features (Version 0.7.0)

- Implementierung einer Zwischenablage-Option für die Texteingabe an der Systemcursor-Position
- Hinzufügung eines benutzerdefinierten Eingabefelds für die Verzögerung bei zeichenweiser Eingabe
- Dynamische Aktivierung/Deaktivierung von Verzögerungsoptionen basierend auf dem ausgewählten Eingabemodus
- Verbesserung der pynput-Integration für zuverlässigere Tastatureingaben

Diese Änderungen verbessern die Flexibilität und Benutzerfreundlichkeit der Anwendung, indem sie mehr Kontrolle über die Texteingabe bieten und die Benutzeroberfläche reaktiver gestalten.

## Hinweise für Entwickler
- Das `whisper`-Paket wird von diesem Projekt verwendet und muss installiert sein. Warnungen des statischen Analysators bezüglich des Imports von `whisper` können ignoriert werden, solange das Paket korrekt installiert ist.
- Bei der Entwicklung neuer Features, beachten Sie bitte die bestehende Codestruktur und Namenskonventionen.
- Fügen Sie für neue Funktionen entsprechende Tests hinzu.

## Entwicklung und Beiträge
1. Forken Sie das Repository auf GitHub
2. Erstellen Sie einen Feature-Branch: `git checkout -b feature/neue-funktion`
3. Committen Sie Ihre Änderungen: `git commit -am 'Füge neue Funktion hinzu'`
4. Pushen Sie zum Branch: `git push origin feature/neue-funktion`
5. Erstellen Sie einen Pull Request

## Lizenz
Apache 2.0 -Lizenz (siehe LICENSE-Datei)

## Kontakt
Für Fragen und Support, bitte ein Issue auf GitHub erstellen oder sich an den Projektbetreuer wenden.
