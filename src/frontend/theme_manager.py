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

import ttkthemes
import tkinter as tk
from tkinter import ttk

class ThemeManager:
    """
    Verwaltet die Themes der Wortweber-Anwendung.
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

    def setup_theme_selection(self, parent):
        """
        Erstellt die GUI-Elemente für die Theme-Auswahl.

        :param parent: Das übergeordnete Widget, in dem die Theme-Auswahl platziert wird
        """
        theme_frame = tk.Frame(parent)
        theme_frame.pack(fill=tk.X, pady=5)

        ttk.Label(theme_frame, text="Theme:").pack(side=tk.LEFT, padx=(0, 5))
        self.theme_dropdown = ttk.Combobox(theme_frame, textvariable=self.current_theme, values=self.themes, state="readonly", width=15)
        self.theme_dropdown.pack(side=tk.LEFT)
        self.theme_dropdown.bind("<<ComboboxSelected>>", self.on_theme_change)

        ttk.Button(theme_frame, text="Vorheriges Theme", command=self.previous_theme).pack(side=tk.LEFT, padx=5)
        ttk.Button(theme_frame, text="Nächstes Theme", command=self.next_theme).pack(side=tk.LEFT)

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

    def next_theme(self):
        """Wechselt zum nächsten verfügbaren Theme."""
        self.current_theme_index = (self.current_theme_index + 1) % len(self.themes)
        self.change_theme(self.themes[self.current_theme_index])

    def previous_theme(self):
        """Wechselt zum vorherigen verfügbaren Theme."""
        self.current_theme_index = (self.current_theme_index - 1) % len(self.themes)
        self.change_theme(self.themes[self.current_theme_index])

    def apply_saved_theme(self):
        """
        Wendet das gespeicherte Theme an oder verwendet das erste verfügbare Theme,
        wenn kein gültiges Theme gespeichert ist.
        """
        saved_theme = self.settings_manager.get_setting("theme")
        if saved_theme in self.themes:
            self.change_theme(saved_theme)
        else:
            self.change_theme(self.themes[0])

# Zusätzliche Erklärungen:

# 1. ttkthemes:
#    Diese Bibliothek erweitert die Standard-Tkinter-Themes um eine Vielzahl zusätzlicher Optionen.
#    Sie ermöglicht es, das Aussehen der Anwendung erheblich zu verbessern und anzupassen.

# 2. Zyklische Theme-Navigation:
#    Die Methoden next_theme und previous_theme implementieren eine zyklische Navigation durch die Themes.
#    Dies ermöglicht es dem Benutzer, einfach durch alle verfügbaren Themes zu blättern.

# 3. Persistenz der Theme-Auswahl:
#    Durch die Verwendung des settings_manager wird die Theme-Auswahl des Benutzers gespeichert
#    und bei erneutem Start der Anwendung wiederhergestellt.

# 4. Fehlertoleranz:
#    Die apply_saved_theme-Methode überprüft, ob das gespeicherte Theme gültig ist,
#    bevor es angewendet wird. Dies verhindert Fehler, falls ein nicht mehr verfügbares Theme gespeichert wurde.

# 5. Separation of Concerns:
#    Durch die Auslagerung der Theme-Verwaltung in eine eigene Klasse wird der Code modularer
#    und leichter zu warten. Es erleichtert auch zukünftige Erweiterungen der Theme-Funktionalität.

# 6. Benutzerfreundlichkeit:
#    Die Kombination aus Dropdown-Menü und Vor-/Zurück-Buttons bietet verschiedene intuitive Möglichkeiten
#    zur Theme-Auswahl, was die Benutzerfreundlichkeit erhöht.
