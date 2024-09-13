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

# src/backend/wortweber_backend.py

from typing import List, Optional, Tuple, Callable
import numpy as np
from src.config import AUDIO_RATE, AUDIO_FORMAT, AUDIO_CHANNELS, AUDIO_CHUNK, DEVICE_INDEX, TARGET_RATE
from src.backend.audio_processor import AudioProcessor
from src.backend.transcriber import Transcriber
import threading
import logging

class WordweberState:
    """
    Repräsentiert den aktuellen Zustand der Wortweber-Anwendung.
    """
    def __init__(self):
        self.recording: bool = False
        self.audio_data: List[bytes] = []
        self.start_time: float = 0
        self.transcription_time: float = 0
        self.language: str = "de"

class WordweberBackend:
    """
    Hauptklasse für die Backend-Logik der Wortweber-Anwendung.
    Koordiniert Audioaufnahme, Transkription und Datenverwaltung.
    """
    def __init__(self):
        self.state = WordweberState()
        self.audio_processor = AudioProcessor()
        self.transcriber = Transcriber()
        self.model_loaded = threading.Event()
        self.on_transcription_complete: Optional[Callable[[str], None]] = None
        self.pending_audio: List[np.ndarray] = []

    def start_recording(self):
        """Startet die Audioaufnahme in einem separaten Thread."""
        self.state.recording = True
        self.state.audio_data = []
        threading.Thread(target=self._record_audio, daemon=True).start()

    def stop_recording(self):
        """
        Stoppt die Aufnahme und verarbeitet das aufgenommene Audio.
        Wenn das Modell geladen ist, wird die Transkription sofort gestartet,
        ansonsten wird das Audio für spätere Verarbeitung gespeichert.
        """
        self.state.recording = False
        if self.model_loaded.is_set():
            self.process_and_transcribe(self.state.language)
        else:
            audio_np = np.frombuffer(b''.join(self.state.audio_data), dtype=np.int16).astype(np.float32) / 32768.0
            audio_resampled = self.audio_processor.resample_audio(audio_np)
            self.pending_audio.append(audio_resampled)
            logging.info("Aufnahme gespeichert. Warte auf Modell-Bereitschaft.")

    def _record_audio(self):
        """Interne Methode zur Durchführung der Audioaufnahme."""
        duration = self.audio_processor.record_audio(self.state)

    def process_and_transcribe(self, language: str) -> str:
        """
        Verarbeitet aufgenommenes Audio und führt die Transkription durch.

        :param language: Sprache des Audios ('de' für Deutsch, 'en' für Englisch)
        :return: Transkribierter Text
        """
        if not self.model_loaded.is_set():
            raise RuntimeError("Modell nicht geladen. Bitte warten Sie, bis das Modell vollständig geladen ist.")

        audio_to_process = self.pending_audio + [np.frombuffer(b''.join(self.state.audio_data), dtype=np.int16).astype(np.float32) / 32768.0]
        self.pending_audio = []  # Leere die Liste der ausstehenden Aufnahmen

        transcribed_text = ""
        for audio_np in audio_to_process:
            audio_resampled = self.audio_processor.resample_audio(audio_np)
            transcribed_text += self.transcriber.transcribe(audio_resampled, language)

        if self.on_transcription_complete:
            self.on_transcription_complete(transcribed_text)

        return transcribed_text

    def load_transcriber_model(self, model_name: str):
        """
        Lädt das spezifizierte Transkriptionsmodell.

        :param model_name: Name des zu ladenden Whisper-Modells
        """
        try:
            self.transcriber.load_model(model_name)
            self.model_loaded.set()
            # Verarbeite ausstehende Aufnahmen
            if self.pending_audio:
                self.process_and_transcribe(self.state.language)
        except Exception as e:
            logging.error(f"Fehler beim Laden des Modells: {e}")
            self.model_loaded.clear()

    def list_audio_devices(self):
        """Listet verfügbare Audiogeräte auf."""
        self.audio_processor.list_audio_devices()

    def check_audio_device(self):
        """
        Überprüft, ob das konfigurierte Audiogerät verfügbar ist.

        :return: True, wenn das Gerät verfügbar ist, sonst False
        """
        try:
            stream = self.audio_processor.p.open(format=AUDIO_FORMAT, channels=AUDIO_CHANNELS, rate=AUDIO_RATE, input=True,
                                                 frames_per_buffer=AUDIO_CHUNK, input_device_index=DEVICE_INDEX)
            stream.close()
            return True
        except Exception as e:
            logging.error(f"Fehler beim Überprüfen des Audiogeräts: {e}")
            return False

    def set_language(self, language: str):
        """
        Setzt die Sprache für die Transkription.

        :param language: 'de' für Deutsch oder 'en' für Englisch
        """
        self.state.language = language

# Zusätzliche Erklärungen:

# 1. Zustandsverwaltung:
#    Die `WordweberState`-Klasse kapselt den Zustand der Anwendung. Dies erleichtert das Debugging
#    und die Erweiterung der Anwendung, da alle relevanten Zustandsinformationen zentral verwaltet werden.

# 2. Asynchrone Verarbeitung:
#    Die Verwendung von Threads für die Audioaufnahme ermöglicht es der Anwendung,
#    reaktionsfähig zu bleiben, während im Hintergrund Audio aufgenommen wird.

# 3. Modell-Lademanagement:
#    Der `model_loaded` Event wird verwendet, um sicherzustellen, dass Transkriptionen erst
#    durchgeführt werden, wenn das Modell vollständig geladen ist. Dies verhindert Fehler durch
#    vorzeitige Transkriptionsversuche.

# 4. Fehlerbehandlung:
#    Umfangreiche Fehlerprotokollierung hilft bei der Diagnose von Problemen, insbesondere
#    bei der Initialisierung von Audiogeräten und dem Laden des Modells.

# 5. Flexibilität:
#    Die Möglichkeit, ausstehende Audioaufnahmen zu speichern und später zu verarbeiten,
#    erhöht die Robustheit der Anwendung, insbesondere wenn das Modell noch nicht geladen ist.
