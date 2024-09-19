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
from src.frontend.transcription_panel import TranscriptionPanel
from src.frontend.options_panel import OptionsPanel
from src.frontend.status_panel import StatusPanel
from src.frontend.options_window import OptionsWindow
from src.utils.error_handling import handle_exceptions, logger

class MainWindow:
    """
    Hauptfenster der Wortweber-Anwendung.
    Koordiniert die verschiedenen UI-Komponenten und deren Layout.
    """

    @handle_exceptions
    def __init__(self, root, gui):
        """
        Initialisiert das Hauptfenster.

        :param root: Das root Tkinter-Fenster
        :param gui: Referenz auf die Hauptgui-Instanz
        """
        self.root = root
        self.gui = gui

        self.setup_ui()
        logger.info("MainWindow initialisiert")

    @handle_exceptions
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

        # Statusleiste hinzufügen
        self.status_bar = tk.Frame(main_frame, bg="black", bd=1, relief="sunken")
        self.status_bar.grid(column=0, row=3, columnspan=2, sticky="ew", padx=1, pady=(1, 0))

        # Konfigurieren der Spalten für das Grid-Layout
        self.status_bar.columnconfigure(0, weight=1)  # Linke Seite
        self.status_bar.columnconfigure(1, weight=1)  # Rechte Seite

        # Linke Statuselemente
        left_frame = tk.Frame(self.status_bar, bg="black")
        left_frame.grid(row=0, column=0, sticky="w")

        self.model_label = tk.Label(left_frame, text="Modell: ", bg="black", fg="white", anchor="w")
        self.model_label.pack(side=tk.LEFT)
        self.model_status = tk.Label(left_frame, text="", bg="black", fg="white", anchor="w")
        self.model_status.pack(side=tk.LEFT)

        self.output_mode_label = tk.Label(left_frame, text="Ausgabemodus: ", bg="black", fg="white", anchor="w")
        self.output_mode_label.pack(side=tk.LEFT)
        self.output_mode_status = tk.Label(left_frame, text="", bg="black", fg="white", anchor="w")
        self.output_mode_status.pack(side=tk.LEFT)

        # Rechte Statuselemente
        right_frame = tk.Frame(self.status_bar, bg="black")
        right_frame.grid(row=0, column=1, sticky="e")

        self.record_time_label = tk.Label(right_frame, text="Aufnahmezeit: ", bg="black", fg="white", anchor="e")
        self.record_time_label.pack(side=tk.LEFT)
        self.record_time = tk.Label(right_frame, text="0.0 s", bg="black", fg="white", anchor="e")
        self.record_time.pack(side=tk.LEFT)

        self.transcription_time_label = tk.Label(right_frame, text="Transkriptionszeit: ", bg="black", fg="white", anchor="e")
        self.transcription_time_label.pack(side=tk.LEFT)
        self.transcription_time = tk.Label(right_frame, text="0.00 s", bg="black", fg="white", anchor="e")
        self.transcription_time.pack(side=tk.LEFT)

        self.hotkey_label = tk.Label(right_frame, text="Hotkey: ", bg="black", fg="white", anchor="e")
        self.hotkey_label.pack(side=tk.LEFT)
        self.hotkey_status = tk.Label(right_frame, text="F12", bg="black", fg="white", anchor="e")
        self.hotkey_status.pack(side=tk.LEFT)

        logger.info("UI-Setup abgeschlossen")


    @handle_exceptions
    def open_options_window(self):
        """Öffnet das Fenster für erweiterte Optionen."""
        logger.info("Öffne Optionsfenster")
        OptionsWindow(self.root, self.gui.theme_manager, self.transcription_panel, self.gui)

    @handle_exceptions
    def update_status_bar(self, model=None, output_mode=None, status=None, record_time=None, transcription_time=None, status_color=None):
        if model:
            self.model_status.config(text=model)
            if "Geladen" in model:
                self.model_status.config(fg="green")
            elif "Wird geladen" in model:
                self.model_status.config(fg="yellow")
            else:
                self.model_status.config(fg="white")

        if output_mode:
            self.output_mode_status.config(text=output_mode)

        if record_time is not None:
            self.record_time.config(text=f"{record_time:.1f} s")
            if record_time > 0:
                self.record_time.config(fg="orange")
            else:
                self.record_time.config(fg="white")

        if transcription_time is not None:
            self.transcription_time.config(text=f"{transcription_time:.2f} s")
            self.transcription_time.config(fg="green")

        # Explizite Aktualisierung des Fensters
        self.root.update_idletasks()


logger.info("MainWindow-Modul geladen")

# Zusätzliche Erklärungen:

# 1. Modulare Struktur:
#    Die Benutzeroberfläche ist in separate Panels aufgeteilt (TranscriptionPanel, OptionsPanel, StatusPanel),
#    was die Wartbarkeit und Erweiterbarkeit verbessert.

# 2. Tkinter Grid-Layout:
#    Das Grid-Layout wird verwendet, um eine flexible und responsive Benutzeroberfläche zu erstellen.
#    Die Verwendung von sticky="nsew" und weight-Parametern ermöglicht eine dynamische Größenanpassung der Elemente.

# 3. Button-Funktionalität:
#    Die Buttons am unteren Rand bieten schnellen Zugriff auf häufig verwendete Funktionen wie das Löschen der Transkription
#    oder das Öffnen der erweiterten Optionen.

# 4. Erweiterbarkeit:
#    Die open_options_window-Methode zeigt, wie zusätzliche Funktionen einfach integriert werden können,
#    indem neue Fenster oder Dialoge geöffnet werden.

# 5. Separation of Concerns:
#    Jedes Panel ist für einen spezifischen Bereich der Benutzeroberfläche zuständig, was die Codeorganisation verbessert
#    und es einfacher macht, einzelne Komponenten zu aktualisieren oder zu ersetzen.

# 6. Statusleiste:
#    Die Statusleiste am unteren Rand des Fensters bietet eine übersichtliche Darstellung wichtiger Informationen.
#    Sie verwendet einen schwarzen Hintergrund mit weißem Text für bessere Lesbarkeit und farbige Hervorhebungen für wichtige Statusänderungen.

# 7. Fehlerbehandlung:
#    Die Verwendung des @handle_exceptions Decorators gewährleistet eine einheitliche Fehlerbehandlung in allen Methoden.
