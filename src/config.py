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
# config.py

import pyaudio

# Audio settings
AUDIO_CHUNK = 4096
AUDIO_FORMAT = 'paInt16'
AUDIO_CHANNELS = 1
AUDIO_RATE = 44100  # Native sample rate des Audio Gerätes
TARGET_RATE = 16000  # Ziel sample rate für Whisper
DEVICE_INDEX = 6

# Recording settings
MIN_RECORD_SECONDS = 0.5

# Whisper model settings
WHISPER_MODEL = "small"  # Optionen: "tiny", "base", "small", "medium", "large"
WHISPER_MODELS = ["tiny", "base", "small", "medium", "large"]

# Language settings
DEFAULT_LANGUAGE = "de"
SUPPORTED_LANGUAGES = {
    "de": "Deutsch",
    "en": "English"
}

# GUI settings
HIGHLIGHT_DURATION = 2000  # Dauer der Hervorhebung in Millisekunden

# PyAudio format
FORMAT = getattr(pyaudio, AUDIO_FORMAT)
CHANNELS = AUDIO_CHANNELS
RATE = AUDIO_RATE
CHUNK = AUDIO_CHUNK

# Important notes
RESAMPLING_NOTE = """
WICHTIG: Resampling ist notwendig, da die Audiogeräte 16000 Hz nicht unterstützen.
Ändern Sie AUDIO_RATE nicht und entfernen Sie das Resampling nicht ohne Rücksprache mit dem Projektteam.
"""
