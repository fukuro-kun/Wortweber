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
from tkinter import ttk, messagebox
import time
import logging
import threading
from typing import Optional, Callable
from functools import wraps

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
from src.config import DEFAULT_WINDOW_SIZE, DEFAULT_CHAR_DELAY, DEFAULT_PUSH_TO_TALK_KEY
from src.utils.error_handling import handle_exceptions, logger
from src.plugin_system.plugin_manager import PluginManager
from src.frontend.context_menu import create_context_menu
from src.frontend.plugin_management_window import PluginManagementWindow

class WordweberGUI:
    """
    Hauptklasse für die grafische Benutzeroberfläche der Wortweber-Anwendung.
    Koordiniert die verschiedenen UI-Komponenten und die Interaktion mit dem Backend.
    """

    @handle_exceptions
    def __init__(self, backend: WordweberBackend, plugin_manager: PluginManager) -> None:
        """
        Initialisiert die GUI der Wortweber-Anwendung.

        :param backend: Eine Instanz der WordweberBackend-Klasse
        :param plugin_manager: Eine Instanz der PluginManager-Klasse
        """
        self.backend = backend
        self.plugin_manager = plugin_manager
        self.settings_manager = SettingsManager()

        self.root = ttkthemes.ThemedTk()
        self.root.title("Wortweber Transkription")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.after(5000, self.update_geometry)

        # Laden der gespeicherten Fenstergeometrie
        saved_geometry = self.settings_manager.get_setting("window_geometry")
        if saved_geometry:
            try:
                self.root.geometry(saved_geometry)
                logger.info(f"Gespeicherte Fenstergeometrie geladen: {saved_geometry}")
            except tk.TclError:
                logger.warning("Ungültige gespeicherte Geometrie, verwende Standardgröße")
                self.root.geometry(DEFAULT_WINDOW_SIZE)
        else:
            logger.info("Keine gespeicherte Geometrie gefunden, verwende Standardgröße")
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
        self.initialize_delay_settings()
        self.setup_menu()
        self.setup_context_menu()

        # Plugins entdecken
        self.plugin_manager.discover_plugins()

        # Fügen Sie einen Protokoll-Handler für das Schließen des Hauptfensters hinzu
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Initialisierung der Shortcut-Anzeige
        self.options_panel.update_shortcut_display(self.settings_manager.get_setting("push_to_talk_key", DEFAULT_PUSH_TO_TALK_KEY))

    @handle_exceptions
    def update_geometry(self):
        current_geometry = self.root.geometry()
        self.settings_manager.set_setting("window_geometry", current_geometry)
        logger.debug(f"Fenstergeometrie aktualisiert: {current_geometry}")
        self.root.after(5000, self.update_geometry)  # Alle 5 Sekunden aktualisieren

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
        self.root.mainloop()

    @handle_exceptions
    def on_closing(self) -> None:
        """Wird aufgerufen, wenn das Anwendungsfenster geschlossen wird."""
        logging.debug("Anwendung wird geschlossen")
        current_geometry = self.root.geometry()
        self.settings_manager.set_setting("window_geometry", current_geometry)
        logger.info(f"Aktuelle Fenstergeometrie gespeichert: {current_geometry}")

        # Verzögerungseinstellungen aus dem OptionsWindow holen
        delay_settings = self.get_delay_settings()
        self.settings_manager.set_setting("delay_mode", delay_settings["delay_mode"])
        self.settings_manager.set_setting("char_delay", delay_settings["char_delay"])

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
    def save_current_geometry(self):
        """Speichert die aktuelle Fenstergeometrie in den Einstellungen."""
        current_geometry = self.root.winfo_geometry()
        self.settings_manager.set_setting("window_geometry", current_geometry)
        logger.debug(f"Fenstergeometrie beim Schließen gespeichert: {current_geometry}")

    @handle_exceptions
    def open_options_window(self) -> None:
        """Öffnet das Fenster für erweiterte Optionen."""
        options_window = OptionsWindow.open_window(self.root, self.theme_manager, self.transcription_panel, self)
        if options_window:
            options_window.protocol("WM_DELETE_WINDOW", lambda: self.on_options_window_closing(options_window))

    def on_options_window_closing(self, window):
        self.save_current_geometry()
        window.destroy()

    @handle_exceptions
    def transcribe_and_update(self) -> None:
        """Führt die Transkription durch und aktualisiert die GUI."""
        def update_gui(text, transcription_time):
            # Verarbeite den Text mit aktiven Plugins
            processed_text = self.plugin_manager.process_text_with_plugins(text)

            self.main_window.update_status_bar(status="Transkription abgeschlossen", status_color="green", transcription_time=transcription_time)
            self.input_processor.process_text(processed_text)  # Verwende den verarbeiteten Text

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
    def start_timer(self):
        """Startet den Timer für die Aufnahmedauer."""
        self.input_processor.start_time = int(time.time())
        self.update_timer()

    @handle_exceptions
    def update_timer(self):
        """Aktualisiert die Anzeige der Aufnahmedauer."""
        if self.backend.state.recording:
            elapsed_time = time.time() - self.input_processor.start_time
            self.main_window.update_status_bar(record_time=elapsed_time)
            self.root.after(100, self.update_timer)

    @handle_exceptions
    def stop_timer(self):
        """Stoppt den Timer für die Aufnahmedauer."""
        self.main_window.update_status_bar(record_time=0.0)

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

    @handle_exceptions
    def initialize_delay_settings(self):
        """Initialisiert die Verzögerungseinstellungen."""
        delay_mode = self.settings_manager.get_setting("delay_mode", "no_delay")
        char_delay = self.settings_manager.get_setting("char_delay", DEFAULT_CHAR_DELAY)
        self.settings_manager.set_setting("delay_mode", delay_mode)
        self.settings_manager.set_setting("char_delay", char_delay)
        logger.info(f"Verzögerungseinstellungen initialisiert: Modus={delay_mode}, Verzögerung={char_delay}")

    @handle_exceptions
    def get_delay_settings(self):
        """Holt die aktuellen Verzögerungseinstellungen."""
        return {
            "delay_mode": self.settings_manager.get_setting("delay_mode", "no_delay"),
            "char_delay": self.settings_manager.get_setting("char_delay", DEFAULT_CHAR_DELAY)
        }

    @handle_exceptions
    def update_shortcut_display(self, new_shortcut):
        """Aktualisiert die Shortcut-Anzeige im OptionsPanel."""
        self.options_panel.update_shortcut_display(new_shortcut)

    @handle_exceptions
    def setup_menu(self):
        """Richtet das Hauptmenü der Anwendung ein."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Datei-Menü
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Datei", menu=file_menu)
        file_menu.add_command(label="Beenden", command=self.root.quit)

        # Bearbeiten-Menü
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Bearbeiten", menu=edit_menu)
        edit_menu.add_command(label="Transkription löschen", command=self.transcription_panel.clear_transcription)
        edit_menu.add_command(label="Alles kopieren", command=self.transcription_panel.copy_all_to_clipboard)

        # Optionen-Menü
        options_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Optionen", menu=options_menu)
        options_menu.add_command(label="Erweiterte Einstellungen", command=self.open_options_window)

        # Plugin-Menü
        plugin_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Plugins", menu=plugin_menu)
        plugin_menu.add_command(label="Plugin-Verwaltung", command=self.open_plugin_management_window)

    @handle_exceptions
    def setup_context_menu(self):
        """Richtet das Kontextmenü für das Transkriptionsfenster ein."""
        def show_context_menu(event):
            create_context_menu(self.transcription_panel.text_widget, event)

        self.transcription_panel.text_widget.bind("<Button-3>", show_context_menu)

    @handle_exceptions
    def open_plugin_management_window(self):
        """Öffnet das Fenster zur Plugin-Verwaltung."""
        PluginManagementWindow.open_window(self.root, self.plugin_manager)


# Zusätzliche Erklärungen:

# 1. Modulare Struktur:
#    Die GUI ist in verschiedene Komponenten aufgeteilt (MainWindow, TranscriptionPanel, OptionsPanel),
#    was die Wartbarkeit und Erweiterbarkeit verbessert.

# 2. Event-Handling:
#    Die Klasse verwendet verschiedene Event-Handler, um auf Benutzerinteraktionen und
#    Systemereignisse zu reagieren, z.B. Fenstergrößenänderungen oder das Schließen der Anwendung.

# 3. Asynchrone Verarbeitung:
#    Modellladung und Transkription werden asynchron durchgeführt, um die GUI reaktiv zu halten.

# 4. Einstellungsverwaltung:
#    Die Klasse interagiert eng mit dem SettingsManager, um Benutzereinstellungen zu laden,
#    zu speichern und anzuwenden.

# 5. Theming und Farbverwaltung:
#    Der ThemeManager wird verwendet, um das Erscheinungsbild der Anwendung anzupassen.

# 6. Plugin-Integration:
#    Das Plugin-System wird durch die setup_menu und open_plugin_management_window Methoden integriert,
#    was die Erweiterbarkeit der Anwendung demonstriert.

# 7. Fehlerbehandlung und Logging:
#    Umfassende Fehlerbehandlung und Logging sind implementiert, um die Stabilität
#    zu erhöhen und die Fehlerbehebung zu erleichtern.

# 8. Kontextmenü:
#    Ein Kontextmenü wurde hinzugefügt, um schnellen Zugriff auf häufig verwendete Funktionen zu bieten.

# 9. Debounce-Funktionalität:
#    Die Implementierung einer Debounce-Funktion hilft, die Häufigkeit bestimmter Ereignisse
#    (wie Fensterkonfigurationsänderungen) zu begrenzen, was die Leistung verbessert.

# Diese Implementierung bietet eine flexible und erweiterbare Basis für die
# Benutzeroberfläche von Wortweber, mit Fokus auf Benutzerfreundlichkeit,
# Anpassbarkeit und robuste Fehlerbehandlung.
