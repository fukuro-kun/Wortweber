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
from src.config import PUSH_TO_TALK_KEY, DEFAULT_INCOGNITO_MODE
from src.utils.error_handling import handle_exceptions, logger

class InputProcessor:
    """
    Verarbeitet Benutzereingaben und steuert die Audioaufnahme und Texteingabe.
    """

    @handle_exceptions
    def __init__(self, gui):
        """
        Initialisiert den InputProcessor.

        :param gui: Referenz auf die Hauptgui-Instanz
        """
        self.gui = gui
        self.keyboard_controller = KeyboardController()
        self.listener = None
        logger.info("InputProcessor initialisiert")

    @handle_exceptions
    def start_listener(self):
        """Startet den Tastatur-Listener für die Push-to-Talk-Funktion."""
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()
        logger.info("Tastatur-Listener gestartet")

    @handle_exceptions
    def stop_listener(self):
        """Stoppt den Tastatur-Listener."""
        if self.listener:
            self.listener.stop()
            logger.info("Tastatur-Listener gestoppt")

    @handle_exceptions
    def on_press(self, key):
        """
        Wird aufgerufen, wenn eine Taste gedrückt wird.
        Startet die Audioaufnahme, wenn die Push-to-Talk-Taste gedrückt wird.

        :param key: Die gedrückte Taste
        """
        if key == getattr(keyboard.Key, PUSH_TO_TALK_KEY.lower()) and not self.gui.backend.state.recording:
            if not self.gui.backend.model_loaded.is_set():
                self.gui.status_panel.update_status("Modell wird noch geladen. Aufnahme startet trotzdem.", "orange")
                logger.warning("Aufnahme gestartet, obwohl Modell noch nicht geladen ist")
            try:
                if self.gui.backend.check_audio_device():
                    self.gui.backend.start_recording()
                    self.gui.status_panel.update_status("Aufnahme läuft...", "red")
                    self.gui.start_timer()
                    logger.info("Audioaufnahme gestartet")
                else:
                    self.gui.status_panel.update_status("Audiogerät nicht verfügbar", "red")
                    logger.error("Audiogerät nicht verfügbar")
            except Exception as e:
                self.gui.status_panel.update_status(f"Fehler beim Starten der Aufnahme: {e}", "red")
                logger.error(f"Fehler beim Starten der Aufnahme: {e}")

    @handle_exceptions
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
            logger.info("Audioaufnahme beendet")
            if self.gui.backend.model_loaded.is_set():
                self.gui.transcribe_and_update()
            else:
                self.gui.status_panel.update_status("Aufnahme gespeichert. Warte auf Modell-Bereitschaft.", "orange")
                logger.info("Aufnahme gespeichert. Warten auf Modell-Bereitschaft.")
                threading.Thread(target=self.wait_and_transcribe, daemon=True).start()

    @handle_exceptions
    def wait_and_transcribe(self):
        """
        Wartet, bis das Modell geladen ist, und führt dann die Transkription durch.
        Wird in einem separaten Thread ausgeführt.
        """
        while not self.gui.backend.model_loaded.is_set():
            time.sleep(0.5)
        self.gui.transcribe_and_update()
        logger.info("Transkription nach Modellladung durchgeführt")

    @handle_exceptions
    def process_text(self, text):
        """
        Verarbeitet den transkribierten Text basierend auf den aktuellen Einstellungen.

        :param text: Der zu verarbeitende Text
        """
        input_mode = self.gui.options_panel.input_mode_var.get()
        delay_mode = self.gui.options_panel.delay_mode_var.get()

        incognito_mode = self.gui.settings_manager.get_setting("incognito_mode", DEFAULT_INCOGNITO_MODE)
        if not incognito_mode:
            logger.debug(f"Verarbeite Text: Eingabemodus = {input_mode}, Verzögerungsmodus = {delay_mode}, Textlänge = {len(text)}")
        else:
            logger.debug(f"Verarbeite Text (Incognito-Modus aktiv): Eingabemodus = {input_mode}, Verzögerungsmodus = {delay_mode}")

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
                if not incognito_mode:
                    logger.debug(f"Originaler Zwischenablage-Inhalt: {original_clipboard[:50]}...")

                pyperclip.copy(text)
                with self.keyboard_controller.pressed(Key.ctrl):
                    self.keyboard_controller.press('v')
                    self.keyboard_controller.release('v')

                pyperclip.copy(original_clipboard)
                if not incognito_mode:
                    logger.debug(f"Zwischenablage-Inhalt nach Wiederherstellung: {pyperclip.paste()[:50]}...")

        if self.gui.status_panel.auto_copy_var.get():
            original_clipboard = pyperclip.paste()
            pyperclip.copy(text)
            if not incognito_mode:
                logger.debug(f"Text in Zwischenablage kopiert: {text[:50]}...")
            self.gui.status_panel.update_status("Text transkribiert und in Zwischenablage kopiert", "green")
        else:
            self.gui.status_panel.update_status("Text transkribiert", "green")

        if not incognito_mode:
            logger.debug(f"Finaler Zwischenablage-Inhalt: {pyperclip.paste()[:50]}...")

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
