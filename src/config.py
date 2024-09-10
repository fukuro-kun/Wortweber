# config.py

# Audio settings
AUDIO_CHUNK = 4096
AUDIO_FORMAT = 'paInt16'
AUDIO_CHANNELS = 1
AUDIO_RATE = 44100  # Native sample rate of audio devices
TARGET_RATE = 16000  # Target sample rate for Whisper
DEVICE_INDEX = 6

# Recording settings
MIN_RECORD_SECONDS = 0.5

# Whisper model settings
WHISPER_MODEL = "small"  # Options: "tiny", "base", "small", "medium", "large"

# Language settings
DEFAULT_LANGUAGE = "de"
SUPPORTED_LANGUAGES = {
    "de": "Deutsch",
    "en": "Englisch"
}

# Important notes
RESAMPLING_NOTE = """
WICHTIG: Resampling ist notwendig, da die Audiogeräte 16000 Hz nicht unterstützen.
Ändern Sie AUDIO_RATE nicht und entfernen Sie das Resampling nicht ohne Rücksprache mit dem Projektteam.
"""
