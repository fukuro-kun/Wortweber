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

"""
Dieses Modul implementiert den PluginManager für die Wortweber-Anwendung.
Es verwaltet das Laden, Aktivieren, Deaktivieren und Ausführen von Plugins.
"""

# Standardbibliotheken
import os
from typing import Dict, List, Union, Optional, Any
from types import MethodType

# Projektspezifische Module
from src.plugin_system.plugin_interface import AbstractPlugin
from src.plugin_system.plugin_loader import PluginLoader
from src.frontend.settings_manager import SettingsManager
from src.utils.error_handling import handle_exceptions, logger
from src.plugin_system.event_system import EventSystem

# Globale Konstante für bedingtes Debug-Logging
DEBUG_LOGGING = False

class PluginManager:
    """
    Verwaltet den gesamten Lebenszyklus der Plugins in der Wortweber-Anwendung.

    Diese Klasse ist verantwortlich für die Entdeckung, Aktivierung, Deaktivierung
    und Aktualisierung von Plugins. Sie stellt auch sicher, dass der Plugin-Status
    konsistent bleibt und verwaltet die Plugin-Einstellungen.

    Attributes:
        plugin_dir (str): Das Verzeichnis, in dem die Plugins gespeichert sind.
        plugins (Dict[str, AbstractPlugin]): Ein Dictionary aller geladenen Plugins.
        active_plugins (List[str]): Eine Liste der Namen der aktuell aktiven Plugins.
        settings_manager (SettingsManager): Verwaltet die Einstellungen für Plugins.
        plugin_loader (PluginLoader): Lädt Plugin-Module dynamisch.
        event_system (EventSystem): Verwaltet das Event-System für Plugins.
        plugin_ui_elements (Dict[str, Dict[str, Any]]): UI-Elemente der Plugins.
        plugin_menu_entries (Dict[str, List[Dict[str, Any]]]): Menüeinträge der Plugins.
        plugin_context_menu_entries (Dict[str, List[Dict[str, Any]]]): Kontextmenüeinträge der Plugins.
    """

    def __init__(self, plugin_dir: str, settings_manager: SettingsManager):
        """
        Initialisiert den PluginManager.

        Args:
            plugin_dir (str): Das Verzeichnis, in dem die Plugins gespeichert sind.
            settings_manager (SettingsManager): Der SettingsManager für die Verwaltung von Plugin-Einstellungen.
        """
        self.plugin_dir = plugin_dir
        self.plugins: Dict[str, AbstractPlugin] = {}
        self.active_plugins: List[str] = []
        self.settings_manager = settings_manager
        self.plugin_loader = PluginLoader(plugin_dir)
        self.event_system = EventSystem()
        self.plugin_ui_elements: Dict[str, Dict[str, Any]] = {}
        self.plugin_menu_entries: Dict[str, List[Dict[str, Any]]] = {}
        self.plugin_context_menu_entries: Dict[str, List[Dict[str, Any]]] = {}
        if DEBUG_LOGGING:
            logger.debug("PluginManager initialisiert")

    @handle_exceptions
    def discover_plugins(self) -> None:
        """
        Durchsucht das Plugin-Verzeichnis nach verfügbaren Plugins und lädt sie.

        Diese Methode scannt das Plugin-Verzeichnis, lädt alle verfügbaren Plugins
        und aktiviert diejenigen, die als aktiviert markiert sind.
        """
        if DEBUG_LOGGING:
            logger.debug(f"Suche nach Plugins in: {self.plugin_dir}")
        plugin_settings = self.settings_manager.get_setting("plugins", {}).get("specific_settings", {})
        loaded_plugins = self.plugin_loader.load_all_plugins(plugin_settings)
        for plugin in loaded_plugins:
            if plugin.name not in self.plugins:
                self.plugins[plugin.name] = plugin
                self.plugin_ui_elements[plugin.name] = plugin.get_ui_elements()
                self.plugin_menu_entries[plugin.name] = plugin.get_menu_entries()
                self.plugin_context_menu_entries[plugin.name] = plugin.get_context_menu_entries()
                logger.info(f"Plugin entdeckt: {plugin.name} v{plugin.version}")
            elif DEBUG_LOGGING:
                logger.debug(f"Plugin {plugin.name} bereits geladen, wird übersprungen")

        self.load_enabled_plugins()
        self.verify_plugin_status()

        logger.info(f"Insgesamt {len(self.plugins)} Plugins geladen, {len(self.active_plugins)} aktiv")

    @handle_exceptions
    def load_enabled_plugins(self) -> None:
        """
        Lädt und aktiviert alle Plugins, die als 'enabled' markiert sind.

        Diese Methode aktiviert alle Plugins, die in den Einstellungen als aktiviert
        markiert sind, und löst deren Abhängigkeiten auf.
        """
        enabled_plugins = self.settings_manager.get_enabled_plugins()
        for plugin_name in enabled_plugins:
            if plugin_name in self.plugins and plugin_name not in self.active_plugins:
                self.activate_plugin(plugin_name)
            elif plugin_name not in self.plugins:
                logger.warning(f"Zuvor aktiviertes Plugin nicht gefunden: {plugin_name}")

        self.resolve_dependencies()

        if DEBUG_LOGGING:
            logger.debug(f"Insgesamt {len(self.plugins)} Plugins geladen, {len(self.active_plugins)} aktiv")

    @handle_exceptions
    def activate_plugin(self, plugin_name: str) -> bool:
        """
        Aktiviert ein spezifisches Plugin.

        Args:
            plugin_name (str): Name des zu aktivierenden Plugins.

        Returns:
            bool: True, wenn das Plugin erfolgreich aktiviert wurde, sonst False.
        """
        if plugin_name in self.plugins and plugin_name not in self.active_plugins:
            plugin = self.plugins[plugin_name]
            settings = self.settings_manager.get_plugin_settings(plugin_name)
            try:
                plugin.activate(settings)
                self.active_plugins.append(plugin_name)
                logger.info(f"Plugin aktiviert: {plugin_name}")
                self.update_enabled_plugins()
                plugin.register_events(self.event_system)
                self.update_plugin_ui_elements(plugin_name)
                self.update_plugin_menu_entries(plugin_name)
                self.update_plugin_context_menu_entries(plugin_name)
                self.event_system.emit('plugin_activated', plugin_name)
                return True
            except Exception as e:
                logger.error(f"Fehler beim Aktivieren des Plugins {plugin_name}: {str(e)}")
        return False

    @handle_exceptions
    def deactivate_plugin(self, plugin_name: str) -> bool:
        """
        Deaktiviert ein spezifisches Plugin.

        Args:
            plugin_name (str): Name des zu deaktivierenden Plugins.

        Returns:
            bool: True, wenn das Plugin erfolgreich deaktiviert wurde, sonst False.
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
                self.remove_plugin_events(plugin)
                self.remove_plugin_ui_elements(plugin_name)
                self.remove_plugin_menu_entries(plugin_name)
                self.remove_plugin_context_menu_entries(plugin_name)
                self.event_system.emit('plugin_deactivated', plugin_name)
                return True
            except Exception as e:
                logger.error(f"Fehler beim Deaktivieren des Plugins {plugin_name}: {str(e)}")
        return False

    @handle_exceptions
    def remove_plugin_events(self, plugin: AbstractPlugin) -> None:
        """
        Entfernt alle Event-Listener eines Plugins.

        Args:
            plugin (AbstractPlugin): Das Plugin, dessen Event-Listener entfernt werden sollen.
        """
        for event_type in self.event_system.listeners:
            self.event_system.listeners[event_type] = [
                listener for listener in self.event_system.listeners[event_type]
                if not isinstance(listener, MethodType) or listener.__self__ is not plugin
            ]

    @handle_exceptions
    def emit_event(self, event_type: str, data: Any = None) -> None:
        """
        Löst ein Event für alle aktiven Plugins aus.

        Args:
            event_type (str): Der Typ des auszulösenden Events.
            data (Any, optional): Optionale Daten, die mit dem Event gesendet werden.
        """
        self.event_system.emit(event_type, data)

    @handle_exceptions
    def update_enabled_plugins(self) -> None:
        """
        Aktualisiert die Liste der aktivierten Plugins in den Einstellungen.

        Diese Methode stellt sicher, dass die Liste der aktivierten Plugins in den
        Einstellungen mit dem aktuellen Zustand des PluginManagers übereinstimmt.
        """
        enabled_plugins = self.settings_manager.get_enabled_plugins()
        plugins_settings = self.settings_manager.get_setting("plugins", {})
        plugins_settings["enabled_plugins"] = enabled_plugins
        self.settings_manager.set_setting("plugins", plugins_settings)

    @handle_exceptions
    def reload_plugin(self, plugin_name: str) -> bool:
        """
        Lädt ein Plugin neu.

        Diese Methode deaktiviert das angegebene Plugin, lädt es neu und aktiviert es wieder,
        falls es zuvor aktiv war. Dies ermöglicht das Aktualisieren von Plugins zur Laufzeit.

        Args:
            plugin_name (str): Name des neu zu ladenden Plugins.

        Returns:
            bool: True, wenn das Plugin erfolgreich neu geladen wurde, sonst False.
        """
        if plugin_name not in self.plugins:
            logger.warning(f"Plugin {plugin_name} nicht gefunden und kann nicht neu geladen werden.")
            return False

        was_active = plugin_name in self.active_plugins
        if was_active:
            self.deactivate_plugin(plugin_name)

        try:
            new_plugin = self.plugin_loader.reload_plugin(plugin_name)
            if new_plugin:
                self.plugins[plugin_name] = new_plugin
                self.plugin_ui_elements[plugin_name] = new_plugin.get_ui_elements()
                self.plugin_menu_entries[plugin_name] = new_plugin.get_menu_entries()
                self.plugin_context_menu_entries[plugin_name] = new_plugin.get_context_menu_entries()
                if was_active:
                    self.activate_plugin(plugin_name)
                new_plugin.on_update()
                logger.info(f"Plugin {plugin_name} erfolgreich neu geladen")
                return True
            else:
                logger.error(f"Fehler beim Neuladen des Plugins {plugin_name}")
                return False
        except Exception as e:
            logger.error(f"Unerwarteter Fehler beim Neuladen des Plugins {plugin_name}: {str(e)}")
            return False

    @handle_exceptions
    def resolve_dependencies(self) -> None:
        """
        Löst Plugin-Abhängigkeiten auf.

        Diese Methode überprüft und aktiviert alle notwendigen Abhängigkeiten für jedes Plugin.
        """
        for plugin in self.plugins.values():
            for dependency in plugin.dependencies:
                if dependency not in self.plugins:
                    logger.warning(f"Abhängigkeit {dependency} für Plugin {plugin.name} nicht gefunden")
                elif dependency not in self.active_plugins:
                    self.activate_plugin(dependency)

    @handle_exceptions
    def update_plugin_settings(self, plugin_name: str, settings: Dict[str, Any]) -> bool:
        """
        Aktualisiert die Einstellungen eines Plugins.

        Args:
            plugin_name (str): Name des Plugins.
            settings (Dict[str, Any]): Neue Einstellungen für das Plugin.

        Returns:
            bool: True, wenn die Einstellungen erfolgreich aktualisiert wurden, sonst False.
        """
        if plugin_name in self.plugins:
            plugin = self.plugins[plugin_name]
            try:
                validated_settings = self.plugin_loader.validate_plugin_settings(plugin, settings)
                plugin.set_settings(validated_settings)
                self.settings_manager.set_plugin_settings(plugin_name, validated_settings)
                logger.info(f"Einstellungen für Plugin {plugin_name} aktualisiert und gespeichert")
                self.event_system.emit('plugin_settings_updated', plugin_name)
                return True
            except Exception as e:
                logger.error(f"Fehler beim Aktualisieren der Einstellungen für Plugin {plugin_name}: {str(e)}")
        else:
            logger.warning(f"Plugin {plugin_name} nicht gefunden, Einstellungen konnten nicht aktualisiert werden")
        return False

    @handle_exceptions
    def process_text_with_plugins(self, text: str) -> str:
        """
        Verarbeitet den Text mit allen aktiven Plugins.

        Args:
            text (str): Der zu verarbeitende Text.

        Returns:
            str: Der verarbeitete Text.
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

        Returns:
            List[Dict[str, Union[str, bool]]]: Eine Liste von Dictionaries mit Plugin-Informationen.
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
    def verify_plugin_status(self) -> bool:
        """
        Überprüft und korrigiert den Status aller Plugins beim Laden.

        Returns:
            bool: True, wenn Änderungen vorgenommen wurden, sonst False.
        """
        changes_made = False
        enabled_plugins = self.settings_manager.get_enabled_plugins()

        # Deaktiviere Plugins, die als aktiviert gespeichert sind, aber nicht mehr existieren
        for plugin_name in enabled_plugins[:]:
            if plugin_name not in self.plugins:
                logger.warning(f"Plugin {plugin_name} ist als aktiviert gespeichert, existiert aber nicht mehr. Wird entfernt.")
                enabled_plugins.remove(plugin_name)
                changes_made = True

        # Aktiviere alle Plugins, die als aktiviert gespeichert sind
        for plugin_name in enabled_plugins:
            if plugin_name not in self.active_plugins:
                self.activate_plugin(plugin_name)
                changes_made = True

        # Deaktiviere alle Plugins, die aktiv sind, aber nicht als aktiviert gespeichert sind
        for plugin_name in list(self.active_plugins):
            if plugin_name not in enabled_plugins:
                self.deactivate_plugin(plugin_name)
                changes_made = True

        # Aktualisiere die Liste der aktivierten Plugins in den Einstellungen
        self.update_enabled_plugins()

        if DEBUG_LOGGING:
            logger.debug(f"Plugin-Status verifiziert. Aktive Plugins: {', '.join(self.active_plugins)}")
        return changes_made

    @handle_exceptions
    def get_plugin_ui_elements(self) -> Dict[str, Dict[str, Any]]:
        """
        Gibt die UI-Elemente aller aktiven Plugins zurück.

        Returns:
            Dict[str, Dict[str, Any]]: Ein Dictionary mit Plugin-Namen als Schlüssel und deren UI-Elementen als Werte.
        """
        return {name: elements for name, elements in self.plugin_ui_elements.items() if name in self.active_plugins}

    @handle_exceptions
    def get_plugin_menu_entries(self) -> List[Dict[str, Any]]:
        """
        Gibt die Menüeinträge aller aktiven Plugins zurück.

        Returns:
            List[Dict[str, Any]]: Eine Liste von Menüeinträgen aller aktiven Plugins.
        """
        entries = []
        for name in self.active_plugins:
            entries.extend(self.plugin_menu_entries.get(name, []))
        return entries

    @handle_exceptions
    def get_plugin_context_menu_entries(self) -> List[Dict[str, Any]]:
        """
        Gibt die Kontextmenüeinträge aller aktiven Plugins zurück.

        Returns:
            List[Dict[str, Any]]: Eine Liste von Kontextmenüeinträgen aller aktiven Plugins.
        """
        entries = []
        for name in self.active_plugins:
            entries.extend(self.plugin_context_menu_entries.get(name, []))
        return entries

    @handle_exceptions
    def update_plugin_ui_elements(self, plugin_name: str) -> None:
        """
        Aktualisiert die UI-Elemente eines spezifischen Plugins.

        Args:
            plugin_name (str): Name des Plugins, dessen UI-Elemente aktualisiert werden sollen.
        """
        if plugin_name in self.plugins and plugin_name in self.active_plugins:
            self.plugin_ui_elements[plugin_name] = self.plugins[plugin_name].get_ui_elements()
        if DEBUG_LOGGING:
            logger.debug(f"UI-Elemente für Plugin {plugin_name} aktualisiert")

    @handle_exceptions
    def update_plugin_menu_entries(self, plugin_name: str) -> None:
        """
        Aktualisiert die Menüeinträge eines spezifischen Plugins.

        Args:
            plugin_name (str): Name des Plugins, dessen Menüeinträge aktualisiert werden sollen.
        """
        if plugin_name in self.plugins and plugin_name in self.active_plugins:
            self.plugin_menu_entries[plugin_name] = self.plugins[plugin_name].get_menu_entries()
        if DEBUG_LOGGING:
            logger.debug(f"Menüeinträge für Plugin {plugin_name} aktualisiert")

    @handle_exceptions
    def update_plugin_context_menu_entries(self, plugin_name: str) -> None:
        """
        Aktualisiert die Kontextmenüeinträge eines spezifischen Plugins.

        Args:
            plugin_name (str): Name des Plugins, dessen Kontextmenüeinträge aktualisiert werden sollen.
        """
        if plugin_name in self.plugins and plugin_name in self.active_plugins:
            self.plugin_context_menu_entries[plugin_name] = self.plugins[plugin_name].get_context_menu_entries()
        if DEBUG_LOGGING:
            logger.debug(f"Kontextmenüeinträge für Plugin {plugin_name} aktualisiert")

    @handle_exceptions
    def remove_plugin_ui_elements(self, plugin_name: str) -> None:
        """
        Entfernt die UI-Elemente eines spezifischen Plugins.

        Args:
            plugin_name (str): Name des Plugins, dessen UI-Elemente entfernt werden sollen.
        """
        self.plugin_ui_elements.pop(plugin_name, None)
        if DEBUG_LOGGING:
            logger.debug(f"UI-Elemente für Plugin {plugin_name} entfernt")

    @handle_exceptions
    def remove_plugin_menu_entries(self, plugin_name: str) -> None:
        """
        Entfernt die Menüeinträge eines spezifischen Plugins.

        Args:
            plugin_name (str): Name des Plugins, dessen Menüeinträge entfernt werden sollen.
        """
        self.plugin_menu_entries.pop(plugin_name, None)
        if DEBUG_LOGGING:
            logger.debug(f"Menüeinträge für Plugin {plugin_name} entfernt")

    @handle_exceptions
    def remove_plugin_context_menu_entries(self, plugin_name: str) -> None:
        """
        Entfernt die Kontextmenüeinträge eines spezifischen Plugins.

        Args:
            plugin_name (str): Name des Plugins, dessen Kontextmenüeinträge entfernt werden sollen.
        """
        self.plugin_context_menu_entries.pop(plugin_name, None)
        if DEBUG_LOGGING:
            logger.debug(f"Kontextmenüeinträge für Plugin {plugin_name} entfernt")

# Zusätzliche Erklärungen:

# 1. Erweiterung für Kontextmenüeinträge:
#    Die Klasse wurde um Attribute und Methoden für Kontextmenüeinträge erweitert,
#    analog zu den bestehenden Implementierungen für UI-Elemente und Hauptmenüeinträge.

# 2. Konsistente Implementierung:
#    Die neuen Methoden für Kontextmenüeinträge (get_plugin_context_menu_entries,
#    update_plugin_context_menu_entries, remove_plugin_context_menu_entries) folgen
#    dem gleichen Muster wie die entsprechenden Methoden für Menüeinträge und UI-Elemente.

# 3. Aktivierung und Deaktivierung:
#    Die Methoden activate_plugin und deactivate_plugin wurden aktualisiert, um
#    auch die Kontextmenüeinträge zu berücksichtigen.

# 4. Reload-Funktionalität:
#    Die reload_plugin Methode wurde angepasst, um auch die Kontextmenüeinträge
#    bei einem Neuladen des Plugins zu aktualisieren.

# 5. Fehlerbehandlung und Logging:
#    Alle Methoden verwenden den @handle_exceptions Decorator und
#    implementieren entsprechendes Logging für eine konsistente Fehlerbehandlung.

# Diese Erweiterungen ermöglichen es Plugins, Kontextmenüeinträge zu definieren und
# zu verwalten, was die Flexibilität und Erweiterbarkeit des Plugin-Systems weiter erhöht.
