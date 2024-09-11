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
from typing import List, Optional
import whisper
import numpy as np
from src.config import RATE, TARGET_RATE
from src.backend.audio_processor import AudioProcessor
from src.backend.transcriber import Transcriber
import threading

class WordweberState:
    def __init__(self):
        self.recording: bool = False
        self.audio_data: List[bytes] = []
        self.start_time: float = 0
        self.model: Optional[whisper.Whisper] = None
        self.transcription_time: float = 0

class WordweberBackend:
    def __init__(self):
        self.state = WordweberState()
        self.audio_processor = AudioProcessor()
        self.transcriber = Transcriber()

    def start_recording(self):
        self.state.recording = True
        self.state.audio_data = []
        threading.Thread(target=self._record_audio, daemon=True).start()

    def stop_recording(self):
        self.state.recording = False

    def _record_audio(self):
        self.audio_processor.record_audio(self.state)

    def process_and_transcribe(self, language: str) -> str:
        audio_np = np.frombuffer(b''.join(self.state.audio_data), dtype=np.int16).astype(np.float32) / 32768.0
        audio_resampled = self.audio_processor.resample_audio(audio_np)
        return self.transcriber.transcribe(audio_resampled, language)

    def load_transcriber_model(self, model_name: str):
        self.transcriber.load_model(model_name)

    def list_audio_devices(self):
        self.audio_processor.list_audio_devices()