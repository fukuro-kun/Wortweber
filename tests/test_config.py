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



# tests/test_config.py

import os

# Minimaler erforderlicher GPU-Speicher in GB
MIN_GPU_MEMORY = 4.0

# Liste der zu testenden Whisper-Modelle
MODELS_TO_TEST = ["tiny", "base", "small", "medium"]

# Pfad zum Testdatenverzeichnis
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "test_data")

# Name der Testaudiodatei
TEST_AUDIO_FILE = "speech_sample.wav" # Enthält den Satz "Das ist ein Test" (auf Deutsch)

# Maximale Anzahl paralleler Tests
MAX_PARALLEL_TESTS = 4

# Timeout für einzelne Transkriptionen in Sekunden
TRANSCRIPTION_TIMEOUT = 300  # 5 Minuten

# Schwellenwert für akzeptable Wortfehlerrate (WER)
ACCEPTABLE_WER = 0.2  # 20% Wortfehlerrate

# Konfiguration für Audioaufnahme während der Tests
TEST_AUDIO_CONFIG = {
    "format": 16,  # 16-bit int sampling
    "channels": 1,  # mono
    "rate": 16000,  # Sampling rate
    "chunk": 1024,  # Größe der Audio-Chunks für die Aufnahme
}

# Sprachen für Transkriptionstests
TEST_LANGUAGES = ["de"]  # Nur Deutsch, da das Testfile auf Deutsch ist

# Zusätzliche Erklärungen:

# 1. Der Pfad zum Testdatenverzeichnis wird dynamisch erstellt, um
#    Portabilität zwischen verschiedenen Systemen zu gewährleisten.

# 2 Die Werte können leicht angepasst werden, um verschiedene Testszenarien
#    zu ermöglichen, ohne den eigentlichen Testcode ändern zu müssen.

# 3. Die Konfiguration für die Audioaufnahme ist als Dictionary strukturiert,
#    was eine einfache Erweiterung oder Änderung ermöglicht.

# 4. Die Verwendung von Konstanten für wiederverwendete Werte verbessert
#    die Wartbarkeit und reduziert potenzielle Fehler durch Hardcoding.
