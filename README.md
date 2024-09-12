# Wortweber

Wortweber ist eine leistungsstarke und benutzerfreundliche Anwendung zur Echtzeit-Transkription von Sprache in Text. Mit Hilfe modernster KI-Technologie bietet Wortweber präzise Spracherkennung in Deutsch und Englisch.

## Hauptfunktionen

- Echtzeit-Audioaufnahme mit Push-to-Talk-Funktionalität (F12-Taste)
- Transkription in Deutsch und Englisch mit verschiedenen Whisper-Modellen
- Intuitive grafische Benutzeroberfläche mit anpassbaren Themes
- Automatisches Kopieren der Transkription in die Zwischenablage (optional)
- Einfache Umwandlung von Zahlwörtern in Ziffern und umgekehrt
- Flexible Eingabemodi: Textfenster oder Systemcursor-Position
- Speichern und Wiederherstellen von Benutzereinstellungen

## Installation und Nutzung

### Voraussetzungen

- Python 3.11 oder höher
- Conda (empfohlen für einfache Installation und Verwaltung der Umgebung)

### Installation

1. Klonen Sie dieses Repository:
   ```
   git clone https://github.com/fukuro-kun/Wortweber.git
   cd Wortweber
   ```

2. Führen Sie das Installations- und Testskript aus:
   ```
   bash install_and_test.sh
   ```

3. Folgen Sie den Anweisungen im Terminal. Sie werden möglicherweise nach Ihrem Passwort gefragt, um Systemabhängigkeiten zu installieren.

### Verwendung

1. Aktivieren Sie die Conda-Umgebung:
   ```
   conda activate wortweber
   ```

2. Starten Sie die Anwendung:
   ```
   python src/wortweber.py
   ```

3. Drücken und halten Sie die F12-Taste, um zu sprechen. Lassen Sie die Taste los, um die Aufnahme zu beenden und die Transkription zu starten.

## Projektstruktur

- `src/`: Enthält den Quellcode
  - `backend/`: Backend-Logik für Audioaufnahme und Transkription
  - `frontend/`: GUI-Komponenten und Benutzerschnittstelle
- `docs/`: Enthält die Projektdokumentation
- `tests/`: Enthält Unittests und Integrationstests
- `requirements.txt`: Liste der Python-Abhängigkeiten
- `install_and_test.sh`: Installations- und Testskript
- `VERSION`: Aktuelle Versionsnummer des Projekts

## Tests

Um alle Tests auszuführen, verwenden Sie den folgenden Befehl im Hauptverzeichnis des Projekts:

```
python run_tests.py
```

## Wichtige Hinweise

- Stellen Sie sicher, dass Sie die Wortweber-Umgebung aktiviert haben, bevor Sie die Anwendung starten.
- Die Anwendung wurde für die Verwendung in einer isolierten Conda-Umgebung entwickelt, um Konflikte mit System-Python-Installationen zu vermeiden.

## Problembehebung

### GLIBCXX_3.4.32 Fehler

Wenn Sie einen Fehler bezüglich `GLIBCXX_3.4.32` erhalten, führen Sie folgenden Befehl aus:

```
cp /usr/lib/x86_64-linux-gnu/libstdc++.so.6 $CONDA_PREFIX/lib/
```

Dies kopiert die benötigte C++-Bibliothek in Ihre Conda-Umgebung. Dieser Schritt ist oft notwendig,
da die in Conda enthaltene Version möglicherweise nicht mit den Systemanforderungen übereinstimmt.

### Weitere Problemlösungen

1. Stellen Sie sicher, dass Sie die neueste Version von Conda verwenden.
2. Überprüfen Sie, ob alle Systemabhängigkeiten korrekt installiert sind.
3. Bei Problemen mit PyAudio, versuchen Sie eine Neuinstallation:
   ```
   pip uninstall pyaudio
   pip install --no-binary :all: pyaudio
   ```
4. Bei Problemen mit der Audiogeräte-Erkennung, passen Sie den DEVICE_INDEX in der `config.py` an.

### Bekannte Probleme

- ALSA-Warnungen können in den meisten Fällen ignoriert werden und sind nicht kritisch für die Funktionalität der Anwendung.
- Bei ALSA-bezogenen Fehlern können Sie versuchen, die ALSA-Bibliotheken zu aktualisieren:
  ```
  sudo apt-get install --reinstall libasound2 libasound2-plugins
  ```

Wenn Sie weiterhin Probleme haben, überprüfen Sie die Konsolenausgabe auf spezifische Fehlermeldungen und suchen Sie nach diesen online oder eröffnen Sie ein Issue in diesem Repository.

## Systemanforderungen

Diese Anwendung wurde erfolgreich getestet auf:
- Ubuntu 22.04 LTS
- Python 3.11
- Conda 23.11.0

## Beitragen

Beiträge zu diesem Projekt sind willkommen! Wenn Sie Verbesserungen vorschlagen oder Fehler melden möchten, erstellen Sie bitte ein Issue oder einen Pull Request auf GitHub.

## Lizenz

Dieses Projekt steht unter der Apache License 2.0. Weitere Details finden Sie in der [LICENSE](LICENSE) Datei.
