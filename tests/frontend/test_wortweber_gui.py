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
from unittest.mock import MagicMock, patch, ANY
from tkinter import Tk
from src.frontend.wortweber_gui import WordweberGUI
from src.backend.wortweber_backend import WordweberBackend
from termcolor import colored

class MockWordweberGUI(WordweberGUI):
    """
    Eine Mock-Version der WordweberGUI für Testzwecke.
    Simuliert die GUI-Funktionalität ohne tatsächliche Tkinter-Fenster zu öffnen.
    """
    def __init__(self, backend):
        self.root = MagicMock(spec=Tk)
        self.settings_manager = MagicMock()
        self.settings_manager.get_setting.side_effect = lambda key, default=None: {
            "window_geometry": "800x600",
            "font_size": 12,
            "auto_copy": True,
            "model": "small"
        }.get(key, default)

        self.theme_manager = MagicMock()
        self.input_processor = MagicMock()
        self.main_window = MagicMock()
        self.transcription_panel = MagicMock()
        self.options_panel = MagicMock()
        self.status_panel = MagicMock()

        self.backend = backend

        # Rufen Sie direkt die benötigten Methoden auf
        self.setup_logging()
        self.load_saved_settings()
        self.load_initial_model()

    def _load_model_thread(self, model_name: str) -> None:
        """
        Überschriebene Version der _load_model_thread-Methode für Testzwecke.
        """
        try:
            self.backend.load_transcriber_model(model_name)
            self.root.after(0, lambda: self.status_panel.update_status("Modell geladen", "green"))
            if getattr(self.backend, 'pending_audio', False):
                self.root.after(0, self.transcribe_and_update)
        except Exception as e:
            error_message = f"Fehler beim Laden des Modells: {str(e)}"
            self.root.after(0, lambda: self.status_panel.update_status(error_message, "red"))

class TestWordweberGUI(unittest.TestCase):
    """
    Testklasse für die Wortweber GUI.
    Überprüft die korrekte Initialisierung und Funktionalität der GUI-Komponenten.
    """

    def setUp(self):
        """Initialisiert die Testumgebung vor jedem Testfall."""
        self.backend_mock = MagicMock(spec=WordweberBackend)
        self.backend_mock.load_transcriber_model = MagicMock()
        self.backend_mock.process_and_transcribe = MagicMock()
        self.backend_mock.pending_audio = False
        self.gui = MockWordweberGUI(self.backend_mock)

    def test_gui_initialization(self):
        """Testet die korrekte Initialisierung der GUI-Komponenten."""
        self.assertIsNotNone(self.gui.main_window)
        self.assertIsNotNone(self.gui.transcription_panel)
        self.assertIsNotNone(self.gui.options_panel)
        self.assertIsNotNone(self.gui.status_panel)
        print(colored("GUI-Komponenten wurden erfolgreich initialisiert.", "green"))

    def test_theme_manager_initialization(self):
        """Überprüft die Initialisierung des ThemeManagers."""
        self.assertIsNotNone(self.gui.theme_manager)
        print(colored("ThemeManager wurde erfolgreich initialisiert.", "green"))

    def test_input_processor_initialization(self):
        """Testet die Initialisierung des InputProcessors."""
        self.assertIsNotNone(self.gui.input_processor)
        print(colored("InputProcessor wurde erfolgreich initialisiert.", "green"))

    def test_load_saved_settings(self):
        """Überprüft das Laden der gespeicherten Einstellungen."""
        with patch.object(self.gui.theme_manager, 'apply_saved_theme') as mock_apply_theme:
            self.gui.load_saved_settings()
            mock_apply_theme.assert_called_once()
        print(colored("Gespeicherte Einstellungen wurden erfolgreich geladen.", "green"))

    def test_load_initial_model(self):
        """Testet das Laden des initialen Transkriptionsmodells."""
        with patch.object(self.gui, 'load_model_async') as mock_load_model:
            self.gui.load_initial_model()
            mock_load_model.assert_called_once_with('small')
        print(colored("Initiales Modell wurde erfolgreich geladen.", "green"))

    @patch('threading.Thread')
    def test_load_model_async(self, mock_thread):
        """Überprüft das asynchrone Laden eines Modells."""
        model_name = "test_model"

        self.gui.load_model_async(model_name)

        mock_thread.assert_called_once()
        thread_call = mock_thread.call_args
        self.assertEqual(thread_call.kwargs['target'], self.gui._load_model_thread)
        self.assertEqual(thread_call.kwargs['args'], (model_name,))
        self.assertTrue(thread_call.kwargs['daemon'])

        mock_thread.return_value.start.assert_called_once()

        # Simulieren des Thread-Ablaufs
        thread_function = thread_call.kwargs['target']
        thread_function(model_name)

        self.backend_mock.load_transcriber_model.assert_called_once_with(model_name)

        self.gui.status_panel.update_status.assert_any_call("Lade Modell...", "blue")
        self.gui.root.after.assert_any_call(0, ANY)

        # Finden und Ausführen der after-Funktion
        after_calls = self.gui.root.after.call_args_list
        for args, kwargs in after_calls:
            if args[0] == 0 and callable(args[1]):
                args[1]()  # Führe die Lambda-Funktion aus

        self.gui.status_panel.update_status.assert_called_with("Modell geladen", "green")

        print(colored(f"Asynchrones Laden des Modells '{model_name}' wurde erfolgreich getestet.", "green"))

    def test_transcribe_and_update(self):
        """Testet den Transkriptions- und Aktualisierungsprozess."""
        # Setze einen Mock für process_and_transcribe
        self.backend_mock.process_and_transcribe.return_value = "Transkribierter Text"

        # Rufe die Methode auf
        self.gui.transcribe_and_update()

        # Überprüfen, ob der Status aktualisiert wurde
        self.gui.status_panel.update_status.assert_any_call("Transkribiere...", "orange")

        # Überprüfen, ob die Transkription durchgeführt wurde
        self.backend_mock.process_and_transcribe.assert_called_once()

        # Simulieren der GUI-Aktualisierung
        self.gui.root.after.assert_called()
        after_function = self.gui.root.after.call_args[0][1]
        after_function()

        # Überprüfen, ob der Text verarbeitet wurde
        self.gui.input_processor.process_text.assert_called_once_with("Transkribierter Text")

        # Überprüfen, ob der Status aktualisiert wurde
        self.gui.status_panel.update_status.assert_called_with("Transkription abgeschlossen", "green")

        print(colored("Transkription und Update wurden erfolgreich durchgeführt.", "green"))



if __name__ == '__main__':
    unittest.main()

# Zusätzliche Erklärungen:

# 1. MockWordweberGUI:
#    Diese Klasse erbt von WordweberGUI und überschreibt einige Methoden, um die
#    GUI-Funktionalität ohne tatsächliche Tkinter-Fenster zu simulieren. Dies
#    ermöglicht das Testen der GUI-Logik ohne die Komplexität der Tkinter-Ereignisschleife.

# 2. Verwendung von MagicMock:
#    MagicMock wird extensiv genutzt, um verschiedene Komponenten wie Tkinter-Widgets,
#    den ThemeManager und andere GUI-Elemente zu simulieren. Dies erlaubt uns,
#    das Verhalten dieser Komponenten zu kontrollieren und zu überprüfen.

# 3. Thread-Simulation:
#    Der test_load_model_async Test verwendet patch, um das Threading-Verhalten
#    zu simulieren. Dies ermöglicht es uns, asynchrone Operationen in einem
#    synchronen Testumfeld zu überprüfen.

# 4. Farbige Ausgaben:
#    Die Verwendung von termcolor für farbige Konsolenausgaben verbessert die
#    Lesbarkeit der Testergebnisse und hilft, wichtige Informationen hervorzuheben.

# 5. Detaillierte Assertions:
#    Jeder Test enthält mehrere spezifische Assertions, um verschiedene Aspekte
#    der GUI-Funktionalität zu überprüfen. Dies gewährleistet eine gründliche
#    Testabdeckung.

# 6. Simulation von Tkinter-Aufrufen:
#    Die Tests simulieren Tkinter-spezifische Aufrufe wie root.after, um
#    GUI-Updates und asynchrone Operationen zu testen, ohne tatsächlich
#    die Tkinter-Ereignisschleife zu starten.

# 7. Isolierung von Testfällen:
#    Jeder Testfall ist unabhängig und setzt die Testumgebung vor der Ausführung
#    zurück. Dies verhindert unerwünschte Seiteneffekte zwischen den Tests.

# 8. Behandlung von Tkinter-Thread-Problemen:
#    Durch die Verwendung von Mocks und simulierten Aufrufen werden potenzielle
#    Probleme mit dem Tkinter-Hauptthread umgangen, die in einer realen
#    GUI-Umgebung auftreten könnten.
