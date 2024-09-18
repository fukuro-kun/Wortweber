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
Dieses Modul definiert das Optionsfenster für die Wortweber-Anwendung.
Es ermöglicht die Anpassung von Theme, Textoptionen und Testaufnahme-Einstellungen.
"""

# Standardbibliotheken
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

# Drittanbieterbibliotheken
from tkcolorpicker import askcolor

# Projektspezifische Module
from src.config import DEFAULT_FONT_FAMILY, DEFAULT_FONT_SIZE, DEFAULT_INCOGNITO_MODE
from src.utils.error_handling import handle_exceptions, logger

class OptionsWindow(tk.Toplevel):
    """
    Fenster für erweiterte Optionen in der Wortweber-Anwendung.
    Ermöglicht die Anpassung von Theme, Textoptionen und Testaufnahme-Einstellungen.
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
    def on_save_test_recording_change(self):
        """
        Behandelt Änderungen der Testaufnahme-Einstellung.
        Speichert die neue Einstellung und aktualisiert die Konfiguration.
        """
        new_value = self.save_test_recording_var.get()
        self.gui.settings_manager.set_setting("save_test_recording", new_value)
        self.gui.settings_manager.save_settings()
        logger.info(f"Testaufnahme-Einstellung geändert: {new_value}")

    @handle_exceptions
    def on_incognito_change(self):
        """
        Behandelt Änderungen der Incognito-Modus-Einstellung.
        Speichert die neue Einstellung und aktualisiert die Konfiguration.
        """
        new_value = self.incognito_var.get()
        self.gui.settings_manager.set_setting("incognito_mode", new_value)
        self.gui.settings_manager.save_settings()
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
            "highlight_bg": self.theme_manager.highlight_bg.get()
        }
        logger.debug("Aktuelle Einstellungen erfasst")
        return settings

    @handle_exceptions
    def create_color_row(self, parent, label, fg_var, bg_var, row):
        """
        Erstellt eine Reihe von UI-Elementen für die Farbauswahl einer Textkategorie.

        :param parent: Das übergeordnete Widget
        :param label: Beschriftung für die Textkategorie
        :param fg_var: StringVar für die Textfarbe
        :param bg_var: StringVar für die Hintergrundfarbe
        :param row: Zeilennummer im Grid-Layout
        """
        fg_preview = tk.Frame(parent, width=30, height=30, bg=fg_var.get())
        fg_preview.grid(row=row, column=0, padx=(5, 2), pady=5, sticky="w")
        fg_preview.bind("<Button-1>", lambda e: self.choose_color(fg_var, fg_preview))

        preview_text = tk.Text(parent, width=40, height=1, font=("TkDefaultFont", 10))
        preview_text.grid(row=row, column=1, padx=2, pady=5, sticky="ew")
        preview_text.insert(tk.END, f"Vorschau: {label}")
        preview_text.config(state=tk.DISABLED, fg=fg_var.get(), bg=bg_var.get())

        bg_preview = tk.Frame(parent, width=30, height=30, bg=bg_var.get())
        bg_preview.grid(row=row, column=2, padx=(2, 5), pady=5, sticky="e")
        bg_preview.bind("<Button-1>", lambda e: self.choose_color(bg_var, bg_preview))

        fg_var.trace_add("write", lambda *args: self.update_preview(preview_text, fg_var, bg_var))
        bg_var.trace_add("write", lambda *args: self.update_preview(preview_text, fg_var, bg_var))

        # Speichern der Referenzen zu den Vorschau-Frames
        setattr(self, f"{label.lower().replace(' ', '_')}_fg_preview", fg_preview)
        setattr(self, f"{label.lower().replace(' ', '_')}_bg_preview", bg_preview)

        logger.debug(f"Farbreihe für {label} erstellt")

    @handle_exceptions
    def update_preview(self, preview_text, fg_var, bg_var):
        """
        Aktualisiert die Vorschau-Textfelder mit den ausgewählten Farben.

        :param preview_text: Das Vorschau-Textfeld
        :param fg_var: StringVar für die Textfarbe
        :param bg_var: StringVar für die Hintergrundfarbe
        """
        try:
            if preview_text.winfo_exists():
                preview_text.config(fg=fg_var.get(), bg=bg_var.get())
                logger.debug("Vorschau-Text aktualisiert")
        except tk.TclError:
            # Widget wurde zerstört, ignoriere den Fehler
            logger.debug("Vorschau-Widget existiert nicht mehr")

    @handle_exceptions
    def choose_color(self, color_var, preview_frame):
        """
        Öffnet den Farbauswahldialog und aktualisiert die gewählte Farbe.

        :param color_var: Die StringVar, die die Farbe speichert
        :param preview_frame: Das Frame, das die Farbvorschau anzeigt
        """
        try:
            if preview_frame.winfo_exists():
                current_color = color_var.get()
                color = askcolor(color=current_color, title="Wähle eine Farbe")
                if color[1]:
                    color_var.set(color[1])
                    preview_frame.config(bg=color[1])
                    setting_name = str(color_var).split('.')[-1]  # Extrahiere den Namen der Variablen
                    self.gui.settings_manager.set_setting(setting_name, color[1])
                    self.gui.settings_manager.save_settings()
                    self.gui.theme_manager.update_colors()
                    logger.info(f"Farbe für {setting_name} auf {color[1]} geändert")
        except tk.TclError:
            logger.warning("Farbauswahl-Widget existiert nicht mehr")

    @handle_exceptions
    def undo_changes(self):
        """Setzt alle Änderungen auf den Stand zurück, als das Fenster geöffnet wurde."""
        self.theme_manager.change_theme(self.initial_settings["theme"])
        self.transcription_panel.set_font(self.initial_settings["font_family"], self.initial_settings["font_size"])
        self.save_test_recording_var.set(self.initial_settings["save_test_recording"])
        self.incognito_var.set(self.initial_settings["incognito_mode"])

        # Aktualisiere die UI-Elemente
        self.size_var.set(str(self.initial_settings["font_size"]))
        self.font_var.set(self.initial_settings["font_family"])
        self.theme_manager.current_theme.set(self.initial_settings["theme"])

        # Setze die Farbeinstellungen zurück und aktualisiere die Vorschau
        color_settings = ['text_fg', 'text_bg', 'select_fg', 'select_bg', 'highlight_fg', 'highlight_bg']
        for setting in color_settings:
            getattr(self.theme_manager, setting).set(self.initial_settings[setting])
            preview_attr = f"{setting.replace('_', '')}_preview"
            if hasattr(self, preview_attr):
                getattr(self, preview_attr).config(bg=self.initial_settings[setting])

        # Aktualisiere die Einstellungen im SettingsManager
        for key, value in self.initial_settings.items():
            self.gui.settings_manager.set_setting(key, value)
        self.gui.settings_manager.save_settings()

        # Aktualisiere die Farben in der GUI
        self.theme_manager.update_colors()

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

        self.gui.settings_manager.save_settings()
        logger.info("Optionsfenster geschlossen, Einstellungen gespeichert")
        self.destroy()

# Zusätzliche Erklärungen:

# 1. Incognito-Modus:
#    Die neue Checkbox für den Incognito-Modus wurde in setup_test_recording_options hinzugefügt.
#    Sie ermöglicht es dem Benutzer, die Protokollierung von Transkriptionsergebnissen zu steuern.

# 2. Einstellungspersistenz:
#    Alle Einstellungen, einschließlich des Incognito-Modus, werden beim Schließen des Fensters gespeichert.
#    Dies gewährleistet, dass die Benutzereinstellungen über Neustarts der Anwendung hinweg erhalten bleiben.

# 3. Rückgängig-Funktionalität:
#    Die undo_changes Methode wurde aktualisiert, um auch den Incognito-Modus zurückzusetzen.
#    Dies ermöglicht es dem Benutzer, alle Änderungen auf einmal rückgängig zu machen.

# 4. Fehlerbehandlung und Logging:
#    Jede Methode ist mit dem @handle_exceptions Decorator versehen, was eine einheitliche
#    Fehlerbehandlung in der gesamten Klasse gewährleistet. Ausführliche Logging-Aufrufe
#    wurden implementiert, um die Nachvollziehbarkeit von Aktionen und potenziellen Problemen zu verbessern.

# 5. Fenstergeometrie:
#    Die Methoden load_window_geometry und on_closing stellen sicher, dass die Größe und Position
#    des Optionsfensters zwischen den Sitzungen beibehalten werden, was die Benutzererfahrung verbessert.

# 6. Modulare Struktur:
#    Die Klasse ist in klar definierte Methoden unterteilt, was die Wartbarkeit und Lesbarkeit des Codes verbessert.
#    Jede Methode hat eine spezifische Verantwortlichkeit, was dem Prinzip der Einzelverantwortung entspricht.

# Diese Implementierung bietet eine umfassende und benutzerfreundliche Oberfläche für die Verwaltung
# verschiedener Anwendungseinstellungen, einschließlich des neuen Incognito-Modus, und gewährleistet
# gleichzeitig die Persistenz und Wiederherstellbarkeit aller Einstellungen.
