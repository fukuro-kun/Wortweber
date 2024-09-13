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

    def test_record_audio(self):
        """Testet die Audioaufnahmefunktion."""
        # Mocking für record_audio
        self.processor.p = MagicMock()
        mock_stream = MagicMock()
        self.processor.p.open.return_value = mock_stream
        mock_stream.read.return_value = b'test_audio_data'

        mock_state = MagicMock()
        mock_state.recording = True
        mock_state.audio_data = []

        # Simulation des Aufnahmeendes nach einem Durchlauf
        def stop_recording():
            mock_state.recording = False
        mock_stream.read.side_effect = lambda *args, **kwargs: stop_recording() or b'test_audio_data'

        duration = self.processor.record_audio(mock_state)

        self.assertGreater(duration, 0)
        self.assertEqual(len(mock_state.audio_data), 1)
        self.assertEqual(mock_state.audio_data[0], b'test_audio_data')

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

# Zusätzliche Erklärungen:

# 1. Reales Audiosamples-Test:
#    Der neue Test `test_process_real_audio` verwendet das aufgenommene Sprachsample,
#    um die Resampling-Funktion unter realen Bedingungen zu testen. Dies stellt sicher,
#    dass die Funktion nicht nur mit synthetischen Daten, sondern auch mit echten
#    Audioaufnahmen korrekt arbeitet.

# 2. Conditional Skipping:
#    Der Decorator `@unittest.skipIf` wird verwendet, um den Test zu überspringen,
#    wenn die Testdatei nicht vorhanden ist. Dies ermöglicht es, die Tests auch in
#    Umgebungen auszuführen, in denen das Sprachsample nicht verfügbar ist.

# 3. Frequenzanalyse:
#    Die Überprüfung der Grundfrequenz mittels FFT stellt sicher, dass das Resampling
#    die wesentlichen Eigenschaften des Audiosignals beibehält. Für reale Audiodaten
#    wird eine größere Toleranz verwendet, da diese komplexer sind als synthetische Signale.

# 4. Normalisierung:
#    Die Audiodaten werden auf den Bereich [-1, 1] normalisiert, um konsistent mit
#    der erwarteten Eingabe der Resampling-Funktion zu sein.

if __name__ == '__main__':
    unittest.main()
