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

# src/utils/error_handling.py

# Standardbibliotheken
import logging
import traceback
import os
import json
from typing import Callable, Any, Optional
from functools import wraps
from logging.handlers import RotatingFileHandler

# Projektspezifische Module
from src.config import DEBUG_LOGGING

# Erstelle das Logs-Verzeichnis, falls es nicht existiert
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# Konfigurieren des Logging
log_file = os.path.join(log_dir, "wortweber.log")
max_log_size = 5 * 1024 * 1024  # 5 MB
backup_count = 3

# Konfiguriere den Root-Logger
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

# Entferne alle bestehenden Handler
for handler in root_logger.handlers[:]:
    root_logger.removeHandler(handler)

# Erstelle einen FileHandler mit Rotation
file_handler = RotatingFileHandler(
    filename=log_file,
    maxBytes=max_log_size,
    backupCount=backup_count
)
file_handler.setLevel(logging.DEBUG if DEBUG_LOGGING else logging.INFO)
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

# Erstelle einen StreamHandler für die Konsole
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG if DEBUG_LOGGING else logging.INFO)
console_formatter = logging.Formatter('%(levelname)s: %(message)s')
console_handler.setFormatter(console_formatter)

# Füge die Handler zum Root-Logger hinzu
root_logger.addHandler(file_handler)
root_logger.addHandler(console_handler)

# Globaler Logger
logger = logging.getLogger(__name__)

def log_and_raise(exception: Exception, message: str, log_level: int = logging.ERROR) -> None:
    """
    Loggt eine Ausnahme und wirft sie erneut.

    :param exception: Die aufgetretene Ausnahme
    :param message: Eine beschreibende Nachricht
    :param log_level: Das Logging-Level (Standard: ERROR)
    """
    logger.log(log_level, f"{message}: {str(exception)}")
    logger.debug(f"Traceback: {traceback.format_exc()}")
    raise exception

def log_settings_error(message: str, exception: Optional[Exception] = None) -> None:
    """
    Loggt einen Fehler, der mit den Einstellungen zusammenhängt.

    :param message: Eine beschreibende Nachricht
    :param exception: Die aufgetretene Ausnahme (optional)
    """
    if exception:
        logger.error(f"Einstellungsfehler: {message} - {str(exception)}")
        if DEBUG_LOGGING:
            logger.debug(f"Traceback: {traceback.format_exc()}")
    else:
        logger.error(f"Einstellungsfehler: {message}")

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
        except FileNotFoundError as e:
            log_settings_error(f"Einstellungsdatei nicht gefunden in {func.__name__}", e)
        except json.JSONDecodeError as e:
            log_settings_error(f"Fehler beim Parsen der Einstellungsdatei in {func.__name__}", e)
        except Exception as e:
            log_and_raise(e, f"Unerwarteter Fehler in {func.__name__}")
    return wrapper

# Zusätzliche Erklärungen:
#
# 1. DEBUG_LOGGING:
#    Die Verwendung der DEBUG_LOGGING-Konstante aus der config.py ermöglicht
#    eine zentrale Steuerung des Logging-Verhaltens. Bei aktiviertem Debug-Modus
#    werden detailliertere Logs sowohl in der Datei als auch in der Konsole ausgegeben.
#
# 2. log_settings_error:
#    Diese neue Funktion wurde speziell für Fehler im Zusammenhang mit dem SettingsManager
#    eingeführt. Sie ermöglicht eine differenzierte Behandlung von Einstellungsfehlern
#    und gibt bei aktiviertem Debug-Modus zusätzliche Traceback-Informationen aus.
#
# 3. Erweiterter handle_exceptions Decorator:
#    Der Decorator wurde um spezifische Ausnahmebehandlungen für FileNotFoundError
#    und json.JSONDecodeError erweitert, um häufige Probleme bei der Arbeit mit
#    Einstellungsdateien gezielt abzufangen und zu loggen.
