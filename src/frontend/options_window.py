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

import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from tkcolorpicker import askcolor
from src.config import DEFAULT_FONT_FAMILY, DEFAULT_FONT_SIZE, DEFAULT_INCOGNITO_MODE, DEFAULT_CHAR_DELAY, DEFAULT_PUSH_TO_TALK_KEY
from src.utils.error_handling import handle_exceptions, logger
from src.frontend.audio_options_panel import AudioOptionsPanel
from src.frontend.shortcut_panel import ShortcutPanel

class OptionsWindow(tk.Toplevel):
    """
    Fenster für erweiterte Optionen in der Wortweber-Anwendung.
    Ermöglicht die Anpassung von Theme, Textoptionen, Testaufnahme-Einstellungen und Shortcuts.
    """

    _instance = None

    @classmethod
    @handle_exceptions
    def open_window(cls, parent, theme_manager, transcription_panel, gui):
        """
        Öffnet das Optionsfenster oder bringt ein bereits geöffnetes in den Vordergrund.

        :param parent: Das übergeordnete Tkinter-Fenster
        :param theme_manager: Instanz des ThemeManagers zur Verwaltung der Themes
        :param transcription_panel: Referenz auf das TranscriptionPanel für Textoptionen
        :param gui: Referenz auf die Hauptgui-Instanz
        """
        if cls._instance is None or not cls._instance.winfo_exists():
            cls._instance = cls(parent, theme_manager, transcription_panel, gui)
        else:
            cls._instance.focus_force()
            cls._instance.lift()
        logger.info("Optionsfenster geöffnet oder in den Vordergrund gebracht")
        return cls._instance

    @handle_exceptions
    def __init__(self, parent, theme_manager, transcription_panel, gui):
        """
        Initialisiert das OptionsWindow.

        :param parent: Das übergeordnete Tkinter-Fenster
        :param theme_manager: Instanz des ThemeManagers zur Verwaltung der Themes
        :param transcription_panel: Referenz auf das TranscriptionPanel für Textoptionen
        :param gui: Referenz auf die Hauptgui-Instanz
        """
        super().__init__(parent)
        self.title("Erweiterte Optionen")
        self.theme_manager = theme_manager
        self.transcription_panel = transcription_panel
        self.gui = gui
        self.available_fonts = sorted(set(tkFont.families()))
        self.initial_settings = self.get_current_settings()
        self.setup_styles()
        self.setup_ui()

        # Mache das Fenster modal
        self.transient(parent)
        self.grab_set()

        # Lade die gespeicherte Fenstergröße und -position
        self.load_window_geometry()

        # Bind das Schließen-Event
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        logger.info("OptionsWindow initialisiert")

    @handle_exceptions
    def setup_styles(self):
        """Richtet benutzerdefinierte Stile für die UI-Elemente ein."""
        style = ttk.Style()
        style.configure('Square.TButton', width=3, padding=0)
        logger.debug("Benutzerdefinierte Stile für UI-Elemente eingerichtet")

    @handle_exceptions
    def setup_ui(self):
        """Richtet die Benutzeroberfläche für das OptionsWindow ein."""
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Audio-Optionen
        audio_options_frame = ttk.Frame(notebook)
        notebook.add(audio_options_frame, text="Audiooptionen")
        self.audio_options_panel = AudioOptionsPanel(
            audio_options_frame,
            self.gui.settings_manager,
            self.gui.backend.update_audio_device,
            self.gui.backend  # Backend wird hier übergeben
        )
        self.audio_options_panel.pack(fill=tk.BOTH, expand=True)

        # Theme-Einstellungen
        theme_frame = ttk.Frame(notebook)
        notebook.add(theme_frame, text="Theme")
        self.theme_manager.setup_theme_selection(theme_frame)

        # Textoptionen-Einstellungen
        text_options_frame = ttk.Frame(notebook)
        notebook.add(text_options_frame, text="Textoptionen")
        self.setup_text_options(text_options_frame)

        # Testaufnahme-Einstellungen
        test_recording_frame = ttk.Frame(notebook)
        notebook.add(test_recording_frame, text="Testaufnahme")
        self.setup_test_recording_options(test_recording_frame)

        # Ausgabemodus-Einstellungen
        output_mode_frame = ttk.Frame(notebook)
        notebook.add(output_mode_frame, text="Ausgabemodus")
        self.setup_output_mode_options(output_mode_frame)

        # Shortcut-Einstellungen
        shortcut_frame = ttk.Frame(notebook)
        notebook.add(shortcut_frame, text="Shortcuts")
        self.shortcut_panel = ShortcutPanel(shortcut_frame, self.gui.settings_manager, self.gui.input_processor)
        self.shortcut_panel.pack(fill=tk.BOTH, expand=True)

        # Button-Frame
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10, fill=tk.X)

        # Rückgängig-Button
        undo_button = ttk.Button(button_frame, text="Rückgängig", command=self.undo_changes)
        undo_button.pack(side=tk.LEFT, padx=5)

        # Schließen-Button
        close_button = ttk.Button(button_frame, text="Schließen", command=self.on_closing)
        close_button.pack(side=tk.RIGHT, padx=5)

        logger.info("OptionsWindow UI eingerichtet")

    @handle_exceptions
    def setup_text_options(self, parent):
        """
        Richtet die Optionen zur Anpassung der Textgröße und Schriftart ein.

        :param parent: Das übergeordnete Frame für die Textoptionen
        """
        options_frame = ttk.Frame(parent)
        options_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        options_frame.columnconfigure(1, weight=1)

        # Textgröße
        ttk.Label(options_frame, text="Textgröße:").grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.size_var = tk.StringVar(value=str(self.transcription_panel.get_font_size()))
        size_spinbox = ttk.Spinbox(options_frame, from_=8, to=24, textvariable=self.size_var, width=5)
        size_spinbox.grid(row=0, column=1, sticky="w")

        # Schriftart
        ttk.Label(options_frame, text="Schriftart:").grid(row=0, column=2, sticky="w", padx=(20, 10))
        self.font_var = tk.StringVar(value=self.transcription_panel.get_font_family())

        font_frame = ttk.Frame(options_frame)
        font_frame.grid(row=0, column=3, sticky="ew")
        font_frame.columnconfigure(0, weight=1)

        self.font_combobox = ttk.Combobox(font_frame, textvariable=self.font_var, values=self.available_fonts, state="readonly")
        self.font_combobox.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        button_frame = ttk.Frame(font_frame)
        button_frame.grid(row=0, column=1)

        prev_button = ttk.Button(button_frame, text="◀", style='Square.TButton', command=lambda: self.scroll_font(-1))
        prev_button.pack(side=tk.LEFT)

        next_button = ttk.Button(button_frame, text="▶", style='Square.TButton', command=lambda: self.scroll_font(1))
        next_button.pack(side=tk.LEFT)

        self.size_var.trace_add("write", self.update_text_options)
        self.font_var.trace_add("write", self.update_text_options)

        logger.debug("Textoptionen eingerichtet")

    @handle_exceptions
    def setup_test_recording_options(self, parent):
        """
        Richtet die Optionen für die Testaufnahme ein.

        :param parent: Das übergeordnete Frame für die Testaufnahmeoptionen
        """
        self.save_test_recording_var = tk.BooleanVar(value=self.gui.settings_manager.get_setting("save_test_recording", False))
        ttk.Checkbutton(parent, text="Letzte Aufnahme als Testdatei speichern",
                        variable=self.save_test_recording_var,
                        command=self.on_save_test_recording_change).pack(pady=10)

        self.incognito_var = tk.BooleanVar(value=self.gui.settings_manager.get_setting("incognito_mode", DEFAULT_INCOGNITO_MODE))
        ttk.Checkbutton(parent, text="Incognito-Modus (keine Transkriptionsprotokollierung)",
                        variable=self.incognito_var,
                        command=self.on_incognito_change).pack(pady=10)

        logger.debug("Testaufnahmeoptionen eingerichtet")

    @handle_exceptions
    def setup_output_mode_options(self, parent):
        """Richtet die Optionen für den Ausgabemodus ein."""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.delay_mode_var = tk.StringVar(value=self.gui.settings_manager.get_setting("delay_mode", "no_delay"))

        ttk.Radiobutton(frame, text="Keine Verzögerung", variable=self.delay_mode_var, value="no_delay", command=self.on_delay_mode_change).pack(anchor=tk.W)

        char_delay_frame = ttk.Frame(frame)
        char_delay_frame.pack(fill=tk.X, pady=5)
        ttk.Radiobutton(char_delay_frame, text="Zeichenweise", variable=self.delay_mode_var, value="char_delay", command=self.on_delay_mode_change).pack(side=tk.LEFT)
        self.char_delay_entry = ttk.Entry(char_delay_frame, width=5)
        self.char_delay_entry.pack(side=tk.LEFT, padx=(5, 0))
        self.char_delay_entry.insert(0, str(self.gui.settings_manager.get_setting("char_delay", DEFAULT_CHAR_DELAY)))
        self.char_delay_entry.bind("<FocusOut>", self.on_char_delay_change)
        ttk.Label(char_delay_frame, text="ms").pack(side=tk.LEFT)

        ttk.Radiobutton(frame, text="Zwischenablage", variable=self.delay_mode_var, value="clipboard", command=self.on_delay_mode_change).pack(anchor=tk.W)

    @handle_exceptions
    def on_delay_mode_change(self):
        """Behandelt Änderungen des Verzögerungsmodus."""
        delay_mode = self.delay_mode_var.get()
        char_delay = self.char_delay_entry.get()
        self.gui.settings_manager.set_setting("delay_mode", delay_mode)
        self.gui.settings_manager.set_setting("char_delay", char_delay)
        logger.info(f"Verzögerungsmodus geändert auf: {delay_mode}, Zeichenverzögerung: {char_delay}")

    @handle_exceptions
    def on_char_delay_change(self, *args):
        """Behandelt Änderungen der eingegebenen zeichenweisen Verzögerung."""
        self.gui.options_panel.update_delay_settings(self.delay_mode_var.get(), self.char_delay_entry.get())
        logger.info(f"Zeichenverzögerung geändert auf: {self.char_delay_entry.get()} ms")

    @handle_exceptions
    def update_text_options(self, *args):
        """Aktualisiert die Textgröße und Schriftart basierend auf den ausgewählten Werten."""
        try:
            new_size = int(self.size_var.get())
            new_font = self.font_var.get()
            self.transcription_panel.set_font(new_font, new_size)
            logger.info(f"Textoptionen aktualisiert: Schriftart={new_font}, Größe={new_size}")
        except ValueError:
            logger.warning("Ungültige Eingabe für Textgröße")

    @handle_exceptions
    def scroll_font(self, direction):
        """
        Scrollt durch die verfügbaren Schriftarten.

        :param direction: 1 für vorwärts, -1 für rückwärts
        """
        current_font = self.font_var.get()
        current_index = self.available_fonts.index(current_font)
        new_index = (current_index + direction) % len(self.available_fonts)
        new_font = self.available_fonts[new_index]
        self.font_var.set(new_font)  # Aktualisiert die Combobox
        logger.debug(f"Schriftart geändert zu: {new_font}")

    @handle_exceptions
    def on_save_test_recording_change(self):
        """
        Behandelt Änderungen der Testaufnahme-Einstellung.
        Speichert die neue Einstellung und aktualisiert die Konfiguration.
        """
        new_value = self.save_test_recording_var.get()
        self.gui.settings_manager.set_setting("save_test_recording", new_value)
        logger.info(f"Testaufnahme-Einstellung geändert: {new_value}")

    @handle_exceptions
    def on_incognito_change(self):
        """
        Behandelt Änderungen der Incognito-Modus-Einstellung.
        Speichert die neue Einstellung und aktualisiert die Konfiguration.
        """
        new_value = self.incognito_var.get()
        self.gui.settings_manager.set_setting("incognito_mode", new_value)
        logger.info(f"Incognito-Modus geändert: {new_value}")

@handle_exceptions
def get_current_settings(self):
    """
    Erfasst die aktuellen Einstellungen.

    :return: Ein Dictionary mit den aktuellen Einstellungen
    """
    settings = {
        "theme": self.theme_manager.current_theme.get(),
        "font_size": self.transcription_panel.get_font_size(),
        "font_family": self.transcription_panel.get_font_family(),
        "save_test_recording": self.gui.settings_manager.get_setting("save_test_recording", False),
        "incognito_mode": self.gui.settings_manager.get_setting("incognito_mode", DEFAULT_INCOGNITO_MODE),
        "text_fg": self.theme_manager.text_fg.get(),
        "text_bg": self.theme_manager.text_bg.get(),
        "select_fg": self.theme_manager.select_fg.get(),
        "select_bg": self.theme_manager.select_bg.get(),
        "highlight_fg": self.theme_manager.highlight_fg.get(),
        "highlight_bg": self.theme_manager.highlight_bg.get(),
        "push_to_talk_key": self.gui.settings_manager.get_setting("push_to_talk_key", DEFAULT_PUSH_TO_TALK_KEY),
        "delay_settings": {
            "delay_mode": self.gui.settings_manager.get_setting("delay_mode", "no_delay"),
            "char_delay": self.gui.settings_manager.get_setting("char_delay", DEFAULT_CHAR_DELAY)
        }
    }
    logger.debug("Aktuelle Einstellungen erfasst")
    return settings

    @handle_exceptions
    def undo_changes(self):
        """Setzt alle Änderungen auf den Stand zurück, als das Fenster geöffnet wurde."""
        # Theme zurücksetzen
        self.theme_manager.change_theme(self.initial_settings["theme"])

        # Schriftart und -größe zurücksetzen
        self.transcription_panel.set_font(self.initial_settings["font_family"], self.initial_settings["font_size"])
        self.size_var.set(str(self.initial_settings["font_size"]))
        self.font_var.set(self.initial_settings["font_family"])

        # Testaufnahme- und Incognito-Einstellungen zurücksetzen
        self.save_test_recording_var.set(self.initial_settings["save_test_recording"])
        self.incognito_var.set(self.initial_settings["incognito_mode"])

        # Audiogeräteeinstellungen zurücksetzen
        self.audio_options_panel.undo_changes()

        # Farbeinstellungen zurücksetzen
        color_settings = ['text_fg', 'text_bg', 'select_fg', 'select_bg', 'highlight_fg', 'highlight_bg']
        for setting in color_settings:
            initial_color = self.initial_settings[setting]
            getattr(self.theme_manager, setting).set(initial_color)
            self.gui.settings_manager.set_setting(setting, initial_color)
            preview_attr = f"{setting.replace('_', '')}_preview"
            if hasattr(self, preview_attr):
                getattr(self, preview_attr).config(bg=initial_color)

        # Verzögerungseinstellungen zurücksetzen
        initial_delay_settings = self.initial_settings.get("delay_settings", {})
        self.delay_mode_var.set(initial_delay_settings.get("delay_mode", "no_delay"))
        self.char_delay_entry.delete(0, tk.END)
        self.char_delay_entry.insert(0, str(initial_delay_settings.get("char_delay", DEFAULT_CHAR_DELAY)))
        self.gui.options_panel.update_delay_settings(
            initial_delay_settings.get("delay_mode", "no_delay"),
            initial_delay_settings.get("char_delay", DEFAULT_CHAR_DELAY)
        )

        # Shortcut zurücksetzen
        initial_shortcut = self.initial_settings.get("push_to_talk_key", DEFAULT_PUSH_TO_TALK_KEY)
        self.shortcut_panel.current_shortcut.set(initial_shortcut)
        self.gui.input_processor.update_shortcut(initial_shortcut)

        # Alle Einstellungen im SettingsManager zurücksetzen
        for key, value in self.initial_settings.items():
            if key not in ['delay_settings']:  # Spezielle Behandlung für verschachtelte Einstellungen
                self.gui.settings_manager.set_setting(key, value)

        # GUI-Elemente aktualisieren
        self.gui.theme_manager.update_colors()
        self.gui.main_window.update_status_bar()

        logger.info("Alle Änderungen rückgängig gemacht")

    @handle_exceptions
    def load_window_geometry(self):
        """Lädt die gespeicherte Fenstergröße und -position."""
        geometry = self.gui.settings_manager.get_setting("options_window_geometry")
        if geometry:
            self.geometry(geometry)
            logger.debug(f"Gespeicherte Fenstergeometrie geladen: {geometry}")
        else:
            # Wenn keine gespeicherte Geometrie vorhanden ist, zentriere das Fenster
            self.update_idletasks()
            width = self.winfo_width()
            height = self.winfo_height()
            x = (self.winfo_screenwidth() // 2) - (width // 2)
            y = (self.winfo_screenheight() // 2) - (height // 2)
            self.geometry('{}x{}+{}+{}'.format(width, height, x, y))
            logger.debug("Fenster zentriert (keine gespeicherte Geometrie)")

    @handle_exceptions
    def on_closing(self):
        """Wird aufgerufen, wenn das Fenster geschlossen wird."""
        # Speichere die aktuelle Fenstergröße und -position
        self.gui.settings_manager.set_setting("options_window_geometry", self.geometry())

        # Speichere alle aktuellen Farbeinstellungen
        color_settings = ['text_fg', 'text_bg', 'select_fg', 'select_bg', 'highlight_fg', 'highlight_bg']
        for setting in color_settings:
            current_color = getattr(self.theme_manager, setting).get()
            self.gui.settings_manager.set_setting(setting, current_color)

        self.gui.main_window.update_status_bar()
        logger.info("Optionsfenster geschlossen, Einstellungen gespeichert")
        self.destroy()

# Zusätzliche Erklärungen:

# 1. Shortcut-Panel Integration:
#    Das neue ShortcutPanel wurde als separater Tab im Optionsfenster hinzugefügt.
#    Es ermöglicht die Anpassung des Push-to-Talk-Shortcuts.

# 2. Erweiterung der Einstellungen:
#    Die Methode get_current_settings wurde um den push_to_talk_key erweitert,
#    um die aktuelle Shortcut-Einstellung zu erfassen.

# 3. Rückgängig-Funktion:
#    Die undo_changes Methode wurde aktualisiert, um auch den Shortcut
#    auf den ursprünglichen Wert zurückzusetzen.

# 4. Fehlerbehandlung und Logging:
#    Alle Methoden verwenden weiterhin den @handle_exceptions Decorator
#    für konsistente Fehlerbehandlung und Logging.

# Diese Implementierung integriert die neue Shortcut-Funktionalität nahtlos
# in das bestehende Optionsfenster und behält dabei die Struktur und
# den Stil der vorhandenen Komponenten bei.
