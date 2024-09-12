import tkinter as tk
from tkinter import ttk

class StatusPanel(ttk.Frame):
    def __init__(self, parent, gui):
        super().__init__(parent)
        self.gui = gui
        self.setup_ui()

    def setup_ui(self):
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

    def update_status(self, message: str, color: str = "black"):
        self.status_var.set(message)
        self.status_label.config(foreground=color)
        self.gui.root.update()

    def update_timer(self, elapsed_time: float):
        self.timer_var.set(f"Aufnahmezeit: {elapsed_time:.1f} s")

    def update_transcription_timer(self, transcription_time: float):
        self.transcription_timer_var.set(f"Transkriptionszeit: {transcription_time:.2f} s")

    def reset_timer(self):
        self.timer_var.set("Aufnahmezeit: 0.0 s")
