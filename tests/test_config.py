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

# tests/test_config.py

import os

# Minimaler erforderlicher GPU-Speicher in GB
MIN_GPU_MEMORY = 4.0

# Liste der zu testenden Whisper-Modelle
MODELS_TO_TEST = ["tiny", "base", "small", "medium"]

# Pfad zum Testdatenverzeichnis
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "test_data")

# Name der Testaudiodatei
TEST_AUDIO_FILE = "speech_sample.wav"

# Maximale Anzahl paralleler Tests
MAX_PARALLEL_TESTS = 2

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
TEST_LANGUAGES = ["de", "en"]

# Zusätzliche Erklärungen:

# 1. Der Pfad zum Testdatenverzeichnis wird dynamisch erstellt, um
#    Portabilität zwischen verschiedenen Systemen zu gewährleisten.

# 2 Die Werte können leicht angepasst werden, um verschiedene Testszenarien
#    zu ermöglichen, ohne den eigentlichen Testcode ändern zu müssen.

# 3. Die Konfiguration für die Audioaufnahme ist als Dictionary strukturiert,
#    was eine einfache Erweiterung oder Änderung ermöglicht.

# 4. Die Verwendung von Konstanten für wiederverwendete Werte verbessert
#    die Wartbarkeit und reduziert potenzielle Fehler durch Hardcoding.
