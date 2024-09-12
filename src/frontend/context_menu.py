import tkinter as tk
from src.backend.text_processor import words_to_digits, digits_to_words

def create_context_menu(text_widget, event):
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

def convert_text(text_widget, conversion_function):
    try:
        selected_text = text_widget.get(tk.SEL_FIRST, tk.SEL_LAST)
        converted_text = conversion_function(selected_text)
        text_widget.delete(tk.SEL_FIRST, tk.SEL_LAST)
        text_widget.insert(tk.INSERT, converted_text)
    except tk.TclError:
        # Kein Text ausgewählt
        pass
