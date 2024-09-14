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
from tkinter import ttk, scrolledtext
import tkinter.font as tkFont
import pyperclip
from src.config import HIGHLIGHT_DURATION, DEFAULT_FONT_SIZE, DEFAULT_FONT_FAMILY
from src.frontend.context_menu import create_context_menu

class TranscriptionPanel(ttk.Frame):
    """
    Panel zur Anzeige und Bearbeitung von Transkriptionen in der Wortweber-Anwendung.
    """

    def __init__(self, parent, gui):
        """
        Initialisiert das TranscriptionPanel.

        :param parent: Das übergeordnete Tkinter-Widget
        :param gui: Referenz auf die Hauptgui-Instanz
        """
        super().__init__(parent)
        self.gui = gui
        self.font_size = self.gui.settings_manager.get_setting("font_size", DEFAULT_FONT_SIZE)
        self.font_family = self.gui.settings_manager.get_setting("font_family", DEFAULT_FONT_FAMILY)
        self.setup_ui()
        self.load_saved_text()

    def setup_ui(self):
        """Richtet die Benutzeroberfläche für das TranscriptionPanel ein."""
        self.text_widget = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=80, height=20)
        self.text_widget.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        self.text_widget.bind("<Button-3>", self.show_context_menu)
        self.text_widget.tag_configure("highlight", background="yellow")
        self.text_widget.tag_configure("select", background="lightblue")
        self.set_font(self.font_family, self.font_size)
        self.text_widget.config(
            insertbackground="red",
            insertwidth=2
        )

        # Event-Handler für Textänderungen hinzufügen
        self.text_widget.bind("<<Modified>>", self.on_text_modified)
        self.text_widget.bind("<<Selection>>", self.on_selection_change)

    def set_font(self, family, size):
        """
        Ändert die Schriftart und -größe des Transkriptionsfelds.

        :param family: Die neue Schriftartfamilie
        :param size: Die neue Schriftgröße
        """
        self.font_family = family
        self.font_size = size
        font = tkFont.Font(family=family, size=size)
        self.text_widget.configure(font=font)
        self.gui.settings_manager.set_setting("font_family", family)
        self.gui.settings_manager.set_setting("font_size", size)
        self.gui.settings_manager.save_settings()

    def get_font_family(self):
        """
        Gibt die aktuelle Schriftartfamilie zurück.

        :return: Die aktuelle Schriftartfamilie
        """
        return self.font_family

    def get_font_size(self):
        """
        Gibt die aktuelle Schriftgröße zurück.

        :return: Die aktuelle Schriftgröße
        """
        return self.font_size

    def show_context_menu(self, event):
        """Zeigt das Kontextmenü an der Position des Mausklicks an."""
        create_context_menu(self.text_widget, event)

    def insert_text(self, text):
        """
        Fügt Text in das Transkriptionsfeld ein und hebt ihn kurzzeitig hervor.

        :param text: Der einzufügende Text
        """
        current_position = self.text_widget.index(tk.INSERT)
        self.text_widget.insert(current_position, text)
        end_position = self.text_widget.index(f"{current_position} + {len(text)}c")
        self.text_widget.tag_add("highlight", current_position, end_position)
        self.text_widget.see(end_position)
        self.gui.root.after(HIGHLIGHT_DURATION, lambda: self.text_widget.tag_remove("highlight", current_position, end_position))
        self.save_text()

    def clear_transcription(self):
        """Löscht den gesamten Text im Transkriptionsfeld."""
        self.text_widget.delete(1.0, tk.END)
        self.save_text()

    def copy_all_to_clipboard(self):
        """Kopiert den gesamten Text des Transkriptionsfelds in die Zwischenablage."""
        all_text = self.text_widget.get(1.0, tk.END)
        pyperclip.copy(all_text)
        self.gui.status_panel.update_status("Gesamter Text in die Zwischenablage kopiert", "green")

    def save_text(self):
        """Speichert den aktuellen Inhalt des Transkriptionsfelds in den Einstellungen."""
        text_content = self.text_widget.get(1.0, tk.END).strip()
        self.gui.settings_manager.set_setting("text_content", text_content)
        self.gui.settings_manager.save_settings()

    def load_saved_text(self):
        """Lädt den gespeicherten Text aus den Einstellungen in das Transkriptionsfeld."""
        saved_text = self.gui.settings_manager.get_setting("text_content")
        if saved_text:
            self.text_widget.insert(tk.END, saved_text)

    def on_text_modified(self, event):
        """
        Wird aufgerufen, wenn der Text im Transkriptionsfeld geändert wurde.
        Speichert den aktualisierten Text.
        """
        # Überprüfen, ob der Text tatsächlich geändert wurde
        if self.text_widget.edit_modified():
            self.save_text()
            # Zurücksetzen des modified flags
            self.text_widget.edit_modified(False)

    def on_selection_change(self, event):
        """Wird aufgerufen, wenn sich die Textauswahl ändert."""
        if self.text_widget.tag_ranges("sel"):
            self.text_widget.tag_remove("select", "1.0", tk.END)
            self.text_widget.tag_add("select", "sel.first", "sel.last")

    def update_colors(self, text_fg, text_bg, select_fg, select_bg, highlight_fg, highlight_bg):
        """
        Aktualisiert die Farben des Textwidgets.

        :param text_fg: Vordergrundfarbe für normalen Text
        :param text_bg: Hintergrundfarbe für normalen Text
        :param select_fg: Vordergrundfarbe für ausgewählten Text
        :param select_bg: Hintergrundfarbe für ausgewählten Text
        :param highlight_fg: Vordergrundfarbe für hervorgehobenen Text
        :param highlight_bg: Hintergrundfarbe für hervorgehobenen Text
        """
        self.text_widget.config(
            fg=text_fg,
            bg=text_bg,
            selectforeground=select_fg,
            selectbackground=select_bg
        )
        self.text_widget.tag_configure("highlight", foreground=highlight_fg, background=highlight_bg)
        self.text_widget.tag_configure("select", foreground=select_fg, background=select_bg)

# Zusätzliche Erklärungen:

# 1. Die Klasse TranscriptionPanel verwaltet das Haupttextfeld für die Transkriptionen.
# 2. Sie bietet Funktionen zum Einfügen, Löschen und Kopieren von Text.
# 3. Die Schriftgröße kann dynamisch angepasst werden.
# 4. Änderungen am Text werden automatisch gespeichert.
# 5. Ein Kontextmenü ermöglicht zusätzliche Textbearbeitungsfunktionen.
# 6. Die Klasse interagiert eng mit dem SettingsManager, um Benutzereinstellungen zu persistieren.
# 7. Die update_colors Methode ermöglicht die dynamische Anpassung der Textfarben.
