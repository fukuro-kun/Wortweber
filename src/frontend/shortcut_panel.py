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

        # Erklärungstext hinzufügen
        explanation_text = ("Klicken Sie auf 'Ändern' und drücken Sie dann die gewünschte Taste oder Tastenkombination.\n"
                            "Die Änderung wird sofort wirksam.")
        explanation_label = ttk.Label(self, text=explanation_text, wraplength=300, justify="left")
        explanation_label.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="w")

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
            self.focus_set()
            self.bind('<Key>', self.on_key_press)
            logger.info("Warte auf Shortcut-Eingabe")
        else:
            self.stop_listening()

    @handle_exceptions
    def on_key_press(self, event):
        """
        Verarbeitet den Tastendruck für den neuen Shortcut.

        :param event: Das Tastenereignis
        """
        if event.keysym in ('Shift_L', 'Shift_R', 'Control_L', 'Control_R', 'Alt_L', 'Alt_R'):
            return

        new_shortcut = event.keysym
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
    def stop_listening(self):
        """Beendet den Prozess zur Änderung des Shortcuts."""
        self.listening_for_key = False
        self.unbind('<Key>')
        self.change_button.config(state="normal")
        logger.debug("Shortcut-Änderung beendet")

    @handle_exceptions
    def is_valid_shortcut(self, shortcut):
        """
        Überprüft, ob der eingegebene Shortcut gültig ist.

        :param shortcut: Der zu überprüfende Shortcut
        :return: True, wenn der Shortcut gültig ist, sonst False
        """
        valid_shortcuts = ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12']
        return shortcut in valid_shortcuts

    @handle_exceptions
    def reset_to_default(self):
        """Setzt den Shortcut auf den Standardwert zurück."""
        default_shortcut = DEFAULT_PUSH_TO_TALK_KEY
        self.current_shortcut.set(default_shortcut)
        self.settings_manager.set_setting("push_to_talk_key", default_shortcut)
        self.input_processor.update_shortcut(default_shortcut)
        logger.info(f"Shortcut auf Standardwert zurückgesetzt: {default_shortcut}")

# Zusätzliche Erklärungen:

# 1. Robustheit:
#    - Die Klasse verwendet Fehlerbehandlung und Logging für alle Methoden.
#    - Es gibt eine Überprüfung auf gültige Shortcuts, um unerwünschte Eingaben zu verhindern.
#    - Der Zustand des Panels wird korrekt verwaltet, um gleichzeitige Änderungen zu vermeiden.

# 2. Benutzerfreundlichkeit:
#    - Ein Erklärungstext informiert den Benutzer über die Funktionsweise.
#    - Der aktuelle Shortcut wird immer angezeigt und sofort aktualisiert.
#    - Es gibt eine Methode zum Zurücksetzen auf den Standardwert.

# 3. Integration:
#    - Die Klasse arbeitet eng mit dem SettingsManager und InputProcessor zusammen.
#    - Änderungen werden sofort gespeichert und angewendet.

# 4. Erweiterbarkeit:
#    - Die Struktur erlaubt einfache Erweiterungen für zusätzliche Shortcuts in der Zukunft.
#    - Die Validierungslogik kann leicht angepasst werden, um mehr oder andere Tasten zuzulassen.

# Diese Implementierung bietet eine robuste und benutzerfreundliche Möglichkeit,
# den Push-to-Talk-Shortcut anzupassen, und integriert sich gut in die bestehende Wortweber-Anwendung.
