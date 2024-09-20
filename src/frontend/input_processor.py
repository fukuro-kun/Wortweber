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
#
# This file uses pynput, which is licensed under LGPLv3.
# pynput is used as a dynamically linked library in compliance with LGPLv3.

"""
Dieses Modul enthält die InputProcessor-Klasse, die für die Verarbeitung von
Benutzereingaben und die Steuerung der Audioaufnahme und Texteingabe zuständig ist.
"""

from pynput import keyboard
from pynput.keyboard import Key, Controller as KeyboardController
import pyperclip
import time
import threading
from src.config import DEFAULT_PUSH_TO_TALK_KEY, DEFAULT_INCOGNITO_MODE, DEFAULT_CHAR_DELAY
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
        self.start_time = 0
        self.push_to_talk_key = self.gui.settings_manager.get_setting("push_to_talk_key", DEFAULT_PUSH_TO_TALK_KEY)
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
        if self.is_push_to_talk_key(key) and not self.gui.backend.state.recording:
            if not self.gui.backend.model_loaded.is_set():
                self.gui.main_window.update_status_bar(status="Modell wird noch geladen. Aufnahme startet trotzdem.", status_color="yellow")
                logger.warning("Aufnahme gestartet, obwohl Modell noch nicht geladen ist")
            try:
                if self.gui.backend.check_audio_device():
                    self.gui.backend.start_recording()
                    self.gui.main_window.update_status_bar(status="Aufnahme läuft...", status_color="red")
                    self.gui.start_timer()
                    logger.info("Audioaufnahme gestartet")
                else:
                    self.gui.main_window.update_status_bar(status="Audiogerät nicht verfügbar", status_color="red")
                    logger.error("Audiogerät nicht verfügbar")
            except Exception as e:
                self.gui.main_window.update_status_bar(status=f"Fehler beim Starten der Aufnahme: {e}", status_color="red")
                logger.error(f"Fehler beim Starten der Aufnahme: {e}")

    @handle_exceptions
    def on_release(self, key):
        if self.is_push_to_talk_key(key) and self.gui.backend.state.recording:
            self.gui.backend.stop_recording()
            self.gui.main_window.update_status_bar(status="Aufnahme beendet", status_color="orange")
            self.gui.stop_timer()
            logger.info("Audioaufnahme beendet")
            if self.gui.backend.model_loaded.is_set():
                self.gui.transcribe_and_update()
            else:
                self.gui.main_window.update_status_bar(status="Aufnahme gespeichert. Warte auf Modell-Bereitschaft.", status_color="yellow")
                logger.info("Aufnahme gespeichert. Warten auf Modell-Bereitschaft.")
                threading.Thread(target=self.wait_and_transcribe, daemon=True).start()

    @handle_exceptions
    def is_push_to_talk_key(self, key):
        """
        Überprüft, ob die gedrückte Taste der Push-to-Talk-Taste entspricht.

        :param key: Die gedrückte Taste
        :return: True, wenn es die Push-to-Talk-Taste ist, sonst False
        """
        if isinstance(key, keyboard.Key):
            return key == getattr(keyboard.Key, self.push_to_talk_key.lower(), None)
        elif isinstance(key, keyboard.KeyCode):
            return key.char == self.push_to_talk_key
        return False

    @handle_exceptions
    def update_record_time(self):
        """Aktualisiert die angezeigte Aufnahmezeit."""
        if self.gui.backend.state.recording:
            elapsed_time = time.time() - self.start_time
            self.gui.main_window.update_status_bar(record_time=elapsed_time)
            self.gui.root.after(100, self.update_record_time)

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
        input_mode = self.gui.settings_manager.get_setting("output_mode", "textfenster")
        delay_mode = self.gui.settings_manager.get_setting("delay_mode", "no_delay")

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
                    delay = float(self.gui.settings_manager.get_setting("char_delay", DEFAULT_CHAR_DELAY)) / 1000
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

        if self.gui.main_window.auto_copy_var.get():
            original_clipboard = pyperclip.paste()
            pyperclip.copy(text)
            if not incognito_mode:
                logger.debug(f"Text in Zwischenablage kopiert: {text[:50]}...")
            self.gui.main_window.update_status_bar(status="Text transkribiert und in Zwischenablage kopiert", status_color="green")
        else:
            self.gui.main_window.update_status_bar(status="Text transkribiert", status_color="green")

        if not incognito_mode:
            logger.debug(f"Finaler Zwischenablage-Inhalt: {pyperclip.paste()[:50]}...")

    @handle_exceptions
    def update_shortcut(self, new_shortcut):
        """
        Aktualisiert den Push-to-Talk-Shortcut.

        :param new_shortcut: Der neue Shortcut-Wert
        """
        self.push_to_talk_key = new_shortcut
        logger.info(f"Push-to-Talk-Shortcut aktualisiert auf: {new_shortcut}")
        # Neustart des Listeners, um den neuen Shortcut zu aktivieren
        self.stop_listener()
        self.start_listener()

# Zusätzliche Erklärungen:

# 1. Shortcut-Aktualisierung:
#    Die neue Methode update_shortcut ermöglicht es, den Push-to-Talk-Shortcut
#    zur Laufzeit zu ändern. Sie aktualisiert den internen Zustand und startet
#    den Listener neu, um die Änderung wirksam zu machen.

# 2. Flexibler Shortcut-Check:
#    Die Methode is_push_to_talk_key wurde hinzugefügt, um flexibel verschiedene
#    Tastentypen (normale Tasten und Funktionstasten) als Shortcut zu unterstützen.

# 3. Verbesserte Fehlerbehandlung:
#    Alle Methoden sind weiterhin mit dem @handle_exceptions Decorator versehen,
#    was eine konsistente Fehlerbehandlung und Logging in der gesamten Klasse gewährleistet.

# 4. Konfigurationsintegration:
#    Die Klasse nutzt nun die DEFAULT_PUSH_TO_TALK_KEY-Konstante aus der Konfigurationsdatei,
#    was eine zentrale Verwaltung von Standardwerten ermöglicht.

# 5. Logging:
#    Umfangreiches Logging wurde beibehalten und um zusätzliche Informationen zur
#    Shortcut-Änderung erweitert.

# Diese Implementierung ermöglicht eine flexible Anpassung des Push-to-Talk-Shortcuts
# und integriert sich nahtlos in die bestehende Struktur der Wortweber-Anwendung.
