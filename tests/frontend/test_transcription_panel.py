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



from termcolor import colored
import unittest
from unittest.mock import MagicMock, patch
from tkinter import Tk
from src.frontend.transcription_panel import TranscriptionPanel

class TestTranscriptionPanel(unittest.TestCase):

    def setUp(self):
        self.root = Tk()
        self.gui_mock = MagicMock()
        self.transcription_panel = TranscriptionPanel(self.root, self.gui_mock)

    def tearDown(self):
        self.root.destroy()

    def test_transcription_panel_initialization(self):
        self.assertIsNotNone(self.transcription_panel.text_widget)
        self.assertEqual(self.transcription_panel.font_size, self.gui_mock.settings_manager.get_setting.return_value)
        self.assertEqual(self.transcription_panel.font_family, self.gui_mock.settings_manager.get_setting.return_value)
        print(colored("TranscriptionPanel wurde erfolgreich initialisiert.", "green"))

    def test_set_font(self):
        test_family = "Arial"
        test_size = 14
        self.transcription_panel.set_font(test_family, test_size)
        self.assertEqual(self.transcription_panel.font_family, test_family)
        self.assertEqual(self.transcription_panel.font_size, test_size)
        self.gui_mock.settings_manager.set_setting.assert_any_call("font_family", test_family)
        self.gui_mock.settings_manager.set_setting.assert_any_call("font_size", test_size)
        print(colored(f"Schriftart wurde erfolgreich auf {test_family}, Größe {test_size} gesetzt.", "green"))

    def test_insert_text(self):
        test_text = "Test Transkription"
        self.transcription_panel.insert_text(test_text)
        inserted_text = self.transcription_panel.text_widget.get("1.0", "end-1c")
        self.assertIn(test_text, inserted_text)
        print(colored(f"Text '{test_text}' wurde erfolgreich eingefügt.", "green"))

    def test_clear_transcription(self):
        self.transcription_panel.insert_text("Some text")
        self.transcription_panel.clear_transcription()
        self.assertEqual(self.transcription_panel.text_widget.get("1.0", "end-1c"), "")
        print(colored("Transkription wurde erfolgreich gelöscht.", "green"))

    @patch('pyperclip.copy')
    def test_copy_all_to_clipboard(self, mock_copy):
        test_text = "Test Clipboard"
        self.transcription_panel.insert_text(test_text)
        self.transcription_panel.copy_all_to_clipboard()
        mock_copy.assert_called_with(test_text + "\n")
        print(colored("Gesamter Text wurde erfolgreich in die Zwischenablage kopiert.", "green"))

    def test_update_colors(self):
        test_colors = {
            "text_fg": "black",
            "text_bg": "white",
            "select_fg": "white",
            "select_bg": "blue",
            "highlight_fg": "red",
            "highlight_bg": "yellow"
        }
        self.transcription_panel.update_colors(**test_colors)
        self.assertEqual(self.transcription_panel.text_widget.cget("fg"), test_colors["text_fg"])
        self.assertEqual(self.transcription_panel.text_widget.cget("bg"), test_colors["text_bg"])
        self.assertEqual(self.transcription_panel.text_widget.cget("selectforeground"), test_colors["select_fg"])
        self.assertEqual(self.transcription_panel.text_widget.cget("selectbackground"), test_colors["select_bg"])
        print(colored("Farben wurden erfolgreich aktualisiert.", "green"))

if __name__ == '__main__':
    unittest.main()
