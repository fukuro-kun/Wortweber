import tkinter as tk
from tkinter import ttk, scrolledtext
import pyperclip
from src.config import HIGHLIGHT_DURATION
from src.frontend.context_menu import create_context_menu

class TranscriptionPanel(ttk.Frame):
    def __init__(self, parent, gui):
        super().__init__(parent)
        self.gui = gui
        self.setup_ui()

    def setup_ui(self):
        self.transcription_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=80, height=20)
        self.transcription_text.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        self.transcription_text.bind("<Button-3>", self.show_context_menu)
        self.transcription_text.tag_configure("highlight", background="yellow")
        self.transcription_text.config(
            insertbackground="red",
            insertwidth=2,
            selectbackground="yellow",
            selectforeground="black"
        )

    def show_context_menu(self, event):
        create_context_menu(self.transcription_text, event)

    def insert_text(self, text):
        current_position = self.transcription_text.index(tk.INSERT)
        self.transcription_text.insert(current_position, text)
        end_position = self.transcription_text.index(f"{current_position} + {len(text)}c")
        self.transcription_text.tag_add("highlight", current_position, end_position)
        self.transcription_text.see(end_position)
        self.gui.root.after(HIGHLIGHT_DURATION, lambda: self.transcription_text.tag_remove("highlight", current_position, end_position))

    def clear_transcription(self):
        self.transcription_text.delete(1.0, tk.END)

    def copy_all_to_clipboard(self):
        all_text = self.transcription_text.get(1.0, tk.END)
        pyperclip.copy(all_text)
        self.gui.status_panel.update_status("Gesamter Text in die Zwischenablage kopiert", "green")
