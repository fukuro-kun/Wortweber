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
from typing import Union
import logging

class Transcriber:
    """
    Diese Klasse ist verantwortlich für die Transkription von Audiodaten
    unter Verwendung des OpenAI Whisper-Modells.
    """

    def __init__(self, model_name: str):
        """
        Initialisiert den Transcriber.

        :param model_name: Name des zu ladenden Whisper-Modells
        """
        self.model = None
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def load_model(self) -> None:
        """
        Lädt das Whisper-Modell.

        :raises Exception: Wenn das Laden des Modells fehlschlägt
        """
        logging.info(f"Lade Spracherkennungsmodell: {self.model_name}")
        try:
            self.model = whisper.load_model(self.model_name).to(self.device)
            logging.info(f"Spracherkennungsmodell {self.model_name} geladen auf {self.device}.")
        except Exception as e:
            logging.error(f"Fehler beim Laden des Modells: {e}")
            raise

    def transcribe(self, audio: Union[np.ndarray, torch.Tensor], language: str) -> str:
        """
        Transkribiert die gegebenen Audiodaten.

        :param audio: Audiodaten als NumPy-Array oder PyTorch-Tensor
        :param language: Sprache der Audiodaten
        :return: Transkribierter Text
        :raises RuntimeError: Wenn das Modell nicht geladen ist
        """
        if self.model is None:
            raise RuntimeError("Modell nicht geladen. Bitte warten Sie, bis das Modell vollständig geladen ist.")

        options = whisper.DecodingOptions(language=language, without_timestamps=True)

        # Ensure audio is in the correct format
        audio = whisper.pad_or_trim(audio)

        logging.debug(f"Audio shape after padding/trimming: {audio.shape}")

        # Create the log-mel spectrogram and move to the same device as the model
        mel = whisper.log_mel_spectrogram(audio).to(self.device)

        logging.debug(f"Mel spectrogram shape: {mel.shape}")

        try:
            result = whisper.decode(self.model, mel, options)
            return result.text
        except Exception as e:
            logging.error(f"Fehler bei der Transkription: {e}")
            logging.error(f"Detaillierter Traceback: {traceback.format_exc()}")
            return f"Fehler bei der Transkription: {str(e)}"

    def release_resources(self) -> None:
        """
        Gibt die Ressourcen des Modells frei.
        """
        if self.model:
            del self.model
            self.model = None
            if self.device == "cuda":
                torch.cuda.empty_cache()  # Explizit den GPU-Speicher leeren, falls CUDA verwendet wurde
        logging.info("Modellressourcen freigegeben.")

# Zusätzliche Erklärungen:

# 1. Gerätekompatibilität:
#    Die explizite Zuweisung des Mel-Spektrogramms zum Modellgerät (mel.to(self.device))
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
#    Ausführliche Logging-Statements ersetzen Print-Statements und bieten bessere
#    Möglichkeiten zur Fehlerdiagnose und Überwachung.

# 5. Ressourcenfreigabe:
#    Die release_resources Methode ermöglicht eine explizite Freigabe der Modellressourcen,
#    was besonders wichtig ist, wenn GPU-Speicher verwendet wird.
