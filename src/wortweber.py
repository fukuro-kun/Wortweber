# Copyright 2024 fukuro-kun
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# src/wortweber.py
import sys
import os
import warnings
import ctypes

# Füge den Projektordner zum Python-Pfad hinzu
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Unterdrücke ALSA-Warnungen
warnings.filterwarnings("ignore", category=RuntimeWarning, module="sounddevice")

# Versuche, die ALSA-Fehlermeldungen zu unterdrücken
ERROR_HANDLER_FUNC = ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p)

def py_error_handler(filename, line, function, err, fmt):
    pass

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

try:
    asound = ctypes.cdll.LoadLibrary('libasound.so.2')
    asound.snd_lib_error_set_handler(c_error_handler)
except:
    pass

# Setze Umgebungsvariable, um PulseAudio-Warnungen zu unterdrücken
os.environ['PULSE_PROP_media.role'] = 'phone'

from src.backend.wortweber_backend import WordweberBackend
from src.frontend.wortweber_gui import WordweberGUI

def main():
    """
    Hauptfunktion der Wortweber-Anwendung.
    Initialisiert das Backend und die GUI und startet die Anwendung.
    """
    backend = WordweberBackend()
    backend.list_audio_devices()  # Zeigt verfügbare Audiogeräte an
    gui = WordweberGUI(backend)
    gui.run()

if __name__ == "__main__":
    main()

# Zusätzliche Erklärungen:

# 1. Pfadmanipulation:
#    Die Zeilen, die den project_root bestimmen und zum sys.path hinzufügen,
#    stellen sicher, dass Python die Module des Projekts finden kann, unabhängig davon,
#    von wo aus das Skript ausgeführt wird.

# 2. Modularität:
#    Die Trennung von Backend und GUI in separate Klassen (WordweberBackend und WordweberGUI)
#    folgt dem Prinzip der Trennung von Belangen (Separation of Concerns) und verbessert
#    die Wartbarkeit und Erweiterbarkeit des Codes.

# 3. Einstiegspunkt:
#    Die main()-Funktion dient als zentraler Einstiegspunkt der Anwendung.
#    Sie wird nur ausgeführt, wenn das Skript direkt gestartet wird (nicht wenn es importiert wird).

# 4. Audiogeräte-Auflistung:
#    Der Aufruf von backend.list_audio_devices() vor dem Start der GUI
#    gibt dem Benutzer wichtige Informationen über verfügbare Audiogeräte,
#    was bei der Konfiguration und Fehlerbehebung hilfreich sein kann.

# 5. Flexibilität:
#    Durch die Trennung von Backend und GUI ist es einfach, in Zukunft alternative
#    Benutzeroberflächen (z.B. eine Kommandozeilenschnittstelle) zu implementieren,
#    ohne das Backend ändern zu müssen.

# 6. Startprozess:
#    Die Reihenfolge der Operationen in main() - zuerst Backend initialisieren,
#    dann Audiogeräte auflisten und schließlich die GUI starten - gewährleistet,
#    dass alle notwendigen Komponenten bereit sind, bevor der Benutzer mit der Anwendung interagiert.

# 7. ALSA-Warnung Unterdrückung:
#    Der neu hinzugefügte Code am Anfang der Datei dient dazu, ALSA-bezogene Warnungen
#    zu unterdrücken, die oft beim Start von Python-Programmen mit Audiogeräten auftreten.
#    Dies verbessert die Benutzerfreundlichkeit, indem es unnötige Warnmeldungen in der Konsole reduziert.

# Hinweis zur Projektstruktur:
# Diese Datei dient als Einstiegspunkt für die gesamte Anwendung.
# Sie verbindet das Backend (die Logik der Anwendung) mit dem Frontend (der Benutzeroberfläche).
# Diese Struktur ermöglicht eine klare Trennung der Verantwortlichkeiten und erleichtert
# sowohl die Wartung als auch zukünftige Erweiterungen der Anwendung.
