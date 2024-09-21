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

from abc import ABC, abstractmethod
from typing import Dict, Any

class AbstractPlugin(ABC):
    """
    Abstrakte Basisklasse für alle Wortweber-Plugins.
    Alle Plugins müssen diese Klasse erweitern und ihre Methoden implementieren.
    """

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

    @abstractmethod
    def activate(self) -> None:
        """Wird aufgerufen, wenn das Plugin aktiviert wird."""
        pass

    @abstractmethod
    def deactivate(self) -> None:
        """Wird aufgerufen, wenn das Plugin deaktiviert wird."""
        pass

    @abstractmethod
    def process_text(self, text: str) -> str:
        """
        Verarbeitet den transkribierten Text.

        :param text: Der zu verarbeitende Text
        :return: Der verarbeitete Text
        """
        pass

    @abstractmethod
    def get_settings(self) -> Dict[str, Any]:
        """
        Gibt die aktuellen Einstellungen des Plugins zurück.

        :return: Ein Dictionary mit den Einstellungen des Plugins
        """
        pass

    @abstractmethod
    def set_settings(self, settings: Dict[str, Any]) -> None:
        """
        Setzt die Einstellungen des Plugins.

        :param settings: Ein Dictionary mit den neuen Einstellungen
        """
        pass

    @abstractmethod
    def get_ui_elements(self) -> Dict[str, Any]:
        """
        Gibt UI-Elemente zurück, die in die Hauptanwendung integriert werden sollen.

        :return: Ein Dictionary mit UI-Elementen (z.B. Tkinter-Widgets)
        """
        pass
