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

"""
Dieses Modul enthält die Hauptlogik für das Backend der Wortweber-Anwendung.
Es koordiniert die Audioaufnahme, Transkription und Datenverwaltung.
"""

# src/backend/wortweber_backend.py

from typing import List, Optional, Tuple, Callable
import numpy as np
from src.config import AUDIO_RATE, AUDIO_FORMAT, AUDIO_CHANNELS, AUDIO_CHUNK, DEVICE_INDEX, TARGET_RATE, DEFAULT_WHISPER_MODEL
from src.backend.audio_processor import AudioProcessor
from src.backend.wortweber_transcriber import Transcriber
import threading
import logging

class WordweberState:
    def __init__(self):
        self.recording: bool = False
        self.audio_data: List[bytes] = []
        self.start_time: float = 0
        self.transcription_time: float = 0
        self.language: str = "de"

class WordweberBackend:
    def __init__(self):
        self.state = WordweberState()
        self.audio_processor = AudioProcessor()
        self.transcriber = Transcriber(DEFAULT_WHISPER_MODEL)
        self.model_loaded = threading.Event()
        self.on_transcription_complete: Optional[Callable[[str], None]] = None
        self.pending_audio: List[np.ndarray] = []

    def start_recording(self):
        self.state.recording = True
        self.state.audio_data = []
        threading.Thread(target=self._record_audio, daemon=True).start()

    def stop_recording(self):
        self.state.recording = False
        if self.model_loaded.is_set():
            self.process_and_transcribe(self.state.language)
        else:
            audio_np = np.frombuffer(b''.join(self.state.audio_data), dtype=np.int16).astype(np.float32) / 32768.0
            audio_resampled = self.audio_processor.resample_audio(audio_np)
            self.pending_audio.append(audio_resampled)
            logging.info("Aufnahme gespeichert. Warte auf Modell-Bereitschaft.")

    def _record_audio(self):
        duration = self.audio_processor.record_audio(self.state)

    def process_and_transcribe(self, language: str) -> str:
        if not self.model_loaded.is_set():
            raise RuntimeError("Modell nicht geladen. Bitte warten Sie, bis das Modell vollständig geladen ist.")

        audio_to_process = self.pending_audio + [np.frombuffer(b''.join(self.state.audio_data), dtype=np.int16).astype(np.float32) / 32768.0]
        self.pending_audio = []

        transcribed_text = ""
        for audio_np in audio_to_process:
            audio_resampled = self.audio_processor.resample_audio(audio_np)
            transcribed_text += self.transcriber.transcribe(audio_resampled, language)

        if self.on_transcription_complete:
            self.on_transcription_complete(transcribed_text)

        return transcribed_text

    def load_transcriber_model(self, model_name: str):
        try:
            self.transcriber.load_model()
            self.model_loaded.set()
            if self.pending_audio:
                self.process_and_transcribe(self.state.language)
        except Exception as e:
            logging.error(f"Fehler beim Laden des Modells: {e}")
            self.model_loaded.clear()

    def list_audio_devices(self):
        self.audio_processor.list_audio_devices()

    def check_audio_device(self):
        try:
            stream = self.audio_processor.p.open(format=AUDIO_FORMAT, channels=AUDIO_CHANNELS, rate=AUDIO_RATE, input=True,
                                                 frames_per_buffer=AUDIO_CHUNK, input_device_index=DEVICE_INDEX)
            stream.close()
            return True
        except Exception as e:
            logging.error(f"Fehler beim Überprüfen des Audiogeräts: {e}")
            return False

    def set_language(self, language: str):
        self.state.language = language
