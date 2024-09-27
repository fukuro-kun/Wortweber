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
import os
import importlib
import importlib.util
import sys
from typing import List, Optional, Dict, Any

# Projektspezifische Module
from src.plugin_system.plugin_interface import AbstractPlugin
from src.utils.error_handling import handle_exceptions, logger
from src.config import DEFAULT_PLUGIN_SETTINGS

class PluginLoader:
    """
    Verantwortlich für das dynamische Laden von Plugin-Modulen.

    Diese Klasse bietet Methoden zum Laden, Neuladen und Verwalten von Plugins
    für die Wortweber-Anwendung. Sie stellt sicher, dass Plugins korrekt
    initialisiert und mit den entsprechenden Einstellungen versehen werden.
    """

    @handle_exceptions
    def __init__(self, plugin_dir: str = "plugins"):
        """
        Initialisiert den PluginLoader mit einem spezifizierten Plugin-Verzeichnis.

        Args:
            plugin_dir (str): Der Pfad zum Verzeichnis, in dem die Plugins gespeichert sind.
                              Standardmäßig ist dies "plugins".
        """
        self.plugin_dir = plugin_dir
        logger.debug(f"PluginLoader initialisiert mit Verzeichnis: {plugin_dir}")

    @handle_exceptions
    def load_plugin(self, plugin_name: str, settings: Optional[Dict[str, Any]] = None) -> Optional[AbstractPlugin]:
        """
        Lädt ein einzelnes Plugin basierend auf seinem Namen und initialisiert es mit den gegebenen Einstellungen.

        Diese Methode sucht nach der Plugin-Datei, lädt das Modul dynamisch, instanziiert die Plugin-Klasse
        und initialisiert sie mit den validierten Einstellungen.

        Args:
            plugin_name (str): Name des zu ladenden Plugins (ohne .py Erweiterung)
            settings (Optional[Dict[str, Any]]): Optionale Einstellungen für das Plugin

        Returns:
            Optional[AbstractPlugin]: Eine Instanz des Plugins oder None, wenn das Laden fehlschlägt
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

            # Validiere und setze die Plugin-Einstellungen
            validated_settings = self.validate_plugin_settings(plugin_instance, settings)
            plugin_instance.set_settings(validated_settings)

            logger.debug(f"Plugin erfolgreich geladen: {plugin_name}")
            return plugin_instance

        except Exception as e:
            logger.error(f"Fehler beim Laden des Plugins {plugin_name}: {str(e)}")
            return None

    @handle_exceptions
    def load_all_plugins(self, settings: Optional[Dict[str, Dict[str, Any]]] = None) -> List[AbstractPlugin]:
        """
        Lädt alle Plugins aus dem Plugin-Verzeichnis und initialisiert sie mit den gegebenen Einstellungen.

        Diese Methode durchsucht das Plugin-Verzeichnis nach Python-Dateien, lädt jedes gefundene Plugin
        und initialisiert es mit den entsprechenden Einstellungen, falls vorhanden.

        Args:
            settings (Optional[Dict[str, Dict[str, Any]]]): Ein Dictionary mit Plugin-Namen als Schlüssel
                                                            und ihren Einstellungen als Werte

        Returns:
            List[AbstractPlugin]: Eine Liste aller erfolgreich geladenen Plugin-Instanzen
        """
        loaded_plugins = []
        for filename in os.listdir(self.plugin_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                plugin_name = filename[:-3]  # Entferne die .py-Erweiterung
                plugin_settings = settings.get(plugin_name) if settings else None
                plugin = self.load_plugin(plugin_name, plugin_settings)
                if plugin:
                    loaded_plugins.append(plugin)

        logger.info(f"{len(loaded_plugins)} Plugins erfolgreich geladen")
        return loaded_plugins

    @handle_exceptions
    def reload_plugin(self, plugin_name: str, settings: Optional[Dict[str, Any]] = None) -> Optional[AbstractPlugin]:
        """
        Lädt ein bereits geladenes Plugin neu und initialisiert es mit den gegebenen Einstellungen.

        Diese Methode entfernt das alte Modul aus dem Cache und lädt es dann neu. Dies ermöglicht
        das Aktualisieren von Plugins zur Laufzeit.

        Args:
            plugin_name (str): Name des neu zu ladenden Plugins
            settings (Optional[Dict[str, Any]]): Optionale neue Einstellungen für das Plugin

        Returns:
            Optional[AbstractPlugin]: Die neu geladene Plugin-Instanz oder None bei Fehler
        """
        # Entferne das alte Modul aus dem Cache, falls vorhanden
        module_name = f"{self.plugin_dir}.{plugin_name}"
        if module_name in sys.modules:
            del sys.modules[module_name]

        return self.load_plugin(plugin_name, settings)

    @handle_exceptions
    def validate_plugin_settings(self, plugin: AbstractPlugin, settings: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validiert die gegebenen Einstellungen für ein Plugin und ergänzt fehlende Standardeinstellungen.

        Diese Methode kombiniert die Standardeinstellungen des Plugins mit den übergebenen Einstellungen
        und den globalen Standardeinstellungen. Sie stellt sicher, dass alle erforderlichen Einstellungen
        vorhanden sind und ignoriert unbekannte Einstellungen.

        Args:
            plugin (AbstractPlugin): Die Plugin-Instanz
            settings (Optional[Dict[str, Any]]): Die zu validierenden Einstellungen

        Returns:
            Dict[str, Any]: Ein Dictionary mit validierten und vervollständigten Einstellungen
        """
        default_settings = plugin.get_default_settings()
        validated_settings = default_settings.copy()

        if settings:
            for key, value in settings.items():
                if key in default_settings:
                    # Hier könnte eine typspezifische Validierung hinzugefügt werden
                    validated_settings[key] = value
                else:
                    logger.warning(f"Unbekannte Einstellung '{key}' für Plugin '{plugin.name}' ignoriert")

        # Füge globale Standardeinstellungen hinzu, falls nicht vorhanden
        for key, value in DEFAULT_PLUGIN_SETTINGS['global'].items():
            if key not in validated_settings:
                validated_settings[key] = value

        return validated_settings

# Zusätzliche Erklärungen:

# 1. load_plugin(plugin_name, settings):
#    Diese Methode wurde erweitert, um optionale Einstellungen zu akzeptieren.
#    Nach dem Erstellen der Plugin-Instanz werden die Einstellungen validiert und gesetzt.

# 2. load_all_plugins(settings):
#    Diese Methode wurde angepasst, um ein Dictionary mit Plugin-Einstellungen zu akzeptieren.
#    Für jedes geladene Plugin werden die entsprechenden Einstellungen übergeben.

# 3. reload_plugin(plugin_name, settings):
#    Diese Methode wurde aktualisiert, um optionale neue Einstellungen beim Neuladen zu berücksichtigen.

# 4. validate_plugin_settings(plugin, settings):
#    Diese neue Methode validiert die Einstellungen für ein Plugin.
#    Sie kombiniert die Standardeinstellungen des Plugins mit den übergebenen Einstellungen
#    und den globalen Standardeinstellungen.

# 5. Fehlerbehandlung und Logging:
#    Alle Methoden verwenden den @handle_exceptions Decorator für einheitliche Fehlerbehandlung.
#    Ausführliches Logging wurde implementiert, um den Lade- und Validierungsprozess nachvollziehbar zu machen.

# Diese Änderungen ermöglichen eine flexible und robuste Handhabung von Plugin-Einstellungen
# während des Ladevorgangs und bieten gleichzeitig Sicherheit durch Validierung.
