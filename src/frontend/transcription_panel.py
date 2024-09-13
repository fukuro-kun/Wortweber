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
from src.config import HIGHLIGHT_DURATION, DEFAULT_FONT_SIZE
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
        self.setup_ui()
        self.load_saved_text()

    def setup_ui(self):
        """Richtet die Benutzeroberfläche für das TranscriptionPanel ein."""
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
        """Zeigt das Kontextmenü an der Position des Mausklicks an."""
        create_context_menu(self.transcription_text, event)

    def insert_text(self, text):
        """
        Fügt Text in das Transkriptionsfeld ein und hebt ihn kurzzeitig hervor.

        :param text: Der einzufügende Text
        """
        current_position = self.transcription_text.index(tk.INSERT)
        self.transcription_text.insert(current_position, text)
        end_position = self.transcription_text.index(f"{current_position} + {len(text)}c")
        self.transcription_text.tag_add("highlight", current_position, end_position)
        self.transcription_text.see(end_position)
        self.gui.root.after(HIGHLIGHT_DURATION, lambda: self.transcription_text.tag_remove("highlight", current_position, end_position))
        self.save_text()

    def clear_transcription(self):
        """Löscht den gesamten Text im Transkriptionsfeld."""
        self.transcription_text.delete(1.0, tk.END)
        self.save_text()

    def copy_all_to_clipboard(self):
        """Kopiert den gesamten Text des Transkriptionsfelds in die Zwischenablage."""
        all_text = self.transcription_text.get(1.0, tk.END)
        pyperclip.copy(all_text)
        self.gui.status_panel.update_status("Gesamter Text in die Zwischenablage kopiert", "green")

    def save_text(self):
        """Speichert den aktuellen Inhalt des Transkriptionsfelds in den Einstellungen."""
        text_content = self.transcription_text.get(1.0, tk.END).strip()
        self.gui.settings_manager.set_setting("text_content", text_content)
        self.gui.settings_manager.save_settings()

    def load_saved_text(self):
        """Lädt den gespeicherten Text aus den Einstellungen in das Transkriptionsfeld."""
        saved_text = self.gui.settings_manager.get_setting("text_content")
        if saved_text:
            self.transcription_text.insert(tk.END, saved_text)

    def on_text_modified(self, event):
        """
        Wird aufgerufen, wenn der Text im Transkriptionsfeld geändert wurde.
        Speichert den aktualisierten Text.
        """
        # Überprüfen, ob der Text tatsächlich geändert wurde
        if self.transcription_text.edit_modified():
            self.save_text()
            # Zurücksetzen des modified flags
            self.transcription_text.edit_modified(False)

    def set_font_size(self, size):
        """
        Ändert die Schriftgröße des Transkriptionsfelds.

        :param size: Die neue Schriftgröße
        """
        self.font_size = size
        current_font = tkFont.Font(font=self.transcription_text['font'])
        current_font.configure(size=size)
        self.transcription_text.configure(font=current_font)
        self.gui.settings_manager.set_setting("font_size", size)
        self.gui.settings_manager.save_settings()

    def get_font_size(self):
        """
        Gibt die aktuelle Schriftgröße zurück.

        :return: Die aktuelle Schriftgröße
        """
        return self.font_size

# Zusätzliche Erklärungen:

# 1. ScrolledText Widget:
#    Verwendet für das Transkriptionsfeld, da es automatisch Scrollbalken hinzufügt,
#    wenn der Inhalt die sichtbare Fläche überschreitet.

# 2. Kontextmenü:
#    Die Methode show_context_menu bindet ein benutzerdefiniertes Kontextmenü an das Transkriptionsfeld,
#    was zusätzliche Funktionalitäten wie die Zahlwort-Konvertierung ermöglicht.

# 3. Text Highlighting:
#    Die insert_text Methode implementiert ein temporäres Highlighting des neu eingefügten Texts,
#    was dem Benutzer visuelles Feedback über die letzte Einfügung gibt.

# 4. Persistenz:
#    Die Methoden save_text und load_saved_text sorgen dafür, dass der Inhalt des Transkriptionsfelds
#    zwischen Sitzungen erhalten bleibt.

# 5. Schriftgrößenanpassung:
#    set_font_size und get_font_size ermöglichen eine dynamische Anpassung der Schriftgröße,
#    was die Zugänglichkeit der Anwendung verbessert.

# 6. Event Handling:
#    on_text_modified wird bei jeder Textänderung aufgerufen und stellt sicher, dass der aktuelle Inhalt
#    gespeichert wird, was Datenverlust verhindert.

# 7. Zwischenablagen-Integration:
#    copy_all_to_clipboard ermöglicht es dem Benutzer, den gesamten Transkriptionstext
#    einfach in andere Anwendungen zu übertragen.
