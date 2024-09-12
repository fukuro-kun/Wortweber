import tkinter as tk
from tkinter import ttk

class OptionsWindow(tk.Toplevel):
    def __init__(self, parent, theme_manager):
        super().__init__(parent)
        self.title("Erweiterte Optionen")
        self.theme_manager = theme_manager
        self.setup_ui()

    def setup_ui(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Theme-Einstellungen
        theme_frame = ttk.LabelFrame(main_frame, text="Theme-Einstellungen")
        theme_frame.pack(fill=tk.X, pady=5)
        self.theme_manager.setup_theme_selection(theme_frame)

        # Hier können Sie weitere Optionen hinzufügen

        ttk.Button(main_frame, text="Schließen", command=self.destroy).pack(pady=10)
