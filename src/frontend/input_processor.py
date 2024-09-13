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

from pynput import keyboard
from pynput.keyboard import Key, Controller as KeyboardController
import pyperclip
import time
import threading
import logging
from src.config import PUSH_TO_TALK_KEY

class InputProcessor:
    """
    Verarbeitet Benutzereingaben und steuert die Audioaufnahme und Texteingabe.
    """

    def __init__(self, gui):
        """
        Initialisiert den InputProcessor.

        :param gui: Referenz auf die Hauptgui-Instanz
        """
        self.gui = gui
        self.keyboard_controller = KeyboardController()
        self.listener = None

    def start_listener(self):
        """Startet den Tastatur-Listener für die Push-to-Talk-Funktion."""
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()

    def stop_listener(self):
        """Stoppt den Tastatur-Listener."""
        if self.listener:
            self.listener.stop()

    def on_press(self, key):
        """
        Wird aufgerufen, wenn eine Taste gedrückt wird.
        Startet die Audioaufnahme, wenn die Push-to-Talk-Taste gedrückt wird.

        :param key: Die gedrückte Taste
        """
        if key == getattr(keyboard.Key, PUSH_TO_TALK_KEY.lower()) and not self.gui.backend.state.recording:
            if not self.gui.backend.model_loaded.is_set():
                self.gui.status_panel.update_status("Modell wird noch geladen. Aufnahme startet trotzdem.", "orange")
            try:
                if self.gui.backend.check_audio_device():
                    self.gui.backend.start_recording()
                    self.gui.status_panel.update_status("Aufnahme läuft...", "red")
                    self.gui.start_timer()
                else:
                    self.gui.status_panel.update_status("Audiogerät nicht verfügbar", "red")
            except Exception as e:
                self.gui.status_panel.update_status(f"Fehler beim Starten der Aufnahme: {e}", "red")

    def on_release(self, key):
        """
        Wird aufgerufen, wenn eine Taste losgelassen wird.
        Beendet die Audioaufnahme und startet die Transkription, wenn die Push-to-Talk-Taste losgelassen wird.

        :param key: Die losgelassene Taste
        """
        if key == getattr(keyboard.Key, PUSH_TO_TALK_KEY.lower()) and self.gui.backend.state.recording:
            self.gui.backend.stop_recording()
            self.gui.status_panel.update_status("Aufnahme beendet", "orange")
            self.gui.stop_timer()
            if self.gui.backend.model_loaded.is_set():
                self.gui.transcribe_and_update()
            else:
                self.gui.status_panel.update_status("Aufnahme gespeichert. Warte auf Modell-Bereitschaft.", "orange")
                threading.Thread(target=self.wait_and_transcribe, daemon=True).start()

    def wait_and_transcribe(self):
        """
        Wartet, bis das Modell geladen ist, und führt dann die Transkription durch.
        Wird in einem separaten Thread ausgeführt.
        """
        while not self.gui.backend.model_loaded.is_set():
            time.sleep(0.5)
        self.gui.transcribe_and_update()

    def process_text(self, text):
        """
        Verarbeitet den transkribierten Text basierend auf den aktuellen Einstellungen.

        :param text: Der zu verarbeitende Text
        """
        input_mode = self.gui.options_panel.input_mode_var.get()
        delay_mode = self.gui.options_panel.delay_mode_var.get()

        logging.debug(f"Verarbeite Text: Eingabemodus = {input_mode}, Verzögerungsmodus = {delay_mode}")

        if input_mode == "textfenster":
            self.gui.transcription_panel.insert_text(text)
        else:
            if delay_mode == "no_delay":
                self.keyboard_controller.type(text)
            elif delay_mode == "char_delay":
                try:
                    delay = float(self.gui.options_panel.char_delay_entry.get()) / 1000
                except ValueError:
                    delay = 0.01  # Fallback auf 10ms bei ungültiger Eingabe
                for char in text:
                    self.keyboard_controller.type(char)
                    time.sleep(delay)
            elif delay_mode == "clipboard":
                original_clipboard = pyperclip.paste()
                logging.debug(f"Originaler Zwischenablage-Inhalt: {original_clipboard[:50]}...")

                pyperclip.copy(text)
                with self.keyboard_controller.pressed(Key.ctrl):
                    self.keyboard_controller.press('v')
                    self.keyboard_controller.release('v')

                pyperclip.copy(original_clipboard)
                logging.debug(f"Zwischenablage-Inhalt nach Wiederherstellung: {pyperclip.paste()[:50]}...")

        if self.gui.status_panel.auto_copy_var.get():
            original_clipboard = pyperclip.paste()
            pyperclip.copy(text)
            logging.debug(f"Text in Zwischenablage kopiert: {text[:50]}...")
            self.gui.status_panel.update_status("Text transkribiert und in Zwischenablage kopiert", "green")
        else:
            self.gui.status_panel.update_status("Text transkribiert", "green")

        logging.debug(f"Finaler Zwischenablage-Inhalt: {pyperclip.paste()[:50]}...")

# Zusätzliche Erklärungen:

# 1. Push-to-Talk-Funktionalität:
#    Die Methoden on_press und on_release implementieren die Push-to-Talk-Funktion.
#    Sie starten und stoppen die Audioaufnahme basierend auf dem Drücken und Loslassen der definierten Taste.

# 2. Asynchrone Verarbeitung:
#    Die wait_and_transcribe-Methode wird in einem separaten Thread ausgeführt, um die GUI reaktiv zu halten,
#    während auf das Laden des Modells gewartet wird.

# 3. Flexible Texteingabe:
#    Die process_text-Methode bietet verschiedene Möglichkeiten zur Texteingabe, einschließlich
#    direkter Eingabe ins Textfenster, Simulation von Tastatureingaben und Verwendung der Zwischenablage.

# 4. Fehlerbehandlung und Logging:
#    Umfangreiches Logging hilft bei der Diagnose von Problemen, insbesondere bei der Zwischenablagenverarbeitung.

# 5. Konfigurierbare Verzögerungen:
#    Die Implementierung verschiedener Verzögerungsmodi (keine, zeichenweise, Zwischenablage) bietet Flexibilität
#    für verschiedene Anwendungsfälle und Systemkonfigurationen.
