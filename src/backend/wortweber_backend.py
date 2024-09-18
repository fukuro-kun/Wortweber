# Wortweber - Echtzeit-Sprachtranskription mit KI
# Copyright (C) 2024 fukuro-kun
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.



"""
Dieses Modul enthält die Hauptlogik für das Backend der Wortweber-Anwendung.
Es koordiniert die Audioaufnahme, Transkription und Datenverwaltung.
"""

from typing import List, Optional, Tuple, Callable
import numpy as np
from src.config import AUDIO_RATE, AUDIO_FORMAT, AUDIO_CHANNELS, AUDIO_CHUNK, DEVICE_INDEX, TARGET_RATE, DEFAULT_WHISPER_MODEL, DEFAULT_INCOGNITO_MODE
from src.backend.audio_processor import AudioProcessor
from src.backend.wortweber_transcriber import Transcriber
import threading
from src.utils.error_handling import handle_exceptions, logger

class WordweberState:
    def __init__(self):
        self.recording: bool = False
        self.audio_data: List[bytes] = []
        self.start_time: float = 0
        self.transcription_time: float = 0
        self.language: str = "de"

class WordweberBackend:
    @handle_exceptions
    def __init__(self, settings_manager):
        self.settings_manager = settings_manager
        self.state = WordweberState()
        self.audio_processor = AudioProcessor(self.settings_manager)
        self.transcriber = Transcriber(DEFAULT_WHISPER_MODEL)
        self.model_loaded = threading.Event()
        self.on_transcription_complete: Optional[Callable[[str], None]] = None
        self.pending_audio: List[np.ndarray] = []
        logger.info("WordweberBackend initialisiert")

    @handle_exceptions
    def start_recording(self) -> None:
        """Startet die Audioaufnahme."""
        if not self.audio_processor.check_device_availability():
            logger.error("Audiogerät nicht verfügbar. Aufnahme kann nicht gestartet werden.")
            return

        self.state.recording = True
        self.state.audio_data = []
        threading.Thread(target=self._record_audio, daemon=True).start()
        logger.info("Audioaufnahme gestartet")

    @handle_exceptions
    def stop_recording(self) -> None:
        """Stoppt die Audioaufnahme und verarbeitet die aufgenommenen Daten."""
        self.state.recording = False
        if self.model_loaded.is_set():
            self.process_and_transcribe(self.state.language)
        else:
            audio_np = np.frombuffer(b''.join(self.state.audio_data), dtype=np.int16).astype(np.float32) / 32768.0
            audio_resampled = self.audio_processor.resample_audio(audio_np)
            self.pending_audio.append(audio_resampled)
            logger.info("Aufnahme gespeichert. Warte auf Modell-Bereitschaft.")

    @handle_exceptions
    def _record_audio(self) -> None:
        """Interne Methode zur Audioaufnahme."""
        duration = self.audio_processor.record_audio(self.state)
        logger.debug(f"Audioaufnahme beendet. Dauer: {duration:.2f} Sekunden")

    @handle_exceptions
    def process_and_transcribe(self, language: str) -> str:
        """
        Verarbeitet und transkribiert die aufgenommenen Audiodaten.

        :param language: Die Sprache für die Transkription
        :return: Der transkribierte Text
        """
        if not self.model_loaded.is_set():
            logger.error("Modell nicht geladen. Bitte warten Sie, bis das Modell vollständig geladen ist.")
            raise RuntimeError("Modell nicht geladen. Bitte warten Sie, bis das Modell vollständig geladen ist.")

        audio_to_process = self.pending_audio + [np.frombuffer(b''.join(self.state.audio_data), dtype=np.int16).astype(np.float32) / 32768.0]
        self.pending_audio = []

        transcribed_text = ""
        for audio_np in audio_to_process:
            audio_resampled = self.audio_processor.resample_audio(audio_np)
            transcribed_text += self.transcriber.transcribe(audio_resampled, language)

        if self.on_transcription_complete:
            self.on_transcription_complete(transcribed_text)

        incognito_mode = self.settings_manager.get_setting("incognito_mode", DEFAULT_INCOGNITO_MODE) if self.settings_manager else DEFAULT_INCOGNITO_MODE
        if not incognito_mode:
            logger.info(f"Transkription abgeschlossen. Länge des Textes: {len(transcribed_text)}")
        else:
            logger.info("Transkription abgeschlossen (Incognito-Modus aktiv)")

        return transcribed_text

    @handle_exceptions
    def load_transcriber_model(self, model_name: str) -> None:
        """
        Lädt das Transkriptionsmodell.

        :param model_name: Der Name des zu ladenden Modells
        """
        try:
            self.transcriber.load_model()
            self.model_loaded.set()
            if self.pending_audio:
                self.process_and_transcribe(self.state.language)
            logger.info(f"Transkriptionsmodell '{model_name}' erfolgreich geladen")
        except Exception as e:
            logger.error(f"Fehler beim Laden des Modells: {e}")
            self.model_loaded.clear()

    @handle_exceptions
    def list_audio_devices(self) -> None:
        """Listet alle verfügbaren Audiogeräte auf."""
        self.audio_processor.list_audio_devices()

    @handle_exceptions
    def check_audio_device(self) -> bool:
        """
        Überprüft, ob das konfigurierte Audiogerät verfügbar ist.

        :return: True, wenn das Gerät verfügbar ist, sonst False
        """
        return self.audio_processor.check_device_availability()

    @handle_exceptions
    def update_audio_device(self, new_index) -> bool:
        """Aktualisiert das Audiogerät basierend auf dem neuen Index."""
        if self.audio_processor.update_device(new_index):
            device_info = self.audio_processor.get_current_device_info()
            if device_info:
                logger.info(f"Audiogerät erfolgreich aktualisiert auf: {device_info['name']} (Index: {device_info['index']})")
                return True
            else:
                logger.warning("Audiogerät aktualisiert, aber keine Geräteinformationen verfügbar.")
                return False
        else:
            logger.error("Fehler beim Aktualisieren des Audiogeräts.")
            return False

    @handle_exceptions
    def get_current_audio_device(self):
        """Gibt Informationen über das aktuell verwendete Audiogerät zurück."""
        return self.audio_processor.get_current_device_info()

    @handle_exceptions
    def set_language(self, language: str) -> None:
        """
        Setzt die Sprache für die Transkription.

        :param language: Der Sprachcode (z.B. 'de' für Deutsch)
        """
        self.state.language = language
        logger.info(f"Sprache für Transkription auf {language} gesetzt")

# Zusätzliche Erklärungen:

# 1. WordweberState:
#    Diese Klasse kapselt den Zustand der Anwendung, einschließlich Aufnahmestatus,
#    Audiodaten und Zeitstempel. Dies verbessert die Übersichtlichkeit und erleichtert
#    die Zustandsverwaltung.

# 2. Asynchrone Verarbeitung:
#    Die Verwendung von Threading ermöglicht es, Audioaufnahmen und Modellladung
#    im Hintergrund durchzuführen, ohne die Hauptanwendung zu blockieren.

# 3. Fehlerbehandlung:
#    Umfassende Fehlerbehandlung und Logging sind implementiert, um robuste
#    Ausführung und einfache Fehlerbehebung zu gewährleisten.

# 4. Modellverwaltung:
#    Das Backend verwaltet den Ladezustand des Transkriptionsmodells und
#    ermöglicht die Verarbeitung von Audiodaten, sobald das Modell bereit ist.

# 5. Flexibilität:
#    Die Struktur erlaubt einfache Erweiterungen, wie z.B. das Hinzufügen
#    neuer Transkriptionsmodelle oder Audioformate in der Zukunft.
