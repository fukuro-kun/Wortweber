from pynput import keyboard
from pynput.keyboard import Key, Controller as KeyboardController
import pyperclip
import time
import threading
import logging
from src.config import PUSH_TO_TALK_KEY

class InputProcessor:
    def __init__(self, gui):
        self.gui = gui
        self.keyboard_controller = KeyboardController()
        self.listener = None

    def start_listener(self):
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()

    def stop_listener(self):
        if self.listener:
            self.listener.stop()

    def on_press(self, key):
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
        while not self.gui.backend.model_loaded.is_set():
            time.sleep(0.5)
        self.gui.transcribe_and_update()

    def process_text(self, text):
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
