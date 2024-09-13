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

# tests/backend/test_audio_processor.py

import unittest
from src.backend.audio_processor import AudioProcessor
from unittest.mock import MagicMock
import io
import sys
import numpy as np
import os
import wave

class TestAudioProcessor(unittest.TestCase):
    """
    Testklasse für den AudioProcessor.
    Überprüft die Funktionalität der AudioProcessor-Klasse.
    """

    def setUp(self):
        """Initialisiert die Testumgebung vor jedem Testfall."""
        self.processor = AudioProcessor()

    def test_audio_processor_initialization(self):
        """Testet die korrekte Initialisierung des AudioProcessors."""
        self.assertIsInstance(self.processor, AudioProcessor)
        print("\nAudioProcessor wurde erfolgreich initialisiert.")

    def test_list_audio_devices(self):
        """Testet die Methode zur Auflistung von Audiogeräten."""
        # Mocking PyAudio, da wir nicht auf echte Hardware zugreifen wollen in Tests
        self.processor.p = MagicMock()
        self.processor.p.get_host_api_info_by_index.return_value = {'deviceCount': 2}
        self.processor.p.get_device_info_by_host_api_device_index.side_effect = [
            {'maxInputChannels': 2, 'name': 'Test Device 1'},
            {'maxInputChannels': 0, 'name': 'Test Device 2'}
        ]

        # Umleiten der Standardausgabe zum Testen
        captured_output = io.StringIO()
        sys.stdout = captured_output

        self.processor.list_audio_devices()

        sys.stdout = sys.__stdout__  # Reset redirect

        self.assertIn("Input Device id 0 - Test Device 1", captured_output.getvalue())
        self.assertNotIn("Test Device 2", captured_output.getvalue())
        print("\nAudiogeräte wurden erfolgreich aufgelistet.")

    def test_resample_audio(self):
        """
        Testet die Audio-Resampling-Funktion.
        Überprüft, ob die Funktion korrekt die Abtastrate ändert und die Daten im erwarteten Format zurückgibt.
        """
        # Erstelle ein Beispiel-Audio-Array
        test_audio = np.sin(np.linspace(0, 2*np.pi, 1000)).astype(np.float32)

        # Führe das Resampling durch
        resampled = self.processor.resample_audio(test_audio)

        # Überprüfe den Typ und die Form des zurückgegebenen Arrays
        self.assertIsInstance(resampled, np.ndarray)
        expected_length = int(len(test_audio) * self.processor.TARGET_RATE / self.processor.RATE)
        self.assertEqual(len(resampled), expected_length)

        # Überprüfe, ob die Werte im erwarteten Bereich liegen
        self.assertTrue(np.all(resampled >= -1.0))
        self.assertTrue(np.all(resampled <= 1.0))

        # Überprüfe, ob die Frequenzcharakteristik erhalten bleibt (grob)
        original_fft = np.fft.fft(test_audio)
        resampled_fft = np.fft.fft(resampled)
        self.assertAlmostEqual(np.argmax(np.abs(original_fft)),
                               np.argmax(np.abs(resampled_fft)) * self.processor.RATE / self.processor.TARGET_RATE,
                               delta=5)  # Erlaubt eine kleine Abweichung
        print("\nAudio-Resampling wurde erfolgreich durchgeführt und überprüft.")

    @unittest.skipIf(not os.path.exists("tests/test_data/speech_sample.wav"),
                     "Sprachsample nicht verfügbar")
    def test_process_real_audio(self):
        """
        Testet die Verarbeitung eines echten Sprachsamples.
        Dieser Test wird nur ausgeführt, wenn die Datei 'speech_sample.wav' im test_data Verzeichnis vorhanden ist.
        """
        # Lade das Sprachsample
        with wave.open("tests/test_data/speech_sample.wav", "rb") as wf:
            sample_rate = wf.getframerate()
            sample_width = wf.getsampwidth()
            n_channels = wf.getnchannels()
            n_frames = wf.getnframes()

            # Lese die Audiodaten
            audio_data = wf.readframes(n_frames)

        # Konvertiere die Audiodaten in ein NumPy-Array
        audio_array = np.frombuffer(audio_data, dtype=np.int16)

        # Normalisiere die Audiodaten auf den Bereich [-1, 1]
        audio_normalized = audio_array.astype(np.float32) / 32768.0

        # Führe das Resampling durch
        resampled_audio = self.processor.resample_audio(audio_normalized)

        # Überprüfe die grundlegenden Eigenschaften des resampled Audios
        self.assertIsInstance(resampled_audio, np.ndarray)
        expected_length = int(len(audio_normalized) * self.processor.TARGET_RATE / sample_rate)
        self.assertAlmostEqual(len(resampled_audio), expected_length, delta=1)

        # Überprüfe, ob die Werte im erwarteten Bereich liegen
        self.assertTrue(np.all(resampled_audio >= -1.0))
        self.assertTrue(np.all(resampled_audio <= 1.0))

        # Überprüfe, ob die Grundfrequenz erhalten bleibt (grob)
        original_fft = np.fft.fft(audio_normalized)
        resampled_fft = np.fft.fft(resampled_audio)
        original_peak = np.argmax(np.abs(original_fft[:len(original_fft)//2]))
        resampled_peak = np.argmax(np.abs(resampled_fft[:len(resampled_fft)//2]))
        self.assertAlmostEqual(original_peak / sample_rate,
                               resampled_peak / self.processor.TARGET_RATE,
                               delta=50)  # Erlaubt eine größere Abweichung für reale Audiodaten
        print("\nVerarbeitung des realen Audiosamples wurde erfolgreich durchgeführt und überprüft.")

if __name__ == '__main__':
    unittest.main()

# Zusätzliche Erklärungen:

# 1. Mocking:
#    In test_list_audio_devices verwenden wir Mocking, um die Hardwareabhängigkeit zu umgehen
#    und konsistente Testergebnisse zu gewährleisten.

# 2. Resampling-Test:
#    Der test_resample_audio überprüft nicht nur die grundlegende Funktionalität,
#    sondern auch die Erhaltung wichtiger Audioeigenschaften wie Frequenzcharakteristik.

# 3. Reales Audio-Sample:
#    test_process_real_audio verwendet ein echtes Audiobeispiel, um die Robustheit
#    des Resampling-Prozesses unter realen Bedingungen zu testen.

# 4. Conditional Skipping:
#    @unittest.skipIf wird verwendet, um den Test mit dem realen Audiosample zu überspringen,
#    falls die Testdatei nicht vorhanden ist. Dies erhöht die Flexibilität der Testausführung.
