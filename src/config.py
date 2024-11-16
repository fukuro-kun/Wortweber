# src/config.py

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

# Standardbibliotheken
import os

# Drittanbieterbibliotheken
import pyaudio

# Projektspezifische Module
# (Keine projektspezifischen Module werden in dieser Datei importiert)

# Pfad zum Projektroot
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Neue Konstanten
SETTINGS_FILE_NAME = "user_settings.json"
DEBUG_LOGGING = True  # Kann auf False gesetzt werden, um detailliertes Logging zu deaktivieren
CONFIG_VERSION = "1.0.0"
PLUGIN_ACTIVATION_TIMEOUT = 5.0  # Timeout in Sekunden für die Plugin-Aktivierung

# Allgemeine Einstellungen
DEFAULT_LANGUAGE = "de"  # Standardsprache für die Transkription
DEFAULT_WHISPER_MODEL = "small"  # Standardmodell für Whisper
DEFAULT_THEME = "black"  # Standardtheme für die GUI
DEFAULT_INCOGNITO_MODE = True  # Standardeinstellung für den Incognito-Modus

# GUI-Einstellungen
DEFAULT_WINDOW_SIZE = "890x404+760+123"  # Standardgröße und -position des Anwendungsfensters
DEFAULT_PLUGIN_WINDOW_GEOMETRY = "892x291+758+594"  # Standardgröße und -position des Plugin-Fensters
DEFAULT_OPTIONS_WINDOW_GEOMETRY = "606x370+1652+124"  # Standardgröße und -position des Optionsfensters
HIGHLIGHT_DURATION = 2000  # Dauer der Texthighlights in Millisekunden
DEFAULT_FONT_SIZE = 12  # Standard-Textgröße
DEFAULT_FONT_FAMILY = "Nimbus Mono L"  # Standard-Schriftart

# Einstellungen, die verzögert gespeichert werden sollen
DELAYED_SAVE_SETTINGS = ['window_geometry', 'plugin_window_geometry', 'options_window_geometry']

# Audio-Einstellungen
AUDIO_FORMAT = pyaudio.paInt16  # 16-bit int Sampling
AUDIO_CHANNELS = 1  # Mono-Aufnahme
AUDIO_RATE = 44100  # Sampling-Rate in Hz
TARGET_RATE = 16000  # Ziel-Sampling-Rate für Whisper
AUDIO_CHUNK = 4096  # Größe der Audio-Chunks für die Aufnahme
DEVICE_INDEX = 6  # Index des zu verwendenden Audiogeräts
DEFAULT_AUDIO_DEVICE_INDEX = 6  # Standard-Audiogeräteindex

# Aufnahme-Einstellungen
MIN_RECORD_SECONDS = 0.5  # Mindestaufnahmedauer in Sekunden

# Eingabe-Einstellungen
DEFAULT_PUSH_TO_TALK_KEY = "F12"  # Standard-Tastenkombination für Push-to-Talk-Funktion

# Verzögerungseinstellungen
DEFAULT_DELAY_MODE = "char_delay"  # Standardverzögerungsmodus
DEFAULT_CHAR_DELAY = 18  # Standardverzögerung zwischen Zeichen in Millisekunden

# Ausgabe-Einstellungen
DEFAULT_AUTO_COPY = True  # Standardeinstellung für automatisches Kopieren
DEFAULT_OUTPUT_MODE = "systemcursor"  # Standardausgabemodus

# Farbeinstellungen
DEFAULT_TEXT_FG = "#FFFFFF"  # Standard-Textfarbe
DEFAULT_TEXT_BG = "#000000"  # Standard-Hintergrundfarbe
DEFAULT_SELECT_FG = "black"  # Standard-Textfarbe für Auswahl
DEFAULT_SELECT_BG = "#FFFFFF"  # Standard-Hintergrundfarbe für Auswahl
DEFAULT_HIGHLIGHT_FG = "#FFFFFF"  # Standard-Textfarbe für Hervorhebung
DEFAULT_HIGHLIGHT_BG = "#FF0000"  # Standard-Hintergrundfarbe für Hervorhebung

# Whisper-Modelle
WHISPER_MODELS = [
    "tiny", "base", "small", "medium", "large",  # Standard-Modelle
    "large-v3"  # Neuestes Modell
]  # Verfügbare Whisper-Modelle

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

# 1. DEFAULT_PLUGIN_DIR:
#    Definiert das Standardverzeichnis, in dem Wortweber nach Plugins sucht.

# 2. DEFAULT_ENABLED_PLUGINS:
#    Eine Liste von Plugins, die standardmäßig aktiviert sind. Benutzer können diese Liste anpassen.

# 3. DEFAULT_PLUGIN_SETTINGS:
#    Globale Einstellungen, die für alle Plugins gelten. Sie definieren Grenzwerte und
#    Verhaltensweisen, die für die Sicherheit und Leistung wichtig sind.

# 4. PLUGIN_SPECIFIC_SETTINGS:
#    Hier können Standardeinstellungen für spezifische Plugins definiert werden.
#    Dies ermöglicht eine feinere Kontrolle über das Verhalten einzelner Plugins.

# 5. PLUGIN_NOTE:
#    Ein wichtiger Hinweis für Entwickler und Benutzer von Plugins, der auf
#    Sicherheits- und Kompatibilitätsaspekte aufmerksam macht.

# Diese Ergänzungen zur config.py unterstützen die Integration des Plugin-Systems
# und bieten gleichzeitig Flexibilität für zukünftige Erweiterungen und Anpassungen.
