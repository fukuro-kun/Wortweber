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

import unittest
import sys
import os
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from termcolor import colored

# Fügen Sie den src-Ordner und den tests-Ordner zum Python-Pfad hinzu
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def import_test_class(module_path, class_name):
    module = __import__(module_path, fromlist=[class_name])
    return getattr(module, class_name)

def run_test_case(test_case):
    suite = unittest.TestLoader().loadTestsFromTestCase(test_case)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return test_case.__name__, result

def parallel_test_execution(test_cases):
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        futures = [executor.submit(run_test_case, test_case) for test_case in test_cases]
        results = []
        for future in as_completed(futures):
            results.append(future.result())
    return results

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run Wortweber tests')
    parser.add_argument('-a', '--all', action='store_true', help='Run all tests')
    parser.add_argument('-b', '--backend', action='store_true', help='Run backend tests')
    parser.add_argument('-f', '--frontend', action='store_true', help='Run frontend tests')
    parser.add_argument('-u', '--utils', action='store_true', help='Run utility tests')
    parser.add_argument('-p', '--parallel', action='store_true', help='Run parallel transcription tests')
    parser.add_argument('-s', '--sequential', action='store_true', help='Run sequential transcription tests')
    parser.add_argument('-g', '--gui', action='store_true', help='Run GUI tests')
    parser.add_argument('-e', '--error', action='store_true', help='Run error handling tests')
    args = parser.parse_args()

    test_cases = []

    if args.all or not any(vars(args).values()):
        test_modules = [
            ('tests.test_parallel_transcription', 'ParallelTranscriptionTest'),
            ('tests.test_sequential_transcription', 'SequentialTranscriptionTest'),
            ('tests.frontend.test_wortweber_gui', 'TestWordweberGUI'),
            ('tests.frontend.test_main_window', 'TestMainWindow'),
            ('tests.frontend.test_options_panel', 'TestOptionsPanel'),
            ('tests.frontend.test_status_panel', 'TestStatusPanel'),
            ('tests.frontend.test_transcription_panel', 'TestTranscriptionPanel'),
            ('tests.backend.test_audio_processor', 'TestAudioProcessor'),
            ('tests.backend.test_audio_recording', 'TestAudioRecording'),
            ('tests.backend.test_transcription', 'TestTranscription'),
            ('tests.backend.test_text_processor', 'TestTextProcessor'),
            ('tests.utils.test_text_processing', 'TestTextProcessing'),
            ('tests.test_error_handling', 'TestErrorHandling')
        ]
        for module_path, class_name in test_modules:
            test_cases.append(import_test_class(module_path, class_name))
    else:
        if args.backend:
            backend_modules = [
                ('tests.backend.test_audio_processor', 'TestAudioProcessor'),
                ('tests.backend.test_audio_recording', 'TestAudioRecording'),
                ('tests.backend.test_transcription', 'TestTranscription'),
                ('tests.backend.test_text_processor', 'TestTextProcessor')
            ]
            for module_path, class_name in backend_modules:
                test_cases.append(import_test_class(module_path, class_name))
        if args.frontend:
            frontend_modules = [
                ('tests.frontend.test_wortweber_gui', 'TestWordweberGUI'),
                ('tests.frontend.test_main_window', 'TestMainWindow'),
                ('tests.frontend.test_options_panel', 'TestOptionsPanel'),
                ('tests.frontend.test_status_panel', 'TestStatusPanel'),
                ('tests.frontend.test_transcription_panel', 'TestTranscriptionPanel')
            ]
            for module_path, class_name in frontend_modules:
                test_cases.append(import_test_class(module_path, class_name))
        if args.utils:
            test_cases.append(import_test_class('tests.utils.test_text_processing', 'TestTextProcessing'))
        if args.parallel:
            test_cases.append(import_test_class('tests.test_parallel_transcription', 'ParallelTranscriptionTest'))
        if args.sequential:
            test_cases.append(import_test_class('tests.test_sequential_transcription', 'SequentialTranscriptionTest'))
        if args.gui:
            gui_modules = [
                ('tests.frontend.test_wortweber_gui', 'TestWordweberGUI'),
                ('tests.frontend.test_main_window', 'TestMainWindow')
            ]
            for module_path, class_name in gui_modules:
                test_cases.append(import_test_class(module_path, class_name))
        if args.error:
            test_cases.append(import_test_class('tests.test_error_handling', 'TestErrorHandling'))

    results = parallel_test_execution(test_cases)

    total_tests = 0
    total_failures = 0
    total_errors = 0

    print("\nTest Ergebnisse:")
    print("----------------")
    for test_name, result in results:
        tests_run = result.testsRun
        failures = len(result.failures)
        errors = len(result.errors)
        total_tests += tests_run
        total_failures += failures
        total_errors += errors

        status = "PASSED" if failures == 0 and errors == 0 else "FAILED"
        color = "green" if status == "PASSED" else "red"
        print(f"{test_name}: {colored(status, color)} (Tests: {tests_run}, Failures: {failures}, Errors: {errors})")

    print("\nTest Summary:")
    print(f"Ran {total_tests} tests")
    successes = total_tests - total_failures - total_errors
    print(f"Successes: {max(0, successes)}")  # Verwende max(), um negative Werte zu vermeiden
    print(f"Failures: {total_failures}")
    print(f"Errors: {total_errors}")


    if total_failures > 0 or total_errors > 0:
        sys.exit(1)

# Zusätzliche Erklärungen:
#
# 1. Dynamische Importe:
#    Statt alle Testklassen am Anfang zu importieren, werden sie nun dynamisch
#    geladen, basierend auf den ausgewählten Testoptionen. Dies verhindert
#    unnötige Importe und potenzielle Konflikte.
#
# 2. Modularität:
#    Die Testmodule sind nun in Listen organisiert, was die Wartung und
#    Erweiterung erleichtert.
#
# 3. Flexibilität:
#    Diese Struktur ermöglicht es, nur die tatsächlich benötigten Tests zu laden
#    und auszuführen, was die Effizienz und Fehlertoleranz erhöht.
#
# 4. Fehlerbehandlung:
#    Durch die dynamischen Importe werden Fehler bei nicht vorhandenen Modulen
#    vermieden, wenn bestimmte Testbereiche nicht ausgeführt werden sollen.
