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

import ttkthemes
import tkinter as tk
from tkinter import ttk
from tkcolorpicker import askcolor

class ThemeManager:
    """
    Verwaltet die Themes und Farbeinstellungen der Wortweber-Anwendung.
    Ermöglicht das Ändern und Speichern von Themes sowie die Erstellung einer Theme-Auswahl-GUI.
    """

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
        self.current_theme = tk.StringVar(value=self.themes[self.current_theme_index])

        # Farbvariablen initialisieren
        self.text_bg = tk.StringVar(value=self.settings_manager.get_setting("text_bg", "white"))
        self.text_fg = tk.StringVar(value=self.settings_manager.get_setting("text_fg", "black"))
        self.select_bg = tk.StringVar(value=self.settings_manager.get_setting("select_bg", "lightblue"))
        self.select_fg = tk.StringVar(value=self.settings_manager.get_setting("select_fg", "black"))

        self.gui = None

    def set_gui(self, gui):
        """
        Setzt die Referenz zur Hauptanwendung.

        :param gui: Referenz zur Hauptanwendung (WordweberGUI-Instanz)
        """
        self.gui = gui

    def setup_theme_selection(self, parent):
        """
        Erstellt die GUI-Elemente für die Theme- und Farbauswahl.

        :param parent: Das übergeordnete Widget, in dem die Auswahlelemente platziert werden
        """
        theme_frame = ttk.LabelFrame(parent, text="Themes und Farben", padding="10")
        theme_frame.pack(fill=tk.X, pady=5)

        ttk.Label(theme_frame, text="Theme:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.theme_dropdown = ttk.Combobox(theme_frame, textvariable=self.current_theme, values=self.themes, state="readonly", width=15)
        self.theme_dropdown.grid(row=0, column=1, padx=5, pady=5)
        self.theme_dropdown.bind("<<ComboboxSelected>>", self.on_theme_change)

        ttk.Button(theme_frame, text="Textfarbe", command=lambda: self.choose_color('text_fg')).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(theme_frame, text="Texthintergrund", command=lambda: self.choose_color('text_bg')).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(theme_frame, text="Auswahlfarbe", command=lambda: self.choose_color('select_fg')).grid(row=2, column=0, padx=5, pady=5)
        ttk.Button(theme_frame, text="Auswahlhintergrund", command=lambda: self.choose_color('select_bg')).grid(row=2, column=1, padx=5, pady=5)

    def on_theme_change(self, event=None):
        """
        Wird aufgerufen, wenn ein neues Theme ausgewählt wird.
        Ändert das aktuelle Theme der Anwendung.
        """
        selected_theme = self.current_theme.get()
        self.change_theme(selected_theme)

    def change_theme(self, theme_name):
        """
        Ändert das aktuelle Theme der Anwendung.

        :param theme_name: Der Name des neuen Themes
        """
        self.root.set_theme(theme_name)
        self.current_theme.set(theme_name)
        self.settings_manager.set_setting("theme", theme_name)

    def choose_color(self, target):
        """
        Öffnet den Farbauswahldialog und aktualisiert die gewählte Farbe.

        :param target: Der Zielbereich für die Farbänderung ('text_fg', 'text_bg', 'select_fg', oder 'select_bg')
        """
        current_color = getattr(self, target).get()
        color = askcolor(color=current_color, title=f"Wähle eine Farbe für {target}")
        if color[1]:
            getattr(self, target).set(color[1])
            self.settings_manager.set_setting(target, color[1])
            self.update_colors()

    def update_colors(self):
        """
        Aktualisiert die Farben im Transkriptionsfenster.
        """
        if self.gui:
            self.gui.update_colors()
        else:
            print("Warnung: GUI-Referenz nicht gesetzt. Farben werden nicht aktualisiert.")

    def apply_saved_theme(self):
        """
        Wendet das gespeicherte Theme und die gespeicherten Farben an.
        """
        saved_theme = self.settings_manager.get_setting("theme")
        if saved_theme in self.themes:
            self.change_theme(saved_theme)
        else:
            self.change_theme(self.themes[0])

        # Gespeicherte Farben anwenden
        for color_setting in ['text_bg', 'text_fg', 'select_bg', 'select_fg']:
            saved_color = self.settings_manager.get_setting(color_setting)
            if saved_color:
                getattr(self, color_setting).set(saved_color)

        self.update_colors()

# Zusätzliche Erklärungen:

# 1. Die Klasse ThemeManager zentralisiert alle Funktionen zur Verwaltung von Themes und Farben.
# 2. Die Methode setup_theme_selection erstellt eine benutzerfreundliche Oberfläche zur Auswahl von Themes und Farben.
# 3. Die choose_color Methode verwendet den tkcolorpicker für eine verbesserte Farbauswahl-Erfahrung.
# 4. Die update_colors Methode ruft die entsprechende Methode in der Hauptanwendung auf.
# 5. Die apply_saved_theme Methode stellt sicher, dass beim Start der Anwendung die zuvor
#    gespeicherten Theme- und Farbeinstellungen angewendet werden.
# 6. Alle Farbeinstellungen werden im settings_manager gespeichert, um sie zwischen Sitzungen beizubehalten.
