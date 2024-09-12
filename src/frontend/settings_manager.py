import json
import os
from src.config import DEFAULT_LANGUAGE, WHISPER_MODEL

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
            "model": WHISPER_MODEL,
            "theme": "arc",
            "window_geometry": "800x600",  # Geändert von "window_size"
            "input_mode": "textfenster",
            "delay_mode": "no_delay",
            "char_delay": "10",
            "auto_copy": True,
            "text_content": "",
        }
