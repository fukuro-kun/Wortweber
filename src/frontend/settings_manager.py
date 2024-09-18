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



# src/frontend/settings_manager.py

import json
import os
from src.config import (DEFAULT_LANGUAGE, DEFAULT_WHISPER_MODEL, DEFAULT_THEME,
                        DEFAULT_WINDOW_SIZE, DEFAULT_CHAR_DELAY, DEFAULT_FONT_SIZE,
                        DEFAULT_INCOGNITO_MODE)
from src.utils.error_handling import handle_exceptions, logger

class SettingsManager:
    """
    Verwaltet das Laden, Speichern und Abrufen von Benutzereinstellungen für die Wortweber-Anwendung.
    """

    @handle_exceptions
    def __init__(self):
        """Initialisiert den SettingsManager und lädt bestehende Einstellungen."""
        self.settings_file = "user_settings.json"
        self.settings = self.load_settings()
        logger.info("SettingsManager initialisiert")

    @handle_exceptions
    def load_settings(self):
        """
        Lädt Benutzereinstellungen aus einer JSON-Datei.
        Falls die Datei nicht existiert oder beschädigt ist, werden Standardeinstellungen verwendet.

        :return: Ein Dictionary mit den geladenen Einstellungen
        """
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, "r") as f:
                    settings = json.load(f)
                logger.info("Einstellungen erfolgreich geladen")
                return settings
            except json.JSONDecodeError:
                logger.error("Fehler beim Laden der Einstellungen. Verwende Standardeinstellungen.")
        return self.get_default_settings()

    @handle_exceptions
    def save_settings(self):
        """Speichert die aktuellen Einstellungen in einer JSON-Datei."""
        with open(self.settings_file, "w") as f:
            json.dump(self.settings, f, indent=4)
        logger.info("Einstellungen erfolgreich gespeichert")

    @handle_exceptions
    def get_setting(self, key, default=None):
        """
        Ruft den Wert einer bestimmten Einstellung ab.

        :param key: Der Schlüssel der gewünschten Einstellung
        :param default: Ein optionaler Standardwert, falls die Einstellung nicht existiert
        :return: Der Wert der Einstellung oder der Standardwert
        """
        value = self.settings.get(key, default or self.get_default_settings().get(key))
        logger.debug(f"Einstellung abgerufen: {key} = {value}")
        return value

    @handle_exceptions
    def set_setting(self, key, value):
        """
        Setzt den Wert einer bestimmten Einstellung und speichert die Änderungen.

        :param key: Der Schlüssel der zu setzenden Einstellung
        :param value: Der neue Wert der Einstellung
        """
        self.settings[key] = value
        self.save_settings()
        if key != "text_content":  # Vermeiden des Loggens von Transkriptionen
            logger.info(f"Einstellung geändert: {key} = {value}")

    @handle_exceptions
    def get_default_settings(self):
        """
        Liefert ein Dictionary mit den Standardeinstellungen der Anwendung.

        :return: Ein Dictionary mit Standardeinstellungen
        """
        default_settings = {
            "language": DEFAULT_LANGUAGE,
            "model": DEFAULT_WHISPER_MODEL,
            "theme": DEFAULT_THEME,
            "window_geometry": DEFAULT_WINDOW_SIZE,
            "input_mode": "textfenster",
            "delay_mode": "no_delay",
            "char_delay": str(DEFAULT_CHAR_DELAY),
            "auto_copy": True,
            "text_content": "",
            "font_size": DEFAULT_FONT_SIZE,
            "save_test_recording": False,
            "incognito_mode": DEFAULT_INCOGNITO_MODE,
        }
        logger.debug("Standardeinstellungen abgerufen")
        return default_settings

# Zusätzliche Erklärungen:

# 1. Neue Einstellung "incognito_mode":
#    Diese Einstellung wurde zum Dictionary der Standardeinstellungen hinzugefügt.
#    Sie steuert, ob Transkriptionsergebnisse protokolliert werden sollen.

# 2. Verwendung von DEFAULT_INCOGNITO_MODE:
#    Der Standardwert für den Incognito-Modus wird aus der Konfigurationsdatei importiert.
#    Dies gewährleistet Konsistenz und erleichtert zukünftige Änderungen.

# 3. Fehlerbehandlung:
#    Die Methoden sind mit dem @handle_exceptions Decorator versehen, was eine
#    einheitliche Fehlerbehandlung und -protokollierung in der gesamten Anwendung sicherstellt.

# 4. Logging:
#    Ausführliche Logging-Aufrufe wurden implementiert, um die Nachvollziehbarkeit
#    von Einstellungsänderungen und potenziellen Problemen zu verbessern.

# 5. Flexibilität:
#    Die Struktur des SettingsManager erlaubt es, leicht neue Einstellungen hinzuzufügen,
#    ohne bestehenden Code zu ändern. Dies erleichtert zukünftige Erweiterungen.

# 6. Persistenz:
#    Durch das Speichern der Einstellungen in einer JSON-Datei bleiben Benutzereinstellungen
#    über Anwendungsneustarts hinweg erhalten.
