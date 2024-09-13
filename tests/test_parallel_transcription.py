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

# tests/test_parallel_transcription.py

import unittest
from concurrent.futures import ThreadPoolExecutor, as_completed
from tests.base_test import BaseTranscriptionTest
from tests.test_config import MODELS_TO_TEST, MAX_PARALLEL_TESTS
from src.backend.wortweber_transcriber import Transcriber
from termcolor import colored

class ParallelTranscriptionTest(BaseTranscriptionTest):
    """
    Testklasse für parallele Transkriptionstests.
    Führt Tests für verschiedene Whisper-Modelle gleichzeitig aus.
    """

    def test_parallel_transcription(self):
        """
        Führt parallele Transkriptionstests für alle konfigurierten Modelle durch.
        Verwendet ThreadPoolExecutor für gleichzeitige Ausführung.
        """
        test_cases = [(model, "de") for model in MODELS_TO_TEST]
        results = []

        with ThreadPoolExecutor(max_workers=MAX_PARALLEL_TESTS) as executor:
            futures = [executor.submit(self.run_single_test, model, "de") for model in MODELS_TO_TEST]

            for future in as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    self.fail(f"Test fehlgeschlagen mit Fehler: {str(e)}")

        # Ausgabe der Ergebnisse
        for model, success, message in results:
            if success:
                print(colored(f"OK: Test für Modell {model} erfolgreich", "green"))
            else:
                print(colored(f"FAIL: Test für Modell {model} fehlgeschlagen - {message}", "red"))

        # Überprüfung, ob alle Tests erfolgreich waren
        self.assertTrue(all(success for _, success, _ in results), "Nicht alle Tests waren erfolgreich")

    def run_single_test(self, model, language):
        """
        Führt einen einzelnen Transkriptionstest für ein spezifisches Modell durch.

        :param model: Name des zu testenden Whisper-Modells
        :param language: Sprache für die Transkription
        :return: Tuple (model, success, message) mit Testergebnis
        """
        try:
            transcriber = Transcriber(model)
            transcriber.load_model()
            audio_path = self.get_test_audio_path()
            audio_data = self.load_and_prepare_audio(audio_path)
            transcribed_text = transcriber.transcribe(audio_data, language)

            self.assertIsNotNone(transcribed_text)
            self.assertTrue(len(transcribed_text) > 0)

            expected_words = self.get_expected_words(language)
            for word in expected_words:
                self.assertIn(word.lower(), transcribed_text.lower())

            return model, True, "Test erfolgreich"
        except Exception as e:
            return model, False, str(e)

# Zusätzliche Erklärungen:

# 1. Die Klasse nutzt ThreadPoolExecutor für parallele Ausführung der Tests,
#    was die Gesamttestzeit reduziert.

# 2. Jeder Test wird in einem separaten Thread ausgeführt, was eine effiziente
#    Nutzung der verfügbaren Ressourcen ermöglicht.

# 3. Die Ergebnisse werden gesammelt und am Ende übersichtlich ausgegeben,
#    wobei erfolgreiche Tests grün und fehlgeschlagene Tests rot markiert werden.

# 4. Die Methode run_single_test kapselt die Logik für einen einzelnen Testdurchlauf,
#    was die Wiederverwendbarkeit und Lesbarkeit des Codes verbessert.

# 5. Fehlerbehandlung ist integriert, um robuste Tests zu gewährleisten und
#    detaillierte Fehlermeldungen zu liefern.
