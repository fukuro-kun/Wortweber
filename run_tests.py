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
Dieses Modul enthält die Hauptlogik für die Ausführung der Wortweber-Tests.
Es bietet Optionen für verschiedene Testszenarien, einschließlich grundlegender Tests,
paralleler und sequenzieller Transkriptionstests.
"""

import unittest
import sys
from termcolor import colored
import argparse
from src.backend.wortweber_utils import check_gpu_resources
from tests.test_config import MIN_GPU_MEMORY, MAX_PARALLEL_TESTS
from tests.test_sequential_transcription import SequentialTranscriptionTest
from tests.test_parallel_transcription import ParallelTranscriptionTest
from tests.backend.test_audio_processor import TestAudioProcessor
from tests.backend.test_transcription import TestTranscription

class ColorTextTestResult(unittest.TextTestResult):
    """Angepasste TestResult-Klasse für farbige Ausgabe der Testergebnisse."""

    def addSuccess(self, test):
        super().addSuccess(test)
        self.stream.writeln(colored(f"OK: {test.shortDescription() or test.id()}", "green"))

    def addError(self, test, err):
        super().addError(test, err)
        self.stream.writeln(colored(f"ERROR: {test.shortDescription() or test.id()}", "red"))
        self.stream.writeln(self.errors[-1][1])

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.stream.writeln(colored(f"FAIL: {test.shortDescription() or test.id()}", "red"))
        self.stream.writeln(self.failures[-1][1])

class ColorTextTestRunner(unittest.TextTestRunner):
    """Angepasster TestRunner für die Verwendung des ColorTextTestResult."""
    resultclass = ColorTextTestResult

def run_tests(parallel=False, sequential=False, run_all=False):
    """
    Führt die spezifizierten Tests aus.

    :param parallel: Wenn True, werden parallele Transkriptionstests ausgeführt
    :param sequential: Wenn True, werden sequenzielle Transkriptionstests ausgeführt
    :param run_all: Wenn True, werden alle Tests ausgeführt
    :return: TestResult-Objekt mit den Testergebnissen
    """
    suite = unittest.TestSuite()

    # Grundlegende Tests immer hinzufügen
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestAudioProcessor))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestTranscription))

    if run_all:
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(SequentialTranscriptionTest))
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ParallelTranscriptionTest))
    elif parallel:
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ParallelTranscriptionTest))
    elif sequential:
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(SequentialTranscriptionTest))

    runner = ColorTextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\nTest Summary:")
    print(f"Ran {result.testsRun} tests")
    print(colored(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}", "green"))
    print(colored(f"Failures: {len(result.failures)}", "red" if result.failures else "green"))
    print(colored(f"Errors: {len(result.errors)}", "red" if result.errors else "green"))

    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Wortweber tests")
    parser.add_argument('-p', '--parallel', action='store_true', help='Run transcription tests in parallel')
    parser.add_argument('-s', '--sequential', action='store_true', help='Run transcription tests sequentially')
    parser.add_argument('-a', '--all', action='store_true', help='Run all tests including both parallel and sequential transcription tests')
    args = parser.parse_args()

    gpu_available, gpu_memory = check_gpu_resources()

    if not gpu_available:
        print(colored("WARNUNG: Keine GPU verfügbar. Tests werden auf der CPU ausgeführt.", "yellow"))
        args.parallel = False
    elif gpu_memory < MIN_GPU_MEMORY:
        print(colored(f"WARNUNG: Nicht genug GPU-Speicher. Verfügbar: {gpu_memory:.2f} GB, Benötigt: {MIN_GPU_MEMORY} GB", "yellow"))
        print(colored("Parallele Transkriptionstests werden deaktiviert.", "yellow"))
        args.parallel = False

    if args.all:
        print(colored("Führe alle Tests einschließlich paralleler und sequenzieller Transkriptionstests aus.", "cyan"))
    elif args.parallel:
        print(colored(f"Führe parallele Transkriptionstests mit maximal {MAX_PARALLEL_TESTS} gleichzeitigen Tests aus.", "cyan"))
    elif args.sequential:
        print(colored("Führe sequenzielle Transkriptionstests aus.", "cyan"))
    else:
        print(colored("Führe grundlegende Tests ohne Transkriptionstests aus.", "cyan"))

    result = run_tests(parallel=args.parallel, sequential=args.sequential, run_all=args.all)

    sys.exit(not result.wasSuccessful())

# Zusätzliche Erklärungen:

# 1. Farbige Testausgabe:
#    Die ColorTextTestResult und ColorTextTestRunner Klassen ermöglichen eine
#    farbige und übersichtliche Ausgabe der Testergebnisse.

# 2. Flexible Testausführung:
#    Die run_tests Funktion ist so gestaltet, dass sie verschiedene Testkombinationen
#    basierend auf den übergebenen Argumenten ausführen kann.

# 3. GPU-Ressourcenüberprüfung:
#    Vor der Ausführung der Tests wird die Verfügbarkeit von GPU-Ressourcen überprüft,
#    um sicherzustellen, dass parallele Tests nur bei ausreichenden Ressourcen ausgeführt werden.

# 4. Kommandozeilenargumente:
#    Die Verwendung von argparse ermöglicht eine flexible Konfiguration der Testausführung
#    über Kommandozeilenargumente, einschließlich Kurzformen (-p, -s, -a).

# 5. Zusammenfassung der Testergebnisse:
#    Am Ende der Testausführung wird eine übersichtliche Zusammenfassung der Ergebnisse ausgegeben.

# Verwendung:
# - Für alle Tests: `python run_tests.py -a` oder `python run_tests.py --all`
# - Für parallele Transkriptionstests: `python run_tests.py -p` oder `python run_tests.py --parallel`
# - Für sequenzielle Transkriptionstests: `python run_tests.py -s` oder `python run_tests.py --sequential`
# - Für grundlegende Tests ohne Transkriptionstests: `python run_tests.py` (ohne Argumente)
