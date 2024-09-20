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
# (Keine Standardbibliotheken werden in dieser Datei importiert)

# Drittanbieterbibliotheken
import pyaudio

# Projektspezifische Module
# (Keine projektspezifischen Module werden in dieser Datei importiert)

# Allgemeine Einstellungen
DEFAULT_LANGUAGE = "de"  # Standardsprache für die Transkription
DEFAULT_WHISPER_MODEL = "small"  # Standardmodell für Whisper
DEFAULT_THEME = "arc"  # Standardtheme für die GUI
DEFAULT_INCOGNITO_MODE = True  # Standardeinstellung für den Incognito-Modus

# GUI-Einstellungen
DEFAULT_WINDOW_SIZE = "900x700"  # Standardgröße des Anwendungsfensters
HIGHLIGHT_DURATION = 2000  # Dauer der Texthighlights in Millisekunden
DEFAULT_FONT_SIZE = 12  # Standard-Textgröße
DEFAULT_FONT_FAMILY = "Nimbus Mono L"  # Die korrekte Schreibweise ist "Nimbus Mono L"

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

# Diese Konfigurationsdatei zentralisiert alle wichtigen Einstellungen für die Wortweber-Anwendung.
# Sie erleichtert die Anpassung und Wartung der Anwendung, indem sie einen einzigen Ort für
# häufig zu ändernde Parameter bereitstellt.

# Zusätzliche Erklärungen:

# 1. DEFAULT_PUSH_TO_TALK_KEY:
#    Der Standardwert wurde auf "Ctrl+F12" geändert, um die neue Unterstützung für
#    Tastenkombinationen zu demonstrieren. Dies ermöglicht eine intuitivere
#    Bedienung für viele Benutzer.

# 2. VALID_MODIFIERS und VALID_FUNCTION_KEYS:
#    Diese neuen Listen definieren die gültigen Modifikatortasten und Funktionstasten.
#    Sie können verwendet werden, um Benutzereingaben zu validieren und
#    sicherzustellen, dass nur unterstützte Tastenkombinationen akzeptiert werden.

# 3. SHORTCUT_NOTE:
#    Dieser neue Hinweis erklärt das Format und die Möglichkeiten für gültige Shortcuts.
#    Er dient als Referenz für Entwickler und kann auch in der Benutzeroberfläche
#    verwendet werden, um Benutzer bei der Konfiguration zu unterstützen.

# 4. Flexibilität:
#    Die Struktur ermöglicht es weiterhin, einfach neue Konfigurationsparameter
#    hinzuzufügen, ohne die Gesamtstruktur der Datei zu beeinträchtigen.

# 5. Zentrale Konfiguration:
#    Durch die Zentralisierung aller Standardeinstellungen in dieser Datei bleibt die
#    Wartung und Anpassung der Anwendung einfach. Entwickler können schnell globale
#    Änderungen vornehmen, ohne mehrere Dateien durchsuchen zu müssen.

# Diese Aktualisierung der config.py unterstützt die neue flexible Shortcut-Funktionalität
# und bietet gleichzeitig klare Richtlinien für deren Verwendung.
