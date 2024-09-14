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
DEFAULT_WINDOW_SIZE = "800x600"  # Standardgröße des Anwendungsfensters
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

# Aufnahme-Einstellungen
MIN_RECORD_SECONDS = 0.5  # Mindestaufnahmedauer in Sekunden

# Eingabe-Einstellungen
PUSH_TO_TALK_KEY = 'F12'  # Taste für Push-to-Talk-Funktion

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
