# Wortweber: Projektübersicht

## Einführung
Dieses Dokument bietet eine umfassende Übersicht über das Wortweber-Tool. Es dient als zentrale Informationsquelle für Entwickler, Benutzer und Stakeholder des Projekts.

## Projektbeschreibung
Wortweber ist eine benutzerfreundliche Anwendung zur Echtzeit-Transkription von Sprache in Text. Es nutzt das OpenAI Whisper-Modell für präzise Spracherkennung und bietet eine intuitive grafische Benutzeroberfläche.

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

## Installation und Nutzung
1. Klonen Sie das Repository: `git clone https://github.com/fukuro-kun/Wortweber.git`
2. Navigieren Sie zum Projektverzeichnis: `cd Wortweber`
3. Führen Sie das Installations- und Testskript aus: `./install_and_test.sh`
4. Aktivieren Sie die Conda-Umgebung: `conda activate wortweber`
5. Starten Sie die Anwendung: `python src/wortweber.py`

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
