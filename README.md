# Wortweber

Wortweber ist ein Projekt zur Echtzeit-Transkription von Sprache in Text, das sich derzeit in der Entwicklungsphase befindet. Es nutzt KI-Technologie für die Spracherkennung in Deutsch und Englisch und ist als Lern- und Experimentierplattform konzipiert.

## Aktueller Entwicklungsstand

Wortweber befindet sich in einer frühen Entwicklungsphase und ist noch nicht für den produktiven Einsatz geeignet. Die aktuelle Version bietet grundlegende Funktionalität, ist aber weder vollständig optimiert noch umfassend getestet. Benutzer sollten mit gelegentlichen Fehlern und Einschränkungen rechnen.

## Geplante Hauptfunktionen

- Echtzeit-Audioaufnahme mit Push-to-Talk-Funktionalität (Standard: F12-Taste, änderbar)
- Transkription in Deutsch und Englisch mit Whisper-Modellen
- Einfache grafische Benutzeroberfläche
- Umwandlung von Zahlwörtern in Ziffern und umgekehrt
- Flexible Eingabemodi: Textfenster oder Systemcursor-Position
- Speichern von Benutzereinstellungen

## Plugin-System

Wortweber verfügt über ein umfangreiches Plugin-System, das es Entwicklern ermöglicht, die Funktionalität der Anwendung zu erweitern. Detaillierte Informationen zur Architektur, Entwicklung und Nutzung von Plugins finden Sie in der [Plugin-System-Dokumentation](docs/PLUGINSYSTEM.md).


## Installation und Nutzung

### Voraussetzungen

- Python 3.11 oder höher
- Conda (für einfache Installation und Verwaltung der Umgebung)
- xclip (für Zwischenablagenoperationen unter Linux)

### Installation

#### 1. Python installieren

Wenn Sie Python 3.12 installieren möchten, können Sie folgendes Kommando in Ihrem Terminal ausführen:

```
sudo apt install python3.12
```

#### 2. Conda installieren

Wir empfehlen die Installation von Miniconda. Folgen Sie diesen Schritten:

```bash
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh
```

Diese Befehle laden die neueste 64-Bit-Version des Linux-Installers herunter, benennen ihn um, installieren ihn im Hintergrund und löschen anschließend den Installer.

Für detailliertere Anweisungen besuchen Sie: https://docs.anaconda.com/miniconda/#quick-command-line-install

#### 3. Wortweber installieren

1. Öffnen Sie ein Terminal und klonen Sie das Wortweber-Repository:
   ```
   git clone https://github.com/fukuro-kun/Wortweber.git
   cd Wortweber
   ```

2. Führen Sie das Installations- und Testskript aus:
   ```
   bash install_and_test.sh
   ```

3. Folgen Sie den Anweisungen im Terminal. Sie werden möglicherweise nach Ihrem Passwort gefragt, um Systemabhängigkeiten zu installieren.

### Wichtige Hinweise

- Die Installation kann je nach System unterschiedlich verlaufen und zusätzliche Schritte erfordern.
- Bei Problemen konsultieren Sie bitte den Abschnitt "Problembehebung" in dieser README oder erstellen Sie ein Issue auf GitHub.
- Stellen Sie sicher, dass Sie nach der Installation von Miniconda Ihr Terminal neu starten oder `source ~/.bashrc` ausführen, um die Conda-Umgebung zu aktivieren.

Wir arbeiten kontinuierlich daran, den Installationsprozess zu verbessern. Wenn Sie auf Schwierigkeiten stoßen, zögern Sie nicht, uns um Hilfe zu bitten.

### Verwendung

Nach der Installation können Sie Wortweber auf zwei Arten starten:

1. Verwenden Sie das bereitgestellte Shell-Skript:
   ```
   ./wortweber.sh
   ```

   Dieses Skript aktiviert automatisch die richtige Conda-Umgebung und startet die Anwendung.

2. Alternativ können Sie die Anwendung manuell starten:
   ```
   conda activate wortweber
   python -m src.wortweber
   ```

3. Drücken und halten Sie die F12-Taste, um zu sprechen. Lassen Sie die Taste los, um die Aufnahme zu beenden und die Transkription zu starten.

## Projektstruktur

- `src/`: Enthält den Quellcode
  - `backend/`: Backend-Logik für Audioaufnahme und Transkription
  - `frontend/`: GUI-Komponenten und Benutzerschnittstelle
  - `plugin_system/`: Kernkomponenten des Plugin-Systems
  - `utils/`: Hilfsfunktionen und -klassen
- `docs/`: Enthält die Projektdokumentation
  - `PLUGINSYSTEM.md`: Umfassende Dokumentation des Plugin-Systems
  - `CHANGELOG.md`: Änderungsprotokoll des Projekts
  - `DEVELOPMENT.md`: Entwicklerdokumentation
  - `TODO.md`: Aufgabenliste für zukünftige Entwicklungen
- `tests/`: Enthält Unittests und Integrationstests
- `plugins/`: Verzeichnis für installierte Plugins
- `logs/`: Enthält Logdateien der Anwendung
- `requirements.txt`: Liste der Python-Abhängigkeiten
- `install_and_test.sh`: Installations- und Testskript
- `VERSION`: Aktuelle Versionsnummer des Projekts
- `wortweber.sh`: Startskript für die Anwendung

## Tests

Um alle Tests auszuführen, verwenden Sie den folgenden Befehl im Hauptverzeichnis des Projekts:

```
python run_tests.py
```

Sie können auch spezifische Testoptionen verwenden:

```
- Für grundlegende Tests ohne Transkriptions- oder GUI-Tests: python run_tests.py
- Für parallele Transkriptionstests: python run_tests.py -p oder python run_tests.py --parallel
- Für sequenzielle Transkriptionstests: python run_tests.py -s oder python run_tests.py --sequential
- Für alle Tests einschließlich paralleler und sequenzieller Transkriptionstests sowie GUI-Tests: python run_tests.py -a oder python run_tests.py --all
- Für GUI-Tests: python run_tests.py -g oder python run_tests.py --gui
```

Beachten Sie:
- Die Verfügbarkeit von GPU-Ressourcen wird automatisch überprüft. Bei unzureichendem GPU-Speicher werden parallele Tests deaktiviert.
- Sie können mehrere Optionen kombinieren, z.B. `python run_tests.py -a -p` für alle Tests mit Priorisierung paralleler Ausführung, wo möglich.

Für detaillierte Informationen zu den Testoptionen können Sie folgenden Befehl ausführen:

```
python run_tests.py --help
```

Bitte beachten Sie, dass die Tests in der aktuellen Entwicklungsphase nicht immer stabil laufen und gelegentlich fehlschlagen können.

## Wichtige Hinweise

- Stellen Sie sicher, dass Sie die Wortweber-Umgebung aktiviert haben, bevor Sie die Anwendung starten.
- Die Anwendung wurde für die Verwendung in einer isolierten Conda-Umgebung entwickelt, um Konflikte mit System-Python-Installationen zu vermeiden.
- Diese Software befindet sich in einem experimentellen Stadium und sollte nicht für kritische oder produktive Zwecke eingesetzt werden.
- Die Leistung und Zuverlässigkeit können stark variieren und sind von verschiedenen Faktoren abhängig.

## Problembehebung

### GLIBCXX_3.4.32 Fehler

Wenn Sie einen Fehler bezüglich `GLIBCXX_3.4.32` erhalten, führen Sie folgenden Befehl aus:

```
cp /usr/lib/x86_64-linux-gnu/libstdc++.so.6 $CONDA_PREFIX/lib/
```

Dies kopiert die benötigte C++-Bibliothek in Ihre Conda-Umgebung. Dieser Schritt ist oft notwendig,
da die in Conda enthaltene Version möglicherweise nicht mit den Systemanforderungen übereinstimmt.

### Pyperclip-Fehler

Wenn Sie eine Fehlermeldung erhalten, die besagt, dass Pyperclip keinen Copy/Paste-Mechanismus für Ihr System finden konnte, installieren Sie bitte xclip:

```
sudo apt-get install xclip
```

Dies sollte das Problem mit der Zwischenablagenfunktionalität beheben.


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
- Ubuntu 24.04 LTS
- Python 3.11
- Conda 23.11.0

## Projektstatuslage und Beiträge

![Maintenance](https://img.shields.io/badge/Maintained%3F-passive-yellow.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome%20but%20may%20be%20slow-brightgreen.svg)

Wortweber ist ein Open-Source-Projekt, das hauptsächlich zu Demonstrationszwecken und für persönliche Nutzung entwickelt wurde. Um Missverständnisse zu vermeiden, möchte ich die aktuelle Projektstatuslage transparent kommunizieren:

1. **Wartung**: Das Projekt wird passiv gewartet. Updates und Fehlerbehebungen erfolgen unregelmäßig und nach persönlichem Bedarf.

2. **Pull Requests (PRs)**:
   - PRs sind willkommen und werden geschätzt.
   - Die Überprüfung und Integration von PRs kann erhebliche Zeit in Anspruch nehmen.
   - Es besteht keine Garantie, dass alle PRs akzeptiert werden.
   - Bitte haben Sie Verständnis, wenn die Bearbeitung länger dauert oder Vorschläge nicht übernommen werden können.

3. **Issues**:
   - Fehlerberichte und Verbesserungsvorschläge können eingereicht werden.
   - Bitte verstehen Sie, dass ihre Bearbeitung nicht garantiert ist und möglicherweise lange dauern kann.

4. **Support**:
   - Aufgrund zeitlicher Beschränkungen kann kein aktiver Support angeboten werden.
   - Die Dokumentation in diesem Repository sollte die meisten Fragen beantworten.

5. **Forking und eigene Nutzung**:
   - Sie sind herzlich eingeladen, das Projekt zu forken und für Ihre eigenen Bedürfnisse anzupassen.
   - Wenn Sie Verbesserungen vornehmen, die Sie teilen möchten, können Sie diese gerne als PR einreichen.

6. **Erwartungsmanagement**:
   - Bitte erwarten Sie keine schnellen Antworten oder Umsetzungen von Vorschlägen.
   - Das Projekt wird nach bestem Wissen und Gewissen, aber ohne Garantien oder Verpflichtungen gepflegt.

Dieses Projekt ist eine Einladung zum Lernen und Experimentieren. Ich freue mich über Ihr Interesse und danke für Ihr Verständnis bezüglich der begrenzten Ressourcen für die Projektpflege.

## Lizenz

Dieses Projekt ist unter der GNU General Public License v3.0 (GPLv3) lizenziert.
Für weitere Details siehe die [LICENSE](LICENSE)-Datei im Projektverzeichnis oder besuchen Sie
[https://www.gnu.org/licenses/gpl-3.0.en.html](https://www.gnu.org/licenses/gpl-3.0.en.html).
