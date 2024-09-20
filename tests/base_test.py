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

"""
Dieses Modul definiert die Basisklasse für Transkriptionstests in der Wortweber-Anwendung.
Es stellt gemeinsam genutzte Funktionen und Konfigurationen für die Transkriptionstests bereit.
"""

import unittest
import os
import numpy as np
import wave
from scipy import signal
from numpy.typing import NDArray
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

    def load_and_prepare_audio(self, audio_path: str) -> NDArray[np.float32]:
            """
            Lädt und bereitet die Audiodatei für die Transkription vor.

            Args:
                audio_path (str): Pfad zur Audiodatei

            Returns:
                NDArray[np.float32]: Vorbereitete Audiodaten als NumPy-Array
            """
            if not os.path.exists(audio_path):
                raise FileNotFoundError(f"Audiodatei nicht gefunden: {audio_path}")

            with wave.open(audio_path, "rb") as wf:
                sample_rate = wf.getframerate()
                audio_data = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16)

            # Normalisiere die Audiodaten auf den Bereich [-1, 1]
            audio_normalized: NDArray[np.float32] = audio_data.astype(np.float32) / 32768.0

            # Resampling auf 16000 Hz (Whisper's erwartete Sampling-Rate)
            if sample_rate != 16000:
                resampled = signal.resample(audio_normalized, int(len(audio_normalized) * 16000 / sample_rate))
                audio_resampled: NDArray[np.float32] = np.asarray(resampled, dtype=np.float32)
            else:
                audio_resampled: NDArray[np.float32] = audio_normalized

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
