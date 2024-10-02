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
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List

# Drittanbieterbibliotheken
import tkinter as tk
from tkinter import ttk

# Projektspezifische Module
from src.utils.error_handling import handle_exceptions, logger
from src.plugin_system.event_system import EventSystem


class AbstractPlugin(ABC):
    """
    Abstrakte Basisklasse für alle Wortweber-Plugins.
    Alle Plugins müssen diese Klasse erweitern und ihre Methoden implementieren.
    """
    dependencies: List[str] = []  # Neue Zeile

    @property
    @abstractmethod
    def name(self) -> str:
        """Gibt den Namen des Plugins zurück."""
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        """Gibt die Version des Plugins zurück."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Gibt eine kurze Beschreibung des Plugins zurück."""
        pass

    @property
    @abstractmethod
    def author(self) -> str:
        """Gibt den Namen des Plugin-Autors zurück."""
        pass

    @handle_exceptions
    def get_default_settings(self) -> Dict[str, Any]:
        """
        Gibt die Standardeinstellungen des Plugins zurück.
        Diese Methode kann von Plugins überschrieben werden, um eigene Standardeinstellungen zu definieren.

        :return: Ein Dictionary mit den Standardeinstellungen des Plugins
        """
        return {}

    @handle_exceptions
    @abstractmethod
    def activate(self, settings: Dict[str, Any]) -> None:
        """
        Wird aufgerufen, wenn das Plugin aktiviert wird.

        :param settings: Ein Dictionary mit den aktuellen Einstellungen des Plugins
        """
        pass

    @handle_exceptions
    @abstractmethod
    def deactivate(self) -> Optional[Dict[str, Any]]:
        """
        Wird aufgerufen, wenn das Plugin deaktiviert wird.

        :return: Ein optionales Dictionary mit den zu speichernden Einstellungen des Plugins
        """
        pass

    @handle_exceptions
    @abstractmethod
    def process_text(self, text: str) -> str:
        """
        Verarbeitet den transkribierten Text.

        :param text: Der zu verarbeitende Text
        :return: Der verarbeitete Text
        """
        pass

    @handle_exceptions
    def get_settings(self) -> Dict[str, Any]:
        """
        Gibt die aktuellen Einstellungen des Plugins zurück.
        Diese Methode kann von Plugins überschrieben werden, um zusätzliche Logik für das Abrufen von Einstellungen zu implementieren.

        :return: Ein Dictionary mit den aktuellen Einstellungen des Plugins
        """
        return self.get_default_settings()

    @handle_exceptions
    def set_settings(self, settings: Dict[str, Any]) -> None:
        """
        Setzt die Einstellungen des Plugins.
        Diese Methode kann von Plugins überschrieben werden, um zusätzliche Logik für das Setzen von Einstellungen zu implementieren.

        :param settings: Ein Dictionary mit den neuen Einstellungen
        """
        pass

    def get_ui_elements(self) -> Dict[str, Any]:
        """
        Gibt UI-Elemente zurück, die in die Hauptanwendung integriert werden sollen.

        Diese Methode behält die bisherige Funktionalität bei und erweitert sie um neue Möglichkeiten.

        Returns:
            Ein Dictionary mit folgenden optionalen Schlüsseln:
            - 'widgets': Ein Dictionary mit Tkinter-Widgets (bisherige Funktionalität)
            - 'buttons': Liste von Button-Konfigurationen für die Plugin-Leiste
            - 'window': Ein Tkinter-Toplevel-Fenster oder eine Funktion, die eines erstellt
            - 'sidebar': Elemente für eine mögliche Seitenleiste

        Beispiel:
        {
            'widgets': {'my_label': tk.Label(text="Mein Plugin")},
            'buttons': [{'text': 'Plugin-Aktion', 'command': self.some_action}],
            'window': self.create_plugin_window,
            'sidebar': [{'text': 'Sidebar-Eintrag', 'command': self.sidebar_action}]
        }
        """
        return {}

    def get_menu_entries(self) -> List[Dict[str, Any]]:
        """
        Gibt eine Liste von Menüeinträgen zurück, die das Plugin zum Hauptmenü hinzufügen möchte.

        Returns:
            Eine Liste von Dictionaries mit den Schlüsseln:
            - 'label': Der anzuzeigende Text des Menüeintrags
            - 'command': Die auszuführende Funktion beim Klick
            - 'submenu': Optional, eine Liste von Untermenü-Einträgen im gleichen Format

        Beispiel:
        [
            {
                'label': 'Mein Plugin',
                'command': self.main_action,
                'submenu': [
                    {'label': 'Unterfunktion', 'command': self.sub_action}
                ]
            }
        ]
        """
        return []

    @handle_exceptions
    def on_config_change(self, key: str, value: Any) -> None:
        """
        Wird aufgerufen, wenn sich eine Konfigurationseinstellung ändert.
        Diese Methode kann von Plugins überschrieben werden, um auf Konfigurationsänderungen zu reagieren.

        :param key: Der Schlüssel der geänderten Einstellung
        :param value: Der neue Wert der Einstellung
        """
        pass

    @handle_exceptions
    def on_update(self) -> None:
        """
        Wird aufgerufen, wenn das Plugin aktualisiert wird.
        Diese Methode kann von konkreten Plugin-Implementierungen überschrieben werden,
        um spezifische Aktionen bei einem Update durchzuführen.
        """
        logger.info(f"Plugin {self.name} wurde aktualisiert.")

    @handle_exceptions
    def get_config_ui(self, parent: tk.Widget) -> ttk.Frame:
        """
        Gibt ein Tkinter Frame mit Konfigurationselementen zurück.
        Diese Methode sollte von konkreten Plugin-Implementierungen überschrieben werden,
        wenn sie eine benutzerdefinierte Konfigurationsoberfläche benötigen.

        :param parent: Das übergeordnete Tkinter-Widget
        :return: Ein ttk.Frame mit Konfigurationselementen
        """
        frame = ttk.Frame(parent)
        ttk.Label(frame, text="Keine Konfigurationsoptionen verfügbar").pack()
        return frame

    @handle_exceptions
    def register_events(self, event_system: EventSystem) -> None:
        """
        Registriert Plugin-Ereignisse.
        Diese Methode sollte von konkreten Plugin-Implementierungen überschrieben werden,
        um sich für bestimmte Ereignisse zu registrieren.

        :param event_system: Das Ereignissystem der Anwendung
        """
        pass

    @handle_exceptions
    def get_context_menu_entries(self) -> List[Dict[str, Any]]:
        """
        Gibt eine Liste von Kontextmenüeinträgen zurück, die das Plugin zum Kontextmenü hinzufügen möchte.

        Returns:
            Eine Liste von Dictionaries mit den Schlüsseln:
            - 'label': Der anzuzeigende Text des Menüeintrags
            - 'command': Die auszuführende Funktion beim Klick

        Beispiel:
        [
            {'label': 'Meine Kontextaktion', 'command': self.context_action}
        ]
        """
        return []

    def get_valid_settings(self) -> List[str]:
        """Gibt eine Liste der gültigen Einstellungsnamen für dieses Plugin zurück."""
        return []

    # Zusätzliche Erklärungen:

    # Die get_context_menu_entries Methode wurde hinzugefügt, um Plugins die Möglichkeit zu geben,
    # Einträge zum Kontextmenü hinzuzufügen. Dies erfolgt analog zur get_menu_entries Methode
    # für das Hauptmenü, um Konsistenz in der Plugin-Entwicklung zu gewährleisten.
    #
    # Die Methode gibt eine Liste von Dictionaries zurück, wobei jedes Dictionary einen
    # Menüeintrag repräsentiert. Dies ermöglicht eine flexible und erweiterbare Struktur
    # für zukünftige Erweiterungen des Kontextmenüs.


# Zusätzliche Erklärungen:

# 1. get_default_settings():
#    Diese neue Methode ermöglicht es Plugins, ihre eigenen Standardeinstellungen zu definieren.
#    Sie kann von konkreten Plugin-Implementierungen überschrieben werden.

# 2. activate(settings):
#    Die activate-Methode wurde erweitert, um Einstellungen als Parameter zu akzeptieren.
#    Dies ermöglicht es Plugins, ihre Einstellungen beim Aktivieren zu laden und zu verwenden.

# 3. deactivate():
#    Die deactivate-Methode wurde geändert, um optional ein Dictionary mit Einstellungen zurückzugeben.
#    Dies ermöglicht es Plugins, ihre aktuellen Einstellungen beim Deaktivieren zu speichern.

# 4. get_settings() und set_settings(settings):
#    Diese Methoden bieten eine Standardimplementierung für das Abrufen und Setzen von Einstellungen.
#    Plugins können diese Methoden überschreiben, um eine benutzerdefinierte Logik zu implementieren.

# 5. on_config_change(key, value):
#    Diese neue Methode ermöglicht es Plugins, auf Änderungen in den Konfigurationseinstellungen zu reagieren.
#    Sie kann von Plugins überschrieben werden, um spezifisches Verhalten zu implementieren.

# 6. Fehlerbehandlung:
#    Alle Methoden sind mit dem @handle_exceptions Decorator versehen, um eine einheitliche
#    Fehlerbehandlung und -protokollierung in der gesamten Anwendung sicherzustellen.

# Diese Änderungen bieten eine flexible und erweiterbare Grundlage für die Integration
# von Plugin-Einstellungen und -Konfigurationen in das Wortweber-Plugin-System.
