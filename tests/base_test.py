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

"""
Dieses Modul definiert die Basisklasse für Transkriptionstests in der Wortweber-Anwendung.
Es stellt gemeinsam genutzte Funktionen und Konfigurationen für die Transkriptionstests bereit.
"""

import unittest
import os
import numpy as np
import wave
import librosa
from typing import List
from src.backend.wortweber_utils import check_gpu_resources
from tests.test_config import MIN_GPU_MEMORY, MODELS_TO_TEST, TEST_DATA_DIR, TEST_AUDIO_FILE

class BaseTranscriptionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """Wird einmal vor allen Testmethoden in dieser Klasse ausgeführt."""
        cls.gpu_available, cls.gpu_memory = check_gpu_resources()
        if cls.gpu_available and cls.gpu_memory < MIN_GPU_MEMORY:
            raise unittest.SkipTest(f"Nicht genug GPU-Speicher. Verfügbar: {cls.gpu_memory:.2f} GB, Benötigt: {MIN_GPU_MEMORY} GB")

    def setUp(self) -> None:
        """Wird vor jeder Testmethode ausgeführt."""
        pass

    def tearDown(self) -> None:
        """Wird nach jeder Testmethode ausgeführt."""
        pass

    def get_test_audio_path(self) -> str:
        """Gibt den Pfad zur Testaufnahme zurück."""
        return os.path.join(TEST_DATA_DIR, TEST_AUDIO_FILE)

    def load_and_prepare_audio(self, audio_path: str) -> np.ndarray:
        """
        Lädt und bereitet die Audiodatei für die Transkription vor.

        Args:
            audio_path (str): Pfad zur Audiodatei

        Returns:
            np.ndarray: Vorbereitete Audiodaten als NumPy-Array
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audiodatei nicht gefunden: {audio_path}")

        with wave.open(audio_path, "rb") as wf:
            sample_rate = wf.getframerate()
            audio_data = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16)

        # Normalisiere die Audiodaten auf den Bereich [-1, 1]
        audio_normalized = audio_data.astype(np.float32) / 32768.0

        # Resampling auf 16000 Hz (Whisper's erwartete Sampling-Rate)
        if sample_rate != 16000:
            audio_resampled = librosa.resample(audio_normalized, orig_sr=sample_rate, target_sr=16000)
        else:
            audio_resampled = audio_normalized

        return audio_resampled

    def get_expected_words(self, language: str) -> List[str]:
        """
        Gibt eine Liste von Wörtern zurück, die in der Transkription erwartet werden.

        Args:
            language (str): Die Sprache der Transkription

        Returns:
            List[str]: Liste der erwarteten Wörter
        """
        if language == 'de':
            return ["das", "ist", "ein", "test"]
        elif language == 'en':
            return ["this", "is", "a", "test"]
        return []

# Zusätzliche Erklärungen:
# 1. Die Klasse erbt von unittest.TestCase und bietet Grundfunktionalitäten für Transkriptionstests.
# 2. setUpClass überprüft die GPU-Verfügbarkeit und den Speicher vor der Ausführung der Tests.
# 3. load_and_prepare_audio bereitet Audiodaten für die Transkription vor, einschließlich Normalisierung und Resampling.
# 4. get_expected_words liefert erwartete Wörter für verschiedene Sprachen zur Überprüfung der Transkriptionsgenauigkeit.
