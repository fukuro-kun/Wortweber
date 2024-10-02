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

# Standardbibliotheken
import json
import os
import threading
from threading import Timer
from typing import Any, Dict, List, Optional

# Projektspezifische Module
from src.config import *
from src.utils.error_handling import handle_exceptions, logger

DEBUG_LOGGING = True  # Ermöglicht detailliertes Logging für Debugging-Zwecke

class SettingsManager:
    """
    Verwaltet das Laden, Speichern und Abrufen von Benutzereinstellungen für die Wortweber-Anwendung.

    Diese Klasse ist verantwortlich für die Verwaltung aller Benutzereinstellungen, einschließlich
    Plugin-Einstellungen. Sie stellt Methoden zum Lesen, Schreiben und Aktualisieren von Einstellungen
    bereit und sorgt für die Persistenz dieser Einstellungen zwischen Anwendungssitzungen.

    Attributes:
        settings_file (str): Der Pfad zur JSON-Datei, in der die Einstellungen gespeichert werden.
        settings (Dict[str, Any]): Ein Dictionary, das die aktuellen Einstellungen enthält.
        lock (threading.Lock): Ein Lock-Objekt für Thread-Sicherheit.
    """

    def __init__(self, settings_file: str = "user_settings.json"):
        """
        Initialisiert den SettingsManager und lädt bestehende Einstellungen.

        Args:
            settings_file (str): Der Pfad zur JSON-Datei für die Einstellungen.
        """
        self.settings_file = settings_file
        self.lock = threading.Lock()
        self.settings: Dict[str, Any] = {}
        self.load_settings()
        self.save_timer = None
        self.migrate_settings()

    def delayed_save(self):
        """Verzögert das Speichern der Einstellungen um 5 Sekunden."""
        if self.save_timer:
            self.save_timer.cancel()
        self.save_timer = Timer(5.0, self.save_settings)
        self.save_timer.start()

    def load_settings(self) -> None:
        """
        Lädt Benutzereinstellungen aus der JSON-Datei.

        Falls die Datei nicht existiert oder beschädigt ist, werden Standardeinstellungen verwendet.
        """
        with self.lock:
            try:
                with open(self.settings_file, 'r') as f:
                    self.settings = json.load(f)
                if DEBUG_LOGGING:
                    logger.debug(f"Einstellungen geladen. Aktivierte Plugins: {self.settings.get('plugins', {}).get('enabled_plugins', [])}")
            except FileNotFoundError:
                logger.warning(f"Einstellungsdatei {self.settings_file} nicht gefunden. Verwende Standardeinstellungen.")
                self.settings = self.get_default_settings()
            except json.JSONDecodeError:
                logger.error(f"Fehler beim Lesen der Einstellungsdatei. Verwende Standardeinstellungen.")
                self.settings = self.get_default_settings()

    def save_settings(self) -> None:
        """
        Speichert die aktuellen Einstellungen in der JSON-Datei.
        """
        with self.lock:
            try:
                self.clean_settings()  # Bereinigen vor dem Speichern
                with open(self.settings_file, 'w') as f:
                    json.dump(self.settings, f, indent=4)
                if DEBUG_LOGGING:
                    logger.debug(f"Einstellungen in {self.settings_file} gespeichert")
                    logger.debug(f"Gespeicherte Einstellungen: {json.dumps(self.settings, indent=2)}")
            except IOError as e:
                logger.error(f"Fehler beim Speichern der Einstellungen: {e}")

    @handle_exceptions
    def get_setting(self, key: str, default: Any = None) -> Any:
        """
        Ruft den Wert einer bestimmten Einstellung ab.

        Args:
            key (str): Der Schlüssel der gewünschten Einstellung.
            default: Ein optionaler Standardwert, falls die Einstellung nicht existiert.

        Returns:
            Any: Der Wert der Einstellung oder der Standardwert.
        """
        with self.lock:
            return self.settings.get(key, default)

    @handle_exceptions
    def set_setting(self, key: str, value: Any) -> None:
        """
        Setzt den Wert einer bestimmten Einstellung und speichert sie.

        Args:
            key (str): Der Schlüssel der zu setzenden Einstellung.
            value (Any): Der neue Wert der Einstellung.
        """
        with self.lock:
            old_value = self.settings.get(key)
            if old_value != value:
                self.settings[key] = value
                self.delayed_save()
                if DEBUG_LOGGING:
                    logger.debug(f"Einstellung geändert. Schlüssel: {key}, Alter Wert: {old_value}, Neuer Wert: {value}")

    def update_settings(self, new_settings: Dict[str, Any]) -> None:
        """
        Aktualisiert mehrere Einstellungen gleichzeitig.

        Args:
            new_settings (Dict[str, Any]): Ein Dictionary mit den zu aktualisierenden Einstellungen.
        """
        with self.lock:
            self.settings.update(new_settings)
            self.save_settings()

    def set_enabled_plugins(self, enabled_plugins: List[str]) -> None:
        """
        Setzt die Liste der aktivierten Plugins.

        Args:
            enabled_plugins (List[str]): Eine Liste der Namen der zu aktivierenden Plugins.
        """
        plugins_settings = self.get_setting('plugins', {})
        plugins_settings['enabled_plugins'] = enabled_plugins
        self.set_setting('plugins', plugins_settings)
        # Entfernen des alten Schlüssels, falls vorhanden
        self.settings.pop('plugins.enabled_plugins', None)

    def get_enabled_plugins(self) -> List[str]:
        """
        Gibt eine Liste der aktivierten Plugins zurück.

        Returns:
            List[str]: Eine Liste der Namen der aktivierten Plugins.
        """
        return self.get_setting('plugins', {}).get('enabled_plugins', [])

    def toggle_plugin(self, plugin_name: str) -> bool:
        """
        Schaltet den Aktivierungsstatus eines Plugins um.

        Args:
            plugin_name (str): Der Name des Plugins.

        Returns:
            bool: True, wenn das Plugin aktiviert wurde, False, wenn es deaktiviert wurde.
        """
        with self.lock:
            enabled_plugins = self.get_enabled_plugins()
            if plugin_name in enabled_plugins:
                enabled_plugins.remove(plugin_name)
                is_enabled = False
            else:
                enabled_plugins.append(plugin_name)
                is_enabled = True
            self.set_enabled_plugins(enabled_plugins)
            return is_enabled

    @handle_exceptions
    def get_plugin_settings(self, plugin_name: str) -> Dict[str, Any]:
        """
        Ruft die Einstellungen für ein spezifisches Plugin ab.

        Args:
            plugin_name (str): Name des Plugins.

        Returns:
            Dict[str, Any]: Ein Dictionary mit den Plugin-Einstellungen.
        """
        return self.get_setting('plugins', {}).get('specific_settings', {}).get(plugin_name, {})

    @handle_exceptions
    def set_plugin_settings(self, plugin_name: str, settings: Dict[str, Any]) -> None:
        """
        Setzt die Einstellungen für ein spezifisches Plugin.

        Args:
            plugin_name (str): Name des Plugins.
            settings (Dict[str, Any]): Ein Dictionary mit den neuen Plugin-Einstellungen.
        """
        plugins_settings = self.get_setting('plugins', {})
        specific_settings = plugins_settings.get('specific_settings', {})
        specific_settings[plugin_name] = settings
        plugins_settings['specific_settings'] = specific_settings
        self.set_setting('plugins', plugins_settings)

    def get_default_settings(self) -> Dict[str, Any]:
        """
        Liefert ein Dictionary mit den Standardeinstellungen der Anwendung.

        Returns:
            Dict[str, Any]: Ein Dictionary mit Standardeinstellungen.
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

    @property
    def text_content(self) -> str:
        """
        Getter für den text_content.

        Returns:
            str: Der aktuelle Textinhalt.
        """
        return self.get_setting('text_content', '')

    @text_content.setter
    def text_content(self, value: str) -> None:
        """
        Setter für den text_content.

        Args:
            value (str): Der neue Textinhalt.
        """
        self.set_setting('text_content', value)

    def get_current_settings(self):
        """
        Gibt eine Kopie der aktuellen Einstellungen zurück.

        Returns:
            Dict[str, Any]: Eine Kopie der aktuellen Einstellungen.
        """
        return self.settings.copy()

    def migrate_settings(self):
        """Migriert alte Einstellungsformate in das neue Format."""
        if 'plugins.enabled_plugins' in self.settings:
            plugins_settings = self.settings.get('plugins', {})
            plugins_settings['enabled_plugins'] = self.settings.pop('plugins.enabled_plugins')
            self.settings['plugins'] = plugins_settings
            self.save_settings()
            if DEBUG_LOGGING:
                logger.debug("Einstellungen migriert: 'plugins.enabled_plugins' in 'plugins.enabled_plugins' verschoben")


    def clean_settings(self) -> None:
        self.settings.pop('plugins.specific_settings.Ollama LLM Chat Plugin', None)
        # Stellen Sie sicher, dass alle Plugin-Einstellungen unter plugins.specific_settings.[plugin_name] sind
        if 'plugins' in self.settings and 'specific_settings' in self.settings['plugins']:
            for plugin_name, settings in self.settings['plugins']['specific_settings'].items():
                if isinstance(settings, dict):
                    self.settings['plugins']['specific_settings'][plugin_name] = settings
        if DEBUG_LOGGING:
            logger.debug(f"Bereinigte Einstellungen: {json.dumps(self.settings, indent=2)}")

# Zusätzliche Erklärungen:

# 1. Thread-Sicherheit:
#    Die Verwendung von threading.Lock stellt sicher, dass alle Operationen auf den Einstellungen
#    thread-sicher sind. Dies ist besonders wichtig in einer Anwendung, die möglicherweise
#    mehrere Threads verwendet, um gleichzeitige Zugriffe und Dateninkonsistenzen zu vermeiden.

# 2. Fehlerbehandlung:
#    Die Methoden load_settings und save_settings enthalten robuste Fehlerbehandlung,
#    um mit fehlenden oder beschädigten Einstellungsdateien umzugehen. Dies erhöht die
#    Zuverlässigkeit der Anwendung.

# 3. Logging:
#    Detailliertes Logging wird durch die DEBUG_LOGGING Konstante gesteuert. Dies ermöglicht
#    eine flexible Debuggingunterstützung ohne Leistungseinbußen im Produktionsbetrieb.

# 4. Plugin-Verwaltung:
#    Die Methoden set_enabled_plugins, get_enabled_plugins und toggle_plugin bieten eine
#    zentrale Stelle für die Verwaltung von Plugin-Aktivierungen. Dies vereinfacht die
#    Integration des Plugin-Systems in die Hauptanwendung.

# 5. Konfigurierbarkeit:
#    Die Verwendung von Konstanten aus der config.py-Datei (wie DEFAULT_LANGUAGE, DEFAULT_WHISPER_MODEL, etc.)
#    macht die Anwendung hochgradig konfigurierbar und erleichtert zukünftige Anpassungen.

# 6. Einstellungsmigration:
#    Die migrate_settings Methode wurde hinzugefügt, um alte Einstellungsformate automatisch
#    in das neue Format zu konvertieren. Dies gewährleistet die Kompatibilität mit älteren Versionen
#    der Anwendung und erleichtert Updates.
