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
from tkinter import ttk, scrolledtext
import tkinter.font as tkFont
import pyperclip
import time
from src.config import HIGHLIGHT_DURATION, DEFAULT_FONT_SIZE, DEFAULT_FONT_FAMILY, DEFAULT_INCOGNITO_MODE
from src.frontend.context_menu import create_context_menu
from src.utils.error_handling import handle_exceptions, logger

class TranscriptionPanel(ttk.Frame):
    """
    Panel zur Anzeige und Bearbeitung von Transkriptionen in der Wortweber-Anwendung.
    """

    @handle_exceptions
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
        self.last_selection_log = 0
        self.selection_log_delay = 0.1  # 100 ms
        self.setup_ui()
        self.load_saved_text()
        logger.info("TranscriptionPanel initialisiert")

    @handle_exceptions
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
        logger.debug("TranscriptionPanel UI eingerichtet")

    @handle_exceptions
    def set_font(self, family, size):
        """
        Ändert die Schriftart und -größe des Transkriptionsfelds.

        :param family: Die neue Schriftartfamilie
        :param size: Die neue Schriftgröße
        """
        try:
            size = int(size)  # Versuchen Sie, size in einen Integer umzuwandeln
        except ValueError:
            size = 12  # Standardgröße, falls die Umwandlung fehlschlägt
        font = tkFont.Font(family=family, size=size)
        self.font_family = family
        self.font_size = size
        self.text_widget.configure(font=font)
        self.gui.settings_manager.set_setting("font_family", family)
        self.gui.settings_manager.set_setting("font_size", size)
        self.gui.settings_manager.save_settings()
        logger.info(f"Schriftart auf {family}, Größe {size} geändert")

    @handle_exceptions
    def get_font_family(self):
        """
        Gibt die aktuelle Schriftartfamilie zurück.

        :return: Die aktuelle Schriftartfamilie
        """
        return self.font_family

    @handle_exceptions
    def get_font_size(self):
        """
        Gibt die aktuelle Schriftgröße zurück.

        :return: Die aktuelle Schriftgröße
        """
        return self.font_size

    @handle_exceptions
    def show_context_menu(self, event):
        """Zeigt das Kontextmenü an der Position des Mausklicks an."""
        create_context_menu(self.text_widget, event)
        logger.debug("Kontextmenü angezeigt")

    @handle_exceptions
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
        incognito_mode = self.gui.settings_manager.get_setting("incognito_mode", DEFAULT_INCOGNITO_MODE)
        if not incognito_mode:
            logger.info(f"Text eingefügt und hervorgehoben: {text[:50]}...")
        else:
            logger.info(f"Text eingefügt und hervorgehoben (Incognito-Modus aktiv). Länge: {len(text)} Zeichen")

    @handle_exceptions
    def clear_transcription(self):
        """Löscht den gesamten Text im Transkriptionsfeld."""
        self.text_widget.delete(1.0, tk.END)
        self.save_text()
        logger.info("Transkription gelöscht")

    @handle_exceptions
    def copy_all_to_clipboard(self):
        """Kopiert den gesamten Text des Transkriptionsfelds in die Zwischenablage."""
        all_text = self.text_widget.get(1.0, tk.END)
        pyperclip.copy(all_text)
        self.gui.main_window.update_status_bar(status="Gesamter Text in die Zwischenablage kopiert", status_color="green")
        incognito_mode = self.gui.settings_manager.get_setting("incognito_mode", DEFAULT_INCOGNITO_MODE)
        if not incognito_mode:
            logger.info(f"Gesamter Text in die Zwischenablage kopiert. Länge: {len(all_text)} Zeichen")
        else:
            logger.info("Gesamter Text in die Zwischenablage kopiert (Incognito-Modus aktiv)")

    @handle_exceptions
    def save_text(self):
        """Speichert den aktuellen Inhalt des Transkriptionsfelds in den Einstellungen."""
        text_content = self.text_widget.get(1.0, tk.END).strip()
        self.gui.settings_manager.set_setting("text_content", text_content)
        self.gui.settings_manager.save_settings()
        incognito_mode = self.gui.settings_manager.get_setting("incognito_mode", DEFAULT_INCOGNITO_MODE)
        if not incognito_mode:
            logger.debug(f"Transkriptionstext gespeichert. Länge: {len(text_content)} Zeichen")
        else:
            logger.debug("Transkriptionstext gespeichert (Incognito-Modus aktiv)")

    @handle_exceptions
    def load_saved_text(self):
        """Lädt den gespeicherten Text aus den Einstellungen in das Transkriptionsfeld."""
        saved_text = self.gui.settings_manager.get_setting("text_content")
        if saved_text:
            self.text_widget.insert(tk.END, saved_text)
            incognito_mode = self.gui.settings_manager.get_setting("incognito_mode", DEFAULT_INCOGNITO_MODE)
            if not incognito_mode:
                logger.info(f"Gespeicherter Text geladen. Länge: {len(saved_text)} Zeichen")
            else:
                logger.info("Gespeicherter Text geladen (Incognito-Modus aktiv)")

    @handle_exceptions
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
            incognito_mode = self.gui.settings_manager.get_setting("incognito_mode", DEFAULT_INCOGNITO_MODE)
            if not incognito_mode:
                logger.debug(f"Text geändert und gespeichert. Neue Länge: {len(self.text_widget.get(1.0, tk.END).strip())} Zeichen")
            else:
                logger.debug("Text geändert und gespeichert (Incognito-Modus aktiv)")

    @handle_exceptions
    def on_selection_change(self, event):
        """Wird aufgerufen, wenn sich die Textauswahl ändert."""
        if self.text_widget.tag_ranges("sel"):
            self.text_widget.tag_remove("select", "1.0", tk.END)
            self.text_widget.tag_add("select", "sel.first", "sel.last")
            self.throttled_log("Textauswahl geändert")

    def throttled_log(self, message):
        """Loggt eine Nachricht, aber nicht öfter als alle 100 ms."""
        current_time = time.time()
        if current_time - self.last_selection_log > self.selection_log_delay:
            logger.debug(message)
            self.last_selection_log = current_time

    @handle_exceptions
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
        logger.info("Textfarben aktualisiert")


# Zusätzliche Erklärungen:

# 1. Die Klasse TranscriptionPanel verwaltet das Haupttextfeld für die Transkriptionen.
# 2. Sie bietet Funktionen zum Einfügen, Löschen und Kopieren von Text.
# 3. Die Schriftgröße kann dynamisch angepasst werden.
# 4. Änderungen am Text werden automatisch gespeichert.
# 5. Ein Kontextmenü ermöglicht zusätzliche Textbearbeitungsfunktionen.
# 6. Die Klasse interagiert eng mit dem SettingsManager, um Benutzereinstellungen zu persistieren.
# 7. Die update_colors Methode ermöglicht die dynamische Anpassung der Textfarben.
