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

import json
import os
import threading
import time
from typing import Dict, Any, Optional, List
from src.config import (DEFAULT_LANGUAGE, DEFAULT_WHISPER_MODEL, DEFAULT_THEME,
                        DEFAULT_WINDOW_SIZE, DEFAULT_CHAR_DELAY, DEFAULT_FONT_SIZE,
                        DEFAULT_INCOGNITO_MODE, DEFAULT_PLUGIN_DIR, DEFAULT_ENABLED_PLUGINS,
                        DEFAULT_PLUGIN_SETTINGS, PLUGIN_SPECIFIC_SETTINGS)
from src.utils.error_handling import handle_exceptions, logger

class SettingsManager:
    """
    Verwaltet das Laden, Speichern und Abrufen von Benutzereinstellungen für die Wortweber-Anwendung.
    """

    @handle_exceptions
    def __init__(self):
        """Initialisiert den SettingsManager und lädt bestehende Einstellungen."""
        self.settings_file = "user_settings.json"
        self.settings: Dict[str, Any] = self.load_settings()
        self.observers: List[Any] = []
        self.changed_settings: set = set()
        self.save_timer: Optional[threading.Timer] = None
        self.last_save_time: float = 0
        self.version: int = self.settings.get("version", 1)
        logger.info("SettingsManager initialisiert", category='SETTINGS')
        self.print_current_settings()

    @handle_exceptions
    def load_settings(self) -> Dict[str, Any]:
        """
        Lädt Benutzereinstellungen aus einer JSON-Datei.
        Falls die Datei nicht existiert oder beschädigt ist, werden Standardeinstellungen verwendet.

        :return: Ein Dictionary mit den geladenen Einstellungen
        """
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, "r") as f:
                    settings = json.load(f)
                logger.info("Einstellungen erfolgreich geladen", category='SETTINGS')
                if "plugins" not in settings:
                    settings["plugins"] = self.get_default_settings()["plugins"]
                return settings
            except json.JSONDecodeError:
                logger.error("Fehler beim Laden der Einstellungen. Verwende Standardeinstellungen.", category='SETTINGS')
        return self.get_default_settings()

    @handle_exceptions
    def save_settings(self):
        """Speichert die aktuellen Einstellungen in einer JSON-Datei."""
        current_time = time.time()
        if current_time - self.last_save_time < 1:  # Verhindert zu häufiges Speichern
            return

        temp_file = f"{self.settings_file}.temp"
        try:
            with open(temp_file, "w") as f:
                json.dump(self.settings, f, indent=4)
            os.replace(temp_file, self.settings_file)
            self.last_save_time = current_time
            logger.info("Einstellungen erfolgreich gespeichert", category='SETTINGS')
            self.notify_observers()
            self.changed_settings.clear()
        except Exception as e:
            logger.error(f"Fehler beim Speichern der Einstellungen: {e}", category='SETTINGS')
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    @handle_exceptions
    def get_setting(self, key: str, default: Optional[Any] = None) -> Any:
        """
        Ruft den Wert einer bestimmten Einstellung ab.

        :param key: Der Schlüssel der gewünschten Einstellung
        :param default: Ein optionaler Standardwert, falls die Einstellung nicht existiert
        :return: Der Wert der Einstellung oder der Standardwert
        """
        value = self.settings.get(key, default)
        if value is None:
            value = self.get_default_settings().get(key, default)
        logger.debug(f"Einstellung abgerufen: {key} = {value}", category='SETTINGS')
        return value

    @handle_exceptions
    def set_setting(self, key: str, value: Any):
        """
        Setzt den Wert einer bestimmten Einstellung und plant das Speichern.

        :param key: Der Schlüssel der zu setzenden Einstellung
        :param value: Der neue Wert der Einstellung
        """
        if self.settings.get(key) != value:
            self.settings[key] = value
            self.changed_settings.add(key)
            if key != "text_content":  # Vermeiden des Loggens von Transkriptionen
                logger.info(f"Einstellung geändert: {key} = {value}", category='SETTINGS')
            self.schedule_save()
            self.notify_observers(key, value)

    @handle_exceptions
    def schedule_save(self):
        """Plant das Speichern der Einstellungen."""
        if self.save_timer is None:
            self.save_timer = threading.Timer(5.0, self.save_settings)
            self.save_timer.start()

    @handle_exceptions
    def get_default_settings(self) -> Dict[str, Any]:
        """
        Liefert ein Dictionary mit den Standardeinstellungen der Anwendung.

        :return: Ein Dictionary mit Standardeinstellungen
        """
        return {
            "version": self.version,
            "language": DEFAULT_LANGUAGE,
            "model": DEFAULT_WHISPER_MODEL,
            "theme": DEFAULT_THEME,
            "window_geometry": DEFAULT_WINDOW_SIZE,
            "output_mode": "textfenster",
            "delay_mode": "no_delay",
            "char_delay": str(DEFAULT_CHAR_DELAY),
            "auto_copy": True,
            "text_content": "",
            "font_size": DEFAULT_FONT_SIZE,
            "save_test_recording": False,
            "incognito_mode": DEFAULT_INCOGNITO_MODE,
            "plugins": {
                "enabled_plugins": DEFAULT_ENABLED_PLUGINS,
                "plugin_dir": DEFAULT_PLUGIN_DIR,
                "global_settings": DEFAULT_PLUGIN_SETTINGS["global"],
                "specific_settings": PLUGIN_SPECIFIC_SETTINGS
            }
        }

    @handle_exceptions
    def get_plugin_settings(self, plugin_name: str) -> Dict[str, Any]:
        """
        Ruft die Einstellungen für ein spezifisches Plugin ab.

        :param plugin_name: Name des Plugins
        :return: Ein Dictionary mit den Plugin-Einstellungen
        """
        plugin_settings = self.settings.get("plugins", {}).get("specific_settings", {}).get(plugin_name, {})
        global_settings = self.settings.get("plugins", {}).get("global_settings", {})
        return {**global_settings, **plugin_settings}

    @handle_exceptions
    def set_plugin_settings(self, plugin_name: str, settings: Dict[str, Any]):
        """
        Setzt die Einstellungen für ein spezifisches Plugin.

        :param plugin_name: Name des Plugins
        :param settings: Ein Dictionary mit den neuen Plugin-Einstellungen
        """
        if "plugins" not in self.settings:
            self.settings["plugins"] = self.get_default_settings()["plugins"]
        if "specific_settings" not in self.settings["plugins"]:
            self.settings["plugins"]["specific_settings"] = {}
        self.settings["plugins"]["specific_settings"][plugin_name] = settings
        self.changed_settings.add(f"plugins.specific_settings.{plugin_name}")
        self.schedule_save()
        logger.info(f"Plugin-Einstellungen für {plugin_name} aktualisiert", category='SETTINGS')

    @handle_exceptions
    def print_current_settings(self):
        """Gibt die aktuellen Einstellungen in lesbarer Form aus."""
        logger.info("Aktuelle Einstellungen:", category='SETTINGS')
        for key, value in self.settings.items():
            if key != "plugins":
                logger.info(f"  {key}: {value}", category='SETTINGS')
            else:
                logger.info("  Plugin-Einstellungen:", category='SETTINGS')
                for plugin_key, plugin_value in value.items():
                    logger.info(f"    {plugin_key}: {plugin_value}", category='SETTINGS')

    def add_observer(self, observer):
        """Fügt einen Beobachter hinzu."""
        self.observers.append(observer)

    def remove_observer(self, observer):
        """Entfernt einen Beobachter."""
        self.observers.remove(observer)

    def notify_observers(self, key=None, value=None):
        """Benachrichtigt alle Beobachter über Änderungen."""
        for observer in self.observers:
            if hasattr(observer, 'on_settings_changed'):
                observer.on_settings_changed(key, value)

    @handle_exceptions
    def migrate_settings(self):
        """Migriert die Einstellungen auf die neueste Version."""
        if self.version < 2:
            # Beispiel für eine Migration von Version 1 zu Version 2
            if "new_setting" not in self.settings:
                self.settings["new_setting"] = "default_value"
            self.version = 2
            self.settings["version"] = self.version
            logger.info(f"Einstellungen auf Version {self.version} migriert", category='SETTINGS')
        # Fügen Sie hier weitere Migrationsschritte hinzu, wenn nötig

    @handle_exceptions
    def validate_settings(self):
        """Überprüft die Gültigkeit der Einstellungen."""
        # Implementieren Sie hier Validierungslogik
        pass


# Zusätzliche Erklärungen:

# 1. Versionierung:
#    Die Versionsnummer wird nun in den Einstellungen gespeichert und kann für
#    zukünftige Migrationen verwendet werden.

# 2. Atomic Writes:
#    Die save_settings Methode verwendet nun temporäre Dateien und os.replace,
#    um atomare Schreibvorgänge zu gewährleisten.

# 3. Verzögertes Speichern:
#    Die schedule_save Methode plant das Speichern mit einer Verzögerung,
#    um häufige Schreibvorgänge zu reduzieren.

# 4. Änderungsverfolgung:
#    changed_settings hält eine Liste der geänderten Einstellungen,
#    um selektives Speichern zu ermöglichen.

# 5. Validierung:
#    Eine Methode zur Validierung der Einstellungen wurde hinzugefügt,
#    die in Zukunft implementiert werden kann.

# 6. Migration:
#    Die migrate_settings Methode ermöglicht es, Einstellungen zwischen
#    verschiedenen Versionen zu migrieren.

# Diese Implementierung bietet eine robuste und erweiterbare Grundlage für die
# Verwaltung von Einstellungen in der Wortweber-Anwendung, mit Fokus auf
# Datenkonsistenz, Effizienz und Zukunftssicherheit.
