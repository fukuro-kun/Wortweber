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

import unittest
from unittest.mock import MagicMock, patch
from tkinter import Tk
from src.frontend.status_panel import StatusPanel
from termcolor import colored
import sys
from io import StringIO

# Zusätzliche Erklärungen:
# 1. Wir verwenden StringIO, um die Standardausgabe zu erfassen und zu überprüfen.
# 2. Die print-Anweisungen mit colored() geben farbige Ausgaben für erfolgreiche Tests.
# 3. Jeder Test hat nun eine klare, farbige Nachricht, die den Erfolg anzeigt.
# 4. Die Kommentare folgen den Projektrichtlinien für einheitliche Dokumentation.

# Funktion zum Erfassen der Standardausgabe
def capture_output(func):
    """
    Dekorator zum Erfassen der Standardausgabe einer Funktion.

    :param func: Die zu dekorierende Funktion
    :return: Die dekorierte Funktion
    """
    def wrapper(*args, **kwargs):
        captured_output = StringIO()
        sys.stdout = captured_output
        func(*args, **kwargs)
        sys.stdout = sys.__stdout__
        return captured_output.getvalue()
    return wrapper

class TestStatusPanel(unittest.TestCase):

    def setUp(self):
        self.root = Tk()
        self.gui_mock = MagicMock()
        self.status_panel = StatusPanel(self.root, self.gui_mock)

    def tearDown(self):
        self.root.destroy()

    @capture_output
    def test_status_panel_initialization(self):
        self.assertIsNotNone(self.status_panel.timer_var)
        self.assertIsNotNone(self.status_panel.transcription_timer_var)
        self.assertIsNotNone(self.status_panel.auto_copy_var)
        self.assertIsNotNone(self.status_panel.status_var)
        print(colored("StatusPanel erfolgreich initialisiert.", "green"))

    @capture_output
    def test_update_status(self):
        message = "Test status"
        color = "red"
        self.status_panel.update_status(message, color)
        self.assertEqual(self.status_panel.status_var.get(), message)
        self.assertEqual(self.status_panel.status_label.cget("foreground"), color)
        print(colored("Status-Update erfolgreich getestet.", "green"))

    @capture_output
    def test_update_timer(self):
        elapsed_time = 10.5
        self.status_panel.update_timer(elapsed_time)
        self.assertEqual(self.status_panel.timer_var.get(), f"Aufnahmezeit: {elapsed_time:.1f} s")
        print(colored("Timer-Update erfolgreich getestet.", "green"))

    @capture_output
    def test_update_transcription_timer(self):
        transcription_time = 5.25
        self.status_panel.update_transcription_timer(transcription_time)
        self.assertEqual(self.status_panel.transcription_timer_var.get(), f"Transkriptionszeit: {transcription_time:.2f} s")
        print(colored("Transkriptions-Timer-Update erfolgreich getestet.", "green"))

    @capture_output
    def test_reset_timer(self):
        self.status_panel.reset_timer()
        self.assertEqual(self.status_panel.timer_var.get(), "Aufnahmezeit: 0.0 s")
        print(colored("Timer-Reset erfolgreich getestet.", "green"))

    @patch('src.frontend.status_panel.DEFAULT_INCOGNITO_MODE', False)
    @capture_output
    def test_auto_copy_checkbox(self):
        self.gui_mock.settings_manager.get_setting.return_value = True
        self.status_panel.setup_ui()
        self.assertTrue(self.status_panel.auto_copy_var.get())
        print(colored("Auto-Copy-Checkbox im normalen Modus erfolgreich getestet.", "green"))

    @patch('src.frontend.status_panel.DEFAULT_INCOGNITO_MODE', True)
    @capture_output
    def test_auto_copy_checkbox_incognito(self):
        self.gui_mock.settings_manager.get_setting.return_value = False
        self.status_panel.setup_ui()
        self.assertFalse(self.status_panel.auto_copy_var.get())
        print(colored("Auto-Copy-Checkbox im Incognito-Modus erfolgreich getestet.", "green"))

if __name__ == '__main__':
    unittest.main()
