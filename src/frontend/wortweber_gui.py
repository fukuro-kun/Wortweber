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
from src.frontend.status_panel import StatusPanel
from src.frontend.theme_manager import ThemeManager
from src.frontend.input_processor import InputProcessor
from src.frontend.settings_manager import SettingsManager

class WordweberGUI:
    def __init__(self, backend: WordweberBackend):
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
            self.root.geometry("800x600")

        self.theme_manager = ThemeManager(self.root, self.settings_manager)
        self.input_processor = InputProcessor(self)

        self.main_window = MainWindow(self.root, self)
        self.transcription_panel = self.main_window.transcription_panel
        self.options_panel = self.main_window.options_panel
        self.status_panel = self.main_window.status_panel

        self.setup_logging()
        self.load_saved_settings()
        self.load_initial_model()

        # Hinzufügen eines Event-Handlers für Größenänderungen
        self.root.bind("<Configure>", self.on_window_configure)

    def setup_logging(self):
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.debug("WordweberGUI initialisiert")

    def load_saved_settings(self):
        self.theme_manager.apply_saved_theme()

    def load_initial_model(self):
        model_name = self.settings_manager.get_setting("model")
        self.load_model_async(model_name)

    def load_model_async(self, model_name: str):
        self.status_panel.update_status("Lade Modell...", "blue")
        threading.Thread(target=self._load_model_thread, args=(model_name,), daemon=True).start()

    def _load_model_thread(self, model_name: str):
        self.backend.load_transcriber_model(model_name)
        self.status_panel.update_status("Modell geladen", "green")
        if self.backend.pending_audio:
            self.status_panel.update_status("Verarbeite zurückgehaltene Aufnahmen...", "orange")
            self.transcribe_and_update()

    def run(self):
        logging.debug("Starte Anwendung")
        self.input_processor.start_listener()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def on_closing(self):
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

    def on_window_configure(self, event):
        if event.widget == self.root:
            self.settings_manager.set_setting("window_geometry", self.root.geometry())
            self.settings_manager.save_settings()

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
        try:
            start_time = time.time()
            text = self.backend.process_and_transcribe(self.options_panel.language_var.get())
            transcription_time = time.time() - start_time
            if text:
                self.input_processor.process_text(text)
                self.status_panel.update_transcription_timer(transcription_time)
                if "[Transkription fehlgeschlagen]" in text:
                    self.status_panel.update_status("Teilweise Transkription fehlgeschlagen", "orange")
                else:
                    self.status_panel.update_status("Text transkribiert", "green")
            else:
                self.status_panel.update_status("Keine Transkription verfügbar", "red")
        except Exception as e:
            self.status_panel.update_status(f"Fehler bei der Transkription: {str(e)}", "red")
        logging.info(f"Transkription abgeschlossen. Text: {text}")

if __name__ == "__main__":
    backend = WordweberBackend()
    gui = WordweberGUI(backend)
    gui.run()
