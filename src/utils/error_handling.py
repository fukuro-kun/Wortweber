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
from typing import Callable, Any
from functools import wraps

# Konfigurieren des Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='wortweber.log'
)

logger = logging.getLogger('Wortweber')

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
