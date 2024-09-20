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



import torch
import numpy as np
import whisper
import traceback
from whisper.audio import SAMPLE_RATE, N_FRAMES, HOP_LENGTH
from typing import Union
from src.utils.error_handling import handle_exceptions, logger
from src.config import DEFAULT_INCOGNITO_MODE

class Transcriber:
    @handle_exceptions
    def __init__(self, model_name: str):
        """
        Initialisiert den Transcriber.

        :param model_name: Name des zu ladenden Whisper-Modells
        """
        self.model = None
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.settings_manager = None  # Wird später von der GUI gesetzt
        logger.info(f"Transcriber initialisiert mit Modell {model_name} auf Gerät {self.device}")

    @handle_exceptions
    def load_model(self) -> None:
        """
        Lädt das Whisper-Modell.

        :raises Exception: Wenn das Laden des Modells fehlschlägt
        """
        logger.info(f"Lade Spracherkennungsmodell: {self.model_name}")
        try:
            self.model = whisper.load_model(self.model_name).to(self.device)
            logger.info(f"Spracherkennungsmodell {self.model_name} geladen auf {self.device}.")
        except Exception as e:
            logger.error(f"Fehler beim Laden des Modells: {e}")
            raise

    @handle_exceptions
    def transcribe(self, audio: Union[np.ndarray, torch.Tensor], language: str) -> str:
        """
        Transkribiert die gegebenen Audiodaten.

        :param audio: Audiodaten als NumPy-Array oder PyTorch-Tensor
        :param language: Sprache der Audiodaten
        :return: Transkribierter Text
        :raises RuntimeError: Wenn das Modell nicht geladen ist
        """
        if self.model is None:
            logger.error("Modell nicht geladen. Bitte warten Sie, bis das Modell vollständig geladen ist.")
            raise RuntimeError("Modell nicht geladen. Bitte warten Sie, bis das Modell vollständig geladen ist.")

        options = whisper.DecodingOptions(language=language, without_timestamps=True)

        # Vergewissern, dass der Ton im richtigen Format vorliegt.
        audio = whisper.pad_or_trim(audio)

        logger.debug(f"Audio shape after padding/trimming: {audio.shape}")

        # Erstellt das Log-Mel-Spektrogramm und verschiebt es auf das gleiche Gerät wie das Modell.
        mel = whisper.log_mel_spectrogram(audio).to(self.device)

        logger.debug(f"Mel spectrogram shape: {mel.shape}")

        try:
            result = whisper.decode(self.model, mel, options)
            transcribed_text = result.text

            incognito_mode = self.settings_manager.get_setting("incognito_mode", DEFAULT_INCOGNITO_MODE) if self.settings_manager else DEFAULT_INCOGNITO_MODE

            if not incognito_mode:
                logger.info(f"Transkription: {transcribed_text}")
            else:
                logger.info("Transkription abgeschlossen (Incognito-Modus aktiv)")

            logger.info(f"Transkriptionslänge: {len(transcribed_text)} Zeichen")

            return transcribed_text
        except Exception as e:
            logger.error(f"Fehler bei der Transkription: {e}")
            logger.error(f"Detaillierter Traceback: {traceback.format_exc()}")
            return f"Fehler bei der Transkription: {str(e)}"


    @handle_exceptions
    def release_resources(self) -> None:
        """
        Gibt die Ressourcen des Modells frei.
        """
        if self.model:
            del self.model
            self.model = None
            if self.device == "cuda":
                torch.cuda.empty_cache()  # Explizit den GPU-Speicher leeren, falls CUDA verwendet wurde
        logger.info("Modellressourcen freigegeben.")

# Zusätzliche Erklärungen:

# 1. Incognito-Modus Integration:
#    In der transcribe Methode wurde eine Abfrage des Incognito-Modus hinzugefügt.
#    Wenn der Incognito-Modus aktiv ist, wird der transkribierte Text nicht geloggt.

# 2. Flexibilität bei fehlender SettingsManager-Instanz:
#    Die Implementierung berücksichtigt den Fall, dass der SettingsManager noch nicht
#    gesetzt wurde, indem sie auf den Standardwert aus der Konfiguration zurückgreift.

# 3. Konsistente Fehlerbehandlung:
#    Alle Methoden verwenden den @handle_exceptions Decorator, was eine einheitliche
#    Fehlerbehandlung und -protokollierung in der gesamten Klasse gewährleistet.

# 4. Detailliertes Logging:
#    Die Klasse verwendet ausführliches Logging, um den Transkriptionsprozess
#    nachvollziehbar zu machen und potenzielle Probleme schnell identifizieren zu können.

# 5. Ressourcenmanagement:
#    Die release_resources Methode stellt sicher, dass GPU-Ressourcen ordnungsgemäß
#    freigegeben werden, was besonders wichtig ist, wenn die Anwendung auf Systemen
#    mit begrenztem GPU-Speicher läuft.

# Diese Implementierung ermöglicht es, den Incognito-Modus nahtlos in den
# Transkriptionsprozess zu integrieren, ohne die Grundfunktionalität zu beeinträchtigen.
