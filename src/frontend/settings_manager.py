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

# src/frontend/settings_manager.py

import json
import os
from typing import Dict, Any
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
        logger.info("SettingsManager initialisiert")
        self.print_current_settings()

    @handle_exceptions
    def load_settings(self):
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
        except Exception as e:
            logger.error(f"Fehler beim Speichern der Einstellungen: {e}")

    @handle_exceptions
    def get_setting(self, key, default=None):
        """
        Ruft den Wert einer bestimmten Einstellung ab.

        :param key: Der Schlüssel der gewünschten Einstellung
        :param default: Ein optionaler Standardwert, falls die Einstellung nicht existiert
        :return: Der Wert der Einstellung oder der Standardwert
        """
        value = self.settings.get(key, default or self.get_default_settings().get(key))
        logger.debug(f"Einstellung abgerufen: {key} = {value}")
        return value

    @handle_exceptions
    def set_setting(self, key, value):
        """
        Setzt den Wert einer bestimmten Einstellung und speichert die Änderungen.

        :param key: Der Schlüssel der zu setzenden Einstellung
        :param value: Der neue Wert der Einstellung
        """
        self.settings[key] = value
        self.save_settings()
        if key != "text_content":  # Vermeiden des Loggens von Transkriptionen
            logger.info(f"Einstellung geändert: {key} = {value}")

        # Überprüfen, ob die Einstellung tatsächlich gespeichert wurde
        saved_value = self.get_setting(key)
        if saved_value != value:
            logger.error(f"Einstellung {key} konnte nicht korrekt gespeichert werden. Erwartet: {value}, Tatsächlich: {saved_value}")

    @handle_exceptions
    def get_default_settings(self):
        """
        Liefert ein Dictionary mit den Standardeinstellungen der Anwendung.

        :return: Ein Dictionary mit Standardeinstellungen
        """
        default_settings = {
            "language": DEFAULT_LANGUAGE,
            "model": DEFAULT_WHISPER_MODEL,
            "theme": DEFAULT_THEME,
            "window_geometry": DEFAULT_WINDOW_SIZE,
            "input_mode": "textfenster",
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
        logger.debug("Standardeinstellungen abgerufen")
        return default_settings

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
        logger.info("Aktuelle Einstellungen:")
        for key, value in self.settings.items():
            if key != "plugins":
                logger.info(f"{key}: {value}")
            else:
                logger.info("Plugin-Einstellungen:")
                for plugin_key, plugin_value in value.items():
                    logger.info(f"  {plugin_key}: {plugin_value}")

# Zusätzliche Erklärungen:

# 1. Plugin-Einstellungen in get_default_settings():
#    Die Standardeinstellungen für Plugins wurden hinzugefügt, einschließlich
#    aktivierter Plugins, Plugin-Verzeichnis und globaler/spezifischer Einstellungen.

# 2. get_plugin_settings(plugin_name):
#    Diese neue Methode ermöglicht es, Einstellungen für ein spezifisches Plugin abzurufen.
#    Sie kombiniert globale und plugin-spezifische Einstellungen.

# 3. set_plugin_settings(plugin_name, settings):
#    Diese neue Methode erlaubt das Setzen von Einstellungen für ein spezifisches Plugin.
#    Sie aktualisiert die Einstellungen und speichert sie persistent.

# 4. Anpassung von load_settings():
#    Die Methode wurde erweitert, um fehlende Plugin-Einstellungen hinzuzufügen,
#    falls sie in den geladenen Einstellungen nicht vorhanden sind.

# 5. print_current_settings():
#    Diese Methode wurde aktualisiert, um auch Plugin-Einstellungen übersichtlich anzuzeigen.

# Diese Änderungen ermöglichen eine flexible und erweiterbare Verwaltung von Plugin-Einstellungen,
# während sie sich nahtlos in die bestehende Struktur des SettingsManager integrieren.
