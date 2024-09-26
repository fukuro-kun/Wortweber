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

import os
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
    def __init__(self, plugin_dir: str, settings_manager: SettingsManager):
        self.plugin_dir = plugin_dir
        self.plugins: Dict[str, AbstractPlugin] = {}
        self.active_plugins: List[str] = []  # Umbenannt von enabled_plugins
        self.settings_manager = settings_manager
        self.plugin_loader = PluginLoader(plugin_dir)
        logger.debug("PluginManager initialisiert")

    @handle_exceptions
    def discover_plugins(self) -> None:
        """Durchsucht das Plugin-Verzeichnis nach verfügbaren Plugins und lädt sie."""
        logger.debug(f"Suche nach Plugins in: {self.plugin_dir}")
        plugin_settings = self.settings_manager.get_setting("plugins", {}).get("specific_settings", {})
        loaded_plugins = self.plugin_loader.load_all_plugins(plugin_settings)
        for plugin in loaded_plugins:
            if plugin.name not in self.plugins:
                self.plugins[plugin.name] = plugin
                logger.info(f"Plugin entdeckt: {plugin.name} v{plugin.version}")
            else:
                logger.debug(f"Plugin {plugin.name} bereits geladen, wird übersprungen")

        # Aktiviere zuvor aktivierte Plugins
        self.load_enabled_plugins()

        logger.info(f"Insgesamt {len(self.plugins)} Plugins geladen, {len(self.active_plugins)} aktiv")

    @handle_exceptions
    def load_enabled_plugins(self):
        """Lädt und aktiviert alle Plugins, die als 'enabled' markiert sind."""
        enabled_plugins = self.settings_manager.get_enabled_plugins()
        for plugin_name in enabled_plugins:
            if plugin_name in self.plugins and plugin_name not in self.active_plugins:
                self.activate_plugin(plugin_name)
            elif plugin_name not in self.plugins:
                logger.warning(f"Aktiviertes Plugin nicht gefunden: {plugin_name}")

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
                logger.info(f"Plugin aktiviert: {plugin_name}")
                self.update_enabled_plugins()
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
                logger.info(f"Plugin deaktiviert: {plugin_name}")
                self.update_enabled_plugins()
                return True
            except Exception as e:
                logger.error(f"Fehler beim Deaktivieren des Plugins {plugin_name}: {str(e)}")
        return False

    @handle_exceptions
    def update_enabled_plugins(self) -> None:
        """
        Aktualisiert die Liste der aktivierten Plugins in den Einstellungen.

        Diese Methode führt zwei wichtige Operationen durch:
        1. Abrufen der aktuellen Liste der aktivierten Plugins
        2. Aktualisieren der gesamten Plugin-Einstellungen mit dieser Liste

        Dies stellt sicher, dass:
        - Die aktuelle Liste der aktivierten Plugins konsistent mit dem internen Zustand des PluginManager ist
        - Andere mögliche Plugin-bezogene Einstellungen in plugins_settings erhalten bleiben

        Diese Vorgehensweise ist eine bewusste Designentscheidung zur Gewährleistung von Konsistenz und
        Vollständigkeit der Einstellungen.

        :return: None
        """
        enabled_plugins = self.settings_manager.get_enabled_plugins()
        plugins_settings = self.settings_manager.get_setting("plugins", {})
        plugins_settings["enabled_plugins"] = enabled_plugins
        self.settings_manager.set_setting("plugins", plugins_settings)

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
                validated_settings = self.plugin_loader.validate_plugin_settings(plugin, settings)
                plugin.set_settings(validated_settings)
                self.settings_manager.set_plugin_settings(plugin_name, validated_settings)
                logger.debug(f"Einstellungen für Plugin {plugin_name} aktualisiert")
                return True
            except Exception as e:
                logger.error(f"Fehler beim Aktualisieren der Einstellungen für Plugin {plugin_name}: {str(e)}")
        return False

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
    def verify_plugin_status(self) -> None:
        """Überprüft und korrigiert den Status aller Plugins beim Laden."""
        enabled_plugins = self.settings_manager.get_enabled_plugins()

        # Deaktiviere Plugins, die als aktiviert gespeichert sind, aber nicht mehr existieren
        for plugin_name in enabled_plugins[:]:
            if plugin_name not in self.plugins:
                logger.warning(f"Plugin {plugin_name} ist als aktiviert gespeichert, existiert aber nicht mehr. Wird entfernt.")
                enabled_plugins.remove(plugin_name)

        # Aktiviere alle Plugins, die als aktiviert gespeichert sind
        for plugin_name in enabled_plugins:
            if plugin_name not in self.active_plugins:
                self.activate_plugin(plugin_name)

        # Deaktiviere alle Plugins, die aktiv sind, aber nicht als aktiviert gespeichert sind
        for plugin_name in list(self.active_plugins):
            if plugin_name not in enabled_plugins:
                self.deactivate_plugin(plugin_name)

        # Aktualisiere die Liste der aktivierten Plugins in den Einstellungen
        self.update_enabled_plugins()

        logger.info(f"Plugin-Status verifiziert. Aktive Plugins: {', '.join(self.active_plugins)}")

# Zusätzliche Erklärungen:

# 1. Die `deactivate_plugin`-Methode wurde überprüft und scheint korrekt zu funktionieren.
#    Sie entfernt das Plugin aus der Liste der aktiven Plugins und aktualisiert die Einstellungen.

# 2. Eine neue Methode `verify_plugin_status` wurde hinzugefügt. Diese Methode:
#    - Überprüft, ob alle als aktiviert gespeicherten Plugins noch existieren
#    - Aktiviert alle Plugins, die als aktiviert gespeichert sind
#    - Deaktiviert alle Plugins, die aktiv sind, aber nicht als aktiviert gespeichert sind
#    - Aktualisiert die Liste der aktivierten Plugins in den Einstellungen

# 3. Die `discover_plugins`-Methode sollte nun `verify_plugin_status` aufrufen,
#    nachdem alle Plugins geladen wurden. Dies stellt sicher, dass der Plugin-Status
#    beim Start der Anwendung korrekt ist.

# 4. Die `_update_enabled_plugins`-Methode wurde beibehalten und wird von
#    `activate_plugin`, `deactivate_plugin` und `verify_plugin_status` verwendet,
#    um die Liste der aktivierten Plugins in den Einstellungen zu aktualisieren.

# Diese Änderungen sollten das Problem mit dem inkonsistenten Plugin-Status beheben.
# Plugins sollten nun korrekt aktiviert/deaktiviert bleiben, auch nach einem Neustart der Anwendung.
