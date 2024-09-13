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

# tests/backend/test_audio_recording.py

import unittest
import pyaudio
import wave
import os
import numpy as np
from src.config import AUDIO_CHUNK, AUDIO_FORMAT, AUDIO_CHANNELS, AUDIO_RATE, DEVICE_INDEX

class TestAudioRecording(unittest.TestCase):
    """
    Testklasse für die Audioaufnahmefunktionalität.
    Überprüft die grundlegende Funktionalität der Audioaufnahme und -speicherung.
    """

    def setUp(self):
        """Initialisiert die Testumgebung vor jedem Testfall."""
        self.p = pyaudio.PyAudio()
        self.RECORD_SECONDS = 2
        self.WAVE_OUTPUT_FILENAME = "test_output.wav"

    def tearDown(self):
        """Räumt die Testumgebung nach jedem Testfall auf."""
        self.p.terminate()
        if os.path.exists(self.WAVE_OUTPUT_FILENAME):
            os.remove(self.WAVE_OUTPUT_FILENAME)

    def test_audio_recording(self):
        """
        Testet den Audioaufnahmeprozess.
        Nimmt eine kurze Audiosequenz auf, speichert sie als WAV-Datei und überprüft die Dateiintegrität.
        """
        stream = self.p.open(format=AUDIO_FORMAT,
                             channels=AUDIO_CHANNELS,
                             rate=AUDIO_RATE,
                             input=True,
                             input_device_index=DEVICE_INDEX,
                             frames_per_buffer=AUDIO_CHUNK)

        print("* recording")

        frames = []

        for _ in range(0, int(AUDIO_RATE / AUDIO_CHUNK * self.RECORD_SECONDS)):
            data = stream.read(AUDIO_CHUNK, exception_on_overflow=False)
            frames.append(data)

        print("* done recording")

        stream.stop_stream()
        stream.close()

        wf = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(AUDIO_CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(AUDIO_FORMAT))
        wf.setframerate(AUDIO_RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        # Überprüfen, ob die Datei erstellt wurde und Audiodaten enthält
        self.assertTrue(os.path.exists(self.WAVE_OUTPUT_FILENAME))
        with wave.open(self.WAVE_OUTPUT_FILENAME, 'rb') as wf:
            self.assertEqual(wf.getnchannels(), AUDIO_CHANNELS)
            self.assertEqual(wf.getframerate(), AUDIO_RATE)
            audio_data = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16)
            self.assertGreater(len(audio_data), 0)
            self.assertNotEqual(np.max(np.abs(audio_data)), 0)  # Sicherstellen, dass nicht-Null-Audiodaten vorhanden sind

# Zusätzliche Erklärungen:

# 1. PyAudio Verwendung:
#    PyAudio wird verwendet, um auf die Audiogeräte des Systems zuzugreifen und Audiostreams zu öffnen.
#    Dies ermöglicht die direkte Aufnahme von Audio für Testzwecke.

# 2. WAV-Datei Erstellung:
#    Der Test erstellt eine temporäre WAV-Datei, um die aufgenommenen Audiodaten zu speichern.
#    Dies simuliert den tatsächlichen Aufnahmeprozess in der Anwendung.

# 3. Datenintegrität:
#    Der Test überprüft nicht nur, ob die Datei erstellt wurde, sondern auch ob sie gültige Audiodaten enthält.
#    Dies stellt sicher, dass der gesamte Aufnahme- und Speicherprozess korrekt funktioniert.

# 4. Aufräumen:
#    Die tearDown-Methode stellt sicher, dass alle verwendeten Ressourcen freigegeben und temporäre Dateien gelöscht werden.
#    Dies ist wichtig für die Isolation zwischen den Tests und verhindert unerwünschte Seiteneffekte.

if __name__ == '__main__':
    unittest.main()
