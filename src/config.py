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

# src/config.py

# Standardbibliotheken
import os

# Drittanbieterbibliotheken
import pyaudio

# Projektspezifische Module
# (Keine projektspezifischen Module werden in dieser Datei importiert)

# Pfad zum Projektroot
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Allgemeine Einstellungen
DEFAULT_LANGUAGE = "de"  # Standardsprache für die Transkription
DEFAULT_WHISPER_MODEL = "small"  # Standardmodell für Whisper
DEFAULT_THEME = "arc"  # Standardtheme für die GUI
DEFAULT_INCOGNITO_MODE = True  # Standardeinstellung für den Incognito-Modus

# GUI-Einstellungen
DEFAULT_WINDOW_SIZE = "900x700"  # Standardgröße des Anwendungsfensters
HIGHLIGHT_DURATION = 2000  # Dauer der Texthighlights in Millisekunden
DEFAULT_FONT_SIZE = 12  # Standard-Textgröße
DEFAULT_FONT_FAMILY = "Nimbus Mono L"  # Standardschriftart

# Audio-Einstellungen
AUDIO_FORMAT = pyaudio.paInt16  # 16-bit int Sampling
AUDIO_CHANNELS = 1  # Mono-Aufnahme
AUDIO_RATE = 44100  # Sampling-Rate in Hz
TARGET_RATE = 16000  # Ziel-Sampling-Rate für Whisper
AUDIO_CHUNK = 4096  # Größe der Audio-Chunks für die Aufnahme
DEVICE_INDEX = 6  # Index des zu verwendenden Audiogeräts
DEFAULT_AUDIO_DEVICE_INDEX = 0  # Eintrag für den Standard-Audiogeräteindex

# Aufnahme-Einstellungen
MIN_RECORD_SECONDS = 0.5  # Mindestaufnahmedauer in Sekunden

# Eingabe-Einstellungen
DEFAULT_PUSH_TO_TALK_KEY = "F12"  # Standard-Tastenkombination für Push-to-Talk-Funktion

# Verzögerungseinstellungen
DEFAULT_CHAR_DELAY = 10  # Standardverzögerung zwischen Zeichen in Millisekunden

# Whisper-Modelle
WHISPER_MODELS = ["tiny", "base", "small", "medium", "large"]  # Verfügbare Whisper-Modelle

# Unterstützte Sprachen
SUPPORTED_LANGUAGES = {
    "de": "Deutsch",
    "en": "English"
}

# Gültige Modifikatortasten
VALID_MODIFIERS = ["Ctrl", "Shift", "Alt"]

# Gültige Funktionstasten
VALID_FUNCTION_KEYS = [f"F{i}" for i in range(1, 13)]  # F1 bis F12

# Plugin-Einstellungen
DEFAULT_PLUGIN_DIR = os.path.join(PROJECT_ROOT, "plugins")  # Standardverzeichnis für Plugins
DEFAULT_ENABLED_PLUGINS = []  # Standardmäßig aktivierte Plugins

# Standardeinstellungen für Plugins
DEFAULT_PLUGIN_SETTINGS = {
    "global": {
        "max_text_length": 1000,  # Maximale Textlänge, die ein Plugin verarbeiten kann
        "processing_timeout": 5.0  # Timeout für die Textverarbeitung in Sekunden
    }
}

# Plugin-spezifische Standardeinstellungen
# Diese können von den Plugins überschrieben werden
PLUGIN_SPECIFIC_SETTINGS = {
    "example_plugin": {
        "option1": True,
        "option2": "default_value"
    }
    # Weitere Plugin-spezifische Einstellungen können hier hinzugefügt werden
}

# Einstellungen für den SettingsManager
SETTINGS_FILE = "user_settings.json"  # Name der Einstellungsdatei
SETTINGS_SAVE_DELAY = 5.0  # Verzögerung in Sekunden für das automatische Speichern von Einstellungen
SETTINGS_VERSION = 1  # Aktuelle Version der Einstellungsstruktur

# Wichtige Hinweise
RESAMPLING_NOTE = """
WICHTIG: Resampling ist notwendig, da die Audiogeräte 16000 Hz nicht unterstützen.
Ändern Sie AUDIO_RATE nicht und entfernen Sie das Resampling nicht ohne Rücksprache mit dem Projektteam.
"""

SHORTCUT_NOTE = """
WICHTIG: Der Push-to-Talk-Shortcut kann aus einer Kombination von Modifikatortasten (Ctrl, Shift, Alt)
und einer normalen Taste oder Funktionstaste bestehen. Beispiele für gültige Shortcuts sind:
- "F12"
- "Ctrl+F12"
- "Ctrl+Shift+P"
Stellen Sie sicher, dass der gewählte Shortcut nicht mit anderen Systemfunktionen kollidiert.
"""

PLUGIN_NOTE = """
WICHTIG: Plugins erweitern die Funktionalität von Wortweber. Beachten Sie beim Entwickeln oder
Installieren von Plugins die Sicherheitsrichtlinien und stellen Sie sicher, dass sie kompatibel
mit der aktuellen Version von Wortweber sind.
"""

# Diese Konfigurationsdatei zentralisiert alle wichtigen Einstellungen für die Wortweber-Anwendung.
# Sie erleichtert die Anpassung und Wartung der Anwendung, indem sie einen einzigen Ort für
# häufig zu ändernde Parameter bereitstellt.

# Zusätzliche Erklärungen:

# 1. PROJECT_ROOT:
#    Definiert den Wurzelpfad des Projekts, was für relative Pfadangaben nützlich ist.

# 2. Audio-Einstellungen:
#    AUDIO_RATE und TARGET_RATE sind unterschiedlich, da ein Resampling erforderlich ist.
#    Dies wird im RESAMPLING_NOTE erklärt.

# 3. Plugin-System:
#    Die Plugin-Einstellungen ermöglichen eine flexible Konfiguration und Erweiterung der Anwendung.

# 4. SettingsManager-Konfiguration:
#    SETTINGS_FILE, SETTINGS_SAVE_DELAY und SETTINGS_VERSION unterstützen die zentrale Verwaltung von Benutzereinstellungen.

# 5. Sicherheitshinweise:
#    RESAMPLING_NOTE, SHORTCUT_NOTE und PLUGIN_NOTE bieten wichtige Informationen für Entwickler und Benutzer.

# Diese Konfigurationsdatei bildet das Rückgrat für die konsistente Einstellungsverwaltung in Wortweber
# und unterstützt die Wartbarkeit und Erweiterbarkeit des Projekts.
