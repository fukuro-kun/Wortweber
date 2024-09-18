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
Dieses Modul enthält die Hauptlogik für die Ausführung der Wortweber-Tests.
Es bietet Optionen für verschiedene Testszenarien, einschließlich grundlegender Tests,
paralleler und sequenzieller Transkriptionstests sowie GUI-Tests.
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
from tests.frontend.test_wortweber_gui import TestWordweberGUI
from tests.frontend.test_main_window import TestMainWindow
import os
import warnings

# Unterdrücke ALSA-Warnungen
warnings.filterwarnings("ignore", category=RuntimeWarning, module="sounddevice")

# Unterdrücke JACK-Warnungen
os.environ['JACK_HIDE_WARNINGS'] = '1'


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

def run_tests(parallel: bool = False, sequential: bool = False, run_all: bool = False, gui: bool = False) -> unittest.TestResult:
    """
    Führt die spezifizierten Tests aus.

    Diese Funktion erstellt eine Test-Suite basierend auf den angegebenen Parametern
    und führt die Tests aus. Sie unterstützt grundlegende Tests, parallele und
    sequenzielle Transkriptionstests sowie GUI-Tests.

    :param parallel: Wenn True, werden parallele Transkriptionstests ausgeführt
    :param sequential: Wenn True, werden sequenzielle Transkriptionstests ausgeführt
    :param run_all: Wenn True, werden alle Tests ausgeführt
    :param gui: Wenn True, werden GUI-Tests ausgeführt
    :return: Ein unittest.TestResult-Objekt mit den Ergebnissen der Testausführung

    Die Funktion gibt eine Zusammenfassung der Testergebnisse aus, einschließlich
    der Anzahl der durchgeführten Tests, erfolgreichen Tests, Fehler und Fehlschläge.
    """
    suite = unittest.TestSuite()

    # Grundlegende Tests immer hinzufügen
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestAudioProcessor))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestTranscription))

    if run_all:
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(SequentialTranscriptionTest))
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ParallelTranscriptionTest))
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestWordweberGUI))
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestMainWindow))
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestTextProcessor))
    elif parallel:
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ParallelTranscriptionTest))
    elif sequential:
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(SequentialTranscriptionTest))
    elif gui:
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestWordweberGUI))
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestMainWindow))

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
    parser.add_argument('-g', '--gui', action='store_true', help='Run GUI tests')
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
        print(colored("Führe alle Tests einschließlich paralleler und sequenzieller Transkriptionstests sowie GUI-Tests aus.", "cyan"))
    elif args.parallel:
        print(colored(f"Führe parallele Transkriptionstests mit maximal {MAX_PARALLEL_TESTS} gleichzeitigen Tests aus.", "cyan"))
    elif args.sequential:
        print(colored("Führe sequenzielle Transkriptionstests aus.", "cyan"))
    elif args.gui:
        print(colored("Führe GUI-Tests aus.", "cyan"))
    else:
        print(colored("Führe grundlegende Tests ohne Transkriptions- oder GUI-Tests aus.", "cyan"))

    result = run_tests(parallel=args.parallel, sequential=args.sequential, run_all=args.all, gui=args.gui)

    sys.exit(not result.wasSuccessful())

# Zusätzliche Erklärungen:

# 1. Farbige Testausgabe:
#    Die ColorTextTestResult und ColorTextTestRunner Klassen ermöglichen eine
#    farbige und übersichtliche Ausgabe der Testergebnisse.

# 2. Flexible Testausführung:
#    Die run_tests Funktion ist so gestaltet, dass sie verschiedene Testkombinationen
#    basierend auf den übergebenen Argumenten ausführen kann, einschließlich GUI-Tests.

# 3. GPU-Ressourcenüberprüfung:
#    Vor der Ausführung der Tests wird die Verfügbarkeit von GPU-Ressourcen überprüft,
#    um sicherzustellen, dass parallele Tests nur bei ausreichenden Ressourcen ausgeführt werden.

# 4. Kommandozeilenargumente:
#    Die Verwendung von argparse ermöglicht eine flexible Konfiguration der Testausführung
#    über Kommandozeilenargumente, einschließlich Kurzformen (-p, -s, -a, -g).

# 5. Zusammenfassung der Testergebnisse:
#    Am Ende der Testausführung wird eine übersichtliche Zusammenfassung der Ergebnisse ausgegeben.

# Verwendung:
# - Für alle Tests: `python run_tests.py -a` oder `python run_tests.py --all`
# - Für parallele Transkriptionstests: `python run_tests.py -p` oder `python run_tests.py --parallel`
# - Für sequenzielle Transkriptionstests: `python run_tests.py -s` oder `python run_tests.py --sequential`
# - Für GUI-Tests: `python run_tests.py -g` oder `python run_tests.py --gui`
# - Für grundlegende Tests ohne Transkriptions- oder GUI-Tests: `python run_tests.py` (ohne Argumente)
