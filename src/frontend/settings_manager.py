# src/frontend/settings_manager.py
import json
import os
from src.config import (DEFAULT_LANGUAGE, DEFAULT_WHISPER_MODEL, DEFAULT_THEME,
                        DEFAULT_WINDOW_SIZE, DEFAULT_CHAR_DELAY)

class SettingsManager:
    def __init__(self):
        self.settings_file = "user_settings.json"
        self.settings = self.load_settings()

    def load_settings(self):
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("Fehler beim Laden der Einstellungen. Verwende Standardeinstellungen.")
        return self.get_default_settings()

    def save_settings(self):
        with open(self.settings_file, "w") as f:
            json.dump(self.settings, f, indent=4)

    def get_setting(self, key):
        return self.settings.get(key, self.get_default_settings().get(key))

    def set_setting(self, key, value):
        self.settings[key] = value
        self.save_settings()

    def get_default_settings(self):
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
        }
