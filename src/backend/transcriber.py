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
import whisper
import numpy as np
from typing import Optional

class Transcriber:
    def __init__(self, model_name: str = "small"):
        self.model: Optional[whisper.Whisper] = None
        self.model_name = model_name
        self.transcription_time: float = 0.0

    def load_model(self, model_name: str):
        """Lädt das Whisper-Modell."""
        print(f"Lade Spracherkennungsmodell: {model_name}")
        self.model = whisper.load_model(model_name)
        print("Spracherkennungsmodell geladen.")

    def transcribe(self, audio: np.ndarray, language: str) -> str:
        """
        Transkribiert das gegebene Audio.

        :param audio: NumPy-Array mit Audiodaten
        :param language: Sprache des Audios (z.B. "de" für Deutsch)
        :return: Transkribierter Text
        """
        if self.model is None:
            raise RuntimeError("Modell nicht geladen. Bitte warten Sie, bis das Modell vollständig geladen ist.")

        options = whisper.DecodingOptions(language=language, without_timestamps=True)
        result = self.model.transcribe(audio, **options.__dict__)

        return result["text"].strip() if isinstance(result["text"], str) else str(result["text"])

    def is_model_loaded(self) -> bool:
        """Überprüft, ob das Modell geladen ist."""
        return self.model is not None
