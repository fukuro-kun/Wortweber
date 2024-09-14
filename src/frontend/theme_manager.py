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
Dieses Modul verwaltet die Themes und Farbeinstellungen der Wortweber-Anwendung.
Es bietet Funktionen zum Ändern von Themes und zur Auswahl benutzerdefinierter Farben.
"""

# Standardbibliotheken
import tkinter as tk
from tkinter import ttk

# Drittanbieterbibliotheken
import ttkthemes
from tkcolorpicker import askcolor

# Projektspezifische Module
from src.config import DEFAULT_THEME
from src.utils.error_handling import handle_exceptions

class ThemeManager:
    """
    Verwaltet die Themes und Farbeinstellungen der Wortweber-Anwendung.
    Ermöglicht das Ändern und Speichern von Themes sowie die Erstellung einer Theme-Auswahl-GUI.
    """

    @handle_exceptions
    def __init__(self, root, settings_manager):
        """
        Initialisiert den ThemeManager.

        :param root: Das Haupt-Tkinter-Fenster
        :param settings_manager: Instanz des SettingsManager zur Verwaltung der Einstellungen
        """
        self.root = root
        self.settings_manager = settings_manager
        self.themes = sorted(ttkthemes.THEMES)
        self.current_theme_index = 0
        self.current_theme = tk.StringVar(value=self.settings_manager.get_setting("theme", DEFAULT_THEME))

        # Farbvariablen initialisieren
        self.text_bg = tk.StringVar(value=self.settings_manager.get_setting("text_bg", "white"))
        self.text_fg = tk.StringVar(value=self.settings_manager.get_setting("text_fg", "black"))
        self.select_bg = tk.StringVar(value=self.settings_manager.get_setting("select_bg", "lightblue"))
        self.select_fg = tk.StringVar(value=self.settings_manager.get_setting("select_fg", "black"))
        self.highlight_bg = tk.StringVar(value=self.settings_manager.get_setting("highlight_bg", "yellow"))
        self.highlight_fg = tk.StringVar(value=self.settings_manager.get_setting("highlight_fg", "black"))

        self.gui = None

    @handle_exceptions
    def set_gui(self, gui):
        """
        Setzt die Referenz zur Hauptanwendung.

        :param gui: Referenz zur Hauptanwendung (WordweberGUI-Instanz)
        """
        self.gui = gui

    @handle_exceptions
    def setup_theme_selection(self, parent):
        """
        Erstellt die GUI-Elemente für die Theme- und Farbauswahl.

        :param parent: Das übergeordnete Widget, in dem die Auswahlelemente platziert werden
        """
        theme_frame = ttk.LabelFrame(parent, text="Themes und Farben", padding="10")
        theme_frame.pack(fill=tk.X, pady=5)

        theme_label = ttk.Label(theme_frame, text="Theme:")
        theme_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.theme_dropdown = ttk.Combobox(theme_frame, textvariable=self.current_theme, values=self.themes, width=15, state="readonly")
        self.theme_dropdown.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
        self.theme_dropdown.bind("<<ComboboxSelected>>", self.on_theme_change)

        # Verbesserte Ereignisbehandlung für das Dropdown-Menü
        self.theme_dropdown.bind("<FocusIn>", self.on_dropdown_focus)
        self.theme_dropdown.bind("<KeyPress>", self.handle_keypress)
        self.theme_dropdown.bind("<Button-1>", self.handle_dropdown_click)

        # Mache das Label klickbar, um das Dropdown-Menü zu fokussieren
        theme_label.bind("<Button-1>", lambda e: self.theme_dropdown.focus_set())

        color_settings = ['text_fg', 'text_bg', 'select_fg', 'select_bg', 'highlight_fg', 'highlight_bg']
        color_labels = ["Normaler Text", "Ausgewählter Text", "Neuer Text"]
        for i, label in enumerate(color_labels):
            self.create_color_row(theme_frame, label, getattr(self, color_settings[i*2]), getattr(self, color_settings[i*2+1]), i+1)

        # Konfiguriere die Spaltengewichtung für das gesamte Frame
        theme_frame.columnconfigure(1, weight=1)

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
        except tk.TclError:
            # Widget wurde zerstört, ignoriere den Fehler
            pass

    @handle_exceptions
    def on_dropdown_focus(self, event):
        """Wird aufgerufen, wenn das Dropdown-Menü den Fokus erhält."""
        try:
            if self.theme_dropdown.winfo_exists():
                current_theme = self.current_theme.get()
                if current_theme in self.themes:
                    index = self.themes.index(current_theme)
                    self.theme_dropdown.current(index)
        except tk.TclError:
            pass
        return "break"

    @handle_exceptions
    def handle_keypress(self, event):
        """Behandelt Tastatureingaben im Dropdown-Menü."""
        if event.keysym in ("Up", "Down"):
            self.navigate_theme(event)
            return "break"  # Verhindert das Standard-Verhalten
        return  # Erlaubt andere Tasten (z.B. für die Suche im Dropdown)

    @handle_exceptions
    def handle_dropdown_click(self, event):
        """Öffnet das Dropdown-Menü bei Klick."""
        if self.theme_dropdown.identify(event.x, event.y) == "arrow":
            # Öffne das Dropdown-Menü bei Klick auf den Pfeil
            self.theme_dropdown.event_generate('<Down>')
        else:
            # Fokussiere das Dropdown-Menü bei Klick anderswo
            self.theme_dropdown.focus_set()
        return "break"

    @handle_exceptions
    def navigate_theme(self, event):
        """Ermöglicht die Navigation durch die Themes mit den Pfeiltasten."""
        try:
            if self.theme_dropdown.winfo_exists():
                current_index = self.themes.index(self.current_theme.get())
                if event.keysym == "Up":
                    new_index = (current_index - 1) % len(self.themes)
                else:  # Down
                    new_index = (current_index + 1) % len(self.themes)
                self.current_theme.set(self.themes[new_index])
                self.on_theme_change()
        except tk.TclError:
            pass

    @handle_exceptions
    def on_theme_change(self, event=None):
        """
        Wird aufgerufen, wenn ein neues Theme ausgewählt wird.
        Ändert das aktuelle Theme der Anwendung.
        """
        try:
            if self.root.winfo_exists():
                selected_theme = self.current_theme.get()
                self.change_theme(selected_theme)
        except tk.TclError:
            pass

    @handle_exceptions
    def change_theme(self, theme_name):
        """
        Ändert das aktuelle Theme der Anwendung.

        :param theme_name: Der Name des neuen Themes
        """
        try:
            if self.root.winfo_exists():
                self.root.set_theme(theme_name)
                self.current_theme.set(theme_name)
                self.settings_manager.set_setting("theme", theme_name)
        except tk.TclError:
            pass

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
                    self.settings_manager.set_setting(setting_name, color[1])
                    self.settings_manager.save_settings()
                    self.update_colors()
        except tk.TclError:
            pass

    @handle_exceptions
    def update_colors(self):
        """
        Aktualisiert die Farben in der gesamten GUI.
        """
        if self.gui:
            try:
                # Aktualisiere die Farben im Transkriptionspanel
                self.gui.transcription_panel.update_colors(
                    text_fg=self.text_fg.get(),
                    text_bg=self.text_bg.get(),
                    select_fg=self.select_fg.get(),
                    select_bg=self.select_bg.get(),
                    highlight_fg=self.highlight_fg.get(),
                    highlight_bg=self.highlight_bg.get()
                )

                # Aktualisiere das Hauptfenster
                self.gui.root.update()

                # Informiere den Benutzer über die Aktualisierung
                print("Farben wurden aktualisiert.")
            except tk.TclError as e:
                print(f"Fehler beim Aktualisieren der Farben: {e}")
        else:
            print("Warnung: GUI-Referenz nicht gesetzt. Farben werden nicht aktualisiert.")

    @handle_exceptions
    def apply_saved_theme(self):
        """
        Wendet das gespeicherte Theme und die gespeicherten Farben an.
        """
        try:
            if self.root.winfo_exists():
                saved_theme = self.settings_manager.get_setting("theme")
                if saved_theme in self.themes:
                    self.change_theme(saved_theme)
                else:
                    self.change_theme(self.themes[0])

                # Gespeicherte Farben anwenden
                color_settings = ['text_fg', 'text_bg', 'select_fg', 'select_bg', 'highlight_fg', 'highlight_bg']
                for color_setting in color_settings:
                    saved_color = self.settings_manager.get_setting(color_setting)
                    if saved_color:
                        getattr(self, color_setting).set(saved_color)

                self.update_colors()
        except tk.TclError:
            pass

# Zusätzliche Erklärungen:

# 1. Dropdown-Menü-Verhalten:
#    Das Standardverhalten des Dropdown-Menüs wurde beibehalten, einschließlich des eingebauten Buttons.
#    Der Button lässt sich nicht gesondert ausblenden, da er Teil des Standard-Widgets ist.

# 2. Ereignisbehandlung:
#    Die Ereignisbehandlung wurde optimiert, um eine bessere Benutzererfahrung zu bieten,
#    insbesondere bei der Verwendung der Tastatur zur Navigation.

# 3. Farbauswahl:
#    Die Farbauswahl-Funktionalität ermöglicht es dem Benutzer, die Farben für verschiedene
#    Textkategorien individuell anzupassen.

# 4. Fehlerbehandlung:
#    Robuste Fehlerbehandlung wurde implementiert, um mögliche TclErrors abzufangen,
#    die auftreten können, wenn Widgets zerstört werden.

# 5. Einstellungspersistenz:
#    Alle Farbeinstellungen und das ausgewählte Theme werden über den SettingsManager
#    gespeichert und beim Neustart der Anwendung wiederhergestellt.

# Diese Implementierung bietet eine ausgewogene Mischung aus Funktionalität und Benutzerfreundlichkeit,
# während sie die Anforderungen an die Themenverwaltung und Farbauswahl erfüllt.
