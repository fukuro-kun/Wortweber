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
from src.utils.error_handling import handle_exceptions

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
        self.setup_language_frame()
        self.setup_model_frame()
        self.setup_output_mode()
        self.setup_delay_options()

    @handle_exceptions
    def setup_language_frame(self):
        """Erstellt und konfiguriert den Rahmen für die Sprachauswahl."""
        language_frame = ttk.LabelFrame(self, text="Sprache")
        language_frame.pack(fill=tk.X, pady=5)
        self.language_var = tk.StringVar(value=self.gui.settings_manager.get_setting("language") or DEFAULT_LANGUAGE)
        for lang_code, lang_name in SUPPORTED_LANGUAGES.items():
            ttk.Radiobutton(language_frame, text=lang_name, variable=self.language_var, value=lang_code, command=self.on_language_change).pack(side=tk.LEFT, padx=5)

    @handle_exceptions
    def setup_model_frame(self):
        """Erstellt und konfiguriert den Rahmen für die Modellauswahl."""
        model_frame = ttk.Frame(self)
        model_frame.pack(fill=tk.X, pady=5)
        ttk.Label(model_frame, text="Whisper-Modell:").grid(column=0, row=0, padx=(0, 5))
        self.model_var = tk.StringVar(value=self.gui.settings_manager.get_setting("model") or DEFAULT_WHISPER_MODEL)
        model_dropdown = ttk.Combobox(model_frame, textvariable=self.model_var, values=WHISPER_MODELS, state="readonly", width=10)
        model_dropdown.grid(column=1, row=0)
        model_dropdown.bind("<<ComboboxSelected>>", self.on_model_change)

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

    @handle_exceptions
    def setup_output_mode(self):
        """Erstellt und konfiguriert die Optionen für den Ausgabemodus."""
        output_mode_frame = ttk.LabelFrame(self, text="Ausgabemodus")
        output_mode_frame.pack(fill=tk.X, pady=5)
        self.output_mode_var = tk.StringVar(value=self.gui.settings_manager.get_setting("output_mode"))
        ttk.Radiobutton(output_mode_frame, text="Ins Textfenster", variable=self.output_mode_var, value="textfenster", command=self.on_output_mode_change).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(output_mode_frame, text="An Systemcursor-Position", variable=self.output_mode_var, value="systemcursor", command=self.on_output_mode_change).pack(side=tk.LEFT, padx=5)

    @handle_exceptions
    def on_language_change(self):
        """Behandelt Änderungen der ausgewählten Sprache."""
        self.gui.settings_manager.set_setting("language", self.language_var.get())
        self.gui.settings_manager.save_settings()

    @handle_exceptions
    def on_model_change(self, event):
        """Behandelt Änderungen des ausgewählten Whisper-Modells."""
        self.gui.settings_manager.set_setting("model", self.model_var.get())
        self.gui.load_model_async(self.model_var.get())

    @handle_exceptions
    def on_output_mode_change(self):
        """Behandelt Änderungen des ausgewählten Ausgabemodus."""
        self.gui.settings_manager.set_setting("output_mode", self.output_mode_var.get())
        self.gui.settings_manager.save_settings()
        self.toggle_delay_options()

    @handle_exceptions
    def toggle_delay_options(self, *args):
        """Schaltet die Verzögerungsoptionen basierend auf dem ausgewählten Ausgabemodus ein oder aus."""
        if self.output_mode_var.get() == "textfenster":
            self.delay_frame.pack_forget()
        else:
            self.delay_frame.pack(fill=tk.X, pady=5)

    @handle_exceptions
    def on_delay_mode_change(self):
        """Behandelt Änderungen des ausgewählten Verzögerungsmodus."""
        self.gui.settings_manager.set_setting("delay_mode", self.delay_mode_var.get())
        self.gui.settings_manager.save_settings()

    @handle_exceptions
    def on_char_delay_change(self, *args):
        """Behandelt Änderungen der eingegebenen zeichenweisen Verzögerung."""
        self.gui.settings_manager.set_setting("char_delay", self.char_delay_entry.get())
        self.gui.settings_manager.save_settings()

# Zusätzliche Erklärungen:

# 1. Dynamische UI-Anpassung:
#    Die toggle_delay_options-Methode passt die Benutzeroberfläche dynamisch an, basierend auf dem ausgewählten Ausgabemodus.
#    Dies verbessert die Benutzerfreundlichkeit, indem nur relevante Optionen angezeigt werden.

# 2. Einstellungspersistenz:
#    Jede Änderung an den Optionen wird sofort in den Einstellungen gespeichert (via settings_manager),
#    um sicherzustellen, dass die Benutzervorlieben über Sitzungen hinweg erhalten bleiben.

# 3. Modulare Struktur:
#    Die Aufteilung in separate setup_*-Methoden verbessert die Lesbarkeit und Wartbarkeit des Codes.
#    Jede Methode ist für einen spezifischen Teil der Benutzeroberfläche verantwortlich.

# 4. Flexibilität:
#    Die Verwendung von Konfigurationsvariablen (wie SUPPORTED_LANGUAGES, WHISPER_MODELS) ermöglicht eine einfache
#    Erweiterung oder Änderung der unterstützten Optionen, ohne den Code wesentlich ändern zu müssen.

# 5. Ereignisbasierte Programmierung:
#    Die on_*-Methoden implementieren eine ereignisbasierte Logik, die auf Benutzerinteraktionen reagiert
#    und entsprechende Aktionen auslöst (z.B. Speichern von Einstellungen, Laden von Modellen).
