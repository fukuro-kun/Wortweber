from pynput import keyboard
from pynput.keyboard import Key, Controller as KeyboardController
import pyperclip
import time
import threading

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
        if key == keyboard.Key.f12 and not self.gui.backend.state.recording:
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
        if key == keyboard.Key.f12 and self.gui.backend.state.recording:
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
                pyperclip.copy(text)
                with self.keyboard_controller.pressed(Key.ctrl):
                    self.keyboard_controller.press('v')
                    self.keyboard_controller.release('v')

        if self.gui.status_panel.auto_copy_var.get():
            pyperclip.copy(text)
            self.gui.status_panel.update_status("Text transkribiert und in Zwischenablage kopiert", "green")
        else:
            self.gui.status_panel.update_status("Text transkribiert", "green")
