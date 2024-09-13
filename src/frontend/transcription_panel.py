import tkinter as tk
from tkinter import ttk, scrolledtext
import tkinter.font as tkFont
import pyperclip
from src.config import HIGHLIGHT_DURATION, DEFAULT_FONT_SIZE
from src.frontend.context_menu import create_context_menu

class TranscriptionPanel(ttk.Frame):
    def __init__(self, parent, gui):
        super().__init__(parent)
        self.gui = gui
        self.font_size = self.gui.settings_manager.get_setting("font_size", DEFAULT_FONT_SIZE)
        self.setup_ui()
        self.load_saved_text()

    def setup_ui(self):
        self.transcription_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=80, height=20)
        self.transcription_text.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        self.transcription_text.bind("<Button-3>", self.show_context_menu)
        self.transcription_text.tag_configure("highlight", background="yellow")
        self.set_font_size(self.font_size)
        self.transcription_text.config(
            insertbackground="red",
            insertwidth=2,
            selectbackground="yellow",
            selectforeground="black"
        )

        # Event-Handler für Textänderungen hinzufügen
        self.transcription_text.bind("<<Modified>>", self.on_text_modified)

    def show_context_menu(self, event):
        create_context_menu(self.transcription_text, event)

    def insert_text(self, text):
        current_position = self.transcription_text.index(tk.INSERT)
        self.transcription_text.insert(current_position, text)
        end_position = self.transcription_text.index(f"{current_position} + {len(text)}c")
        self.transcription_text.tag_add("highlight", current_position, end_position)
        self.transcription_text.see(end_position)
        self.gui.root.after(HIGHLIGHT_DURATION, lambda: self.transcription_text.tag_remove("highlight", current_position, end_position))
        self.save_text()

    def clear_transcription(self):
        self.transcription_text.delete(1.0, tk.END)
        self.save_text()

    def copy_all_to_clipboard(self):
        all_text = self.transcription_text.get(1.0, tk.END)
        pyperclip.copy(all_text)
        self.gui.status_panel.update_status("Gesamter Text in die Zwischenablage kopiert", "green")

    def save_text(self):
        text_content = self.transcription_text.get(1.0, tk.END).strip()
        self.gui.settings_manager.set_setting("text_content", text_content)
        self.gui.settings_manager.save_settings()

    def load_saved_text(self):
        saved_text = self.gui.settings_manager.get_setting("text_content")
        if saved_text:
            self.transcription_text.insert(tk.END, saved_text)

    def on_text_modified(self, event):
        # Überprüfen, ob der Text tatsächlich geändert wurde
        if self.transcription_text.edit_modified():
            self.save_text()
            # Zurücksetzen des modified flags
            self.transcription_text.edit_modified(False)

    def set_font_size(self, size):
        self.font_size = size
        current_font = tkFont.Font(font=self.transcription_text['font'])
        current_font.configure(size=size)
        self.transcription_text.configure(font=current_font)
        self.gui.settings_manager.set_setting("font_size", size)
        self.gui.settings_manager.save_settings()

    def get_font_size(self):
        return self.font_size
