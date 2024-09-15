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
from tkinter import Tk, ttk
from src.frontend.main_window import MainWindow
from termcolor import colored

class TestMainWindow(unittest.TestCase):
    """
    Testklasse für das MainWindow der Wortweber-Anwendung.
    Überprüft die korrekte Initialisierung und Funktionalität der Hauptfenster-Komponenten.
    """

    def setUp(self):
        """Initialisiert die Testumgebung vor jedem Testfall."""
        self.root = Tk()
        self.gui_mock = MagicMock()
        self.gui_mock.settings_manager.get_setting.side_effect = lambda key, default=None: {
            "font_size": 12,
            "auto_copy": True
        }.get(key, default)
        self.main_window = MainWindow(self.root, self.gui_mock)

    def tearDown(self):
        """Räumt die Testumgebung nach jedem Testfall auf."""
        self.root.destroy()

    def test_main_window_initialization(self):
        """Testet die korrekte Initialisierung der Hauptfenster-Komponenten."""
        self.assertIsNotNone(self.main_window.transcription_panel)
        self.assertIsNotNone(self.main_window.options_panel)
        self.assertIsNotNone(self.main_window.status_panel)
        print(colored("MainWindow-Komponenten wurden erfolgreich initialisiert.", "green"))

    def test_setup_ui(self):
        """Überprüft die korrekte Erstellung der UI-Elemente."""
        self.assertIsInstance(self.main_window.transcription_panel, ttk.Frame)
        self.assertIsInstance(self.main_window.options_panel, ttk.Frame)
        self.assertIsInstance(self.main_window.status_panel, ttk.Frame)
        print(colored("UI-Setup wurde erfolgreich durchgeführt.", "green"))

    def test_open_options_window(self):
        """Testet das Öffnen des Optionsfensters."""
        with patch('src.frontend.main_window.OptionsWindow') as mock_options_window:
            self.main_window.open_options_window()
            mock_options_window.assert_called_once()
        print(colored("Optionsfenster wurde erfolgreich geöffnet.", "green"))

    def test_button_functionality(self):
        """Überprüft die Funktionalität der Hauptfenster-Buttons."""
        # Finden der Buttons im button_frame
        main_frame = self.main_window.root.children['!frame']
        button_frame = main_frame.children['!frame']
        clear_button = button_frame.children['!button']
        copy_button = button_frame.children['!button2']
        options_button = button_frame.children['!button3']
        quit_button = button_frame.children['!button4']

        # Testen des "Transkription löschen" Buttons
        with patch.object(self.main_window.transcription_panel, 'clear_transcription') as mock_clear:
            clear_button.invoke()
            mock_clear.assert_called_once()
        print(colored("'Transkription löschen'-Button funktioniert korrekt.", "green"))

        # Testen des "Alles kopieren" Buttons
        with patch.object(self.main_window.transcription_panel, 'copy_all_to_clipboard') as mock_copy:
            copy_button.invoke()
            mock_copy.assert_called_once()
        print(colored("'Alles kopieren'-Button funktioniert korrekt.", "green"))

        # Testen des "Erweiterte Optionen" Buttons
        with patch.object(self.main_window, 'open_options_window') as mock_open_options:
            options_button.invoke()
            mock_open_options.assert_called_once()
        print(colored("'Erweiterte Optionen'-Button funktioniert korrekt.", "green"))

        # Testen des "Beenden" Buttons
        with patch.object(self.main_window.root, 'quit') as mock_quit:
            quit_button.invoke()
            mock_quit.assert_called_once()
        print(colored("'Beenden'-Button funktioniert korrekt.", "green"))

    def test_grid_layout(self):
        """Testet die korrekte Anordnung des Hauptfenster-Layouts."""
        main_frame = self.main_window.root.children['!frame']

        # Überprüfen der Hauptframe-Konfiguration
        self.assertEqual(main_frame.grid_info()['row'], 0)
        self.assertEqual(main_frame.grid_info()['column'], 0)
        self.assertEqual(main_frame.grid_info()['sticky'], 'nsew')

        # Überprüfen der Panel-Positionen
        self.assertEqual(self.main_window.options_panel.grid_info()['row'], 0)
        self.assertEqual(self.main_window.options_panel.grid_info()['column'], 0)
        self.assertEqual(self.main_window.options_panel.grid_info()['sticky'], 'nw')

        self.assertEqual(self.main_window.status_panel.grid_info()['row'], 0)
        self.assertEqual(self.main_window.status_panel.grid_info()['column'], 1)
        self.assertEqual(self.main_window.status_panel.grid_info()['sticky'], 'ne')

        self.assertEqual(self.main_window.transcription_panel.grid_info()['row'], 1)
        self.assertEqual(self.main_window.transcription_panel.grid_info()['column'], 0)
        self.assertEqual(self.main_window.transcription_panel.grid_info()['columnspan'], 2)
        self.assertEqual(self.main_window.transcription_panel.grid_info()['sticky'], 'nsew')

        print(colored("Grid-Layout des Hauptfensters ist korrekt konfiguriert.", "green"))

if __name__ == '__main__':
    unittest.main()

# Zusätzliche Erklärungen:

# 1. Die Tests wurden an die tatsächliche Implementierung in main_window.py angepasst.
# 2. Der test_button_functionality-Test wurde erweitert, um alle Buttons im button_frame zu überprüfen.
# 3. Der test_grid_layout-Test wurde hinzugefügt, um die korrekte Positionierung aller UI-Elemente zu überprüfen.
# 4. Die Verwendung von patch ermöglicht es, das Verhalten von Methoden zu simulieren, ohne die tatsächliche Funktionalität auszuführen.
# 5. Farbige Konsolenausgaben wurden beibehalten, um die Lesbarkeit der Testergebnisse zu verbessern.
# 6. Die Tests decken nun besser die verschiedenen Aspekte der MainWindow-Funktionalität ab, einschließlich Button-Funktionen und Layout.
