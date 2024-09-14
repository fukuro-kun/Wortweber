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

# src/frontend/wortweber_gui.py

import tkinter as tk
from tkinter import ttk
import ttkthemes
import time
import logging
import threading
from src.backend.wortweber_backend import WordweberBackend
from src.frontend.main_window import MainWindow
from src.frontend.transcription_panel import TranscriptionPanel
from src.frontend.options_panel import OptionsPanel
from src.frontend.options_window import OptionsWindow
from src.frontend.status_panel import StatusPanel
from src.frontend.theme_manager import ThemeManager
from src.frontend.input_processor import InputProcessor
from src.frontend.settings_manager import SettingsManager
from src.config import DEFAULT_WINDOW_SIZE

class WordweberGUI:
    """
    Hauptklasse für die grafische Benutzeroberfläche der Wortweber-Anwendung.
    Koordiniert die verschiedenen UI-Komponenten und die Interaktion mit dem Backend.
    """

    def __init__(self, backend: WordweberBackend):
        """
        Initialisiert die GUI der Wortweber-Anwendung.

        :param backend: Eine Instanz der WordweberBackend-Klasse
        """
        self.backend = backend
        self.settings_manager = SettingsManager()

        self.root = ttkthemes.ThemedTk()
        self.root.title("Wortweber Transkription")

        # Laden der gespeicherten Fenstergeometrie
        saved_geometry = self.settings_manager.get_setting("window_geometry")
        if saved_geometry:
            self.root.geometry(saved_geometry)
        else:
            # Standardgröße, falls keine gespeicherte Geometrie vorhanden ist
            self.root.geometry(DEFAULT_WINDOW_SIZE)

        self.theme_manager = ThemeManager(self.root, self.settings_manager)
        self.input_processor = InputProcessor(self)

        self.main_window = MainWindow(self.root, self)
        self.transcription_panel = self.main_window.transcription_panel
        self.options_panel = self.main_window.options_panel
        self.status_panel = self.main_window.status_panel

        self.theme_manager.set_gui(self)

        self.setup_logging()
        self.load_saved_settings()
        self.load_initial_model()

        # Hinzufügen eines Event-Handlers für Größenänderungen
        self.root.bind("<Configure>", self.on_window_configure)

    def setup_logging(self):
        """Konfiguriert das Logging für die Anwendung."""
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.debug("WordweberGUI initialisiert")

    def load_saved_settings(self):
        """Lädt und wendet gespeicherte Einstellungen an."""
        self.theme_manager.apply_saved_theme()

    def load_initial_model(self):
        """Lädt das initial konfigurierte Whisper-Modell."""
        model_name = self.settings_manager.get_setting("model")
        self.load_model_async(model_name)

    def load_model_async(self, model_name: str):
        """
        Lädt das Whisper-Modell asynchron.

        :param model_name: Name des zu ladenden Modells
        """
        self.status_panel.update_status("Lade Modell...", "blue")
        threading.Thread(target=self._load_model_thread, args=(model_name,), daemon=True).start()

    def _load_model_thread(self, model_name: str):
        """
        Thread-Funktion zum Laden des Whisper-Modells.

        :param model_name: Name des zu ladenden Modells
        """
        self.backend.load_transcriber_model(model_name)
        self.status_panel.update_status("Modell geladen", "green")
        if self.backend.pending_audio:
            self.transcribe_and_update()

    def run(self):
        """Startet die Hauptschleife der GUI."""
        logging.debug("Starte Anwendung")
        self.input_processor.start_listener()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def on_closing(self):
        """Wird aufgerufen, wenn das Anwendungsfenster geschlossen wird."""
        logging.debug("Anwendung wird geschlossen")
        self.settings_manager.set_setting("window_geometry", self.root.geometry())
        self.settings_manager.set_setting("input_mode", self.options_panel.input_mode_var.get())
        self.settings_manager.set_setting("delay_mode", self.options_panel.delay_mode_var.get())
        self.settings_manager.set_setting("char_delay", self.options_panel.char_delay_entry.get())
        self.settings_manager.save_settings()
        self.input_processor.stop_listener()
        if self.backend.transcriber.model is not None:
            del self.backend.transcriber.model
        self.root.destroy()

    def open_options_window(self):
        """Öffnet das Fenster für erweiterte Optionen."""
        OptionsWindow.open_window(self.root, self.theme_manager, self.transcription_panel, self)

    def on_window_configure(self, event):
        """
        Wird aufgerufen, wenn sich die Fenstergröße ändert.
        Speichert die neue Fenstergröße in den Einstellungen.

        :param event: Das Konfigurationsereignis
        """
        if event.widget == self.root:
            self.settings_manager.set_setting("window_geometry", self.root.geometry())
            self.settings_manager.save_settings()

    def start_timer(self):
        """Startet den Timer für die Aufnahmedauer."""
        self.start_time = time.time()
        self.update_timer()

    def stop_timer(self):
        """Stoppt den Timer für die Aufnahmedauer."""
        self.status_panel.reset_timer()

    def update_timer(self):
        """Aktualisiert die Anzeige der Aufnahmedauer."""
        if self.backend.state.recording:
            elapsed_time = time.time() - self.start_time
            self.status_panel.update_timer(elapsed_time)
            self.root.after(100, self.update_timer)

    def transcribe_and_update(self):
        """Führt die Transkription durch und aktualisiert die GUI."""
        self.status_panel.update_status("Transkribiere...", "orange")
        start_time = time.time()
        text = self.backend.process_and_transcribe(self.options_panel.language_var.get())
        transcription_time = time.time() - start_time
        self.input_processor.process_text(text)
        self.status_panel.update_transcription_timer(transcription_time)

        # Speichern der Testaufnahme, wenn aktiviert
        if self.settings_manager.get_setting("save_test_recording", False):
            self.backend.audio_processor.save_last_recording()

    def update_colors(self):
        """
        Aktualisiert die Farben im Transkriptionsfenster und anderen relevanten UI-Elementen.
        """
        self.transcription_panel.update_colors(
            text_fg=self.theme_manager.text_fg.get(),
            text_bg=self.theme_manager.text_bg.get(),
            select_fg=self.theme_manager.select_fg.get(),
            select_bg=self.theme_manager.select_bg.get(),
            highlight_fg=self.theme_manager.highlight_fg.get(),
            highlight_bg=self.theme_manager.highlight_bg.get()
        )

# Zusätzliche Erklärungen:

# 1. Die WordweberGUI-Klasse ist der zentrale Punkt für die Verwaltung der Benutzeroberfläche.
# 2. Sie koordiniert die Interaktionen zwischen verschiedenen UI-Komponenten und dem Backend.
# 3. Die Methode update_colors wurde hinzugefügt, um die Farbänderungen im Transkriptionsfenster zu aktualisieren.
# 4. Die Initialisierung des ThemeManagers wurde angepasst, um die GUI-Referenz zu setzen.
# 5. Verschiedene Event-Handler und Timer-Funktionen steuern das dynamische Verhalten der Anwendung.
# 6. Die Methoden zum Laden des Modells und zur Transkription sind asynchron, um die GUI reaktiv zu halten.
