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



import unittest
import os
import numpy as np
import wave
import librosa
from src.backend.wortweber_transcriber import Transcriber
from src.config import DEFAULT_WHISPER_MODEL
import whisper
from src.backend.wortweber_backend import WordweberBackend
import time

class TestTranscription(unittest.TestCase):
    """
    Testklasse für die Transkriptionsfunktionalität.
    Überprüft die Genauigkeit der Transkription anhand eines Sprachsamples.
    """

    @unittest.skipIf(not os.path.exists("tests/test_data/speech_sample.wav"),
                     "Sprachsample nicht verfügbar")
    def test_transcription_accuracy(self):
        """
        Testet die Genauigkeit der Transkription.
        Lädt ein Sprachsample, führt die Transkription durch und überprüft,
        ob die erwartete Phrase korrekt erkannt wurde.
        """
        # Lade das Sprachsample
        with wave.open("tests/test_data/speech_sample.wav", "rb") as wf:
            sample_rate = wf.getframerate()
            sample_width = wf.getsampwidth()
            n_channels = wf.getnchannels()
            n_frames = wf.getnframes()
            audio_data = wf.readframes(n_frames)

        # Konvertiere die Audiodaten in ein NumPy-Array und normalisiere sie
        audio_array = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0

        # Debugging: Ausgabe der Audiodaten-Informationen
        print(f"Original sample rate: {sample_rate}")
        print(f"Original audio shape: {audio_array.shape}")
        print(f"Audio dtype: {audio_array.dtype}")
        print(f"Audio min: {audio_array.min()}, max: {audio_array.max()}")

        # Resampling auf 16000 Hz (Whisper's erwartete Sampling-Rate)
        if sample_rate != whisper.audio.SAMPLE_RATE:
            print(f"Resampling audio from {sample_rate} Hz to {whisper.audio.SAMPLE_RATE} Hz")
            audio_array = librosa.resample(audio_array, orig_sr=sample_rate, target_sr=whisper.audio.SAMPLE_RATE)

        print(f"Resampled audio shape: {audio_array.shape}")

        # Initialisiere den Transcriber und lade das Modell
        transcriber = Transcriber(DEFAULT_WHISPER_MODEL)
        transcriber.load_model()

        # Führe die Transkription durch
        transcribed_text = transcriber.transcribe(audio_array, "de")

        print(f"Transcribed text: '{transcribed_text}'")

        # Überprüfe, ob die erwarteten Worte in der Transkription enthalten sind
        expected_phrase = "Das ist ein Test"
        self.assertIn(expected_phrase, transcribed_text,
                      f"Die erwartete Phrase '{expected_phrase}' wurde nicht in der Transkription gefunden. "
                      f"Transkribierter Text: '{transcribed_text}'")
        print(f"\nErwartete Phrase: '{expected_phrase}'")
        print(f"Transkribierter Text: '{transcribed_text}'")

class TestModelLoading(unittest.TestCase):
    """
    Testklasse für das Laden des Transkriptionsmodells.
    Überprüft die korrekte Verarbeitung von Audiodaten vor und nach dem Modell-Laden.
    """

    def test_audio_processing_before_model_loading(self):
        """
        Testet die Audioverarbeitung vor dem Laden des Modells.
        Überprüft, ob Audiodaten korrekt zwischengespeichert und nach dem Modell-Laden verarbeitet werden.
        """
        backend = WordweberBackend()

        # Simuliere eine Audioaufnahme vor dem Laden des Modells
        dummy_audio = np.random.rand(16000).astype(np.float32)
        backend.state.audio_data = [dummy_audio.tobytes()]

        # Stoppe die "Aufnahme", was die Daten in pending_audio speichern sollte
        backend.stop_recording()

        self.assertEqual(len(backend.pending_audio), 1, "Audio wurde nicht in pending_audio gespeichert")
        print("\nAudio wurde erfolgreich in pending_audio gespeichert.")

        # Lade das Modell
        backend.load_transcriber_model(DEFAULT_WHISPER_MODEL)

        # Warte auf das Laden des Modells
        timeout = 60  # 60 Sekunden Timeout
        start_time = time.time()
        while not backend.model_loaded.is_set() and time.time() - start_time < timeout:
            time.sleep(1)

        self.assertTrue(backend.model_loaded.is_set(), "Modell wurde nicht innerhalb des Timeouts geladen")
        print("Modell wurde erfolgreich geladen.")

        self.assertEqual(len(backend.pending_audio), 0, "Pending audio wurde nicht verarbeitet")
        print("Pending audio wurde erfolgreich verarbeitet.")

if __name__ == '__main__':
    unittest.main()

# Zusätzliche Erklärungen:

# 1. Sprachsample-Test:
#    Der test_transcription_accuracy verwendet ein voraufgezeichnetes Sprachsample,
#    um die Genauigkeit der Transkription unter kontrollierten Bedingungen zu testen.

# 2. Resampling:
#    Vor der Transkription wird das Audio auf die von Whisper erwartete Abtastrate (16000 Hz) konvertiert.
#    Dies stellt sicher, dass die Eingabe für das Modell korrekt formatiert ist.

# 3. Modell-Ladetest:
#    test_audio_processing_before_model_loading simuliert den realen Anwendungsfall,
#    bei dem Audiodaten möglicherweise vor dem vollständigen Laden des Modells aufgenommen werden.

# 4. Asynchrones Modell-Laden:
#    Der Test wartet mit einem Timeout auf das Laden des Modells, um asynchrones Verhalten zu berücksichtigen.

# 5. Debugging-Ausgaben:
#    Umfangreiche Print-Statements helfen bei der Diagnose potenzieller Probleme
#    und geben Einblick in den Zustand der Audiodaten und des Transkriptionsprozesses.
