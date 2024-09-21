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
import importlib.util
import sys
from typing import List, Optional
from src.plugin_system.plugin_interface import AbstractPlugin
from src.utils.error_handling import handle_exceptions, logger

class PluginLoader:
    """
    Verantwortlich für das dynamische Laden von Plugin-Modulen.
    """

    @handle_exceptions
    def __init__(self, plugin_dir: str = "plugins"):
        self.plugin_dir = plugin_dir
        logger.info(f"PluginLoader initialisiert mit Verzeichnis: {plugin_dir}")

    @handle_exceptions
    def load_plugin(self, plugin_name: str) -> Optional[AbstractPlugin]:
        """
        Lädt ein einzelnes Plugin basierend auf seinem Namen.

        :param plugin_name: Name des zu ladenden Plugins (ohne .py Erweiterung)
        :return: Eine Instanz des Plugins oder None, wenn das Laden fehlschlägt
        """
        plugin_path = os.path.join(self.plugin_dir, f"{plugin_name}.py")

        if not os.path.exists(plugin_path):
            logger.error(f"Plugin-Datei nicht gefunden: {plugin_path}")
            return None

        try:
            spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
            if spec is not None and spec.loader is not None:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
            else:
                logger.error(f"Konnte kein gültiges Modul-Spec für {plugin_name} erstellen")
                return None

            # Suche nach der Plugin-Klasse im geladenen Modul
            plugin_class = None
            for item in dir(module):
                obj = getattr(module, item)
                if isinstance(obj, type) and issubclass(obj, AbstractPlugin) and obj is not AbstractPlugin:
                    plugin_class = obj
                    break

            if plugin_class is None:
                logger.error(f"Keine gültige Plugin-Klasse in {plugin_name} gefunden")
                return None

            plugin_instance = plugin_class()
            logger.info(f"Plugin erfolgreich geladen: {plugin_name}")
            return plugin_instance

        except Exception as e:
            logger.error(f"Fehler beim Laden des Plugins {plugin_name}: {str(e)}")
            return None

    @handle_exceptions
    def load_all_plugins(self) -> List[AbstractPlugin]:
        """
        Lädt alle Plugins aus dem Plugin-Verzeichnis.

        :return: Eine Liste aller erfolgreich geladenen Plugin-Instanzen
        """
        loaded_plugins = []
        for filename in os.listdir(self.plugin_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                plugin_name = filename[:-3]  # Entferne die .py-Erweiterung
                plugin = self.load_plugin(plugin_name)
                if plugin:
                    loaded_plugins.append(plugin)

        logger.info(f"{len(loaded_plugins)} Plugins erfolgreich geladen")
        return loaded_plugins

    @handle_exceptions
    def reload_plugin(self, plugin_name: str) -> Optional[AbstractPlugin]:
        """
        Lädt ein bereits geladenes Plugin neu.

        :param plugin_name: Name des neu zu ladenden Plugins
        :return: Die neu geladene Plugin-Instanz oder None bei Fehler
        """
        # Entferne das alte Modul aus dem Cache, falls vorhanden
        module_name = f"{self.plugin_dir}.{plugin_name}"
        if module_name in sys.modules:
            del sys.modules[module_name]

        return self.load_plugin(plugin_name)

# Zusätzliche Erklärungen:

# 1. load_plugin:
#    Diese Methode lädt ein einzelnes Plugin dynamisch. Sie verwendet
#    importlib.util.spec_from_file_location und importlib.util.module_from_spec
#    für flexibles Laden von Modulen aus beliebigen Dateipfaden.

# 2. load_all_plugins:
#    Durchsucht das Plugin-Verzeichnis und lädt alle gültigen Plugins.

# 3. reload_plugin:
#    Ermöglicht das Neuladen eines Plugins zur Laufzeit, was nützlich für
#    Entwicklung und Debugging sein kann.

# 4. Fehlerbehandlung:
#    Jede Methode verwendet den @handle_exceptions Decorator und implementiert
#    spezifische Fehlerbehandlung, um robustes Laden zu gewährleisten.

# 5. Logging:
#    Ausführliches Logging hilft bei der Diagnose von Problemen beim Laden von Plugins.

# Diese Implementierung bietet eine flexible und robuste Möglichkeit, Plugins
# dynamisch zu laden und zu verwalten. Sie ergänzt den PluginManager gut und
# ermöglicht eine saubere Trennung zwischen dem Laden und der Verwaltung von Plugins.
