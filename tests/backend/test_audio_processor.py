# tests/backend/test_audio_processor.py

import unittest
from src.backend.audio_processor import AudioProcessor

class TestAudioProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = AudioProcessor()

    def test_audio_processor_initialization(self):
        self.assertIsInstance(self.processor, AudioProcessor)

    def test_list_audio_devices(self):
        # Dies ist ein einfacher Test, der sicherstellt, dass die Methode ohne Fehler ausgeführt wird
        try:
            self.processor.list_audio_devices()
        except Exception as e:
            self.fail(f"list_audio_devices raised {type(e).__name__} unexpectedly!")

if __name__ == "__main__":
    unittest.main()
