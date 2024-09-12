import tkinter as tk
from tkinter import ttk
import ttkthemes
import time
import logging
from src.backend.wortweber_backend import WordweberBackend
from src.frontend.main_window import MainWindow
from src.frontend.transcription_panel import TranscriptionPanel
from src.frontend.options_panel import OptionsPanel
from src.frontend.status_panel import StatusPanel
from src.frontend.theme_manager import ThemeManager
from src.frontend.input_processor import InputProcessor
from src.frontend.settings_manager import SettingsManager

class WordweberGUI:
    def __init__(self, backend: WordweberBackend):
        self.backend = backend
        self.root = ttkthemes.ThemedTk()
        self.root.title("Wortweber Transkription")

        self.settings_manager = SettingsManager()
        self.theme_manager = ThemeManager(self.root, self.settings_manager)
        self.input_processor = InputProcessor(self)

        self.main_window = MainWindow(self.root, self)
        self.transcription_panel = self.main_window.transcription_panel
        self.options_panel = self.main_window.options_panel
        self.status_panel = self.main_window.status_panel

        self.setup_logging()
        self.load_saved_settings()

    def setup_logging(self):
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.debug("WordweberGUI initialisiert")

    def load_saved_settings(self):
        window_size = self.settings_manager.get_setting("window_size")
        self.root.geometry(window_size)
        self.theme_manager.apply_saved_theme()

    def run(self):
        logging.debug("Starte Anwendung")
        self.input_processor.start_listener()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def on_closing(self):
        logging.debug("Anwendung wird geschlossen")
        self.settings_manager.set_setting("window_size", self.root.geometry())
        self.input_processor.stop_listener()
        if self.backend.transcriber.model is not None:
            del self.backend.transcriber.model
        self.root.destroy()

    def start_timer(self):
        self.start_time = time.time()
        self.update_timer()

    def stop_timer(self):
        self.status_panel.reset_timer()

    def update_timer(self):
        if self.backend.state.recording:
            elapsed_time = time.time() - self.start_time
            self.status_panel.update_timer(elapsed_time)
            self.root.after(100, self.update_timer)

    def transcribe_and_update(self):
        self.status_panel.update_status("Transkribiere...", "orange")
        text = self.backend.process_and_transcribe(self.options_panel.language_var.get())
        self.input_processor.process_text(text)
        self.status_panel.update_transcription_timer(self.backend.state.transcription_time)

    def load_model(self, model_name: str):
        self.status_panel.update_status("Lade Modell...", "blue")
        self.backend.load_transcriber_model(model_name)
        self.status_panel.update_status("Modell geladen", "green")

if __name__ == "__main__":
    backend = WordweberBackend()
    gui = WordweberGUI(backend)
    gui.run()
