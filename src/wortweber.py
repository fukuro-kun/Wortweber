# Wortweber - Echtzeit-Sprachtranskription mit KI
# Copyright (C) 2024 fukuro-kun
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# src/wortweber.py
import sys
import os
import warnings
import ctypes
import atexit

# Füge den Projektordner zum Python-Pfad hinzu
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.utils.error_handling import handle_exceptions, logger

# Unterdrücke ALSA-Warnungen
warnings.filterwarnings("ignore", category=RuntimeWarning, module="sounddevice")

# Unterdrücke JACK-Fehlermeldungen
os.environ['JACK_NO_START_SERVER'] = '1'

# Versuche, die ALSA-Fehlermeldungen zu unterdrücken
ERROR_HANDLER_FUNC = ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p)

def py_error_handler(filename, line, function, err, fmt):
    pass

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

try:
    asound = ctypes.cdll.LoadLibrary('libasound.so.2')
    asound.snd_lib_error_set_handler(c_error_handler)
except:
    logger.warning("Konnte ALSA-Fehlermeldungen nicht unterdrücken")

# Setze Umgebungsvariable, um PulseAudio-Warnungen zu unterdrücken
os.environ['PULSE_PROP_media.role'] = 'phone'

from src.backend.wortweber_backend import WordweberBackend
from src.frontend.wortweber_gui import WordweberGUI
from src.frontend.settings_manager import SettingsManager

class Wortweber:
    @handle_exceptions
    def __init__(self):
        self.settings_manager = SettingsManager()
        self.backend = WordweberBackend(self.settings_manager)
        self.gui = WordweberGUI(self.backend)

        # Füge diese Zeile hinzu, um die aktuellen Einstellungen zu drucken
        self.settings_manager.print_current_settings()

    @handle_exceptions
    def run(self):
        self.backend.list_audio_devices()  # Zeigt verfügbare Audiogeräte an
        self.gui.run()

    def cleanup(self):
        if hasattr(self, 'backend'):
            self.backend.audio_processor.cleanup()
        logger.info("Wortweber-Anwendung beendet und Ressourcen bereinigt")

@handle_exceptions
def main():
    """
    Hauptfunktion der Wortweber-Anwendung.
    Initialisiert das Backend und die GUI und startet die Anwendung.
    """
    logger.info("Starte Wortweber-Anwendung")
    app = Wortweber()
    atexit.register(app.cleanup)
    app.run()

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
