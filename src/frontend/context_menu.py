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
    context_menu.add_command(label="Ausschneiden", command=lambda: text_widget.event_generate("<<Cut>>"))
    context_menu.add_command(label="Kopieren", command=lambda: text_widget.event_generate("<<Copy>>"))
    context_menu.add_command(label="Einfügen", command=lambda: text_widget.event_generate("<<Paste>>"))
    context_menu.add_command(label="Löschen", command=lambda: text_widget.event_generate("<<Clear>>"))
    context_menu.add_separator()
    context_menu.add_command(label="Alles auswählen", command=lambda: text_widget.tag_add(tk.SEL, "1.0", tk.END))
    context_menu.add_separator()
    context_menu.add_command(label="Zahlwörter nach Ziffern", command=lambda: convert_text(text_widget, words_to_digits))
    context_menu.add_command(label="Ziffern nach Zahlwörtern", command=lambda: convert_text(text_widget, digits_to_words))
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
