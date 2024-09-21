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
from src.backend.text_processor import words_to_digits, digits_to_words
from src.utils.error_handling import handle_exceptions, logger

@handle_exceptions
def create_context_menu(text_widget, event):
    """
    Erstellt und zeigt ein Kontextmenü für das gegebene Text-Widget an.

    :param text_widget: Das Tkinter Text-Widget, für das das Kontextmenü erstellt wird
    :param event: Das Ereignis, das das Kontextmenü auslöst (typischerweise ein Rechtsklick)
    """
    context_menu = tk.Menu(text_widget, tearoff=0)

    # Ursprüngliche Funktionalitäten
    context_menu.add_command(label="Rückgängig", command=text_widget.edit_undo)
    context_menu.add_command(label="Wiederherstellen", command=text_widget.edit_redo)
    context_menu.add_separator()
    context_menu.add_command(label="Ausschneiden", command=lambda: text_widget.event_generate("<<Cut>>"))
    context_menu.add_command(label="Kopieren", command=lambda: text_widget.event_generate("<<Copy>>"))
    context_menu.add_command(label="Einfügen", command=lambda: text_widget.event_generate("<<Paste>>"))
    context_menu.add_command(label="Alles auswählen", command=lambda: text_widget.tag_add(tk.SEL, "1.0", tk.END))
    context_menu.add_separator()
    context_menu.add_command(label="Zahlwörter nach Ziffern", command=lambda: convert_text(text_widget, words_to_digits))
    context_menu.add_command(label="Ziffern nach Zahlwörtern", command=lambda: convert_text(text_widget, digits_to_words))

    # Neue Optionen
    context_menu.add_separator()
    context_menu.add_command(label="Transkription löschen", command=lambda: text_widget.delete(1.0, tk.END))
    context_menu.add_command(label="Alles kopieren", command=lambda: text_widget.event_generate("<<Copy>>"))

    context_menu.tk_popup(event.x_root, event.y_root)
    logger.debug("Kontextmenü erstellt und angezeigt")


@handle_exceptions
def convert_text(text_widget, conversion_function):
    """
    Konvertiert den ausgewählten Text im Widget mit der angegebenen Konvertierungsfunktion.

    :param text_widget: Das Text-Widget, das den zu konvertierenden Text enthält
    :param conversion_function: Die Funktion, die zur Textkonvertierung verwendet wird
    """
    try:
        selected_text = text_widget.get(tk.SEL_FIRST, tk.SEL_LAST)
        converted_text = conversion_function(selected_text)
        text_widget.delete(tk.SEL_FIRST, tk.SEL_LAST)
        text_widget.insert(tk.INSERT, converted_text)
        logger.info(f"Text erfolgreich konvertiert: {selected_text} -> {converted_text}")
    except tk.TclError:
        # Kein Text ausgewählt, tue nichts
        logger.debug("Keine Textauswahl für Konvertierung")

# Diese Datei implementiert das Kontextmenü für das Transkriptionsfenster.
# Es bietet grundlegende Textbearbeitungsfunktionen sowie spezielle Optionen
# zur Konvertierung von Zahlwörtern in Ziffern und umgekehrt.

# Hinweise:
# 1. Die Lambda-Funktionen werden verwendet, um die Tkinter-Ereignisse auszulösen,
#    die die Standardaktionen für Ausschneiden, Kopieren, etc. implementieren.
# 2. Die Konvertierungsfunktionen words_to_digits und digits_to_words werden aus
#    dem Backend-Modul importiert, um eine konsistente Textverarbeitung zu gewährleisten.
# 3. Die try-except-Struktur in convert_text fängt den Fall ab, dass kein Text
#    ausgewählt ist, wenn die Konvertierung versucht wird.
# 4. Die digits_to_words Funktion nutzt nun intern die neue ziffern_zu_zahlwoerter
#    Funktion für eine verbesserte Konvertierung von Ziffern zu Zahlwörtern.
