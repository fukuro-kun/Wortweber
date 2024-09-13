# src/backend/transcriber.py
import whisper
import numpy as np
from typing import Optional
import logging
import torch
from src.config import DEFAULT_WHISPER_MODEL

class Transcriber:
    def __init__(self, model_name: str = DEFAULT_WHISPER_MODEL):
        self.model: Optional[whisper.Whisper] = None
        self.model_name = model_name
        self.transcription_time: float = 0.0

    def load_model(self, model_name: str):
        print(f"Lade Spracherkennungsmodell: {model_name}")
        try:
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
        return self.model is not None
