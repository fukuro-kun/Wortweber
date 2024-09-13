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

# src/frontend/settings_manager.py

import json
import os
from src.config import (DEFAULT_LANGUAGE, DEFAULT_WHISPER_MODEL, DEFAULT_THEME,
                        DEFAULT_WINDOW_SIZE, DEFAULT_CHAR_DELAY, DEFAULT_FONT_SIZE)

class SettingsManager:
    """
    Verwaltet das Laden, Speichern und Abrufen von Benutzereinstellungen für die Wortweber-Anwendung.
    """

    def __init__(self):
        """Initialisiert den SettingsManager und lädt bestehende Einstellungen."""
        self.settings_file = "user_settings.json"
        self.settings = self.load_settings()

    def load_settings(self):
        """
        Lädt Benutzereinstellungen aus einer JSON-Datei.
        Falls die Datei nicht existiert oder beschädigt ist, werden Standardeinstellungen verwendet.

        :return: Ein Dictionary mit den geladenen Einstellungen
        """
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("Fehler beim Laden der Einstellungen. Verwende Standardeinstellungen.")
        return self.get_default_settings()

    def save_settings(self):
        """Speichert die aktuellen Einstellungen in einer JSON-Datei."""
        with open(self.settings_file, "w") as f:
            json.dump(self.settings, f, indent=4)

    def get_setting(self, key, default=None):
        """
        Ruft den Wert einer bestimmten Einstellung ab.

        :param key: Der Schlüssel der gewünschten Einstellung
        :param default: Ein optionaler Standardwert, falls die Einstellung nicht existiert
        :return: Der Wert der Einstellung oder der Standardwert
        """
        return self.settings.get(key, default or self.get_default_settings().get(key))

    def set_setting(self, key, value):
        """
        Setzt den Wert einer bestimmten Einstellung und speichert die Änderungen.

        :param key: Der Schlüssel der zu setzenden Einstellung
        :param value: Der neue Wert der Einstellung
        """
        self.settings[key] = value
        self.save_settings()

    def get_default_settings(self):
        """
        Liefert ein Dictionary mit den Standardeinstellungen der Anwendung.

        :return: Ein Dictionary mit Standardeinstellungen
        """
        return {
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
            "save_test_recording": False,  # Neue Einstellung für Testaufnahmen
        }

# Zusätzliche Erklärungen:

# 1. JSON für Einstellungsspeicherung:
#    JSON wird als Format für die Einstellungsdatei verwendet, da es leicht lesbar und schreibbar ist,
#    sowohl für Menschen als auch für Maschinen.

# 2. Fehlerbehandlung beim Laden:
#    Die load_settings-Methode fängt JSONDecodeError ab, um robust mit beschädigten Einstellungsdateien umzugehen.
#    In diesem Fall werden die Standardeinstellungen verwendet.

# 3. Standardwerte:
#    Die get_default_settings-Methode zentralisiert die Definition von Standardwerten.
#    Dies erleichtert die Wartung und stellt sicher, dass alle Teile der Anwendung konsistente Standardwerte verwenden.

# 4. Einstellungspersistenz:
#    Jeder Aufruf von set_setting speichert sofort die Änderungen. Dies stellt sicher,
#    dass keine Einstellungen verloren gehen, selbst wenn die Anwendung unerwartet beendet wird.

# 5. Flexibilität:
#    Die Verwendung eines Dictionaries für Einstellungen ermöglicht eine einfache Erweiterung um neue Einstellungen,
#    ohne die Struktur der Klasse ändern zu müssen.

# 6. Typsicherheit:
#    Einige Werte (wie char_delay) werden als Strings gespeichert, um Konsistenz mit GUI-Elementen zu gewährleisten.
#    Bei der Verwendung dieser Werte sollte eine entsprechende Typumwandlung erfolgen.

# 7. Neue Einstellung für Testaufnahmen:
#    Die Einstellung "save_test_recording" wurde hinzugefügt, um die Option zum Speichern von Testaufnahmen zu steuern.
#    Standardmäßig ist diese Option deaktiviert.
