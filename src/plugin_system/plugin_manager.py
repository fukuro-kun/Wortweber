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
        self.active_plugins: List[str] = []
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
        enabled_plugins = self.settings_manager.get_setting("plugins", {}).get("enabled_plugins", [])
        for plugin_name in enabled_plugins:
            if plugin_name in self.plugins and plugin_name not in self.active_plugins:
                self.activate_plugin(plugin_name)
            elif plugin_name not in self.plugins:
                logger.warning(f"Zuvor aktiviertes Plugin nicht gefunden: {plugin_name}")

        logger.info(f"Insgesamt {len(self.plugins)} Plugins geladen, {len(self.active_plugins)} aktiv")

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
                self._update_enabled_plugins()
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
                self._update_enabled_plugins()
                return True
            except Exception as e:
                logger.error(f"Fehler beim Deaktivieren des Plugins {plugin_name}: {str(e)}")
        return False

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
    def _update_enabled_plugins(self) -> None:
        """Aktualisiert die Liste der aktivierten Plugins in den Einstellungen."""
        plugins_settings = self.settings_manager.get_setting("plugins", {})
        plugins_settings["enabled_plugins"] = self.active_plugins
        self.settings_manager.set_setting("plugins", plugins_settings)

# Zusätzliche Erklärungen:

# 1. Plugin-Verwaltung:
#    Die Klasse PluginManager ist verantwortlich für die Verwaltung aller Plugins,
#    einschließlich des Ladens, Aktivierens, Deaktivierens und Ausführens.

# 2. Entdeckung von Plugins:
#    Die discover_plugins-Methode durchsucht das Plugin-Verzeichnis nach verfügbaren
#    Plugins und lädt sie. Zuvor aktivierte Plugins werden automatisch wieder aktiviert.

# 3. Aktivierung und Deaktivierung:
#    Die Methoden activate_plugin und deactivate_plugin ermöglichen es, Plugins zur
#    Laufzeit zu aktivieren oder zu deaktivieren. Die Liste der aktiven Plugins wird
#    in den Einstellungen gespeichert.

# 4. Einstellungsverwaltung:
#    Die update_plugin_settings-Methode ermöglicht es, die Einstellungen einzelner
#    Plugins zu aktualisieren. Die Einstellungen werden validiert und im SettingsManager gespeichert.

# 5. Textverarbeitung:
#    Die process_text_with_plugins-Methode verarbeitet Text mit allen aktiven Plugins,
#    was eine flexible Erweiterung der Textverarbeitungsfunktionen ermöglicht.

# 6. Fehlerbehandlung:
#    Alle Methoden verwenden den @handle_exceptions Decorator für eine einheitliche
#    Fehlerbehandlung und -protokollierung.

# 7. Logging:
#    Ausführliches Logging wird verwendet, um den Zustand des PluginManagers und
#    Aktionen im Zusammenhang mit Plugins zu protokollieren.

# Diese Implementierung bietet eine robuste und erweiterbare Grundlage für die
# Plugin-Verwaltung in der Wortweber-Anwendung.
