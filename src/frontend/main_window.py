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
from src.frontend.transcription_panel import TranscriptionPanel
from src.frontend.options_panel import OptionsPanel
from src.frontend.status_panel import StatusPanel
from src.frontend.options_window import OptionsWindow

class MainWindow:
    """
    Hauptfenster der Wortweber-Anwendung.
    Koordiniert die verschiedenen UI-Komponenten und deren Layout.
    """

    def __init__(self, root, gui):
        """
        Initialisiert das Hauptfenster.

        :param root: Das root Tkinter-Fenster
        :param gui: Referenz auf die Hauptgui-Instanz
        """
        self.root = root
        self.gui = gui

        self.setup_ui()

    def setup_ui(self):
        """
        Richtet die Benutzeroberfläche ein, einschließlich aller Panels und Buttons.
        """
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.transcription_panel = TranscriptionPanel(main_frame, self.gui)
        self.options_panel = OptionsPanel(main_frame, self.gui)
        self.status_panel = StatusPanel(main_frame, self.gui)

        self.options_panel.grid(column=0, row=0, sticky="nw")
        self.status_panel.grid(column=1, row=0, sticky="ne")
        self.transcription_panel.grid(column=0, row=1, columnspan=2, sticky="nsew")

        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Buttons am unteren Rand hinzufügen
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(column=0, row=2, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Transkription löschen",
                   command=self.transcription_panel.clear_transcription).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Alles kopieren",
                   command=self.transcription_panel.copy_all_to_clipboard).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Erweiterte Optionen",
                   command=self.open_options_window).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Beenden",
                   command=self.root.quit).pack(side=tk.LEFT, padx=5)

    def open_options_window(self):
        """Öffnet das Fenster für erweiterte Optionen."""
        OptionsWindow(self.root, self.gui.theme_manager, self.transcription_panel)

# Zusätzliche Erklärungen:

# 1. Modulare Struktur:
#    Die Benutzeroberfläche ist in separate Panels aufgeteilt (TranscriptionPanel, OptionsPanel, StatusPanel),
#    was die Wartbarkeit und Erweiterbarkeit verbessert.

# 2. Tkinter Grid-Layout:
#    Das Grid-Layout wird verwendet, um eine flexible und responsive Benutzeroberfläche zu erstellen.
#    Die Verwendung von sticky="nsew" und weight-Parametern ermöglicht eine dynamische Größenanpassung der Elemente.
#    - sticky definiert, wie sich ein Widget innerhalb seiner Zelle verhält, wenn die Zelle größer ist als das Widget.
#    - "n, s, e, w" steht für North, South, East und West: Das Widget haftet am oberen, unteren, rechten oder linken Rand der Zelle.
#    - Die Kombination "nsew" bedeutet, dass das Widget in alle Richtungen "klebt" und sich somit
#      in alle Richtungen ausdehnt, um die gesamte Zelle auszufüllen.
#    - weight=1 gibt an, dass diese Spalte oder Zeile sich ausdehnen soll, wenn das Fenster vergrößert wird.
#    - In Kombination mit sticky="nsew" ermöglicht dies ein vollständig responsives Layout, verfügbarer Platz wird optimal ausgenutzt.

# 3. Button-Funktionalität:
#    Die Buttons am unteren Rand bieten schnellen Zugriff auf häufig verwendete Funktionen wie das Löschen der Transkription
#    oder das Öffnen der erweiterten Optionen.

# 4. Erweiterbarkeit:
#    Die open_options_window-Methode zeigt, wie zusätzliche Funktionen einfach integriert werden können,
#    indem neue Fenster oder Dialoge geöffnet werden.

# 5. Separation of Concerns:
#    Jedes Panel ist für einen spezifischen Bereich der Benutzeroberfläche zuständig, was die Codeorganisation verbessert
#    und es einfacher macht, einzelne Komponenten zu aktualisieren oder zu ersetzen.
