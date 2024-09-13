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

import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

class OptionsWindow(tk.Toplevel):
    """
    Fenster für erweiterte Optionen in der Wortweber-Anwendung.
    Ermöglicht die Anpassung von Theme und Textgröße.
    """

    def __init__(self, parent, theme_manager, transcription_panel):
        """
        Initialisiert das OptionsWindow.

        :param parent: Das übergeordnete Tkinter-Fenster
        :param theme_manager: Instanz des ThemeManagers zur Verwaltung der Themes
        :param transcription_panel: Referenz auf das TranscriptionPanel für Textgrößenänderungen
        """
        super().__init__(parent)
        self.title("Erweiterte Optionen")
        self.theme_manager = theme_manager
        self.transcription_panel = transcription_panel
        self.setup_ui()

    def setup_ui(self):
        """Richtet die Benutzeroberfläche für das OptionsWindow ein."""
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Theme-Einstellungen
        theme_frame = ttk.Frame(notebook)
        notebook.add(theme_frame, text="Theme")
        self.theme_manager.setup_theme_selection(theme_frame)

        # Textgröße-Einstellungen
        text_size_frame = ttk.Frame(notebook)
        notebook.add(text_size_frame, text="Textgröße")
        self.setup_text_size_options(text_size_frame)

        ttk.Button(self, text="Schließen", command=self.destroy).pack(pady=10)

    def setup_text_size_options(self, parent):
        """
        Richtet die Optionen zur Anpassung der Textgröße ein.

        :param parent: Das übergeordnete Frame für die Textgrößenoptionen
        """
        ttk.Label(parent, text="Textgröße:").pack(pady=(10, 5))
        size_var = tk.StringVar(value=str(self.transcription_panel.get_font_size()))
        size_spinbox = ttk.Spinbox(parent, from_=8, to=24, textvariable=size_var, width=5)
        size_spinbox.pack()

        def update_size():
            """Aktualisiert die Textgröße basierend auf dem Spinbox-Wert."""
            try:
                new_size = int(size_var.get())
                self.transcription_panel.set_font_size(new_size)
            except ValueError:
                pass  # Ignoriere ungültige Eingaben

        ttk.Button(parent, text="Anwenden", command=update_size).pack(pady=(5, 10))

# Zusätzliche Erklärungen:

# 1. Toplevel-Fenster:
#    OptionsWindow erbt von tk.Toplevel, was ein separates Fenster erstellt, das vom Hauptfenster abhängig ist.
#    Dies ist nützlich für Einstellungen oder Dialoge, die nicht ständig sichtbar sein müssen.

# 2. Notebook-Widget:
#    ttk.Notebook wird verwendet, um verschiedene Einstellungskategorien in Tabs zu organisieren.
#    Dies verbessert die Übersichtlichkeit und Benutzerfreundlichkeit bei vielen Optionen.

# 3. Delegation der Theme-Einstellungen:
#    Die Theme-Einstellungen werden an den theme_manager delegiert, was eine gute Trennung der Zuständigkeiten zeigt.

# 4. Textgrößenanpassung:
#    Die Textgrößenanpassung verwendet ein Spinbox-Widget, das eine einfache numerische Eingabe ermöglicht.
#    Die update_size-Funktion stellt sicher, dass nur gültige Werte angewendet werden.

# 5. Modularität:
#    Durch die Aufteilung in separate Methoden (setup_ui, setup_text_size_options) bleibt der Code übersichtlich
#    und ermöglicht einfache Erweiterungen um zusätzliche Optionen in der Zukunft.

# 6. Fehlerbehandlung:
#    Die try-except-Struktur in update_size fängt potenzielle Fehler bei der Eingabe ungültiger Werte ab,
#    was die Robustheit der Anwendung erhöht.
