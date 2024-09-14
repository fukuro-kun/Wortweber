# src/utils/error_handling.py

# Copyright 2024 fukuro-kun
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
