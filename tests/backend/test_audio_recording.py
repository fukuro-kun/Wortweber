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

        print("\nAudioaufnahme wurde erfolgreich durchgeführt, gespeichert und überprüft.")

if __name__ == '__main__':
    unittest.main()

# Zusätzliche Erklärungen:

# 1. PyAudio Setup:
#    Wir verwenden PyAudio, um auf die Audiogeräte des Systems zuzugreifen und Audiostreams zu öffnen.
#    Dies ermöglicht realistische Tests der Audioaufnahmefunktionalität.

# 2. Temporäre Datei:
#    Der Test erstellt eine temporäre WAV-Datei, um die aufgenommenen Audiodaten zu speichern.
#    Dies simuliert den tatsächlichen Aufnahmeprozess in der Anwendung.

# 3. Dateiintegrität:
#    Nach der Aufnahme überprüfen wir nicht nur die Existenz der Datei, sondern auch
#    ihre Eigenschaften (Kanäle, Abtastrate) und den Inhalt (nicht-leere Audiodaten).

# 4. Ressourcenmanagement:
#    Die tearDown-Methode stellt sicher, dass alle verwendeten Ressourcen freigegeben
#    und temporäre Dateien gelöscht werden, um Seiteneffekte zwischen Tests zu vermeiden.

# 5. Konfigurationsabhängigkeit:
#    Der Test verwendet Konfigurationsvariablen aus src.config, um sicherzustellen,
#    dass die Testbedingungen mit den tatsächlichen Anwendungseinstellungen übereinstimmen.
