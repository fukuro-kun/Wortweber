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
from src.backend.wortweber_backend import WordweberBackend
from src.frontend.wortweber_gui import WordweberGUI
from src.frontend.settings_manager import SettingsManager
from src.plugin_system.plugin_manager import PluginManager
from src.plugin_system.plugin_loader import PluginLoader

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

class Wortweber:
    """
    Hauptklasse der Wortweber-Anwendung.
    Koordiniert die Initialisierung und das Zusammenspiel der verschiedenen Komponenten.
    """

    @handle_exceptions
    def __init__(self):
        """
        Initialisiert die Wortweber-Anwendung.
        Erstellt Instanzen von SettingsManager, PluginManager, WordweberBackend und WordweberGUI.
        """
        self.settings_manager = SettingsManager()
        self.plugin_manager = PluginManager(self.settings_manager)
        self.backend = WordweberBackend(self.settings_manager)
        self.gui = WordweberGUI(self.backend, self.plugin_manager)
        self.restore_plugin_status()
        logger.info(f"Initiale aktive Plugins: {self.plugin_manager.active_plugins}")

        # Drucke die aktuellen Einstellungen zur Überprüfung
        self.settings_manager.print_current_settings()

    @handle_exceptions
    def restore_plugin_status(self):
        """
        Stellt den Status der Plugins wieder her.
        Aktiviert die Plugins, die beim letzten Beenden der Anwendung aktiv waren.
        """
        last_active_plugins = self.settings_manager.get_setting("active_plugins", [])
        for plugin_name in last_active_plugins:
            if plugin_name in self.plugin_manager.plugins:
                try:
                    self.plugin_manager.activate_plugin(plugin_name)
                    logger.info(f"Plugin {plugin_name} erfolgreich aktiviert")
                except Exception as e:
                    logger.error(f"Fehler beim Aktivieren von Plugin {plugin_name}: {str(e)}")
        logger.info(f"Plugin-Status wiederhergestellt. Aktive Plugins: {self.plugin_manager.active_plugins}")

    @handle_exceptions
    def run(self):
        """
        Startet die Wortweber-Anwendung.
        Initialisiert das Backend und startet die GUI.
        """
        logger.info("Starte Wortweber-Anwendung")
        self.backend.list_audio_devices()  # Zeigt verfügbare Audiogeräte an
        self.gui.run()

    def cleanup(self):
        """
        Führt Aufräumarbeiten durch, wenn die Anwendung beendet wird.
        Deaktiviert alle aktiven Plugins und speichert den finalen Zustand.
        """
        if hasattr(self, 'backend'):
            self.backend.audio_processor.cleanup()

        # Speichern des Aktivierungsstatus vor der Deaktivierung
        active_plugins = self.plugin_manager.active_plugins.copy()
        self.settings_manager.set_setting("active_plugins", active_plugins)

        # Deaktivieren aller aktiven Plugins
        for plugin_name in self.plugin_manager.active_plugins.copy():
            try:
                self.plugin_manager.deactivate_plugin(plugin_name)
                logger.info(f"Plugin {plugin_name} erfolgreich deaktiviert")
            except Exception as e:
                logger.error(f"Fehler beim Deaktivieren von Plugin {plugin_name}: {str(e)}")

        # Explizites Speichern der Einstellungen
        self.settings_manager.save_settings()

        logger.info(f"Finale aktive Plugins gespeichert: {active_plugins}")
        logger.info("Wortweber-Anwendung beendet und Ressourcen bereinigt")

@handle_exceptions
def main():
    """
    Hauptfunktion zum Starten der Wortweber-Anwendung.
    """
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

# 2. Fehlerunterdrückung:
#    Die Unterdrückung von ALSA- und JACK-Fehlermeldungen verbessert die Benutzerfreundlichkeit,
#    indem störende, oft irrelevante Warnungen in der Konsole reduziert werden.

# 3. Modularität:
#    Die Trennung von Backend, GUI und Einstellungsverwaltung in separate Klassen
#    (WordweberBackend, WordweberGUI, SettingsManager) folgt dem Prinzip der Trennung von Belangen
#    und verbessert die Wartbarkeit und Erweiterbarkeit des Codes.

# 4. Hauptanwendungsklasse:
#    Die Wortweber-Klasse dient als zentraler Koordinator, der die verschiedenen
#    Komponenten der Anwendung initialisiert und verwaltet.

# 5. Ressourcenverwaltung:
#    Die cleanup-Methode und ihre Registrierung mit atexit stellen sicher, dass
#    Ressourcen ordnungsgemäß freigegeben werden, wenn die Anwendung beendet wird.

# 6. Fehlerbehandlung und Logging:
#    Die Verwendung des @handle_exceptions Decorators und des Loggers gewährleistet
#    eine konsistente Fehlerbehandlung und -protokollierung in der gesamten Anwendung.

# 7. Einstiegspunkt:
#    Die main()-Funktion dient als zentraler Einstiegspunkt der Anwendung.
#    Sie wird nur ausgeführt, wenn das Skript direkt gestartet wird (nicht wenn es importiert wird).

# 8. Erweiterbarkeit:
#    Die Struktur der Anwendung, einschließlich der Integration des Plugin-Systems,
#    ermöglicht einfache Erweiterungen und Anpassungen der Funktionalität.

# 9. Konfigurationsmanagement:
#    Die Verwendung eines SettingsManagers zentralisiert die Verwaltung von
#    Benutzereinstellungen und erleichtert deren konsistente Anwendung in der gesamten Anwendung.

# Diese Implementierung bietet eine robuste und erweiterbare Grundlage für die
# Wortweber-Anwendung, mit besonderem Augenmerk auf Modularität, Fehlertoleranz,
# Benutzerfreundlichkeit und einfache Wartbarkeit.
