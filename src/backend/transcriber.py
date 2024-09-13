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

# src/backend/transcriber.py
import whisper
import numpy as np
from typing import Optional
import logging
import torch
from src.config import DEFAULT_WHISPER_MODEL

class Transcriber:
    """
    Diese Klasse ist verantwortlich für die Transkription von Audiodaten in Text.
    Sie verwendet das OpenAI Whisper-Modell für die Spracherkennung.
    """

    def __init__(self, model_name: str = DEFAULT_WHISPER_MODEL):
        """
        Initialisiert den Transcriber.

        :param model_name: Name des zu verwendenden Whisper-Modells (Standard ist in der Konfiguration definiert)
        """
        self.model: Optional[whisper.Whisper] = None
        self.model_name = model_name
        self.transcription_time: float = 0.0

    def load_model(self, model_name: str):
        """
        Lädt das spezifizierte Whisper-Modell.

        :param model_name: Name des zu ladenden Modells
        """
        print(f"Lade Spracherkennungsmodell: {model_name}")
        try:
            # Wenn CUDA verfügbar ist, wird das Modell auf die GPU geladen
            if torch.cuda.is_available():
                self.model = whisper.load_model(model_name).cuda()
            else:
                self.model = whisper.load_model(model_name)
            print("Spracherkennungsmodell geladen.")
        except Exception as e:
            print(f"Fehler beim Laden des Modells: {e}")
            logging.exception("Detaillierter Traceback beim Laden des Modells:")
            raise

    def transcribe(self, audio: np.ndarray, language: str) -> str:
        """
        Transkribiert das gegebene Audio in Text.

        :param audio: NumPy-Array mit den Audiodaten
        :param language: Sprache des Audios ('de' für Deutsch, 'en' für Englisch)
        :return: Transkribierter Text
        """
        if self.model is None:
            raise RuntimeError("Modell nicht geladen. Bitte warten Sie, bis das Modell vollständig geladen ist.")

        try:
            logging.debug(f"Transkription gestartet. Audio shape: {audio.shape}, dtype: {audio.dtype}")
            options = whisper.DecodingOptions(language=language, without_timestamps=True)
            result = self.model.transcribe(audio, **options.__dict__)
            transcribed_text = result["text"].strip() if isinstance(result["text"], str) else str(result["text"])
            logging.debug(f"Transkribierter Text: {transcribed_text[:100]}...")
            return transcribed_text
        except Exception as e:
            logging.error(f"Fehler bei der Transkription: {e}")
            logging.exception("Detaillierter Traceback:")
            return f"Fehler bei der Transkription: {str(e)}"

    def is_model_loaded(self) -> bool:
        """
        Überprüft, ob das Modell geladen ist.

        :return: True, wenn das Modell geladen ist, sonst False
        """
        return self.model is not None

# Zusätzliche Erklärungen:

# 1. Whisper-Modell:
#    OpenAI's Whisper ist ein leistungsfähiges Spracherkennungsmodell, das mehrere Sprachen unterstützt.
#    Es kann Sprache in Text umwandeln und bietet verschiedene Modellgrößen für unterschiedliche Genauigkeits- und Geschwindigkeitsanforderungen.

# 2. CUDA-Unterstützung:
#    Die Methode `load_model` prüft auf CUDA-Verfügbarkeit. CUDA ermöglicht die Nutzung von NVIDIA GPUs für beschleunigte Berechnungen,
#    was die Transkriptionsgeschwindigkeit erheblich verbessern kann.

# 3. Fehlerbehandlung:
#    Sowohl beim Laden des Modells als auch bei der Transkription werden ausführliche Fehlerprotokolle erstellt.
#    Dies ist besonders wichtig für die Diagnose von Problemen in Produktionsumgebungen.

# 4. Transkriptionsoptions:
#    Die `DecodingOptions` in der `transcribe`-Methode ermöglichen eine feinere Kontrolle über den Transkriptionsprozess.
#    Hier wird die Sprache festgelegt und Zeitstempel werden deaktiviert.

# 5. Modellstatus:
#    Die Methode `is_model_loaded` dient als einfache Statusprüfung, die von anderen Teilen der Anwendung verwendet werden kann,
#    um sicherzustellen, dass das Modell bereit ist, bevor eine Transkription versucht wird.
