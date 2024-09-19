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

"""
Dieses Modul enthält die Hauptklasse für die grafische Benutzeroberfläche der Wortweber-Anwendung.
Es koordiniert die verschiedenen UI-Komponenten und die Interaktion mit dem Backend.
"""

# Standardbibliotheken
import tkinter as tk
import time
import logging
import threading
from typing import Optional

# Drittanbieterbibliotheken
import ttkthemes

# Projektspezifische Module
from src.backend.wortweber_backend import WordweberBackend
from src.frontend.main_window import MainWindow
from src.frontend.transcription_panel import TranscriptionPanel
from src.frontend.options_panel import OptionsPanel
from src.frontend.options_window import OptionsWindow
from src.frontend.theme_manager import ThemeManager
from src.frontend.input_processor import InputProcessor
from src.frontend.settings_manager import SettingsManager
from src.config import DEFAULT_WINDOW_SIZE
from src.utils.error_handling import handle_exceptions

class WordweberGUI:
    """
    Hauptklasse für die grafische Benutzeroberfläche der Wortweber-Anwendung.
    Koordiniert die verschiedenen UI-Komponenten und die Interaktion mit dem Backend.
    """

    @handle_exceptions
    def __init__(self, backend: WordweberBackend) -> None:
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
            try:
                self.root.geometry(saved_geometry)
            except tk.TclError:
                # Wenn die gespeicherte Geometrie ungültig ist, verwenden wir die Standardgröße
                self.root.geometry(DEFAULT_WINDOW_SIZE)
        else:
            self.root.geometry(DEFAULT_WINDOW_SIZE)

        self.theme_manager = ThemeManager(self.root, self.settings_manager)
        self.input_processor = InputProcessor(self)

        self.main_window = MainWindow(self.root, self)
        self.transcription_panel = self.main_window.transcription_panel
        self.options_panel = self.main_window.options_panel

        self.theme_manager.set_gui(self)

        self.setup_logging()
        self.load_saved_settings()
        self.load_initial_model()

        # Hinzufügen eines Event-Handlers für Größenänderungen
        self.root.bind("<Configure>", self.on_window_configure)

    @handle_exceptions
    def setup_logging(self) -> None:
        """Konfiguriert das Logging für die Anwendung."""
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.debug("WordweberGUI initialisiert")

    @handle_exceptions
    def load_saved_settings(self) -> None:
        """Lädt und wendet gespeicherte Einstellungen an."""
        self.theme_manager.apply_saved_theme()
        self.update_colors()

    @handle_exceptions
    def load_initial_model(self) -> None:
        """Lädt das initial konfigurierte Whisper-Modell."""
        model_name = self.settings_manager.get_setting("model", "small")
        self.load_model_async(model_name)

    @handle_exceptions
    def load_model_async(self, model_name: str) -> None:
        """
        Lädt das Whisper-Modell asynchron.

        :param model_name: Name des zu ladenden Modells
        """
        self.main_window.update_status_bar(model=f"{model_name} - Wird geladen...", status="Lade Modell...", status_color="yellow")
        threading.Thread(target=self._load_model_thread, args=(model_name,), daemon=True).start()

    @handle_exceptions
    def _load_model_thread(self, model_name: str) -> None:
        """
        Thread-Funktion zum Laden des Whisper-Modells.

        :param model_name: Name des zu ladenden Modells
        """
        try:
            self.backend.load_transcriber_model(model_name)
            self.root.after(0, lambda: self.main_window.update_status_bar(model=f"{model_name} - Geladen", status="Modell geladen", status_color="green"))
            if self.backend.pending_audio:
                self.root.after(0, self.transcribe_and_update)
        except Exception as e:
            self.root.after(0, lambda: self.main_window.update_status_bar(status=f"Fehler beim Laden des Modells: {str(e)}", status_color="red"))
            logging.error(f"Fehler beim Laden des Modells: {str(e)}")

    @handle_exceptions
    def run(self) -> None:
        """Startet die Hauptschleife der GUI."""
        logging.debug("Starte Anwendung")
        self.input_processor.start_listener()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    @handle_exceptions
    def on_closing(self) -> None:
        """Wird aufgerufen, wenn das Anwendungsfenster geschlossen wird."""
        logging.debug("Anwendung wird geschlossen")
        self.settings_manager.set_setting("window_geometry", self.root.geometry())
        self.settings_manager.set_setting("output_mode", self.options_panel.output_mode_var.get())
        self.settings_manager.set_setting("delay_mode", self.options_panel.delay_mode_var.get())
        self.settings_manager.set_setting("char_delay", self.options_panel.char_delay_entry.get())

        # Speichere alle aktuellen Farbeinstellungen
        color_settings = ['text_fg', 'text_bg', 'select_fg', 'select_bg', 'highlight_fg', 'highlight_bg']
        for setting in color_settings:
            current_color = getattr(self.theme_manager, setting).get()
            self.settings_manager.set_setting(setting, current_color)

        self.settings_manager.save_settings()
        self.input_processor.stop_listener()
        if self.backend.transcriber.model is not None:
            del self.backend.transcriber.model
        self.root.destroy()

    @handle_exceptions
    def open_options_window(self) -> None:
        """Öffnet das Fenster für erweiterte Optionen."""
        OptionsWindow.open_window(self.root, self.theme_manager, self.transcription_panel, self)

    @handle_exceptions
    def on_window_configure(self, event: tk.Event) -> None:
        """
        Wird aufgerufen, wenn sich die Fenstergröße ändert.
        Speichert die neue Fenstergröße in den Einstellungen.

        :param event: Das Konfigurationsereignis
        """
        if event.widget == self.root:
            self.settings_manager.set_setting("window_geometry", self.root.geometry())
            self.settings_manager.save_settings()

    @handle_exceptions
    def transcribe_and_update(self) -> None:
        """Führt die Transkription durch und aktualisiert die GUI."""
        def update_gui(text, transcription_time):
            self.main_window.update_status_bar(status="Transkription abgeschlossen", status_color="green")
            self.input_processor.process_text(text)
            self.main_window.update_status_bar(transcription_time=transcription_time)

            output_mode = self.options_panel.output_mode_var.get()
            self.main_window.update_status_bar(output_mode=output_mode)

            if self.main_window.auto_copy_var.get():
                self.main_window.update_status_bar(status="Text transkribiert und in Zwischenablage kopiert", status_color="green")
            else:
                self.main_window.update_status_bar(status="Text transkribiert", status_color="green")

        self.main_window.update_status_bar(status="Transkribiere...", status_color="orange")
        start_time = time.time()
        text = self.backend.process_and_transcribe(self.options_panel.language_var.get())
        transcription_time = time.time() - start_time

        self.root.after(0, lambda: update_gui(text, transcription_time))


    @handle_exceptions
    def update_colors(self) -> None:
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
# 7. Der @handle_exceptions Decorator wurde für alle Methoden hinzugefügt, um eine einheitliche Fehlerbehandlung zu gewährleisten.
# 8. Die Verwendung von self.root.after() in _load_model_thread und transcribe_and_update stellt sicher, dass GUI-Updates im Hauptthread erfolgen.
# 9. Fehlerbehandlung wurde in _load_model_thread hinzugefügt, um Benutzer über Probleme beim Laden des Modells zu informieren.
# 10. Die transcribe_and_update Methode wurde überarbeitet, um alle GUI-Aktualisierungen im Hauptthread durchzuführen.
# 11. Die Statusleiste wird nun für alle relevanten Statusaktualisierungen verwendet, einschließlich farbiger Anzeigen.
