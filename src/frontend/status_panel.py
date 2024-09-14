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
from src.utils.error_handling import handle_exceptions

class StatusPanel(ttk.Frame):
    """
    Panel zur Anzeige von Statusinformationen und Timern in der Wortweber-Anwendung.
    """

    @handle_exceptions
    def __init__(self, parent, gui):
        """
        Initialisiert das StatusPanel.

        :param parent: Das übergeordnete Tkinter-Widget
        :param gui: Referenz auf die Hauptgui-Instanz
        """
        super().__init__(parent)
        self.gui = gui
        self.setup_ui()

    @handle_exceptions
    def setup_ui(self):
        """Richtet die Benutzeroberfläche für das StatusPanel ein."""
        ttk.Label(self, text="Drücken und halten Sie F12, um zu sprechen").grid(column=0, row=0, pady=5)

        self.timer_var = tk.StringVar(value="Aufnahmezeit: 0.0 s")
        ttk.Label(self, textvariable=self.timer_var).grid(column=0, row=1, pady=5)

        self.transcription_timer_var = tk.StringVar(value="Transkriptionszeit: 0.00 s")
        ttk.Label(self, textvariable=self.transcription_timer_var).grid(column=0, row=2, pady=5)

        self.auto_copy_var = tk.BooleanVar(value=self.gui.settings_manager.get_setting("auto_copy"))
        self.auto_copy_checkbox = ttk.Checkbutton(self, text="Automatisch in Zwischenablage kopieren",
                                                  variable=self.auto_copy_var)
        self.auto_copy_checkbox.grid(column=0, row=3, pady=5, sticky="w")

        self.status_var = tk.StringVar()
        self.status_label = ttk.Label(self, textvariable=self.status_var)
        self.status_label.grid(column=0, row=4, pady=5)

    @handle_exceptions
    def update_status(self, message: str, color: str = "black"):
        """
        Aktualisiert die Statusanzeige mit einer Nachricht und Farbe.

        :param message: Die anzuzeigende Statusnachricht
        :param color: Die Farbe des Statustextes
        """
        self.status_var.set(message)
        self.status_label.config(foreground=color)
        self.gui.root.update()

    @handle_exceptions
    def update_timer(self, elapsed_time: float):
        """
        Aktualisiert die Anzeige der Aufnahmezeit.

        :param elapsed_time: Die verstrichene Aufnahmezeit in Sekunden
        """
        self.timer_var.set(f"Aufnahmezeit: {elapsed_time:.1f} s")

    @handle_exceptions
    def update_transcription_timer(self, transcription_time: float):
        """
        Aktualisiert die Anzeige der Transkriptionszeit.

        :param transcription_time: Die für die Transkription benötigte Zeit in Sekunden
        """
        self.transcription_timer_var.set(f"Transkriptionszeit: {transcription_time:.2f} s")

    @handle_exceptions
    def reset_timer(self):
        """Setzt die Aufnahmezeit-Anzeige zurück."""
        self.timer_var.set("Aufnahmezeit: 0.0 s")

# Zusätzliche Erklärungen:

# 1. Tkinter-Variablen:
#    Die Verwendung von StringVar und BooleanVar ermöglicht eine automatische Aktualisierung der GUI,
#    wenn sich die Werte ändern. Dies ist besonders nützlich für dynamische Anzeigen wie Timer.

# 2. Grid-Layout:
#    Das Grid-Layout wird hier verwendet, um eine präzise Positionierung der Elemente zu ermöglichen.
#    Es bietet mehr Kontrolle über das Layout als pack() und ist flexibler als place().

# 3. Checkbox für automatisches Kopieren:
#    Die auto_copy_checkbox ermöglicht es dem Benutzer, das automatische Kopieren in die Zwischenablage
#    ein- oder auszuschalten. Der Zustand wird aus den gespeicherten Einstellungen geladen.

# 4. Farbige Statusanzeige:
#    Die update_status-Methode erlaubt es, den Status mit unterschiedlichen Farben anzuzeigen.
#    Dies kann verwendet werden, um wichtige Informationen hervorzuheben oder den Benutzer auf
#    bestimmte Zustände aufmerksam zu machen (z.B. Rot für Fehler, Grün für Erfolg).

# 5. Timer-Funktionalität:
#    Die Methoden update_timer und update_transcription_timer ermöglichen eine Echtzeit-Anzeige
#    der Aufnahme- und Verarbeitungszeiten, was dem Benutzer wichtiges Feedback gibt.

# 6. GUI-Aktualisierung:
#    Der Aufruf von self.gui.root.update() in update_status stellt sicher, dass die GUI sofort
#    aktualisiert wird, was besonders bei schnellen Statusänderungen wichtig ist.
