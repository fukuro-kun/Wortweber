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
# src/plugin_system/event_system.py
"""
Das EventSystem-Modul implementiert ein einfaches Event-Handling-System für das Wortweber Plugin-System.

Es ermöglicht das Registrieren von Listenern für bestimmte Event-Typen, das Entfernen von Listenern
und das Auslösen von Events. Dieses System unterstützt die lose Kopplung zwischen verschiedenen
Komponenten des Plugin-Systems und ermöglicht eine flexible Erweiterbarkeit.
"""
# Standardbibliotheken
from typing import Dict, List, Callable, Any, Union
from types import MethodType

# Projektspezifische Module
from src.utils.error_handling import handle_exceptions, logger


class EventSystem:
    def __init__(self):
        self.listeners: Dict[str, List[Union[Callable, MethodType]]] = {}

    @handle_exceptions
    def add_listener(self, event_type: str, listener: Union[Callable, MethodType]):
        """
        Fügt einen Listener für einen bestimmten Event-Typ hinzu.

        :param event_type: Der Typ des Events
        :param listener: Die Callback-Funktion oder Methode, die aufgerufen wird, wenn das Event auftritt
        """
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(listener)
        logger.debug(f"Listener für Event-Typ '{event_type}' hinzugefügt")

    @handle_exceptions
    def remove_listener(self, event_type: str, listener: Union[Callable, MethodType]):
        """
        Entfernt einen Listener für einen bestimmten Event-Typ.

        :param event_type: Der Typ des Events
        :param listener: Die zu entfernende Callback-Funktion oder Methode
        """
        if event_type in self.listeners and listener in self.listeners[event_type]:
            self.listeners[event_type].remove(listener)
            logger.debug(f"Listener für Event-Typ '{event_type}' entfernt")

    @handle_exceptions
    def emit(self, event_type: str, data: Any = None):
        """
        Löst ein Event aus und ruft alle registrierten Listener auf.

        :param event_type: Der Typ des auszulösenden Events
        :param data: Optionale Daten, die mit dem Event gesendet werden
        """
        if event_type in self.listeners:
            for listener in self.listeners[event_type]:
                try:
                    listener(data)
                except Exception as e:
                    logger.error(f"Fehler beim Ausführen des Listeners für Event-Typ '{event_type}': {str(e)}")
        logger.debug(f"Event '{event_type}' ausgelöst")
