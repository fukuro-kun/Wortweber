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
  - config.py: Zentrale Konfigurationsdatei
  - wortweber.py: Hauptanwendung
  - text_operations.py: Funktionen für Textoperationen
- docs/
  - README.md: Allgemeine Projektinformationen
  - CHANGELOG.md: Änderungsprotokoll
  - DEVELOPMENT.md: Entwicklerdokumentation (dieses Dokument)
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

## Versionierung
- Die aktuelle Version des Projekts wird in der VERSION-Datei im Hauptverzeichnis gespeichert.
- Bei jeder Änderung, die eine neue Version rechtfertigt, muss diese Datei aktualisiert werden.
- Das Format der Versionsnummer folgt der Semantischen Versionierung (MAJOR.MINOR.PATCH).
- Bei der Erstellung eines neuen Git-Tags sollte die Versionsnummer aus dieser Datei verwendet werden.

## Umfassendes Refactoring (Version 0.6.0)

Am 2024-09-11 wurde ein umfassendes Code-Refactoring durchgeführt, um die Struktur und Wartbarkeit des Projekts zu verbessern. Die Hauptänderungen umfassen:

1. Einführung von Klassen:
   - WordweberState: Verwaltet den Zustand der Anwendung
   - AudioProcessor: Handhabt die Audioaufnahme und -verarbeitung
   - Transcriber: Verantwortlich für die Transkription
   - WordweberGUI: Hauptklasse für die grafische Benutzeroberfläche

2. Verbesserte Dokumentation:
   - Hinzufügung ausführlicher Docstrings zu allen Klassen und Methoden
   - Aktualisierung der Kommentare im Code für bessere Verständlichkeit

3. Typ-Annotationen und -Überprüfungen:
   - Einführung von Typ-Annotationen für alle Funktionen und Methoden
   - Implementierung expliziter Typüberprüfungen zur Vermeidung von None-Wert-Fehlern

4. Konfigurationsverbesserungen:
   - Einführung von HIGHLIGHT_DURATION in der Konfigurationsdatei für konsistentere Einstellungen

5. Fehlerbehandlung:
   - Überarbeitung der Fehlerbehandlung in kritischen Funktionen wie Audioaufnahme und Transkription

Diese Änderungen zielen darauf ab, die Codebase robuster, lesbarer und einfacher zu warten zu machen.
Entwickler, die an diesem Projekt arbeiten, sollten sich mit der neuen Struktur vertraut machen und die
eingeführten Konventionen für zukünftige Entwicklungen beibehalten.


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

## Git-Workflow Best Practices
[Der Abschnitt bleibt unverändert]

## Lizenz
Apache 2.0 -Lizenz (siehe LICENSE-Datei)

## Kontakt
Für Fragen und Support, bitte ein Issue auf GitHub erstellen oder sich an den Projektbetreuer wenden.
