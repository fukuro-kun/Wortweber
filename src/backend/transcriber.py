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

import torch
import numpy as np
import whisper
from whisper.audio import SAMPLE_RATE, N_FRAMES, HOP_LENGTH

class Transcriber:
    def __init__(self, model_name: str):
        """
        Initialisiert den Transcriber mit einem spezifizierten Modellnamen.

        :param model_name: Name des zu ladenden Whisper-Modells
        """
        self.model = None
        self.model_name = model_name

    def load_model(self, model_name: str):
        """
        Lädt das spezifizierte Whisper-Modell und weist es dem korrekten Gerät zu.

        :param model_name: Name des zu ladenden Whisper-Modells
        """
        print(f"Lade Spracherkennungsmodell: {model_name}")
        try:
            # Bestimme das verfügbare Gerät (CUDA GPU wenn verfügbar, sonst CPU)
            device = "cuda" if torch.cuda.is_available() else "cpu"
            # Lade das Modell und weise es dem bestimmten Gerät zu
            self.model = whisper.load_model(model_name).to(device)
            print(f"Spracherkennungsmodell geladen auf {device}.")
        except Exception as e:
            print(f"Fehler beim Laden des Modells: {e}")
            raise

    def transcribe(self, audio: np.ndarray, language: str) -> str:
        """
        Führt die Transkription des gegebenen Audioarrays durch.

        :param audio: NumPy-Array des Audiosamples
        :param language: Sprache des Audios für die Transkription
        :return: Transkribierter Text
        """
        if self.model is None:
            raise RuntimeError("Modell nicht geladen. Bitte warten Sie, bis das Modell vollständig geladen ist.")

        try:
            print(f"Transcribe Input - Audio shape: {audio.shape}, dtype: {audio.dtype}")

            # Stelle sicher, dass das Audio die korrekte Form und den korrekten Typ hat
            if len(audio.shape) == 2:
                audio = audio.mean(axis=1)  # Konvertiere Stereo zu Mono
            audio = audio.astype(np.float32)

            # Padde oder kürze das Audio auf die korrekte Länge
            audio = whisper.pad_or_trim(audio)

            # Erstelle das log-Mel-Spektrogramm und verschiebe es auf das Gerät des Modells
            mel = whisper.log_mel_spectrogram(audio).to(self.model.device)

            print(f"Mel-Spektrogramm shape: {mel.shape}")

            # Dekodiere das Audio
            options = whisper.DecodingOptions(language=language, without_timestamps=True)
            result = whisper.decode(self.model, mel, options)

            transcribed_text = result.text.strip()
            print(f"Whisper Ausgabe: {transcribed_text}")
            return transcribed_text

        except Exception as e:
            print(f"Fehler bei der Transkription: {e}")
            import traceback
            print(f"Detaillierter Traceback: {traceback.format_exc()}")
            return f"Fehler bei der Transkription: {str(e)}"

# Zusätzliche Erklärungen:

# 1. Gerätekompatibilität:
#    Die explizite Zuweisung des Mel-Spektrogramms zum Modellgerät (mel.to(self.model.device))
#    stellt sicher, dass alle Tensoren auf demselben Gerät sind, was kritisch für die
#    reibungslose Ausführung des Modells ist.

# 2. Audiovorverarbeitung:
#    Die Verwendung von whisper.pad_or_trim() und whisper.log_mel_spectrogram()
#    gewährleistet, dass das Audio in einem Format vorliegt, das vom Whisper-Modell
#    erwartet wird, und verhindert Formfehler.

# 3. Fehlerbehandlung:
#    Umfassende Try-Except-Blöcke mit detaillierten Fehlerausgaben erleichtern das
#    Debugging und die Identifikation von Problemen während der Transkription.

# 4. Logging:
#    Ausführliche Print-Statements geben Einblick in den Zustand des Audios und
#    des Mel-Spektrogramms in verschiedenen Verarbeitungsstufen.
