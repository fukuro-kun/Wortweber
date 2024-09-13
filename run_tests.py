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

# run_tests.py

import unittest
import sys
from termcolor import colored
import warnings

# Unterdrücke Warnungen, die oft bei Audiooperationen auftreten können
warnings.filterwarnings("ignore", category=RuntimeWarning)

class ColorTextTestResult(unittest.TextTestResult):
    """
    Angepasste TestResult-Klasse für farbige Ausgabe der Testergebnisse.
    """

    def addSuccess(self, test):
        """
        Wird aufgerufen, wenn ein Test erfolgreich ist.

        :param test: Der erfolgreich durchgeführte Test
        """
        super().addSuccess(test)
        self.stream.writeln(colored(f"OK: {test.shortDescription() or test.id()}", "green"))

    def addError(self, test, err):
        """
        Wird aufgerufen, wenn bei einem Test ein Fehler auftritt.

        :param test: Der fehlgeschlagene Test
        :param err: Die aufgetretene Fehlerinformation
        """
        super().addError(test, err)
        self.stream.writeln(colored(f"ERROR: {test.shortDescription() or test.id()}", "red"))
        self.stream.writeln(self.errors[-1][1])

    def addFailure(self, test, err):
        """
        Wird aufgerufen, wenn ein Test fehlschlägt.

        :param test: Der fehlgeschlagene Test
        :param err: Die Fehlerinformation
        """
        super().addFailure(test, err)
        self.stream.writeln(colored(f"FAIL: {test.shortDescription() or test.id()}", "red"))
        self.stream.writeln(self.failures[-1][1])

class ColorTextTestRunner(unittest.TextTestRunner):
    """
    Angepasster TestRunner für die Verwendung des ColorTextTestResult.
    """
    resultclass = ColorTextTestResult

if __name__ == "__main__":
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests')

    runner = ColorTextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    print("\nTest Summary:")
    print(f"Ran {result.testsRun} tests")
    print(colored(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}", "green"))
    print(colored(f"Failures: {len(result.failures)}", "red" if result.failures else "green"))
    print(colored(f"Errors: {len(result.errors)}", "red" if result.errors else "green"))

    sys.exit(not result.wasSuccessful())

# Zusätzliche Erklärungen:

# 1. ColorTextTestResult:
#    Diese Klasse erweitert die StandardTestResult-Klasse, um farbige Ausgaben zu ermöglichen.
#    Sie überschreibt die Methoden für erfolgreiche Tests, Fehler und Fehlschläge.

# 2. ColorTextTestRunner:
#    Ein angepasster TestRunner, der die ColorTextTestResult-Klasse verwendet.

# 3. Test Discovery:
#    Der TestLoader durchsucht automatisch das 'tests'-Verzeichnis nach Testdateien.

# 4. Zusammenfassung:
#    Am Ende wird eine Zusammenfassung der Testergebnisse ausgegeben, einschließlich
#    der Anzahl der durchgeführten Tests, Erfolge, Fehlschläge und Fehler.
