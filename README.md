# Wortweber

Wortweber ist eine leistungsstarke und benutzerfreundliche Anwendung zur Echtzeit-Transkription von Sprache in Text. Mit Hilfe modernster KI-Technologie bietet Wortweber präzise Spracherkennung in Deutsch und Englisch.

## Hauptfunktionen

- Echtzeit-Audioaufnahme mit Push-to-Talk-Funktionalität
- Transkription in Deutsch und Englisch
- Intuitive grafische Benutzeroberfläche
- Automatisches Kopieren der Transkription in die Zwischenablage
- Einfache Umwandlung von Zahlwörtern in Ziffern und umgekehrt

## Installation und Nutzung

### Installation

1. Stellen Sie sicher, dass Sie Conda installiert haben.

2. Klonen Sie dieses Repository:
   ```
   git clone https://github.com/fukuro-kun/Wortweber.git
   cd Wortweber
   ```

3. Führen Sie das Installations- und Testskript aus:
   ```
   ./install_and_test.sh
   ```

4. Folgen Sie den Anweisungen im Terminal. Sie werden möglicherweise nach Ihrem Passwort gefragt, um Systemabhängigkeiten zu installieren.

### Verwendung

1. Aktivieren Sie die Conda-Umgebung:
   ```
   conda activate wortweber
   ```

2. Führen Sie das Skript aus:
   ```
   python src/wortweber.py
   ```

3. Drücken und halten Sie die F12-Taste, um zu sprechen. Lassen Sie die Taste los, um die Aufnahme zu beenden und die Transkription zu starten.

## Versionen

Dieses Projekt ist in zwei Versionen verfügbar, um unterschiedliche Anforderungen und Lizenzierungspräferenzen zu berücksichtigen:

1. Hauptversion (main branch):
   - Verwendet eine eigene Implementierung für die Zahlwort-zu-Ziffer und Ziffer-zu-Zahlwort Konvertierung.
   - Ist unabhängig von externen Bibliotheken für diese Funktionalität.
   - Empfohlen für die meisten Anwendungsfälle.

2. Erweiterte Version (feature/num2words_and_gui_improvements branch):
   - Verwendet zusätzliche Bibliotheken für erweiterte Zahlwort-Konvertierungsfunktionen.
   - Bietet umfangreichere Unterstützung für verschiedene Sprachen und Zahlensysteme.
   - Kann zusätzlichen Lizenzbedingungen unterliegen.

### Wechseln zwischen den Versionen

Um zwischen den Versionen zu wechseln, verwenden Sie die folgenden Git-Befehle:

Für die Hauptversion:
```bash
git checkout main
```

Für die erweiterte Version:
```bash
git checkout feature/num2words_and_gui_improvements
```

Bitte beachten Sie: Nach dem Wechsel zur erweiterten Version müssen Sie die zusätzlichen Abhängigkeiten installieren:

```bash
pip install -r requirements.txt
```

Stellen Sie sicher, dass Sie die Lizenzbedingungen aller verwendeten Bibliotheken in der erweiterten Version überprüfen und einhalten.

## Projektstruktur
- `src/`: Enthält den Quellcode
- `docs/`: Enthält die Dokumentation
- `requirements.txt`: Liste der Python-Abhängigkeiten
- `install_and_test.sh`: Installations- und Testskript
- `VERSION`: Aktuelle Versionsnummer des Projekts


## Wichtiger Hinweis

Dieses Tool wurde entwickelt, um in einer isolierten Conda-Umgebung zu laufen.
Bitte stellen Sie sicher, dass Sie die Wortweber-Umgebung aktiviert haben,
bevor Sie das Tool verwenden. Dies gewährleistet die korrekte Funktionalität und verhindert
unbeabsichtigte Änderungen an Ihrem System-Python.

## Deinstallation

Um die Wortweber-Umgebung zu entfernen, führen Sie folgenden Befehl aus:
```
conda remove --name wortweber --all
```

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
3. Bei ALSA-Fehlern versuchen Sie, die ALSA-Bibliotheken zu aktualisieren:
   ```
   sudo apt-get install --reinstall libasound2 libasound2-plugins
   ```
4. Wenn Sie Probleme mit PyAudio haben, versuchen Sie, es neu zu installieren:
   ```
   pip uninstall pyaudio
   pip install --no-binary :all: pyaudio
   ```

Wenn Sie weiterhin Probleme haben, überprüfen Sie die Konsolenausgabe auf spezifische Fehlermeldungen und suchen Sie nach diesen online oder eröffnen Sie ein Issue in diesem Repository.

## Systemanforderungen

Dieses Tool wurde erfolgreich getestet auf:
- Ubuntu 22.04 LTS
- Python 3.11
- Conda 23.11.0

## Funktionsweise

Das Wortweber-Tool nutzt das OpenAI Whisper Modell für Echtzeit-Spracherkennung. Es nimmt Audioaufnahmen über das Mikrofon auf und verarbeitet diese mit Whisper, um eine textuelle Transkription zu erzeugen.

## Beitragen

Beiträge zu diesem Projekt sind willkommen! Wenn Sie Verbesserungen vorschlagen oder Fehler melden möchten, erstellen Sie bitte ein Issue oder einen Pull Request auf GitHub.

## Lizenz

Dieses Projekt steht unter der Apache License 2.0. Weitere Details finden Sie in der [LICENSE](LICENSE) Datei.
Bitte beachten Sie, dass die erweiterte Version zusätzliche Abhängigkeiten hat und möglicherweise anderen Lizenzbedingungen unterliegt. Stellen Sie sicher, dass Sie die Lizenzbedingungen aller verwendeten Bibliotheken in der erweiterten Version überprüfen und einhalten.
