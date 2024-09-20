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
DEFAULT_AUDIO_DEVICE_INDEX = 0 # Eintrag für den Standard-Audiogeräteindex

# Aufnahme-Einstellungen
MIN_RECORD_SECONDS = 0.5  # Mindestaufnahmedauer in Sekunden

# Eingabe-Einstellungen
DEFAULT_PUSH_TO_TALK_KEY = 'F12'  # Taste für Push-to-Talk-Funktion

# Verzögerungseinstellungen
DEFAULT_CHAR_DELAY = 10  # Standardverzögerung zwischen Zeichen in Millisekunden

# Whisper-Modelle
WHISPER_MODELS = ["tiny", "base", "small", "medium", "large"]  # Verfügbare Whisper-Modelle

# Unterstützte Sprachen
SUPPORTED_LANGUAGES = {
    "de": "Deutsch",
    "en": "English"
}

# Wichtige Hinweise
RESAMPLING_NOTE = """
WICHTIG: Resampling ist notwendig, da die Audiogeräte 16000 Hz nicht unterstützen.
Ändern Sie AUDIO_RATE nicht und entfernen Sie das Resampling nicht ohne Rücksprache mit dem Projektteam.
"""

# Diese Konfigurationsdatei zentralisiert alle wichtigen Einstellungen für die Wortweber-Anwendung.
# Sie erleichtert die Anpassung und Wartung der Anwendung, indem sie einen einzigen Ort für
# häufig zu ändernde Parameter bereitstellt.

# Zusätzliche Erklärungen:

# 1. DEFAULT_INCOGNITO_MODE:
#    Diese neue Einstellung steuert, ob Transkriptionsergebnisse standardmäßig protokolliert werden.
#    Der Wert True bedeutet, dass der Incognito-Modus standardmäßig aktiviert ist,
#    was die Privatsphäre der Benutzer schützt, indem keine Transkriptionen geloggt werden.

# 2. Zentrale Konfiguration:
#    Durch die Zentralisierung aller Standardeinstellungen in dieser Datei wird die
#    Wartung und Anpassung der Anwendung erheblich erleichtert. Entwickler können
#    schnell globale Änderungen vornehmen, ohne mehrere Dateien durchsuchen zu müssen.

# 3. Dokumentation:
#    Jeder Konfigurationsparameter ist mit einem Kommentar versehen, der seine Funktion erklärt.
#    Dies ist besonders wichtig für neue Entwickler oder bei der Fehlersuche.

# 4. Gruppierung:
#    Die Einstellungen sind in logische Gruppen unterteilt (z.B. GUI, Audio, Eingabe),
#    was die Übersichtlichkeit und Wartbarkeit verbessert.

# 5. Erweiterbarkeit:
#    Die Struktur ermöglicht es, einfach neue Konfigurationsparameter hinzuzufügen,
#    ohne die Gesamtstruktur der Datei zu beeinträchtigen.
