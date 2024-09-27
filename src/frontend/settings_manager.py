# src/frontend/settings_manager.py

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
from typing import Dict, Any, List
from src.config import *    # Importiert alle Variablen und Funktionen aus der config.py-Datei
from src.utils.error_handling import handle_exceptions, logger

class SettingsManager:
    """
    Verwaltet das Laden, Speichern und Abrufen von Benutzereinstellungen für die Wortweber-Anwendung.
    """

    @handle_exceptions
    def __init__(self):
        """
        Initialisiert den SettingsManager und lädt bestehende Einstellungen.

        Diese Methode setzt den Pfad zur Einstellungsdatei, lädt vorhandene Einstellungen,
        initialisiert Standardeinstellungen und stellt die Konsistenz sicher. Falls keine
        Einstellungsdatei existiert, wird sie mit Standardwerten erstellt.
        """
        self.settings_file = "user_settings.json"
        self.settings = self.load_settings()
        self.default_settings = self.get_default_settings()
        self.ensure_settings_consistency()
        if not os.path.exists(self.settings_file):
            self.save_settings()  # Speichert die Standardeinstellungen, wenn keine Datei existiert
        logger.debug("SettingsManager initialisiert")
        self.print_current_settings()

    @handle_exceptions
    def save_settings(self):
        """
        Speichert die aktuellen Einstellungen in der JSON-Datei.

        Diese Methode schreibt den aktuellen Zustand der Einstellungen in die
        'user_settings.json' Datei. Sie wird verwendet, um Änderungen zu persistieren
        und um die Datei mit Standardwerten zu initialisieren, falls sie nicht existiert.
        """
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f, indent=4)
        logger.info(f"Einstellungen in {self.settings_file} gespeichert")

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
                logger.debug("Einstellungen erfolgreich geladen")
                return settings
            except json.JSONDecodeError:
                logger.error("Fehler beim Laden der Einstellungen. Verwende Standardeinstellungen.")
        return self.get_default_settings()

    @handle_exceptions
    def ensure_settings_consistency(self):
        """Stellt sicher, dass alle erforderlichen Schlüssel in den Einstellungen vorhanden sind."""
        for key, value in self.default_settings.items():
            if key not in self.settings:
                self.settings[key] = value
            elif isinstance(value, dict) and isinstance(self.settings[key], dict):
                # Rekursiv für verschachtelte Dictionaries
                self.settings[key] = self.merge_dicts(value, self.settings[key])
        logger.debug("Einstellungskonsistenz sichergestellt")

    def merge_dicts(self, default: Dict, current: Dict) -> Dict:
        """Führt zwei Dictionaries zusammen und stellt sicher, dass alle Schlüssel vorhanden sind."""
        for key, value in default.items():
            if key not in current:
                current[key] = value
            elif isinstance(value, dict) and isinstance(current[key], dict):
                current[key] = self.merge_dicts(value, current[key])
        return current

    @handle_exceptions
    def save_setting(self, key: str, value: Any) -> None:
        """
        Speichert eine einzelne Einstellung und aktualisiert die JSON-Datei.

        :param key: Der Schlüssel der zu speichernden Einstellung
        :param value: Der neue Wert der Einstellung
        """
        try:
            # Aktualisiere den internen Zustand
            self.update_nested_dict(self.settings, key.split('.'), value)

            # Speichere die gesamten Einstellungen in der Datei
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=4)
            logger.debug(f"Einstellung gespeichert: {key} = {value}")
        except Exception as e:
            logger.error(f"Fehler beim Speichern der Einstellung {key}: {e}")

    def update_nested_dict(self, d: Dict, keys: List[str], value: Any):
        """Aktualisiert ein verschachteltes Dictionary basierend auf einer Liste von Schlüsseln."""
        for key in keys[:-1]:
            d = d.setdefault(key, {})
        d[keys[-1]] = value

    @handle_exceptions
    def get_setting(self, key: str, default=None):
        """
        Ruft den Wert einer bestimmten Einstellung ab.

        :param key: Der Schlüssel der gewünschten Einstellung
        :param default: Ein optionaler Standardwert, falls die Einstellung nicht existiert
        :return: Der Wert der Einstellung oder der Standardwert
        """
        # Immer die aktuellsten Einstellungen aus der Datei laden
        self.sync_settings_from_file()

        keys = key.split('.')
        value = self.settings
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        logger.debug(f"Einstellung abgerufen: {key} = {value}")
        return value

    @handle_exceptions
    def set_setting(self, key: str, value: Any) -> None:
        """
        Setzt den Wert einer bestimmten Einstellung und speichert die Änderungen sofort.

        :param key: Der Schlüssel der zu setzenden Einstellung
        :param value: Der neue Wert der Einstellung
        """
        if self.get_setting(key) != value:
            self.save_setting(key, value)
            if key != "text_content":  # Vermeiden des Loggens von Transkriptionen
                logger.debug(f"Einstellung geändert und sofort gespeichert: {key} = {value}")

    @handle_exceptions
    def get_current_settings(self):
        """
        Gibt ein Dictionary mit allen aktuellen Einstellungen zurück.

        :return: Ein Dictionary mit den aktuellen Einstellungen
        """
        return {
            "language": self.get_setting("language", DEFAULT_LANGUAGE),
            "model": self.get_setting("model", DEFAULT_WHISPER_MODEL),
            "theme": self.get_setting("theme", DEFAULT_THEME),
            "window_geometry": self.get_setting("window_geometry", DEFAULT_WINDOW_SIZE),
            "plugin_window_geometry": self.get_setting("plugin_window_geometry", DEFAULT_PLUGIN_WINDOW_GEOMETRY),
            "options_window_geometry": self.get_setting("options_window_geometry", DEFAULT_OPTIONS_WINDOW_GEOMETRY),
            "delay_mode": self.get_setting("delay_mode", DEFAULT_DELAY_MODE),
            "char_delay": self.get_setting("char_delay", DEFAULT_CHAR_DELAY),
            "auto_copy": self.get_setting("auto_copy", DEFAULT_AUTO_COPY),
            "text_content": self.get_setting("text_content", ""),
            "font_size": self.get_setting("font_size", DEFAULT_FONT_SIZE),
            "font_family": self.get_setting("font_family", DEFAULT_FONT_FAMILY),
            "save_test_recording": self.get_setting("save_test_recording", False),
            "incognito_mode": self.get_setting("incognito_mode", DEFAULT_INCOGNITO_MODE),
            "audio_device_index": self.get_setting("audio_device_index", DEFAULT_AUDIO_DEVICE_INDEX),
            "text_fg": self.get_setting("text_fg", DEFAULT_TEXT_FG),
            "text_bg": self.get_setting("text_bg", DEFAULT_TEXT_BG),
            "select_fg": self.get_setting("select_fg", DEFAULT_SELECT_FG),
            "select_bg": self.get_setting("select_bg", DEFAULT_SELECT_BG),
            "highlight_fg": self.get_setting("highlight_fg", DEFAULT_HIGHLIGHT_FG),
            "highlight_bg": self.get_setting("highlight_bg", DEFAULT_HIGHLIGHT_BG),
            "output_mode": self.get_setting("output_mode", DEFAULT_OUTPUT_MODE),
            "push_to_talk_key": self.get_setting("push_to_talk_key", DEFAULT_PUSH_TO_TALK_KEY)
        }
        logger.debug("Standardeinstellungen abgerufen")

    @handle_exceptions
    def get_default_settings(self):
        """
        Liefert ein Dictionary mit den Standardeinstellungen der Anwendung.

        :return: Ein Dictionary mit Standardeinstellungen
        """
        return {
            "language": DEFAULT_LANGUAGE,
            "model": DEFAULT_WHISPER_MODEL,
            "theme": DEFAULT_THEME,
            "window_geometry": DEFAULT_WINDOW_SIZE,
            "plugin_window_geometry": DEFAULT_PLUGIN_WINDOW_GEOMETRY,
            "options_window_geometry": DEFAULT_OPTIONS_WINDOW_GEOMETRY,
            "delay_mode": DEFAULT_DELAY_MODE,
            "char_delay": DEFAULT_CHAR_DELAY,
            "auto_copy": DEFAULT_AUTO_COPY,
            "text_content": "",
            "font_size": DEFAULT_FONT_SIZE,
            "font_family": DEFAULT_FONT_FAMILY,
            "save_test_recording": False,
            "incognito_mode": DEFAULT_INCOGNITO_MODE,
            "audio_device_index": DEFAULT_AUDIO_DEVICE_INDEX,
            "text_fg": DEFAULT_TEXT_FG,
            "text_bg": DEFAULT_TEXT_BG,
            "select_fg": DEFAULT_SELECT_FG,
            "select_bg": DEFAULT_SELECT_BG,
            "highlight_fg": DEFAULT_HIGHLIGHT_FG,
            "highlight_bg": DEFAULT_HIGHLIGHT_BG,
            "output_mode": DEFAULT_OUTPUT_MODE,
            "push_to_talk_key": DEFAULT_PUSH_TO_TALK_KEY,
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
        plugin_settings = self.get_setting(f"plugins.specific_settings.{plugin_name}", {})
        global_settings = self.get_setting("plugins.global_settings", {})
        return {**global_settings, **plugin_settings}

    @handle_exceptions
    def set_plugin_settings(self, plugin_name: str, settings: Dict[str, Any]):
        """
        Setzt die Einstellungen für ein spezifisches Plugin und speichert sie sofort.

        :param plugin_name: Name des Plugins
        :param settings: Ein Dictionary mit den neuen Plugin-Einstellungen
        """
        self.set_setting(f"plugins.specific_settings.{plugin_name}", settings)
        logger.info(f"Plugin-Einstellungen für {plugin_name} aktualisiert und sofort gespeichert")

    @handle_exceptions
    def print_current_settings(self):
        """
        Gibt die aktuellen Einstellungen aus.
        """
        essential_settings = ['language', 'model', 'theme', 'incognito_mode', 'output_mode']
        logger.info("Wesentliche Einstellungen:")
        for key in essential_settings:
            value = self.settings.get(key, "Nicht gesetzt")
            logger.info(f"{key}: {value}")

        logger.info("Plugin-Einstellungen:")
        logger.info(f"  Anzahl aktiver Plugins: {len(self.settings.get('plugins', {}).get('enabled_plugins', []))}")

    @handle_exceptions
    def sync_settings_from_file(self):
        """
        Synchronisiert den internen Zustand mit der JSON-Datei.

        Diese Methode liest die aktuellen Einstellungen aus der JSON-Datei und
        aktualisiert den internen Zustand des SettingsManager entsprechend.
        Wenn die Datei nicht existiert, wird sie mit Standardeinstellungen erstellt.
        """
        if not os.path.exists(self.settings_file):
            logger.warning(f"Einstellungsdatei {self.settings_file} nicht gefunden. Erstelle neue Datei mit Standardeinstellungen.")
            self.save_settings()
            return

        try:
            with open(self.settings_file, 'r') as f:
                file_settings = json.load(f)

            # Aktualisiere rekursiv die Einstellungen
            self.settings = self.merge_dicts(self.settings, file_settings)

            logger.debug("Einstellungen erfolgreich mit Datei synchronisiert")
        except json.JSONDecodeError:
            logger.error(f"Fehler beim Lesen der Einstellungsdatei. Die Datei könnte beschädigt sein.")
            # Erstelle eine Sicherungskopie der beschädigten Datei
            backup_file = f"{self.settings_file}.bak"
            os.rename(self.settings_file, backup_file)
            logger.info(f"Beschädigte Einstellungsdatei wurde als {backup_file} gesichert.")
            # Erstelle eine neue Datei mit Standardeinstellungen
            self.save_settings()
        except Exception as e:
            logger.error(f"Unerwarteter Fehler beim Synchronisieren der Einstellungen: {e}")

    @handle_exceptions
    def get_enabled_plugins(self) -> List[str]:
        plugins_settings = self.get_setting("plugins", {})
        return plugins_settings.get("enabled_plugins", [])

    @handle_exceptions
    def set_enabled_plugins(self, enabled_plugins: List[str]) -> None:
        plugins_settings = self.get_setting("plugins", {})
        plugins_settings["enabled_plugins"] = enabled_plugins
        self.set_setting("plugins", plugins_settings)

# Zusätzliche Erklärungen:

# 1. sync_settings_from_file Methode:
#    Diese Methode wurde hinzugefügt, um den internen Zustand mit der JSON-Datei zu synchronisieren.
#    Sie wird in der get_setting Methode aufgerufen, um sicherzustellen, dass immer die aktuellsten
#    Einstellungen abgerufen werden.

# 2. Überarbeitete get_setting Methode:
#    Die Methode ruft nun sync_settings_from_file auf, bevor sie den Wert zurückgibt.
#    Dies stellt sicher, dass immer die aktuellsten Einstellungen aus der Datei gelesen werden.

# 3. save_setting Methode:
#    Diese Methode aktualisiert nun sowohl den internen Zustand als auch die JSON-Datei.
#    Sie verwendet update_nested_dict, um auch verschachtelte Einstellungen korrekt zu aktualisieren.

# 4. set_setting Methode:
#    Diese Methode wurde beibehalten, um die Kompatibilität mit dem bestehenden Code zu gewährleisten.
#    Sie ruft save_setting auf, um die Änderungen sofort zu speichern.

# Diese Änderungen stellen sicher, dass die Einstellungen immer konsistent zwischen dem internen Zustand
# und der JSON-Datei sind, und dass Änderungen sofort gespeichert werden.
