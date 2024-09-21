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
import importlib
from typing import Dict, List, Union
from src.plugin_system.plugin_interface import AbstractPlugin
from src.utils.error_handling import handle_exceptions, logger

class PluginManager:
    """
    Verwaltet das Laden, Aktivieren, Deaktivieren und Ausführen von Plugins.
    """

    @handle_exceptions
    def __init__(self, plugin_dir: str = "plugins"):
        self.plugin_dir = plugin_dir
        self.plugins: Dict[str, AbstractPlugin] = {}
        self.active_plugins: List[str] = []
        logger.info("PluginManager initialisiert")

    @handle_exceptions
    def discover_plugins(self) -> None:
        """Durchsucht das Plugin-Verzeichnis nach verfügbaren Plugins."""
        for filename in os.listdir(self.plugin_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                plugin_name = filename[:-3]  # Entferne die .py-Erweiterung
                try:
                    module = importlib.import_module(f"{self.plugin_dir}.{plugin_name}")
                    for attribute_name in dir(module):
                        attribute = getattr(module, attribute_name)
                        if isinstance(attribute, type) and issubclass(attribute, AbstractPlugin) and attribute is not AbstractPlugin:
                            plugin = attribute()
                            self.plugins[plugin.name] = plugin
                            logger.info(f"Plugin entdeckt: {plugin.name} v{plugin.version}")
                except Exception as e:
                    logger.error(f"Fehler beim Laden des Plugins {plugin_name}: {str(e)}")

    @handle_exceptions
    def activate_plugin(self, plugin_name: str) -> bool:
        """
        Aktiviert ein spezifisches Plugin.

        :param plugin_name: Name des zu aktivierenden Plugins
        :return: True, wenn das Plugin erfolgreich aktiviert wurde, sonst False
        """
        if plugin_name in self.plugins and plugin_name not in self.active_plugins:
            try:
                self.plugins[plugin_name].activate()
                self.active_plugins.append(plugin_name)
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
            try:
                self.plugins[plugin_name].deactivate()
                self.active_plugins.remove(plugin_name)
                logger.info(f"Plugin deaktiviert: {plugin_name}")
                return True
            except Exception as e:
                logger.error(f"Fehler beim Deaktivieren des Plugins {plugin_name}: {str(e)}")
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
                "active": plugin.name in self.active_plugins
            }
            for plugin in self.plugins.values()
        ]


# Zusätzliche Erklärungen:

# 1. discover_plugins:
#    Diese Methode durchsucht das Plugin-Verzeichnis nach Python-Dateien,
#    die Klassen enthalten, welche von AbstractPlugin erben.

# 2. activate_plugin und deactivate_plugin:
#    Diese Methoden ermöglichen das Ein- und Ausschalten von Plugins zur Laufzeit.

# 3. process_text_with_plugins:
#    Verarbeitet den Text mit allen aktiven Plugins in der Reihenfolge ihrer Aktivierung.

# 4. get_plugin_info:
#    Gibt Informationen über alle verfügbaren Plugins zurück, was nützlich für die GUI sein wird.

# 5. Fehlerbehandlung:
#    Jede Methode verwendet den @handle_exceptions Decorator und implementiert
#    spezifische Fehlerbehandlung, um die Stabilität zu gewährleisten.

# 6. Logging:
#    Ausführliches Logging hilft bei der Diagnose von Problemen mit Plugins.

# Diese Implementierung bietet eine solide Grundlage für das Plugin-System,
# ermöglicht dynamisches Laden und Verwalten von Plugins und integriert sich
# gut in die bestehende Fehlerbehandlungs- und Logging-Struktur von Wortweber.
