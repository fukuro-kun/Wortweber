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
from tkinter import ttk
from pynput import keyboard
from src.utils.error_handling import handle_exceptions, logger
from src.config import DEFAULT_PUSH_TO_TALK_KEY

class ShortcutPanel(ttk.Frame):
    """
    Ein Panel zur Anpassung von Tastaturkürzeln in der Wortweber-Anwendung.
    """

    @handle_exceptions
    def __init__(self, parent, settings_manager, input_processor):
        """
        Initialisiert das ShortcutPanel.

        :param parent: Das übergeordnete Tkinter-Widget
        :param settings_manager: Der SettingsManager der Anwendung
        :param input_processor: Der InputProcessor der Anwendung
        """
        super().__init__(parent)
        self.settings_manager = settings_manager
        self.input_processor = input_processor
        self.current_shortcut = tk.StringVar(value=self.settings_manager.get_setting("push_to_talk_key", DEFAULT_PUSH_TO_TALK_KEY))
        self.listening_for_key = False
        self.active_modifiers = set()
        self.setup_ui()
        logger.info("ShortcutPanel initialisiert")

    @handle_exceptions
    def setup_ui(self):
        """Richtet die Benutzeroberfläche für das ShortcutPanel ein."""
        ttk.Label(self, text="Push-to-Talk Shortcut:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.shortcut_display = ttk.Entry(self, textvariable=self.current_shortcut, state="readonly", width=20)
        self.shortcut_display.grid(row=0, column=1, padx=5, pady=5)
        self.change_button = ttk.Button(self, text="Ändern", command=self.start_shortcut_change)
        self.change_button.grid(row=0, column=2, padx=5, pady=5)

        # Anzeige für aktive Modifikatoren
        self.modifier_display = ttk.Label(self, text="")
        self.modifier_display.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="w")

        # Erklärungstext hinzufügen
        explanation_text = ("Klicken Sie auf 'Ändern' und drücken Sie dann die gewünschte Taste oder Tastenkombination.\n"
                            "Die Änderung wird sofort wirksam.")
        explanation_label = ttk.Label(self, text=explanation_text, wraplength=300, justify="left")
        explanation_label.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="w")

        logger.debug("ShortcutPanel UI eingerichtet")

    @handle_exceptions
    def start_shortcut_change(self):
        """Startet den Prozess zur Änderung des Shortcuts."""
        if not self.listening_for_key:
            self.listening_for_key = True
            self.change_button.config(state="disabled")
            self.shortcut_display.config(state="normal")
            self.shortcut_display.delete(0, tk.END)
            self.shortcut_display.insert(0, "Drücken Sie eine Taste...")
            self.shortcut_display.config(state="readonly")
            self.active_modifiers.clear()
            self.update_modifier_display()
            self.focus_set()
            self.bind('<KeyPress>', self.on_key_press)
            self.bind('<KeyRelease>', self.on_key_release)
            logger.info("Warte auf Shortcut-Eingabe")
        else:
            self.stop_listening()

    @handle_exceptions
    def on_key_press(self, event):
        """
        Verarbeitet den Tastendruck für den neuen Shortcut.

        :param event: Das Tastenereignis
        """
        key = event.keysym
        if key in ('Shift_L', 'Shift_R', 'Control_L', 'Control_R', 'Alt_L', 'Alt_R'):
            self.active_modifiers.add(key.split('_')[0])
            self.update_modifier_display()
        else:
            new_shortcut = self.format_shortcut(key)
            self.stop_listening()
            if self.is_valid_shortcut(new_shortcut):
                self.current_shortcut.set(new_shortcut)
                self.settings_manager.set_setting("push_to_talk_key", new_shortcut)
                self.input_processor.update_shortcut(new_shortcut)
                logger.info(f"Shortcut geändert auf: {new_shortcut}")
            else:
                self.current_shortcut.set(self.settings_manager.get_setting("push_to_talk_key", DEFAULT_PUSH_TO_TALK_KEY))
                logger.warning(f"Ungültiger Shortcut: {new_shortcut}")

    @handle_exceptions
    def on_key_release(self, event):
        """
        Verarbeitet das Loslassen einer Taste während der Shortcut-Eingabe.

        :param event: Das Tastenereignis
        """
        key = event.keysym
        if key in ('Shift_L', 'Shift_R', 'Control_L', 'Control_R', 'Alt_L', 'Alt_R'):
            self.active_modifiers.discard(key.split('_')[0])
            self.update_modifier_display()

    @handle_exceptions
    def update_modifier_display(self):
        """Aktualisiert die Anzeige der aktiven Modifikatortasten."""
        modifier_text = " + ".join(sorted(self.active_modifiers)) if self.active_modifiers else "Keine Modifikatoren"
        self.modifier_display.config(text=f"Aktive Modifikatoren: {modifier_text}")

    @handle_exceptions
    def stop_listening(self):
        """Beendet den Prozess zur Änderung des Shortcuts."""
        self.listening_for_key = False
        self.unbind('<KeyPress>')
        self.unbind('<KeyRelease>')
        self.change_button.config(state="normal")
        self.active_modifiers.clear()
        self.update_modifier_display()
        logger.debug("Shortcut-Änderung beendet")

    @handle_exceptions
    def is_valid_shortcut(self, shortcut):
        """
        Überprüft, ob der eingegebene Shortcut gültig ist.

        :param shortcut: Der zu überprüfende Shortcut
        :return: True, wenn der Shortcut gültig ist, sonst False
        """
        parts = shortcut.split('+')
        if len(parts) == 1:
            # Einzelne Taste (ohne Modifikatoren)
            return parts[0] in ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12']
        elif len(parts) > 1:
            # Tastenkombination mit Modifikatoren
            modifiers = parts[:-1]
            key = parts[-1]
            valid_modifiers = all(mod in ['Control', 'Shift', 'Alt'] for mod in modifiers)
            valid_key = key.isalpha() or key in ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12']
            return valid_modifiers and valid_key
        return False

    @handle_exceptions
    def format_shortcut(self, key):
        """
        Formatiert den Shortcut als String.

        :param key: Die Haupttaste des Shortcuts
        :return: Formatierter Shortcut-String
        """
        modifiers = sorted(self.active_modifiers)
        if modifiers:
            return "+".join(modifiers + [key])
        return key

    @handle_exceptions
    def reset_to_default(self):
        """Setzt den Shortcut auf den Standardwert zurück."""
        default_shortcut = DEFAULT_PUSH_TO_TALK_KEY
        self.current_shortcut.set(default_shortcut)
        self.settings_manager.set_setting("push_to_talk_key", default_shortcut)
        self.input_processor.update_shortcut(default_shortcut)
        logger.info(f"Shortcut auf Standardwert zurückgesetzt: {default_shortcut}")

# Zusätzliche Erklärungen:

# 1. Flexibilität bei Tastenkombinationen:
#    - Die Klasse unterstützt nun Kombinationen von Modifikatortasten (Ctrl, Shift, Alt) mit anderen Tasten.
#    - Die aktiven Modifikatoren werden in Echtzeit angezeigt.

# 2. Verbesserte Validierung:
#    - Die is_valid_shortcut-Methode wurde erweitert, um verschiedene Kombinationen zu überprüfen.
#    - Es werden sowohl einzelne Funktionstasten als auch Kombinationen mit Buchstaben unterstützt.

# 3. Echtzeitanzeige der Modifikatoren:
#    - Die update_modifier_display-Methode zeigt dem Benutzer, welche Modifikatoren gerade aktiv sind.

# 4. Verbesserte Benutzerfreundlichkeit:
#    - Klare Anweisungen und Echtzeit-Feedback machen den Prozess der Shortcut-Änderung intuitiver.

# 5. Robuste Fehlerbehandlung:
#    - Alle Methoden verwenden den @handle_exceptions Decorator für konsistente Fehlerbehandlung.

# 6. Logging:
#    - Ausführliches Logging hilft bei der Nachverfolgung von Änderungen und möglichen Problemen.

# Diese Implementierung bietet eine flexible und benutzerfreundliche Möglichkeit,
# den Push-to-Talk-Shortcut anzupassen, und integriert sich nahtlos in die bestehende Wortweber-Anwendung.
