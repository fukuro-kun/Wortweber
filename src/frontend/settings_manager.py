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
from typing import Dict, Any, Optional
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
        self.settings = self.load_settings()
        self.observers = []
        logger.info("SettingsManager initialisiert")
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
                logger.info("Einstellungen erfolgreich geladen")
                # Füge fehlende Plugin-Einstellungen hinzu
                if "plugins" not in settings:
                    settings["plugins"] = self.get_default_settings()["plugins"]
                return settings
            except json.JSONDecodeError:
                logger.error("Fehler beim Laden der Einstellungen. Verwende Standardeinstellungen.")
        return self.get_default_settings()

    @handle_exceptions
    def save_settings(self):
        """Speichert die aktuellen Einstellungen in einer JSON-Datei."""
        try:
            with open(self.settings_file, "w") as f:
                json.dump(self.settings, f, indent=4)
            logger.info("Einstellungen erfolgreich gespeichert")
            self.notify_observers()
        except Exception as e:
            logger.error(f"Fehler beim Speichern der Einstellungen: {e}")

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
        logger.debug(f"Einstellung abgerufen: {key} = {value}")
        return value

    @handle_exceptions
    def set_setting(self, key: str, value: Any):
        """
        Setzt den Wert einer bestimmten Einstellung und speichert die Änderungen.

        :param key: Der Schlüssel der zu setzenden Einstellung
        :param value: Der neue Wert der Einstellung
        """
        if self.settings.get(key) != value:
            self.settings[key] = value
            self.save_settings()
            if key != "text_content":  # Vermeiden des Loggens von Transkriptionen
                logger.info(f"Einstellung geändert: {key} = {value}")
            self.notify_observers(key, value)

    @handle_exceptions
    def get_default_settings(self) -> Dict[str, Any]:
        """
        Liefert ein Dictionary mit den Standardeinstellungen der Anwendung.

        :return: Ein Dictionary mit Standardeinstellungen
        """
        return {
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
        self.save_settings()
        logger.info(f"Plugin-Einstellungen für {plugin_name} aktualisiert")

    @handle_exceptions
    def print_current_settings(self):
        """Gibt die aktuellen Einstellungen in lesbarer Form aus."""
        logger.info("Aktuelle Einstellungen:")
        for key, value in self.settings.items():
            if key != "plugins":
                logger.info(f"  {key}: {value}")
            else:
                logger.info("  Plugin-Einstellungen:")
                for plugin_key, plugin_value in value.items():
                    logger.info(f"    {plugin_key}: {plugin_value}")

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

# Zusätzliche Erklärungen:

# 1. Robuste Fehlerbehandlung:
#    Alle Methoden verwenden den @handle_exceptions Decorator, um eine einheitliche
#    Fehlerbehandlung und Logging zu gewährleisten.

# 2. Typisierung:
#    Die Verwendung von Typ-Annotationen verbessert die Lesbarkeit und ermöglicht
#    eine bessere statische Codeanalyse.

# 3. Standardeinstellungen:
#    Die get_default_settings Methode zentralisiert die Definition von Standardwerten,
#    was die Wartung und Aktualisierung erleichtert.

# 4. Plugin-Unterstützung:
#    Spezielle Methoden für Plugin-Einstellungen ermöglichen eine flexible Verwaltung
#    von Plugin-spezifischen Konfigurationen.

# 5. Logging:
#    Umfangreiches Logging hilft bei der Fehlersuche und Überwachung des Einstellungsverhaltens.

# 6. Beobachter-Muster:
#    Die Implementation des Beobachter-Musters ermöglicht es anderen Teilen der Anwendung,
#    auf Einstellungsänderungen zu reagieren.

# 7. Datenpersistenz:
#    Die Klasse kümmert sich um das Laden und Speichern von Einstellungen in einer JSON-Datei,
#    was die Persistenz zwischen Anwendungssitzungen gewährleistet.

# Diese Implementierung bietet eine robuste und erweiterbare Grundlage für die
# Verwaltung von Einstellungen in der Wortweber-Anwendung.
