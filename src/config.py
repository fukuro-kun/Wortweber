# src/config.py
import pyaudio

# Allgemeine Einstellungen
DEFAULT_LANGUAGE = "de"
DEFAULT_WHISPER_MODEL = "small"
DEFAULT_THEME = "arc"

# GUI-Einstellungen
DEFAULT_WINDOW_SIZE = "800x600"
HIGHLIGHT_DURATION = 2000  # in Millisekunden

# Audio-Einstellungen
AUDIO_FORMAT = pyaudio.paInt16
AUDIO_CHANNELS = 1
AUDIO_RATE = 44100
TARGET_RATE = 16000
AUDIO_CHUNK = 4096
DEVICE_INDEX = 6

# Aufnahme-Einstellungen
MIN_RECORD_SECONDS = 0.5

# Eingabe-Einstellungen
PUSH_TO_TALK_KEY = 'F12'

# Verzögerungseinstellungen
DEFAULT_CHAR_DELAY = 10

# Whisper-Modelle
WHISPER_MODELS = ["tiny", "base", "small", "medium", "large"]

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
