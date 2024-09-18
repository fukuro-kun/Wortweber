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
from unittest.mock import MagicMock, patch
from tkinter import StringVar, Tk
from src.frontend.options_panel import OptionsPanel
from src.config import SUPPORTED_LANGUAGES, WHISPER_MODELS, DEFAULT_LANGUAGE, DEFAULT_WHISPER_MODEL
from termcolor import colored

class TestOptionsPanel(unittest.TestCase):
    """
    Testklasse für das OptionsPanel.
    Überprüft die korrekte Initialisierung und Funktionalität der Optionen.
    """

    def setUp(self):
        """Initialisiert die Testumgebung vor jedem Testfall."""
        self.root = Tk()
        self.gui_mock = MagicMock()
        self.options_panel = OptionsPanel(self.root, self.gui_mock)

    def tearDown(self):
        """Räumt die Testumgebung nach jedem Testfall auf."""
        self.root.destroy()

    def test_options_panel_initialization(self):
        """Testet die korrekte Initialisierung des OptionsPanels."""
        self.assertIsInstance(self.options_panel.language_var, StringVar)
        self.assertIsInstance(self.options_panel.model_var, StringVar)
        self.assertIsInstance(self.options_panel.input_mode_var, StringVar)
        self.assertIsInstance(self.options_panel.delay_mode_var, StringVar)
        print(colored("OptionsPanel wurde erfolgreich initialisiert.", "green"))

    def test_language_options(self):
        """Überprüft, ob alle unterstützten Sprachen korrekt geladen werden."""
        for lang_code in SUPPORTED_LANGUAGES:
            self.assertIn(lang_code, self.options_panel.language_var.get())
        print(colored("Sprachoptionen wurden erfolgreich geladen.", "green"))

    def test_model_options(self):
        """Überprüft, ob alle Whisper-Modelle korrekt geladen werden."""
        for model in WHISPER_MODELS:
            self.assertIn(model, self.options_panel.model_var.get())
        print(colored("Modelloptionen wurden erfolgreich geladen.", "green"))

    @patch('src.frontend.options_panel.OptionsPanel.on_language_change')
    def test_language_change(self, mock_on_language_change):
        """Testet die Reaktion auf Sprachänderungen."""
        self.options_panel.language_var.set('en')
        mock_on_language_change.assert_called_once()
        print(colored("Sprachänderung wurde erfolgreich getestet.", "green"))

    @patch('src.frontend.options_panel.OptionsPanel.on_model_change')
    def test_model_change(self, mock_on_model_change):
        """Testet die Reaktion auf Modelländerungen."""
        self.options_panel.model_var.set('medium')
        mock_on_model_change.assert_called_once()
        print(colored("Modelländerung wurde erfolgreich getestet.", "green"))

    def test_input_mode_change(self):
        """Testet die Änderung des Eingabemodus."""
        with patch.object(self.options_panel, 'toggle_delay_options') as mock_toggle:
            self.options_panel.on_input_mode_change()
            self.gui_mock.settings_manager.set_setting.assert_called_with("input_mode", self.options_panel.input_mode_var.get())
            self.gui_mock.settings_manager.save_settings.assert_called_once()
            mock_toggle.assert_called_once()
        print(colored("Änderung des Eingabemodus wurde erfolgreich getestet.", "green"))

    def test_delay_mode_change(self):
        """Testet die Änderung des Verzögerungsmodus."""
        self.options_panel.on_delay_mode_change()
        self.gui_mock.settings_manager.set_setting.assert_called_with("delay_mode", self.options_panel.delay_mode_var.get())
        self.gui_mock.settings_manager.save_settings.assert_called_once()
        print(colored("Änderung des Verzögerungsmodus wurde erfolgreich getestet.", "green"))

    def test_char_delay_change(self):
        """Testet die Änderung der Zeichenverzögerung."""
        self.options_panel.on_char_delay_change()
        self.gui_mock.settings_manager.set_setting.assert_called_with("char_delay", self.options_panel.char_delay_entry.get())
        self.gui_mock.settings_manager.save_settings.assert_called_once()
        print(colored("Änderung der Zeichenverzögerung wurde erfolgreich getestet.", "green"))

    def test_toggle_delay_options(self):
        """Testet das Ein- und Ausblenden der Verzögerungsoptionen."""
        self.options_panel.input_mode_var.set("textfenster")
        self.options_panel.toggle_delay_options()
        self.assertFalse(self.options_panel.delay_frame.winfo_ismapped())

        self.options_panel.input_mode_var.set("systemcursor")
        self.options_panel.toggle_delay_options()
        self.assertTrue(self.options_panel.delay_frame.winfo_ismapped())
        print(colored("Ein- und Ausblenden der Verzögerungsoptionen wurde erfolgreich getestet.", "green"))

if __name__ == '__main__':
    unittest.main()
