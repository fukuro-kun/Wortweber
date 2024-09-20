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
        self.push_to_talk_key = self.parse_shortcut(self.gui.settings_manager.get_setting("push_to_talk_key", DEFAULT_PUSH_TO_TALK_KEY))
        self.currently_pressed_keys = set()
        self.recording_active = False
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

        :param key: Die gedrückte Taste
        """
        normalized_key = self.normalize_key(key)
        self.currently_pressed_keys.add(normalized_key)
        logger.debug(f"Taste gedrückt: {normalized_key}")
        logger.debug(f"Aktuell gedrückte Tasten: {self.currently_pressed_keys}")

        if self.is_push_to_talk_key(key) and not self.recording_active:
            self.start_recording()

    @handle_exceptions
    def on_release(self, key):
        """
        Wird aufgerufen, wenn eine Taste losgelassen wird.

        :param key: Die losgelassene Taste
        """
        normalized_key = self.normalize_key(key)
        self.currently_pressed_keys.discard(normalized_key)
        logger.debug(f"Taste losgelassen: {normalized_key}")
        logger.debug(f"Aktuell gedrückte Tasten nach Loslassen: {self.currently_pressed_keys}")

        if self.recording_active and self.is_push_to_talk_key(key):
            self.stop_recording()


    @handle_exceptions
    def is_push_to_talk_key(self, key):
        """
        Überprüft, ob die aktuelle Tastenkombination dem Push-to-Talk-Shortcut entspricht.

        :param key: Die zu überprüfende Taste
        :return: True, wenn es die Push-to-Talk-Tastenkombination ist, sonst False
        """
        required_modifiers = self.push_to_talk_key['modifiers']
        required_key = self.push_to_talk_key['key']

        logger.debug(f"Überprüfe Push-to-Talk für Taste: {key}")
        logger.debug(f"Erforderliche Modifikatoren: {required_modifiers}")
        logger.debug(f"Erforderliche Haupttaste: {required_key}")
        logger.debug(f"Aktuell gedrückte Tasten: {self.currently_pressed_keys}")

        if not required_modifiers:
            # Für einzelne Tasten ohne Modifikatoren
            return self.normalize_key(key) == required_key.lower()

        # Für Tastenkombinationen
        return all(mod.name.lower() in self.currently_pressed_keys for mod in required_modifiers) and \
               self.normalize_key(key) == required_key.lower()

    @handle_exceptions
    def normalize_key(self, key):
        """
        Normalisiert den Tastenname für konsistente Vergleiche.

        :param key: Die zu normalisierende Taste
        :return: Der normalisierte Tastenwert
        """
        if isinstance(key, keyboard.Key):
            return key.name.lower()
        elif isinstance(key, keyboard.KeyCode):
            return key.char.lower() if key.char else f"key.{key.vk}"
        return str(key).lower()

    @handle_exceptions
    def parse_shortcut(self, shortcut_str):
        """
        Parst den Shortcut-String in ein Dictionary mit Tasten und Modifikatoren.

        :param shortcut_str: Der zu parsende Shortcut-String
        :return: Ein Dictionary mit den geparsten Tasten und Modifikatoren
        """
        parts = shortcut_str.split('+')
        modifiers = set()
        key = None

        for part in parts:
            part = part.strip().lower()
            if part in ['ctrl', 'control']:
                modifiers.add(Key.ctrl)
            elif part == 'shift':
                modifiers.add(Key.shift)
            elif part == 'alt':
                modifiers.add(Key.alt)
            else:
                # Letzte Teil ist die Haupttaste
                key = part.upper() if part.startswith('f') and part[1:].isdigit() else part

        logger.debug(f"Geparster Shortcut: Modifikatoren={modifiers}, Haupttaste={key}")
        return {'modifiers': modifiers, 'key': key}

    @handle_exceptions
    def start_recording(self):
        """Startet die Audioaufnahme."""
        if not self.gui.backend.model_loaded.is_set():
            self.gui.main_window.update_status_bar(status="Modell wird noch geladen. Aufnahme startet trotzdem.", status_color="yellow")
            logger.warning("Aufnahme gestartet, obwohl Modell noch nicht geladen ist")
        try:
            if self.gui.backend.check_audio_device():
                self.gui.backend.start_recording()
                self.gui.main_window.update_status_bar(status="Aufnahme läuft...", status_color="red")
                self.gui.start_timer()
                self.recording_active = True
                logger.info("Audioaufnahme gestartet")
            else:
                self.gui.main_window.update_status_bar(status="Audiogerät nicht verfügbar", status_color="red")
                logger.error("Audiogerät nicht verfügbar")
        except Exception as e:
            self.gui.main_window.update_status_bar(status=f"Fehler beim Starten der Aufnahme: {e}", status_color="red")
            logger.error(f"Fehler beim Starten der Aufnahme: {e}")

    @handle_exceptions
    def stop_recording(self):
        """Stoppt die Audioaufnahme und startet die Transkription."""
        self.gui.backend.stop_recording()
        self.gui.main_window.update_status_bar(status="Aufnahme beendet", status_color="orange")
        self.gui.stop_timer()
        self.recording_active = False
        logger.info("Audioaufnahme beendet")
        if self.gui.backend.model_loaded.is_set():
            self.gui.transcribe_and_update()
        else:
            self.gui.main_window.update_status_bar(status="Aufnahme gespeichert. Warte auf Modell-Bereitschaft.", status_color="yellow")
            logger.info("Aufnahme gespeichert. Warten auf Modell-Bereitschaft.")
            threading.Thread(target=self.wait_and_transcribe, daemon=True).start()

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
        Aktualisiert den Push-to-Talk-Shortcut ohne eine Transkription auszulösen.

        :param new_shortcut: Der neue Shortcut-Wert
        """
        # Temporär den Listener deaktivieren
        self.stop_listener()

        # Shortcut aktualisieren
        self.push_to_talk_key = self.parse_shortcut(new_shortcut)
        logger.info(f"Push-to-Talk-Shortcut aktualisiert auf: {new_shortcut}")

        # Sicherstellen, dass keine Aufnahme aktiv ist
        if self.recording_active:
            self.stop_recording()

        # Tastenstatus zurücksetzen
        self.currently_pressed_keys.clear()
        self.recording_active = False

        # Listener neu starten
        self.start_listener()


# Zusätzliche Erklärungen:

# 1. Verbesserte Shortcut-Erkennung:
#    Die is_push_to_talk_key Methode wurde überarbeitet, um sowohl einzelne Tasten
#    als auch Kombinationen mit Modifikatoren zuverlässig zu erkennen.

# 2. Robustes Tasten-Tracking:
#    Mit self.currently_pressed_keys wird ein Set aller aktuell gedrückten Tasten
#    präzise verwaltet. Dies ermöglicht eine genaue Erkennung von Tastenkombinationen.

# 3. Separate Aufnahmesteuerung:
#    Die Methoden start_recording und stop_recording wurden eingeführt, um die
#    Aufnahmelogik zu zentralisieren und besser zu kontrollieren.

# 4. Verbessertes Logging:
#    Zusätzliche Debug-Logging-Aufrufe wurden hinzugefügt, um die Nachvollziehbarkeit
#    der Tastenerkennung und Shortcut-Verarbeitung zu erhöhen.

# 5. Flexibilität bei Shortcuts:
#    Die parse_shortcut Methode wurde verbessert, um verschiedene Shortcut-Formate
#    zu unterstützen und korrekt zu interpretieren.

# Diese Implementierung bietet eine robuste und flexible Lösung für die Handhabung
# von Push-to-Talk-Shortcuts, einschließlich einzelner Tasten und komplexer
# Tastenkombinationen, und integriert sich nahtlos in die bestehende Struktur
# der Wortweber-Anwendung.
