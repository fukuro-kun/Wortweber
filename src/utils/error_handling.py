# src/utils/error_handling.py

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

import logging
import traceback
from typing import Callable, Any, Dict
from functools import wraps
from logging.handlers import RotatingFileHandler

class CustomLogger:
    """
    Angepasste Logger-Klasse für Wortweber mit Unterstützung für Kategorien und selektives Logging.
    """

    def __init__(self):
        """
        Initialisiert den CustomLogger mit vordefinierten Kategorien und Logging-Konfigurationen.
        """
        self.logger = logging.getLogger('Wortweber')
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(category)s: %(message)s')

        file_handler = RotatingFileHandler('wortweber.log', maxBytes=1024*1024, backupCount=5)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Vordefinierte Kategorien mit ihren Standard-Logging-Levels
        self.categories = {
            'STARTUP': logging.INFO,
            'SHUTDOWN': logging.INFO,
            'PLUGIN': logging.INFO,
            'AUDIO': logging.INFO,
            'TRANSCRIPTION': logging.INFO,
            'UI': logging.INFO,
            'SETTINGS': logging.INFO,
            'ERROR': logging.ERROR
        }

        self.disabled_categories = set()

    def log(self, category: str, message: str, level: int = None):
        """
        Loggt eine Nachricht mit der angegebenen Kategorie und dem Logging-Level.

        :param category: Die Logging-Kategorie
        :param message: Die zu loggende Nachricht
        :param level: Das Logging-Level (optional)
        """
        if category not in self.categories:
            category = 'GENERAL'
        if level is None:
            level = self.categories.get(category, logging.INFO)
        if category not in self.disabled_categories:
            self.logger.log(level, message, extra={'category': category})

    def set_category_level(self, category: str, level: int):
        """
        Setzt das Logging-Level für eine bestimmte Kategorie.

        :param category: Die zu ändernde Kategorie
        :param level: Das neue Logging-Level
        """
        self.categories[category] = level

    def disable_category(self, category: str):
        """
        Deaktiviert das Logging für eine bestimmte Kategorie.

        :param category: Die zu deaktivierende Kategorie
        """
        self.disabled_categories.add(category)

    def enable_category(self, category: str):
        """
        Aktiviert das Logging für eine zuvor deaktivierte Kategorie.

        :param category: Die zu aktivierende Kategorie
        """
        self.disabled_categories.discard(category)

logger = CustomLogger()

def log_and_raise(exception: Exception, message: str, category: str = 'ERROR', log_level: int = logging.ERROR) -> None:
    """
    Loggt eine Ausnahme und wirft sie erneut.

    :param exception: Die aufgetretene Ausnahme
    :param message: Eine beschreibende Nachricht
    :param category: Die Logging-Kategorie
    :param log_level: Das Logging-Level (Standard: ERROR)
    """
    logger.log(category, f"{message}: {str(exception)}", log_level)
    logger.log('ERROR', f"Traceback: {traceback.format_exc()}", logging.DEBUG)
    raise exception

def handle_exceptions(func: Callable) -> Callable:
    """
    Ein Decorator zur einheitlichen Ausnahmebehandlung.

    :param func: Die zu dekorierende Funktion
    :return: Die dekorierte Funktion
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            log_and_raise(e, f"Fehler in {func.__name__}")
    return wrapper

# Zusätzliche Erklärungen:

# 1. Kategoriebasiertes Logging:
#    Der CustomLogger ermöglicht es, Logs in verschiedene Kategorien einzuteilen.
#    Dies verbessert die Übersichtlichkeit und ermöglicht eine gezielte Filterung von Logs.

# 2. Selektives Logging:
#    Durch die Methoden disable_category() und enable_category() können bestimmte
#    Log-Kategorien temporär deaktiviert oder wieder aktiviert werden. Dies ist
#    besonders nützlich für Debugging-Zwecke oder um die Log-Ausgabe zu reduzieren.

# 3. Anpassbare Logging-Levels pro Kategorie:
#    Mit set_category_level() kann das Logging-Level für jede Kategorie individuell
#    angepasst werden, was eine feinere Kontrolle über die Log-Ausgabe ermöglicht.

# 4. Rotierendes Datei-Logging:
#    Durch die Verwendung von RotatingFileHandler wird sichergestellt, dass die
#    Log-Dateien nicht unbegrenzt wachsen. Stattdessen werden neue Log-Dateien
#    erstellt, wenn die aktuelle Datei eine bestimmte Größe erreicht.

# 5. Einheitliche Ausnahmebehandlung:
#    Der handle_exceptions Decorator bietet eine konsistente Methode zur
#    Ausnahmebehandlung und Logging in der gesamten Anwendung.

# Diese Implementierung bietet eine flexible und leistungsfähige Logging-Lösung,
# die speziell auf die Bedürfnisse des Wortweber-Projekts zugeschnitten ist.
