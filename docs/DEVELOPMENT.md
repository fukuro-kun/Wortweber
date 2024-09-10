<<<<<<< HEAD
# Whisper Transkriptions-Tool: Projektübersicht

## Einführung
Dieses Dokument bietet eine umfassende Übersicht über das Whisper Transkriptions-Tool. Es dient als zentrale Informationsquelle für Entwickler, Benutzer und Stakeholder des Projekts.

## Projektbeschreibung
Das Whisper Transkriptions-Tool ist eine benutzerfreundliche Anwendung zur Echtzeit-Transkription von Sprache in Text. Es nutzt das OpenAI Whisper-Modell für präzise Spracherkennung und bietet eine intuitive grafische Benutzeroberfläche.

## Hauptfunktionen
- Echtzeit-Audioaufnahme mit Push-to-Talk-Funktionalität (F12-Taste)
- Transkription in Deutsch und Englisch mit Sprachauswahl
- Benutzerfreundliche GUI mit Statusanzeigen und Timer
- Kopieren der Transkription in die Zwischenablage
- Entwicklungsversion mit erweiterter Funktionalität

## Technische Details
- Programmiersprache: Python 3.11
- Hauptbibliotheken: OpenAI Whisper, PyAudio, Tkinter, NumPy, SciPy
- Audioformat: 16-bit PCM
- Unterstützte Eingabegeräte: Alle vom System erkannten Audiogeräte
- Whisper Modell: "small" (konfigurierbar)

## Projektstruktur
- src/
  - config.py: Zentrale Konfigurationsdatei
  - whisper_push_to_talk.py: Hauptanwendung
  - whisper_push_to_talk_dev.py: Entwicklungsversion mit zusätzlichen Features
- docs/
  - README.md: Allgemeine Projektinformationen
  - CHANGELOG.md: Änderungsprotokoll
  - DEVELOPMENT.md: Entwicklerdokumentation (dieses Dokument)
- requirements.txt: Liste der Python-Abhängigkeiten

## Installation und Nutzung
1. Klonen Sie das Repository: `git clone https://github.com/fukuro-kun/whisper-transcription-tool.git`
2. Navigieren Sie zum Projektverzeichnis: `cd whisper-transcription-tool`
3. Installieren Sie die Abhängigkeiten: `pip install -r requirements.txt`
4. Starten Sie die Anwendung: `python src/whisper_push_to_talk.py`

## Entwicklung und Beiträge
1. Forken Sie das Repository auf GitHub
2. Erstellen Sie einen Feature-Branch: `git checkout -b feature/neue-funktion`
3. Committen Sie Ihre Änderungen: `git commit -am 'Füge neue Funktion hinzu'`
4. Pushen Sie zum Branch: `git push origin feature/neue-funktion`
5. Erstellen Sie einen Pull Request

## Lizenz
MIT-Lizenz (siehe LICENSE-Datei)

## Kontakt
Für Fragen und Support, bitte ein Issue auf GitHub erstellen oder sich an den Projektbetreuer wenden.
=======
## Chunk-weise Verarbeitung und Echtzeittranskription (Experimentell)

Die Implementierung der Chunk-weisen Verarbeitung und Echtzeittranskription war ein experimenteller Ansatz, der letztendlich nicht wie erwartet funktionierte und daher nicht in den Hauptentwicklungszweig integriert wurde.

Hauptmerkmale des Versuchs:
1. Dynamische Anpassung der Chunk-Größe basierend auf erkannten Sprechpausen.
2. Echtzeitverarbeitung der Audiodaten für sofortige Transkription.
3. Implementierung von Sprachauswahl und optionaler Zahlennormalisierung.

Unüberwindbare Probleme:
- Wiederholungen in der Transkription: Die Chunk-weise Verarbeitung führte zu häufigen Wiederholungen von bereits transkribiertem Text.
- Inkonsistente Ergebnisse: Die Qualität der Transkription variierte stark zwischen verschiedenen Chunks.
- Erhöhte Komplexität: Der Ansatz erhöhte die Komplexität des Systems, ohne die erwarteten Vorteile zu liefern.

Relevante Commits:
- 3c1339e: Initiale Implementierung der Pausenerkennung und dynamischen Chunk-Erstellung
- ddeff46, f32bcbb, b0e8adc: Versuche, die Robustheit der Pausenerkennung zu verbessern
- ed6015e: Hinzufügung von Sprachauswahl und Zahlennormalisierung

Dieser Entwicklungszweig wird nicht weiter aktiv verfolgt, bleibt aber als Referenz und für mögliche zukünftige Überarbeitungen erhalten.
>>>>>>> 4dfd1b0 (Dokumentiere Probleme und Status der Chunk-weisen Verarbeitung)
