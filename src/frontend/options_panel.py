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

# Standardbibliotheken
import tkinter as tk
from tkinter import ttk

# Projektspezifische Module
from src.config import (
    SUPPORTED_LANGUAGES,
    WHISPER_MODELS,
    DEFAULT_LANGUAGE,
    DEFAULT_WHISPER_MODEL,
    DEFAULT_CHAR_DELAY,
    DEFAULT_PUSH_TO_TALK_KEY
)
from src.utils.error_handling import handle_exceptions, logger


class OptionsPanel(ttk.Frame):
    """
    Panel für Benutzeroptionen und Einstellungen in der Wortweber-Anwendung.

    Dieses Panel ermöglicht die Konfiguration verschiedener Anwendungseinstellungen
    wie Sprache, Whisper-Modell und Ausgabemodus.
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

    @handle_exceptions
    def setup_ui(self):
        """
        Richtet die Benutzeroberfläche für das OptionsPanel ein.

        Diese Methode erstellt und positioniert alle UI-Elemente des Panels,
        einschließlich Sprachauswahl, Modellauswahl, Ausgabemodus und Shortcut-Anzeige.
        """
        self.columnconfigure(0, weight=1)

        main_frame = ttk.Frame(self)
        main_frame.grid(row=0, column=0, sticky="ew")
        main_frame.columnconfigure(3, weight=1)  # Spalte für den flexiblen Leerraum

        # Sprache
        lang_frame = ttk.Frame(main_frame)
        lang_frame.grid(row=0, column=0, padx=(0, 20), sticky="w")
        ttk.Label(lang_frame, text="Sprache:").pack(side=tk.LEFT, padx=(0, 5))
        self.language_var = tk.StringVar(value=self.gui.settings_manager.get_setting("language", DEFAULT_LANGUAGE))
        for lang_code, lang_name in SUPPORTED_LANGUAGES.items():
            ttk.Radiobutton(lang_frame, text=lang_name, variable=self.language_var, value=lang_code, command=self.on_language_change).pack(side=tk.LEFT, padx=5)

        # Whisper-Modell
        model_frame = ttk.Frame(main_frame)
        model_frame.grid(row=0, column=1, padx=(0, 20), sticky="w")
        ttk.Label(model_frame, text="Whisper-Modell:").pack(side=tk.LEFT, padx=(0, 5))
        self.model_var = tk.StringVar(value=self.gui.settings_manager.get_setting("model", DEFAULT_WHISPER_MODEL))
        self.model_dropdown = ttk.Combobox(model_frame, textvariable=self.model_var, values=WHISPER_MODELS, state="readonly", width=10)
        self.model_dropdown.pack(side=tk.LEFT)
        self.model_dropdown.bind("<<ComboboxSelected>>", self.on_model_change)

        # Ausgabemodus
        output_frame = ttk.Frame(main_frame)
        output_frame.grid(row=0, column=2, padx=(0, 20), sticky="w")
        ttk.Label(output_frame, text="Ausgabemodus:").pack(side=tk.LEFT, padx=(0, 5))
        self.output_mode_var = tk.StringVar(value=self.gui.settings_manager.get_setting("output_mode", "textfenster"))
        ttk.Radiobutton(output_frame, text="Textfenster", variable=self.output_mode_var, value="textfenster", command=self.on_output_mode_change).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(output_frame, text="Systemcursor", variable=self.output_mode_var, value="systemcursor", command=self.on_output_mode_change).pack(side=tk.LEFT, padx=5)

        # Flexibler Leerraum
        spacer = ttk.Frame(main_frame)
        spacer.grid(row=0, column=3, sticky="ew")

        # Shortcut-Anzeige
        shortcut_frame = tk.Frame(main_frame, bg="black", bd=1, relief="sunken")
        shortcut_frame.grid(row=0, column=4, sticky="e")
        self.shortcut_label = tk.Label(shortcut_frame, text=f"{DEFAULT_PUSH_TO_TALK_KEY} um aufzunehmen",
                                       bg="black", fg="white", padx=5, pady=2)
        self.shortcut_label.pack()

        logger.info("OptionsPanel UI eingerichtet")

    @handle_exceptions
    def on_language_change(self):
        """
        Behandelt Änderungen der ausgewählten Sprache.

        Aktualisiert die Spracheinstellung in den Anwendungseinstellungen
        und protokolliert die Änderung.
        """
        self.gui.settings_manager.set_setting("language", self.language_var.get())
        logger.info(f"Sprache geändert auf: {self.language_var.get()}")

    @handle_exceptions
    def on_model_change(self, event):
        """
        Behandelt Änderungen des ausgewählten Whisper-Modells.

        Aktualisiert die Modelleinstellung, lädt das neue Modell asynchron
        und protokolliert die Änderung.

        :param event: Das Ereignis, das die Änderung ausgelöst hat (wird nicht verwendet)
        """
        self.gui.settings_manager.set_setting("model", self.model_var.get())
        self.gui.load_model_async(self.model_var.get())
        logger.info(f"Whisper-Modell geändert auf: {self.model_var.get()}")

    @handle_exceptions
    def on_output_mode_change(self):
        """
        Behandelt Änderungen des ausgewählten Ausgabemodus.

        Aktualisiert die Ausgabemodus-Einstellung, aktualisiert die Statusleiste
        und protokolliert die Änderung.
        """
        new_output_mode = self.output_mode_var.get()
        self.gui.settings_manager.set_setting("output_mode", new_output_mode)
        self.gui.main_window.update_status_bar(output_mode=new_output_mode)
        logger.info(f"Ausgabemodus geändert auf: {new_output_mode}")

    @handle_exceptions
    def get_delay_settings(self):
        """
        Holt die aktuellen Verzögerungseinstellungen.

        :return: Ein Dictionary mit den aktuellen Verzögerungseinstellungen
        """
        return {
            "delay_mode": self.gui.settings_manager.get_setting("delay_mode", "no_delay"),
            "char_delay": self.gui.settings_manager.get_setting("char_delay", DEFAULT_CHAR_DELAY)
        }

    @handle_exceptions
    def update_shortcut_display(self, new_shortcut):
        """
        Aktualisiert die Anzeige des aktuellen Shortcuts.

        :param new_shortcut: Der neue Shortcut, der angezeigt werden soll
        """
        self.shortcut_label.config(text=f"{new_shortcut} um aufzunehmen")
        logger.info(f"Shortcut-Anzeige aktualisiert auf: {new_shortcut}")

    @handle_exceptions
    def update_delay_settings(self, delay_mode, char_delay):
        """
        Aktualisiert die Verzögerungseinstellungen.

        :param delay_mode: Der neue Verzögerungsmodus
        :param char_delay: Die neue Zeichenverzögerung
        """
        self.gui.settings_manager.set_setting("delay_mode", delay_mode)
        self.gui.settings_manager.set_setting("char_delay", char_delay)
        logger.info(f"Verzögerungseinstellungen aktualisiert: Modus={delay_mode}, Verzögerung={char_delay}")


# Zusätzliche Erklärungen:

# 1. Modulare Struktur:
#    Die Klasse OptionsPanel ist in logische Abschnitte unterteilt, die jeweils
#    für einen bestimmten Aspekt der Benutzeroberfläche verantwortlich sind.

# 2. Einstellungspersistenz:
#    Alle Änderungen an den Optionen werden sofort in den Einstellungen gespeichert,
#    um sicherzustellen, dass die Benutzervorlieben über Sitzungen hinweg erhalten bleiben.

# 3. Fehlerbehandlung:
#    Jede Methode ist mit dem @handle_exceptions Decorator versehen, was eine einheitliche
#    Fehlerbehandlung in der gesamten Klasse gewährleistet.

# 4. Logging:
#    Ausführliche Logging-Aufrufe wurden implementiert, um die Nachvollziehbarkeit von
#    Benutzeraktionen und möglichen Problemen zu verbessern.

# 5. Flexibilität:
#    Die Verwendung von Konfigurationsvariablen (wie SUPPORTED_LANGUAGES, WHISPER_MODELS)
#    ermöglicht eine einfache Erweiterung oder Änderung der unterstützten Optionen,
#    ohne den Code wesentlich ändern zu müssen.

# 6. Layout:
#    Das Layout wurde so gestaltet, dass die Sprachauswahl, das Whisper-Modell und der
#    Ausgabemodus nebeneinander in einer Reihe angeordnet sind, was eine übersichtliche
#    und platzsparende Darstellung ermöglicht.

# 7. Shortcut-Anzeige:
#    Die Shortcut-Anzeige wurde am rechten Rand des Panels hinzugefügt, um dem
#    Benutzer eine schnelle visuelle Referenz für den aktuellen Aufnahme-Shortcut zu bieten.
