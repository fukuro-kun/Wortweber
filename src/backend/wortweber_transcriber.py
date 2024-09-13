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
        self.model = None
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def load_model(self):
        print(f"Lade Spracherkennungsmodell: {self.model_name}")
        try:
            self.model = whisper.load_model(self.model_name).to(self.device)
            print(f"Spracherkennungsmodell {self.model_name} geladen auf {self.device}.")
        except Exception as e:
            print(f"Fehler beim Laden des Modells: {e}")
            raise

    def transcribe(self, audio: np.ndarray, language: str) -> str:
        if self.model is None:
            raise RuntimeError("Modell nicht geladen. Bitte warten Sie, bis das Modell vollständig geladen ist.")

        options = whisper.DecodingOptions(language=language, without_timestamps=True)

        # Ensure audio is in the correct format
        audio = whisper.pad_or_trim(audio)

        # Log the shape of the audio after padding/trimming
        print(f"Audio shape after padding/trimming: {audio.shape}")

        # Create the log-mel spectrogram and move to the same device as the model
        mel = whisper.log_mel_spectrogram(audio).to(self.device)

        # Log the shape of the mel spectrogram
        print(f"Mel spectrogram shape: {mel.shape}")

        try:
            result = whisper.decode(self.model, mel, options)
            return result.text
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
