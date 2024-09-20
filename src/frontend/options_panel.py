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

from tkinter import ttk
import tkinter as tk
from src.config import (
    SUPPORTED_LANGUAGES,
    WHISPER_MODELS,
    DEFAULT_CHAR_DELAY,
    DEFAULT_LANGUAGE,
    DEFAULT_WHISPER_MODEL
)
from src.utils.error_handling import handle_exceptions, logger

class OptionsPanel(ttk.Frame):
    """
    Panel für Benutzeroptionen und Einstellungen in der Wortweber-Anwendung.
    """

    @handle_exceptions
    def __init__(self, parent, gui):
        """
        Initialisiert das OptionsPanel.

        :param parent: Das übergeordnete Tkinter-Widget
        :param gui: Referenz auf die Hauptgui-Instanz
        """
        super().__init__(parent)
        self.gui = gui
        self.setup_ui()
        self.toggle_delay_options()

    @handle_exceptions
    def setup_ui(self):
        """Richtet die Benutzeroberfläche für das OptionsPanel ein."""
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.X, pady=5)

        # Sprache
        ttk.Label(main_frame, text="Sprache:").grid(row=0, column=0, padx=5, sticky="w")
        self.language_var = tk.StringVar(value=self.gui.settings_manager.get_setting("language") or DEFAULT_LANGUAGE)
        for i, (lang_code, lang_name) in enumerate(SUPPORTED_LANGUAGES.items()):
            ttk.Radiobutton(main_frame, text=lang_name, variable=self.language_var, value=lang_code, command=self.on_language_change).grid(row=0, column=i+1, padx=5)

        # Whisper-Modell
        ttk.Label(main_frame, text="Whisper-Modell:").grid(row=0, column=len(SUPPORTED_LANGUAGES)+1, padx=(20,5), sticky="w")
        self.model_var = tk.StringVar(value=self.gui.settings_manager.get_setting("model") or DEFAULT_WHISPER_MODEL)
        self.model_dropdown = ttk.Combobox(main_frame, textvariable=self.model_var, values=WHISPER_MODELS, state="readonly", width=10)
        self.model_dropdown.grid(row=0, column=len(SUPPORTED_LANGUAGES)+2, padx=5)
        self.model_dropdown.bind("<<ComboboxSelected>>", self.on_model_change)

        # Ausgabemodus
        ttk.Label(main_frame, text="Ausgabemodus:").grid(row=0, column=len(SUPPORTED_LANGUAGES)+3, padx=(20,5), sticky="w")
        self.output_mode_var = tk.StringVar(value=self.gui.settings_manager.get_setting("output_mode"))
        ttk.Radiobutton(main_frame, text="Textfenster", variable=self.output_mode_var, value="textfenster", command=self.on_output_mode_change).grid(row=0, column=len(SUPPORTED_LANGUAGES)+4, padx=5)
        ttk.Radiobutton(main_frame, text="Systemcursor", variable=self.output_mode_var, value="systemcursor", command=self.on_output_mode_change).grid(row=0, column=len(SUPPORTED_LANGUAGES)+5, padx=5)

        # Konfigurieren der Spaltengewichtung
        for i in range(len(SUPPORTED_LANGUAGES)+6):
            main_frame.columnconfigure(i, weight=1)

        # Verzögerungsoptionen
        self.setup_delay_options()

        logger.info("OptionsPanel UI eingerichtet")

    @handle_exceptions
    def setup_delay_options(self):
        """Erstellt und konfiguriert die Optionen für Eingabeverzögerungen."""
        self.delay_frame = ttk.LabelFrame(self, text="Verzögerungsmodus")
        self.delay_frame.pack(fill=tk.X, pady=5)

        self.delay_mode_var = tk.StringVar(value=self.gui.settings_manager.get_setting("delay_mode"))

        self.no_delay_radio = ttk.Radiobutton(self.delay_frame, text="Keine Verzögerung", variable=self.delay_mode_var, value="no_delay", command=self.on_delay_mode_change)
        self.no_delay_radio.pack(anchor=tk.W)

        char_delay_frame = ttk.Frame(self.delay_frame)
        char_delay_frame.pack(anchor=tk.W, fill=tk.X)

        self.char_delay_radio = ttk.Radiobutton(char_delay_frame, text="Zeichenweise", variable=self.delay_mode_var, value="char_delay", command=self.on_delay_mode_change)
        self.char_delay_radio.pack(side=tk.LEFT)

        self.char_delay_entry = ttk.Entry(char_delay_frame, width=5)
        self.char_delay_entry.pack(side=tk.LEFT, padx=(5, 0))
        self.char_delay_entry.insert(0, str(self.gui.settings_manager.get_setting("char_delay") or DEFAULT_CHAR_DELAY))
        self.char_delay_entry.bind("<FocusOut>", self.on_char_delay_change)

        ttk.Label(char_delay_frame, text="ms").pack(side=tk.LEFT)

        self.clipboard_radio = ttk.Radiobutton(self.delay_frame, text="Zwischenablage", variable=self.delay_mode_var, value="clipboard", command=self.on_delay_mode_change)
        self.clipboard_radio.pack(anchor=tk.W)

        self.delay_widgets = [self.no_delay_radio, self.char_delay_radio, self.char_delay_entry, self.clipboard_radio]

        # Anfänglich unsichtbar machen
        self.toggle_delay_options()

        logger.debug("Verzögerungsoptionen eingerichtet")

    @handle_exceptions
    def on_language_change(self):
        """Behandelt Änderungen der ausgewählten Sprache."""
        self.gui.settings_manager.set_setting("language", self.language_var.get())
        self.gui.settings_manager.save_settings()
        logger.info(f"Sprache geändert auf: {self.language_var.get()}")

    @handle_exceptions
    def on_model_change(self, event):
        """Behandelt Änderungen des ausgewählten Whisper-Modells."""
        self.gui.settings_manager.set_setting("model", self.model_var.get())
        self.gui.load_model_async(self.model_var.get())
        logger.info(f"Whisper-Modell geändert auf: {self.model_var.get()}")

    @handle_exceptions
    def on_output_mode_change(self):
        """Behandelt Änderungen des ausgewählten Ausgabemodus."""
        new_output_mode = self.output_mode_var.get()
        self.gui.settings_manager.set_setting("output_mode", new_output_mode)
        self.gui.settings_manager.save_settings()
        self.toggle_delay_options()
        self.gui.main_window.update_status_bar(output_mode=new_output_mode)
        logger.info(f"Ausgabemodus geändert auf: {new_output_mode}")

    @handle_exceptions
    def toggle_delay_options(self, *args):
        """Schaltet die Verzögerungsoptionen basierend auf dem ausgewählten Ausgabemodus ein oder aus."""
        if self.output_mode_var.get() == "textfenster":
            self.delay_frame.pack_forget()
        else:
            self.delay_frame.pack(fill=tk.X, pady=5)
        logger.debug(f"Verzögerungsoptionen Sichtbarkeit geändert: {self.output_mode_var.get() != 'textfenster'}")

    @handle_exceptions
    def on_delay_mode_change(self):
        """Behandelt Änderungen des ausgewählten Verzögerungsmodus."""
        self.gui.settings_manager.set_setting("delay_mode", self.delay_mode_var.get())
        self.gui.settings_manager.save_settings()
        logger.info(f"Verzögerungsmodus geändert auf: {self.delay_mode_var.get()}")

    @handle_exceptions
    def on_char_delay_change(self, *args):
        """Behandelt Änderungen der eingegebenen zeichenweisen Verzögerung."""
        self.gui.settings_manager.set_setting("char_delay", self.char_delay_entry.get())
        self.gui.settings_manager.save_settings()
        logger.info(f"Zeichenverzögerung geändert auf: {self.char_delay_entry.get()} ms")

# Zusätzliche Erklärungen:

# 1. Modulare Struktur:
#    Die Klasse OptionsPanel ist in logische Abschnitte unterteilt, die jeweils
#    für einen bestimmten Aspekt der Benutzeroberfläche verantwortlich sind.

# 2. Einstellungspersistenz:
#    Alle Änderungen an den Optionen werden sofort in den Einstellungen gespeichert,
#    um sicherzustellen, dass die Benutzervorlieben über Sitzungen hinweg erhalten bleiben.

# 3. Dynamische UI-Anpassung:
#    Die toggle_delay_options-Methode passt die Benutzeroberfläche dynamisch an,
#    basierend auf dem ausgewählten Ausgabemodus. Dies verbessert die Benutzerfreundlichkeit,
#    indem nur relevante Optionen angezeigt werden.

# 4. Fehlerbehandlung:
#    Jede Methode ist mit dem @handle_exceptions Decorator versehen, was eine einheitliche
#    Fehlerbehandlung in der gesamten Klasse gewährleistet.

# 5. Logging:
#    Ausführliche Logging-Aufrufe wurden implementiert, um die Nachvollziehbarkeit von
#    Benutzeraktionen und möglichen Problemen zu verbessern.

# 6. Flexibilität:
#    Die Verwendung von Konfigurationsvariablen (wie SUPPORTED_LANGUAGES, WHISPER_MODELS)
#    ermöglicht eine einfache Erweiterung oder Änderung der unterstützten Optionen,
#    ohne den Code wesentlich ändern zu müssen.
