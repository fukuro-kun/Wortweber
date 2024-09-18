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



# tests/test_sequential_transcription.py

import unittest
from tests.base_test import BaseTranscriptionTest
from tests.test_config import MODELS_TO_TEST, TEST_LANGUAGES
from src.backend.wortweber_transcriber import Transcriber
import logging

class SequentialTranscriptionTest(BaseTranscriptionTest):
    """
    Testklasse für sequenzielle Transkriptionstests.
    Führt Tests für verschiedene Whisper-Modelle nacheinander aus.
    """
    def load_model(self, model_name: str):
        """
        Lädt das Whisper-Modell für den Test.

        :param model_name: Name des zu ladenden Modells
        """
        self.transcriber = Transcriber(model_name)
        self.transcriber.load_model()

    def test_sequential_transcription(self):
        """
        Führt sequenzielle Transkriptionstests für alle konfigurierten Modelle
        und Sprachen durch.
        """
        for model in MODELS_TO_TEST:
            with self.subTest(model=model):
                for language in TEST_LANGUAGES:
                    with self.subTest(language=language):
                        self.basic_transcription_test(model, language)

    def basic_transcription_test(self, model_name: str, language: str):
        """
        Führt einen grundlegenden Transkriptionstest für ein spezifisches Modell
        und eine spezifische Sprache durch.

        :param model_name: Name des zu testenden Whisper-Modells
        :param language: Sprache für die Transkription
        """
        logging.info(f"Starte Test für Modell {model_name} in Sprache {language}")
        self.load_model(model_name)
        if self.transcriber is None:
            raise ValueError("Transcriber wurde nicht korrekt initialisiert")

        audio_path = self.get_test_audio_path()
        audio_data = self.load_and_prepare_audio(audio_path)

        transcribed_text = self.transcriber.transcribe(audio_data, language)

        logging.info(f"Transkribierter Text ({model_name}, {language}): {transcribed_text}")

        self.assertIsNotNone(transcribed_text)
        self.assertTrue(len(transcribed_text) > 0)

        expected_words = self.get_expected_words(language)
        logging.info(f"Erwartete Wörter: {expected_words}")
        for word in expected_words:
            self.assertIn(word.lower(), transcribed_text.lower(),
                          f"Erwartetes Wort '{word}' nicht in '{transcribed_text}' gefunden")

# Zusätzliche Erklärungen:

# 1. Die Klasse nutzt verschachtelte subTests, um detaillierte Informationen
#    über fehlgeschlagene Tests für spezifische Modell-Sprach-Kombinationen zu erhalten.

# 2. Die basic_transcription_test Methode kapselt die Logik für einen einzelnen
#    Testdurchlauf, was die Wiederverwendbarkeit und Lesbarkeit des Codes verbessert.

# 3. Es wird eine explizite Überprüfung durchgeführt, ob der Transcriber
#    korrekt initialisiert wurde, um potenzielle Fehler frühzeitig zu erkennen.

# 4. Die Methode überprüft sowohl die Existenz als auch den Inhalt der
#    transkribierten Texte, um die Korrektheit der Transkription sicherzustellen.

# 5. Durch die Verwendung von Konfigurationsvariablen (MODELS_TO_TEST, TEST_LANGUAGES)
#    ist der Test leicht erweiterbar und anpassbar.
