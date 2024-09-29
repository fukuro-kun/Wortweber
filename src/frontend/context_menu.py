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

# Standardbibliotheken
import tkinter as tk
from typing import Callable

# Projektspezifische Module
from src.backend.text_processor import words_to_digits, digits_to_words
from src.utils.error_handling import handle_exceptions, logger
from src.plugin_system.plugin_manager import PluginManager

@handle_exceptions
def create_context_menu(text_widget: tk.Text, event: tk.Event, plugin_manager: PluginManager) -> None:
    """
    Erstellt und zeigt ein Kontextmenü für das gegebene Text-Widget an.

    :param text_widget: Das Tkinter Text-Widget, für das das Kontextmenü erstellt wird
    :param event: Das Ereignis, das das Kontextmenü auslöst (typischerweise ein Rechtsklick)
    :param plugin_manager: Der PluginManager, um Plugin-Einträge zu erhalten
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

    # Plugin-Einträge hinzufügen
    plugin_entries = plugin_manager.get_plugin_context_menu_entries()
    if plugin_entries:
        context_menu.add_separator()
        for entry in plugin_entries:
            context_menu.add_command(label=entry['label'], command=entry['command'])

    context_menu.tk_popup(event.x_root, event.y_root)
    logger.debug("Kontextmenü erstellt und angezeigt")


@handle_exceptions
def convert_text(text_widget: tk.Text, conversion_function: Callable[[str], str]) -> None:
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


# Zusätzliche Erklärungen:

# 1. Lambda-Funktionen:
#    Die Lambda-Funktionen werden verwendet, um die Tkinter-Ereignisse auszulösen,
#    die die Standardaktionen für Ausschneiden, Kopieren, etc. implementieren.
#    Dies ermöglicht eine direkte Bindung der Aktionen an die Menüeinträge.

# 2. Konvertierungsfunktionen:
#    Die Funktionen words_to_digits und digits_to_words werden aus dem Backend-Modul
#    importiert. Dies gewährleistet eine konsistente Textverarbeitung in der gesamten Anwendung.

# 3. Fehlerbehandlung:
#    Die try-except-Struktur in convert_text fängt den Fall ab, dass kein Text
#    ausgewählt ist, wenn die Konvertierung versucht wird. Dies verhindert unerwartete
#    Fehler und verbessert die Benutzerfreundlichkeit.

# 4. Logging:
#    Die Verwendung des Loggers ermöglicht eine konsistente Fehlerprotokollierung
#    und erleichtert das Debugging.

# 5. Typisierung:
#    Die Funktionsparameter wurden mit Typ-Hinweisen versehen, um die Codequalität
#    und Lesbarkeit zu verbessern.
