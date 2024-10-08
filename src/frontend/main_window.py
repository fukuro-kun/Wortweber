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

# Standardbibliotheken
import tkinter as tk
from tkinter import ttk

# Projektspezifische Module
from src.frontend.transcription_panel import TranscriptionPanel
from src.frontend.options_panel import OptionsPanel
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
        self.settings_manager = self.gui.settings_manager
        self.setup_ui()
        logger.info("MainWindow initialisiert")

    @handle_exceptions
    def setup_ui(self):
        """
        Richtet die Benutzeroberfläche für das MainWindow ein.
        """
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        self.options_panel = OptionsPanel(main_frame, self.gui)
        self.options_panel.grid(column=0, row=0, sticky="ew")

        self.transcription_panel = TranscriptionPanel(main_frame, self.gui)
        self.transcription_panel.grid(column=0, row=1, sticky="nsew")

        # Neuer Frame für die Plugin-Leiste
        self.plugin_bar_frame = ttk.Frame(self.options_panel)
        self.plugin_bar_frame.grid(column=3, row=0, sticky="e")  # Annahme: Spalte 3 ist der bisherige Leerraum

        # Statusleiste
        self.status_bar = tk.Frame(main_frame, bg="black", bd=1, relief="sunken")
        self.status_bar.grid(column=0, row=2, sticky="ew", padx=1, pady=(1, 0))

        # Konfigurieren der Spalten für das Grid-Layout
        self.status_bar.columnconfigure(0, weight=1)  # Linke Seite
        self.status_bar.columnconfigure(1, weight=2)  # Mitte (mehr Gewicht für die Hauptstatusanzeige)
        self.status_bar.columnconfigure(2, weight=1)  # Rechte Seite

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

        # Mittleres Statuselement (Hauptstatusanzeige)
        self.main_status = tk.Label(self.status_bar, text="Bereit", bg="black", fg="white", anchor="center")
        self.main_status.grid(row=0, column=1, sticky="nsew")

        # Rechte Statuselemente
        right_frame = tk.Frame(self.status_bar, bg="black")
        right_frame.grid(row=0, column=2, sticky="e")

        self.record_time_label = tk.Label(right_frame, text="Aufnahmezeit: ", bg="black", fg="white", anchor="e")
        self.record_time_label.pack(side=tk.LEFT)
        self.record_time = tk.Label(right_frame, text="0.0 s", bg="black", fg="white", anchor="e")
        self.record_time.pack(side=tk.LEFT)

        self.transcription_time_label = tk.Label(right_frame, text="Transkriptionszeit: ", bg="black", fg="white", anchor="e")
        self.transcription_time_label.pack(side=tk.LEFT)
        self.transcription_time = tk.Label(right_frame, text="0.00 s", bg="black", fg="white", anchor="e")
        self.transcription_time.pack(side=tk.LEFT)

        self.auto_copy_var = tk.BooleanVar(value=self.settings_manager.get_setting("auto_copy", False))
        self.auto_copy_checkbox = tk.Checkbutton(right_frame, text="Auto-Kopieren", variable=self.auto_copy_var,
                                                 bg="black", fg="white", selectcolor="black", activebackground="black",
                                                 command=self.on_auto_copy_change)
        self.auto_copy_checkbox.pack(side=tk.RIGHT)

        self.load_settings()
        logger.info("UI-Setup abgeschlossen")

    @handle_exceptions
    def update_status_bar(self, model=None, output_mode=None, status=None, record_time=None, transcription_time=None, status_color=None):
        """
        Aktualisiert die Statusleiste mit den gegebenen Informationen.

        :param model: Aktuelles Modell (optional)
        :param output_mode: Aktueller Ausgabemodus (optional)
        :param status: Statusnachricht (optional)
        :param record_time: Aufnahmezeit in Sekunden (optional)
        :param transcription_time: Transkriptionszeit in Sekunden (optional)
        :param status_color: Farbe für die Statusnachricht (optional)
        """
        if model:
            self.model_status.config(text=model)
            if "Geladen" in model:
                self.model_status.config(fg="green")
                self.settings_manager.set_setting_instant("current_model", model.split(" - ")[0])
            elif "Wird geladen" in model:
                self.model_status.config(fg="yellow")
            else:
                self.model_status.config(fg="white")

        if output_mode:
            self.output_mode_status.config(text=output_mode)
            self.settings_manager.set_setting_instant("output_mode", output_mode)

        if status:
            self.main_status.config(text=status)
            if status_color:
                self.main_status.config(fg=status_color)
            else:
                self.main_status.config(fg="white")

        if record_time is not None:
            self.record_time.config(text=f"{record_time:.1f} s")

        if transcription_time is not None:
            self.transcription_time.config(text=f"{transcription_time:.2f} s")

        # Explizite Aktualisierung des Fensters, um sicherzustellen, dass Änderungen sofort sichtbar sind
        self.root.update_idletasks()

    @handle_exceptions
    def on_auto_copy_change(self):
        """Behandelt Änderungen der Auto-Kopieren-Einstellung."""
        auto_copy_value = self.auto_copy_var.get()
        self.settings_manager.set_setting_instant("auto_copy", auto_copy_value)
        logger.debug(f"Auto-Kopieren-Einstellung geändert auf: {auto_copy_value}")

    @handle_exceptions
    def load_settings(self):
        """Lädt die gespeicherten Einstellungen und aktualisiert die UI-Elemente."""
        self.auto_copy_var.set(self.settings_manager.get_setting("auto_copy", False))
        current_model = self.settings_manager.get_setting("current_model", "")
        if current_model:
            self.update_status_bar(model=f"{current_model} - Geladen")
        current_output_mode = self.settings_manager.get_setting("output_mode", "textfenster")
        self.update_status_bar(output_mode=current_output_mode)
        logger.info("Einstellungen geladen und UI aktualisiert")

# Zusätzliche Erklärungen:

# 1. Modulare Struktur:
#    Die Benutzeroberfläche ist in separate Panels aufgeteilt (TranscriptionPanel, OptionsPanel),
#    was die Wartbarkeit und Erweiterbarkeit verbessert.

# 2. Tkinter Grid-Layout:
#    Das Grid-Layout wird verwendet, um eine flexible und responsive Benutzeroberfläche zu erstellen.
#    Die Verwendung von sticky="nsew" und weight-Parametern ermöglicht eine dynamische Größenanpassung der Elemente.

# 3. Statusleiste:
#    Die Statusleiste am unteren Rand des Fensters bietet eine übersichtliche Darstellung wichtiger Informationen.
#    Sie enthält Anzeigen für das Modell, den Ausgabemodus, den allgemeinen Status, die Aufnahmezeit und die Transkriptionszeit.

# 4. Fehlerbehandlung:
#    Die Verwendung des @handle_exceptions Decorators gewährleistet eine einheitliche Fehlerbehandlung in allen Methoden.

# 5. Logging:
#    Ausführliches Logging hilft bei der Diagnose von Problemen und der Nachverfolgung des Programmablaufs.

# 6. Dynamische Statusaktualisierung:
#    Die update_status_bar Methode ermöglicht es, verschiedene Teile der Statusleiste unabhängig voneinander zu aktualisieren,
#    was eine flexible und effiziente Statusanzeige ermöglicht.

# 7. Sofortige Einstellungsspeicherung:
#    Die on_auto_copy_change Methode wurde angepasst, um Änderungen der Auto-Kopieren-Einstellung sofort zu speichern.
#    In der update_status_bar Methode wird nun der Ausgabemodus sofort gespeichert, wenn er sich ändert.

# 8. Plugin-Leiste:
#    Ein neuer Frame für die Plugin-Leiste wurde im oberen rechten Bereich des OptionsPanel hinzugefügt,
#    um Platz für Plugin-spezifische UI-Elemente zu schaffen.

# 9. Einstellungen laden:
#    Die load_settings Methode wurde implementiert, um alle relevanten Einstellungen beim Start zu laden
#    und die UI-Elemente entsprechend zu aktualisieren. Dies gewährleistet, dass die Benutzeroberfläche
#    immer den aktuellen Einstellungen entspricht.
