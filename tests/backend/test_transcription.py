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

import unittest
import os
import numpy as np
import wave
import librosa
from src.backend.transcriber import Transcriber
from src.config import DEFAULT_WHISPER_MODEL
import whisper

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
        transcriber.load_model(DEFAULT_WHISPER_MODEL)

        # Führe die Transkription durch
        transcribed_text = transcriber.transcribe(audio_array, "de")

        print(f"Transcribed text: '{transcribed_text}'")

        # Überprüfe, ob die erwarteten Worte in der Transkription enthalten sind
        expected_phrase = "Das ist ein Test"
        self.assertIn(expected_phrase, transcribed_text,
                      f"Die erwartete Phrase '{expected_phrase}' wurde nicht in der Transkription gefunden. "
                      f"Transkribierter Text: '{transcribed_text}'")

if __name__ == '__main__':
    unittest.main()

# Zusätzliche Erklärungen:

# 1. Testdatenvorbereitung:
#    Der Test lädt ein vordefiniertes Sprachsample und bereitet es für die Verarbeitung vor.
#    Dies stellt sicher, dass wir konsistente Eingabedaten für unsere Tests haben.

# 2. Audiovorverarbeitung:
#    Das Audio wird normalisiert und auf die von Whisper erwartete Sampling-Rate umgewandelt.
#    Dies ist entscheidend, da Whisper spezifische Anforderungen an das Eingabeformat hat.

# 3. Modellinitialisierung:
#    Der Test verwendet das in der Konfiguration definierte Standard-Whisper-Modell.
#    Dies ermöglicht eine konsistente Testumgebung und erleichtert Änderungen des Modells.

# 4. Fehlerbehandlung:
#    Der Test verwendet einen AssertIn-Check, um zu überprüfen, ob die erwartete Phrase
#    in der Transkription enthalten ist. Dies ermöglicht eine gewisse Flexibilität bei
#    der Bewertung der Transkriptionsgenauigkeit.

# 5. Debugging-Ausgaben:
#    Umfangreiche Print-Statements geben Einblick in die Eigenschaften des Audios
#    in verschiedenen Verarbeitungsstufen, was bei der Fehlersuche hilfreich ist.
