import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

class OptionsWindow(tk.Toplevel):
    def __init__(self, parent, theme_manager, transcription_panel):
        super().__init__(parent)
        self.title("Erweiterte Optionen")
        self.theme_manager = theme_manager
        self.transcription_panel = transcription_panel
        self.setup_ui()

    def setup_ui(self):
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
        ttk.Label(parent, text="Textgröße:").pack(pady=(10, 5))
        size_var = tk.StringVar(value=str(self.transcription_panel.get_font_size()))
        size_spinbox = ttk.Spinbox(parent, from_=8, to=24, textvariable=size_var, width=5)
        size_spinbox.pack()

        def update_size():
            try:
                new_size = int(size_var.get())
                self.transcription_panel.set_font_size(new_size)
            except ValueError:
                pass

        ttk.Button(parent, text="Anwenden", command=update_size).pack(pady=(5, 10))
