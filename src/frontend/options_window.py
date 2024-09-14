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
from src.config import DEFAULT_FONT_FAMILY, DEFAULT_FONT_SIZE

class OptionsWindow(tk.Toplevel):
    """
    Fenster für erweiterte Optionen in der Wortweber-Anwendung.
    Ermöglicht die Anpassung von Theme, Textoptionen und Testaufnahme-Einstellungen.
    """

    _instance = None

    @classmethod
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

    def setup_styles(self):
        """Richtet benutzerdefinierte Stile für die UI-Elemente ein."""
        style = ttk.Style()
        style.configure('Square.TButton', width=3, padding=0)

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

    def update_text_options(self, *args):
        """Aktualisiert die Textgröße und Schriftart basierend auf den ausgewählten Werten."""
        try:
            new_size = int(self.size_var.get())
            new_font = self.font_var.get()
            self.transcription_panel.set_font(new_font, new_size)
        except ValueError:
            pass  # Ignoriere ungültige Eingaben

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

    def setup_test_recording_options(self, parent):
        """
        Richtet die Optionen für die Testaufnahme ein.

        :param parent: Das übergeordnete Frame für die Testaufnahmeoptionen
        """
        self.save_test_recording_var = tk.BooleanVar(value=self.gui.settings_manager.get_setting("save_test_recording", False))
        ttk.Checkbutton(parent, text="Letzte Aufnahme als Testdatei speichern",
                        variable=self.save_test_recording_var,
                        command=self.on_save_test_recording_change).pack(pady=10)

    def on_save_test_recording_change(self):
        """
        Behandelt Änderungen der Testaufnahme-Einstellung.
        Speichert die neue Einstellung und aktualisiert die Konfiguration.
        """
        self.gui.settings_manager.set_setting("save_test_recording", self.save_test_recording_var.get())
        self.gui.settings_manager.save_settings()

    def get_current_settings(self):
        """
        Erfasst die aktuellen Einstellungen.

        :return: Ein Dictionary mit den aktuellen Einstellungen
        """
        return {
            "theme": self.theme_manager.current_theme.get(),
            "font_size": self.transcription_panel.get_font_size(),
            "font_family": self.transcription_panel.get_font_family(),
            "save_test_recording": self.gui.settings_manager.get_setting("save_test_recording", False),
            "text_fg": self.theme_manager.text_fg.get(),
            "text_bg": self.theme_manager.text_bg.get(),
            "select_fg": self.theme_manager.select_fg.get(),
            "select_bg": self.theme_manager.select_bg.get(),
            "highlight_fg": self.theme_manager.highlight_fg.get(),
            "highlight_bg": self.theme_manager.highlight_bg.get()
        }

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
        except tk.TclError:
            # Widget wurde zerstört, ignoriere den Fehler
            pass

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
        except tk.TclError:
            pass

    def undo_changes(self):
        """Setzt alle Änderungen auf den Stand zurück, als das Fenster geöffnet wurde."""
        self.theme_manager.change_theme(self.initial_settings["theme"])
        self.transcription_panel.set_font(self.initial_settings["font_family"], self.initial_settings["font_size"])
        self.save_test_recording_var.set(self.initial_settings["save_test_recording"])

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

    def load_window_geometry(self):
        """Lädt die gespeicherte Fenstergröße und -position."""
        geometry = self.gui.settings_manager.get_setting("options_window_geometry")
        if geometry:
            self.geometry(geometry)
        else:
            # Wenn keine gespeicherte Geometrie vorhanden ist, zentriere das Fenster
            self.update_idletasks()
            width = self.winfo_width()
            height = self.winfo_height()
            x = (self.winfo_screenwidth() // 2) - (width // 2)
            y = (self.winfo_screenheight() // 2) - (height // 2)
            self.geometry('{}x{}+{}+{}'.format(width, height, x, y))

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
        self.destroy()

# Zusätzliche Erklärungen:

# 1. Speichern der Fenstergröße und -position:
#    - Die Methode load_window_geometry() lädt die gespeicherte Geometrie beim Öffnen des Fensters.
#    - Die Methode on_closing() speichert die aktuelle Geometrie beim Schließen des Fensters.

# 2. Erweiterung der Rückgängig-Funktionalität:
#    - get_current_settings() erfasst nun auch die Farbeinstellungen.
#    - undo_changes() setzt jetzt auch die Farbeinstellungen zurück und aktualisiert die GUI entsprechend.

# 3. Aktualisierung der Farben:
#    - Nach dem Zurücksetzen der Farben wird theme_manager.update_colors() aufgerufen,
#      um die Änderungen in der gesamten GUI zu reflektieren.

# Diese Implementierung stellt sicher, dass die Fenstergröße und -position gespeichert werden
# und dass der Rückgängig-Button für alle Bereiche des Optionsmenüs funktioniert, einschließlich
# der Farbeinstellungen.
