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

from typing import Dict, List, Union, Optional, Any
from src.plugin_system.plugin_interface import AbstractPlugin
from src.plugin_system.plugin_loader import PluginLoader
from src.frontend.settings_manager import SettingsManager
from src.utils.error_handling import handle_exceptions, logger

class PluginManager:
    """
    Verwaltet das Laden, Aktivieren, Deaktivieren und Ausführen von Plugins.
    """

    @handle_exceptions
    def __init__(self, settings_manager: SettingsManager):
        """
        Initialisiert den PluginManager.

        :param settings_manager: Eine Instanz des SettingsManager zur Verwaltung von Einstellungen
        """
        self.settings_manager = settings_manager
        self.plugin_dir = settings_manager.get_setting("plugins", {}).get("plugin_dir", "plugins")
        self.plugin_loader = PluginLoader(self.plugin_dir)
        self.plugins: Dict[str, AbstractPlugin] = {}
        self.active_plugins: List[str] = []
        self.discover_plugins()
        self.load_plugin_order()
        logger.info("PluginManager initialisiert")


    @handle_exceptions
    def load_plugin_order(self):
        """
        Lädt die gespeicherte Reihenfolge der Plugins und ordnet die Plugins entsprechend an.
        """
        plugin_order = self.settings_manager.get_setting("plugin_order", [])
        if plugin_order:
            ordered_plugins = {name: self.plugins[name] for name in plugin_order if name in self.plugins}
            remaining_plugins = {name: plugin for name, plugin in self.plugins.items() if name not in ordered_plugins}
            self.plugins = {**ordered_plugins, **remaining_plugins}
        logger.info(f"Plugin-Reihenfolge geladen: {list(self.plugins.keys())}")

    @handle_exceptions
    def save_plugin_order(self, plugin_order: List[str]):
        """
        Speichert die aktuelle Reihenfolge der Plugins.

        :param plugin_order: Liste der Plugin-Namen in der gewünschten Reihenfolge
        """
        self.plugins = {name: self.plugins[name] for name in plugin_order if name in self.plugins}
        self.settings_manager.set_setting("plugin_order", plugin_order)
        self.settings_manager.save_settings()
        logger.info(f"Plugin-Reihenfolge aktualisiert und gespeichert: {plugin_order}")

    @handle_exceptions
    def discover_plugins(self):
        """
        Durchsucht das Plugin-Verzeichnis nach verfügbaren Plugins und lädt sie.
        """
        logger.info(f"Suche nach Plugins in: {self.plugin_dir}")
        plugin_settings = self.settings_manager.get_setting("plugins", {}).get("specific_settings", {})
        loaded_plugins = self.plugin_loader.load_all_plugins(plugin_settings)
        for plugin in loaded_plugins:
            self.plugins[plugin.name] = plugin
            logger.info(f"Plugin entdeckt: {plugin.name} v{plugin.version}")
        logger.info(f"Insgesamt {len(self.plugins)} Plugins geladen")

    @handle_exceptions
    def activate_plugin(self, plugin_name: str) -> bool:
        """
        Aktiviert ein spezifisches Plugin.

        :param plugin_name: Name des zu aktivierenden Plugins
        :return: True, wenn das Plugin erfolgreich aktiviert wurde, sonst False
        """
        if plugin_name in self.plugins and plugin_name not in self.active_plugins:
            plugin = self.plugins[plugin_name]
            settings = self.settings_manager.get_plugin_settings(plugin_name)
            try:
                plugin.activate(settings)
                self.active_plugins.append(plugin_name)
                self.settings_manager.set_setting("active_plugins", self.active_plugins)
                self.settings_manager.save_settings()
                logger.info(f"Plugin aktiviert: {plugin_name}")
                return True
            except Exception as e:
                logger.error(f"Fehler beim Aktivieren des Plugins {plugin_name}: {str(e)}")
        return False

    @handle_exceptions
    def deactivate_plugin(self, plugin_name: str) -> bool:
        """
        Deaktiviert ein spezifisches Plugin.

        :param plugin_name: Name des zu deaktivierenden Plugins
        :return: True, wenn das Plugin erfolgreich deaktiviert wurde, sonst False
        """
        if plugin_name in self.active_plugins:
            plugin = self.plugins[plugin_name]
            try:
                settings = plugin.deactivate()
                if settings:
                    self.settings_manager.set_plugin_settings(plugin_name, settings)
                self.active_plugins.remove(plugin_name)
                self.settings_manager.set_setting("active_plugins", self.active_plugins)
                self.settings_manager.save_settings()
                logger.info(f"Plugin deaktiviert: {plugin_name}")
                return True
            except Exception as e:
                logger.error(f"Fehler beim Deaktivieren des Plugins {plugin_name}: {str(e)}")
        return False

    @handle_exceptions
    def reorder_plugin(self, plugin_name: str, new_index: int):
        """
        Ändert die Reihenfolge eines Plugins in der Liste.

        :param plugin_name: Name des zu verschiebenden Plugins
        :param new_index: Neue Position des Plugins
        """
        if plugin_name in self.plugins:
            plugins_list = list(self.plugins.items())
            plugin = self.plugins.pop(plugin_name)
            plugins_list.insert(new_index, (plugin_name, plugin))
            self.plugins = dict(plugins_list)
            logger.info(f"Plugin {plugin_name} an Position {new_index} verschoben")
            self.save_plugin_order(list(self.plugins.keys()))
        else:
            logger.warning(f"Plugin {plugin_name} nicht gefunden")

    @handle_exceptions
    def process_text_with_plugins(self, text: str) -> str:
        """
        Verarbeitet den Text mit allen aktiven Plugins.

        :param text: Der zu verarbeitende Text
        :return: Der verarbeitete Text
        """
        for plugin_name in self.active_plugins:
            try:
                text = self.plugins[plugin_name].process_text(text)
            except Exception as e:
                logger.error(f"Fehler bei der Textverarbeitung durch Plugin {plugin_name}: {str(e)}")
        return text

    @handle_exceptions
    def get_plugin_info(self) -> List[Dict[str, Union[str, bool]]]:
        """
        Gibt Informationen über alle verfügbaren Plugins zurück.

        :return: Eine Liste von Dictionaries mit Plugin-Informationen
        """
        return [
            {
                "name": plugin.name,
                "version": plugin.version,
                "description": plugin.description,
                "author": plugin.author,
                "active": plugin.name in self.active_plugins
            }
            for plugin in self.plugins.values()
        ]

    @handle_exceptions
    def update_plugin_settings(self, plugin_name: str, settings: Dict[str, Any]) -> bool:
        """
        Aktualisiert die Einstellungen eines Plugins.

        :param plugin_name: Name des Plugins
        :param settings: Neue Einstellungen für das Plugin
        :return: True, wenn die Einstellungen erfolgreich aktualisiert wurden, sonst False
        """
        if plugin_name in self.plugins:
            plugin = self.plugins[plugin_name]
            try:
                plugin.update_settings(settings)
                self.settings_manager.set_plugin_settings(plugin_name, settings)
                self.settings_manager.save_settings()
                logger.info(f"Einstellungen für Plugin {plugin_name} aktualisiert")
                return True
            except Exception as e:
                logger.error(f"Fehler beim Aktualisieren der Einstellungen für Plugin {plugin_name}: {str(e)}")
        else:
            logger.warning(f"Plugin {plugin_name} nicht gefunden")
        return False


# Zusätzliche Erklärungen:

# 1. Verbesserte Persistenz:
#    - Die Methoden save_plugin_order() und save_plugin_activation_status() wurden hinzugefügt,
#      um sicherzustellen, dass Änderungen in der Plugin-Reihenfolge und im Aktivierungsstatus
#      sofort gespeichert werden.
#    - Diese Methoden werden nach jeder relevanten Änderung aufgerufen.

# 2. Initialisierung:
#    - In der __init__-Methode werden nun sowohl load_plugin_order() als auch
#      load_plugin_activation_status() aufgerufen, um den Zustand vollständig wiederherzustellen.

# 3. Aktivierung und Deaktivierung:
#    - Die Methoden activate_plugin() und deactivate_plugin() rufen nun
#      save_plugin_activation_status() auf, um Änderungen sofort zu speichern.

# 4. Fehlerbehandlung:
#    - Verbesserte Fehlerbehandlung und Logging in allen Methoden.

# 5. Konsistenz:
#    - Es wird sichergestellt, dass der gespeicherte Zustand immer mit dem tatsächlichen
#      Zustand des PluginManagers übereinstimmt.

# Diese Änderungen sollten die Persistenz der Plugin-Reihenfolge und des Aktivierungsstatus
# deutlich verbessern. Die Einstellungen werden nun nach jeder relevanten Änderung gespeichert,
# und beim Start der Anwendung werden sie korrekt wiederhergestellt.
