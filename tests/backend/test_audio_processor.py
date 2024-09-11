import unittest
from src.backend.audio_processor import AudioProcessor
from unittest.mock import MagicMock
import io
import sys
import numpy as np

class TestAudioProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = AudioProcessor()

    def test_audio_processor_initialization(self):
        self.assertIsInstance(self.processor, AudioProcessor)

    def test_list_audio_devices(self):
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
        import numpy as np
        test_audio = np.array([0, 1, 2, 3, 4, 5], dtype=np.float32)
        resampled = self.processor.resample_audio(test_audio)
        self.assertIsInstance(resampled, np.ndarray)
        self.assertEqual(len(resampled), len(test_audio) * self.processor.TARGET_RATE // self.processor.RATE)

    def test_process_audio(self):
        mock_state = MagicMock()
        mock_state.audio_data = [b'\x00\x80', b'\x00\x00', b'\x00\x00', b'\xFF\x7F']
        processed = self.processor.process_audio(mock_state)
        print(f"Debug: Processed audio in test: {processed}")

        self.assertIsInstance(processed, np.ndarray)
        self.assertGreaterEqual(len(processed), 2)
        self.assertTrue(np.all(processed >= -1.001))  # Erlaubt eine kleine Toleranz
        self.assertTrue(np.all(processed <= 1.001))   # Erlaubt eine kleine Toleranz
        self.assertLess(processed[0], 0)  # Erster Wert sollte negativ sein
        self.assertGreater(processed[-1], 0)  # Letzter Wert sollte positiv sein

        # Test mit sehr kurzer Eingabe
        mock_state.audio_data = [b'\x00\x80', b'\xFF\x7F']
        processed_short = self.processor.process_audio(mock_state)
        print(f"Debug: Processed short audio in test: {processed_short}")

        self.assertGreaterEqual(len(processed_short), 2)
        self.assertTrue(np.all(processed_short >= -1.001))  # Erlaubt eine kleine Toleranz
        self.assertTrue(np.all(processed_short <= 1.001))   # Erlaubt eine kleine Toleranz
        self.assertLess(processed_short[0], 0)
        self.assertGreater(processed_short[-1], 0)

if __name__ == '__main__':
    unittest.main()
