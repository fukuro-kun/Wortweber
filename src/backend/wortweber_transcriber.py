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

        Der Transcriber ist für die Spracherkennung zuständig und verwendet das OpenAI Whisper-Modell.
        Er unterstützt sowohl CPU- als auch GPU-basierte Verarbeitung und wählt automatisch die beste
        verfügbare Hardware aus.

        Args:
            model_name (str): Name des zu ladenden Whisper-Modells (z.B. "tiny", "base", "small", "medium", "large", "large-v3")

        Attributes:
            model: Das geladene Whisper-Modell
            model_name (str): Name des ausgewählten Modells
            device (str): Verwendete Hardware ("cuda" für GPU, "cpu" für CPU)
            settings_manager: Referenz zum SettingsManager (wird später von der GUI gesetzt)
        """
        self.model = None
        self.model_name = model_name
        
        # Versuche CUDA zu nutzen, falle auf CPU zurück wenn Probleme auftreten
        try:
            if torch.cuda.is_available():
                self.device = "cuda"
            else:
                self.device = "cpu"
        except Exception as e:
            logger.warning(f"CUDA-Initialisierung fehlgeschlagen, nutze CPU: {e}")
            self.device = "cpu"
            
        self.settings_manager = None  # Wird später von der GUI gesetzt
        logger.debug(f"Transcriber initialisiert mit Modell {model_name} auf Gerät {self.device}")

    @handle_exceptions
    def load_model(self) -> None:
        """
        Lädt das Whisper-Modell in den Speicher.

        Diese Methode initialisiert das Whisper-Modell und lädt es auf das ausgewählte Gerät (GPU/CPU).
        Das Laden kann je nach Modellgröße und Hardware einige Zeit in Anspruch nehmen.

        Raises:
            Exception: Wenn das Laden des Modells fehlschlägt, z.B. wegen Speichermangel oder ungültigem Modellnamen
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
        Transkribiert die gegebenen Audiodaten in Text.

        Diese Methode verwendet die OpenAI Whisper high-level API für die Transkription.
        Die Verwendung der high-level API bietet mehrere Vorteile:
        1. Automatische Audio-Vorverarbeitung (Padding, Mel-Spektrogramm)
        2. Integrierte Fehlerbehandlung
        3. Optimierte Performance
        4. Einfachere Wartung

        Die Transkriptionsparameter sind für optimale Qualität und Geschwindigkeit eingestellt:
        - beam_size=5: Anzahl der parallel betrachteten Transkriptionshypothesen
        - best_of=5/1: Anzahl der generierten Kandidaten (5 für GPU, 1 für CPU)
        - temperature=0.0: Deterministische Ausgabe
        - compression_ratio_threshold=2.4: Verhindert zu lange Ausgaben
        - logprob_threshold=-1.0: Minimale Wahrscheinlichkeit für akzeptierte Tokens
        - no_speech_threshold=0.6: Schwellenwert für Stille-Erkennung

        Args:
            audio (Union[np.ndarray, torch.Tensor]): Audiodaten als NumPy-Array oder PyTorch-Tensor
            language (str): Sprache der Audiodaten (z.B. "de" für Deutsch)

        Returns:
            str: Der transkribierte Text

        Raises:
            RuntimeError: Wenn das Modell nicht geladen ist
            Exception: Bei Fehlern während der Transkription
        """
        # Überprüfen, ob das Modell geladen ist
        if self.model is None:
            logger.error("Modell nicht geladen. Bitte warten Sie, bis das Modell vollständig geladen ist.")
            raise RuntimeError("Modell nicht geladen.")

        try:
            # Transkriptionsoptionen
            result = self.model.transcribe(
                audio,
                language=language,
                task="transcribe",
                beam_size=5,
                best_of=5 if self.device == "cuda" else 1,
                temperature=0.0,
                compression_ratio_threshold=2.4,
                logprob_threshold=-1.0,
                no_speech_threshold=0.6
            )
            
            # Extrahiere den transkribierten Text
            transcribed_text = result["text"].strip()

            # Überprüfen des Incognito-Modus für das Logging
            incognito_mode = self.settings_manager.get_setting("incognito_mode", DEFAULT_INCOGNITO_MODE) if self.settings_manager else DEFAULT_INCOGNITO_MODE

            # Erstellen einer geeigneten Log-Nachricht basierend auf dem Incognito-Modus
            if incognito_mode:
                log_message = f"Transkription abgeschlossen. Länge: {len(transcribed_text)} Zeichen."
            else:
                log_message = f"Transkription: {transcribed_text}"

            logger.info(log_message)

            return transcribed_text

        except Exception as e:
            logger.error(f"Fehler bei der Transkription: {e}")
            logger.debug(f"Traceback: {traceback.format_exc()}")
            raise

    @handle_exceptions
    def release_resources(self) -> None:
        """
        Gibt die vom Modell belegten Ressourcen frei.

        Diese Methode sollte aufgerufen werden, wenn das Modell nicht mehr benötigt wird.
        Sie stellt sicher, dass:
        1. Das Modell aus dem Speicher entfernt wird
        2. Bei GPU-Nutzung der CUDA-Speicher explizit freigegeben wird
        3. Alle anderen assoziierten Ressourcen freigegeben werden
        """
        if self.model:
            del self.model
            self.model = None
            if self.device == "cuda":
                torch.cuda.empty_cache()  # Explizit den GPU-Speicher leeren, falls CUDA verwendet wurde
        logger.info("Modellressourcen freigegeben.")


# Zusätzliche Erklärungen:

# 1. Whisper Modell-Architektur:
#    Der Transcriber verwendet OpenAI's Whisper, ein Transformer-basiertes Modell für
#    Spracherkennung. Die Architektur besteht aus einem Encoder-Decoder-System:
#    - Encoder: Verarbeitet das Audio-Signal und erstellt eine kontextuelle Repräsentation
#    - Decoder: Generiert den transkribierten Text basierend auf der Encoder-Ausgabe

# 2. Audio-Vorverarbeitung:
#    Whisper's high-level API führt automatisch wichtige Vorverarbeitungsschritte durch:
#    - Padding/Trimming: Anpassung der Audiolänge an die Modellanforderungen
#    - Mel-Spektrogramm: Transformation des Audiosignals in eine für das Modell verständliche Form
#    - Normalisierung: Anpassung der Audiodaten an den erwarteten Wertebereich

# 3. Transkriptionsparameter:
#    Die Parameter wurden für optimale Ergebnisse eingestellt:
#    - beam_size und best_of: Verbessern die Qualität durch Mehrfach-Hypothesen
#    - temperature=0.0: Macht die Ausgabe deterministisch
#    - compression_ratio_threshold: Verhindert "Halluzinationen" des Modells
#    - logprob_threshold: Filtert unsichere Vorhersagen
#    - no_speech_threshold: Optimiert die Stille-Erkennung

# 4. Ressourcenmanagement:
#    Der Transcriber implementiert effizientes Ressourcenmanagement:
#    - Automatische GPU/CPU-Erkennung
#    - Explizite Speicherfreigabe
#    - Fehlerbehandlung mit Logging
#    - Incognito-Modus für Datenschutz

# 5. Performance-Optimierung:
#    - GPU-Beschleunigung wenn verfügbar
#    - Optimierte Parameter für Echtzeit-Transkription
#    - Effiziente Speichernutzung
#    - Robuste Fehlerbehandlung

# Diese Implementierung bietet eine ausgewogene Balance zwischen
# Transkriptionsqualität, Geschwindigkeit und Ressourceneffizienz.
# Sie ist sowohl für Entwickler als auch für Endbenutzer optimiert
# und bietet gleichzeitig Flexibilität für zukünftige Erweiterungen.
