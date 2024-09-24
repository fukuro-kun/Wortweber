# src/utils/error_handling.py

import logging
import traceback
from typing import Callable, Any
from functools import wraps
from logging.handlers import RotatingFileHandler
import os

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
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

# Erstelle einen StreamHandler für die Konsole
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
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
