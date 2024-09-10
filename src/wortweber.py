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

from typing import List, Optional
import tkinter as tk
from tkinter import scrolledtext, ttk, Menu
import pyaudio
import numpy as np
import whisper
import threading
import time
from scipy import signal
import pyperclip
import text_operations
from config import *
from pynput import keyboard
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)

print("Starte Wortweber...")

WHISPER_MODELS = ["tiny", "base", "small", "medium", "large"]
FORMAT = getattr(pyaudio, AUDIO_FORMAT)
CHANNELS = AUDIO_CHANNELS
RATE = AUDIO_RATE
CHUNK = AUDIO_CHUNK


class WordweberState:
    """Klasse zur Verwaltung des Zustands der Wortweber-Anwendung."""

    def __init__(self):
        self.recording: bool = False
        self.audio_data: List[bytes] = []
        self.start_time: float = 0
        self.recording_thread: Optional[threading.Thread] = None
        self.timer_thread: Optional[threading.Thread] = None
        self.model: Optional[whisper.Whisper] = None
        self.transcription_time: float = 0


class AudioProcessor:
    """Klasse zur Verarbeitung von Audioaufnahmen."""

    def __init__(self):
        self.p = pyaudio.PyAudio()

    def list_audio_devices(self):
        """Listet alle verfügbaren Audioeingabegeräte auf."""
        info = self.p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        if numdevices is not None:
            for i in range(int(numdevices)):
                device_info = self.p.get_device_info_by_host_api_device_index(0, i)
                max_channels = device_info.get('maxInputChannels')
                if max_channels is not None and int(max_channels) > 0:
                    print(f"Input Device id {i} - {device_info.get('name')}")

    def record_audio(self, state: WordweberState) -> float:
        """
        Nimmt Audio auf und speichert es im Zustand.

        Args:
            state (WordweberState): Der aktuelle Zustand der Anwendung.

        Returns:
            float: Die Dauer der Aufnahme in Sekunden.
        """
        try:
            stream = self.p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True,
                                 frames_per_buffer=CHUNK, input_device_index=DEVICE_INDEX)

            print("Aufnahme gestartet.")
            start_time = time.time()
            state.audio_data = []
            while state.recording:
                data = stream.read(CHUNK, exception_on_overflow=False)
                state.audio_data.append(data)

            stream.stop_stream()
            stream.close()
            duration = time.time() - start_time
            print(f"Aufnahme beendet. Dauer: {duration:.2f} Sekunden")

            return duration
        except Exception as e:
            print(f"Fehler bei der Audioaufnahme: {e}")
            return 0

    def resample_audio(self, audio_np: np.ndarray, orig_sr: int, target_sr: int) -> np.ndarray:
        """
        Resampled das Audiosignal auf die Ziel-Samplerate.

        Args:
            audio_np (np.ndarray): Das originale Audiosignal.
            orig_sr (int): Die originale Samplerate.
            target_sr (int): Die Ziel-Samplerate.

        Returns:
            np.ndarray: Das resamplete Audiosignal.
        """
        return np.array(signal.resample(audio_np, int(len(audio_np) * target_sr / orig_sr)))


class Transcriber:
    """Klasse zur Transkription von Audioaufnahmen."""

    def __init__(self, state: WordweberState):
        self.state = state

    def load_model(self, model_name: str):
        """
        Lädt das Whisper-Modell.

        Args:
            model_name (str): Der Name des zu ladenden Modells.
        """
        print(f"Lade Spracherkennungsmodell: {model_name}")
        self.state.model = whisper.load_model(model_name)
        print("Spracherkennungsmodell geladen.")

    def transcribe(self, audio_resampled: np.ndarray, language: str) -> str:
        """
        Transkribiert das gegebene Audio.

        Args:
            audio_resampled (np.ndarray): Das resamplete Audiosignal.
            language (str): Die Sprache des Audios.

        Returns:
            str: Der transkribierte Text.
        """
        try:
            options = whisper.DecodingOptions(language=language, without_timestamps=True)
            if self.state.model is None:
                raise RuntimeError("Modell nicht geladen. Bitte warten Sie, bis das Modell vollständig geladen ist.")

            start_time = time.time()
            result = self.state.model.transcribe(audio_resampled, **options.__dict__)
            self.state.transcription_time = time.time() - start_time
            return result["text"].strip() if isinstance(result["text"], str) else str(result["text"])
        except Exception as e:
            return f"Fehler bei der Transkription: {e}"


class WordweberGUI:
    """Hauptklasse für die grafische Benutzeroberfläche von Wortweber."""

    def __init__(self, state: WordweberState, audio_processor: AudioProcessor, transcriber: Transcriber):
        self.state = state
        self.audio_processor = audio_processor
        self.transcriber = transcriber
        self.root = tk.Tk()
        self.root.title("Wortweber Transkription")
        self.setup_gui()

    def setup_gui(self):
        """Richtet die grafische Benutzeroberfläche ein."""
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabelframe', borderwidth=0)
        style.configure('TCombobox', selectbackground='#0078D7', selectforeground='white')

        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(column=0, row=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.setup_left_frame(main_frame)
        self.setup_right_frame(main_frame)
        self.setup_transcription_area(main_frame)
        self.setup_buttons(main_frame)

    def setup_left_frame(self, parent):
        """Richtet den linken Rahmen der GUI ein."""
        left_frame = ttk.Frame(parent)
        left_frame.grid(column=0, row=0, sticky="nw")

        self.language_var = tk.StringVar(value=DEFAULT_LANGUAGE)
        language_frame = ttk.LabelFrame(left_frame, text="Sprache")
        language_frame.grid(column=0, row=0, pady=5, sticky="ew")
        for lang_code, lang_name in SUPPORTED_LANGUAGES.items():
            ttk.Radiobutton(language_frame, text=lang_name, variable=self.language_var, value=lang_code).pack(side=tk.LEFT, padx=5)

        model_frame = ttk.Frame(left_frame)
        model_frame.grid(column=0, row=1, pady=5, sticky="ew")

        ttk.Label(model_frame, text="Whisper-Modell:").grid(column=0, row=0, padx=(0, 5))

        self.model_var = tk.StringVar(value=WHISPER_MODEL)
        model_dropdown = ttk.Combobox(model_frame, textvariable=self.model_var, values=WHISPER_MODELS, state="readonly", width=10)
        model_dropdown.grid(column=1, row=0)

        self.loading_label = ttk.Label(model_frame, text="Modell wird geladen...", foreground="blue")
        self.loading_label.grid(column=2, row=0, padx=(10, 0))
        self.loading_label.grid_remove()

        self.model_var.trace("w", self.on_model_change)

    def setup_right_frame(self, parent):
        """Richtet den rechten Rahmen der GUI ein."""
        right_frame = ttk.Frame(parent)
        right_frame.grid(column=1, row=0, sticky="ne")

        ttk.Label(right_frame, text="Drücken und halten Sie F12, um zu sprechen").grid(column=0, row=0, pady=5)

        self.timer_var = tk.StringVar(value="Aufnahmezeit: 0.0 s")
        ttk.Label(right_frame, textvariable=self.timer_var).grid(column=0, row=1, pady=5)

        self.transcription_timer_var = tk.StringVar(value="Transkriptionszeit: 0.00 s")
        ttk.Label(right_frame, textvariable=self.transcription_timer_var).grid(column=0, row=2, pady=5)

        self.status_var = tk.StringVar()
        self.status_label = ttk.Label(right_frame, textvariable=self.status_var)
        self.status_label.grid(column=0, row=3, pady=5)
        self.update_status("Initialisiere...", "blue")

    def setup_transcription_area(self, parent):
        """Richtet den Transkriptionsbereich der GUI ein."""
        transcription_frame = ttk.LabelFrame(parent, text="Transkription")
        transcription_frame.grid(column=0, row=1, columnspan=2, sticky="nsew", pady=10)
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(1, weight=1)

        self.transcription_text = scrolledtext.ScrolledText(transcription_frame, wrap=tk.WORD, width=80, height=20)
        self.transcription_text.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        self.transcription_text.bind("<Button-3>", self.create_context_menu)

        self.transcription_text.config(insertbackground="red", insertwidth=2)
        self.transcription_text.config(selectbackground="yellow", selectforeground="black")
        self.transcription_text.tag_configure("highlight", background="light green")

    def setup_buttons(self, parent):
        """Richtet die Schaltflächen der GUI ein."""
        button_frame = ttk.Frame(parent)
        button_frame.grid(column=0, row=2, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Transkription löschen", command=self.clear_transcription).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Alles kopieren (Zwischenablage)", command=self.copy_all_to_clipboard).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Beenden", command=self.root.quit).pack(side=tk.LEFT, padx=5)

    def update_status(self, message: str, color: str = "black"):
        """
        Aktualisiert die Statusanzeige.

        Args:
            message (str): Die anzuzeigende Nachricht.
            color (str, optional): Die Farbe der Nachricht. Standard ist "black".
        """
        self.status_var.set(message)
        self.status_label.config(foreground=color)
        self.root.update()

    def on_model_change(self, *args):
        """Behandelt Änderungen in der Modellauswahl."""
        self.loading_label.grid()
        self.root.update()
        threading.Thread(target=lambda: self.load_model(self.model_var.get() if self.model_var else WHISPER_MODEL), daemon=True).start()

    def load_model(self, model_name: str):
        """
        Lädt das ausgewählte Whisper-Modell.

        Args:
            model_name (str): Der Name des zu ladenden Modells.
        """
        self.transcriber.load_model(model_name)
        self.loading_label.grid_remove()
        self.update_status("Bereit", "green")

    def create_context_menu(self, event):
        """Erstellt das Kontextmenü für den Transkriptionsbereich."""
        context_menu = Menu(self.root, tearoff=0)
        if self.transcription_text:
            for label, command in [
                ("Ausschneiden", "<<Cut>>"),
                ("Kopieren", "<<Copy>>"),
                ("Einfügen", "<<Paste>>"),
                ("Löschen", "<<Clear>>")
            ]:
                context_menu.add_command(label=label, command=lambda cmd=command: self.transcription_text.event_generate(cmd))
            context_menu.add_separator()
            context_menu.add_command(label="Zahlwörter nach Ziffern", command=self.words_to_digits)
            context_menu.add_command(label="Ziffern nach Zahlwörtern", command=self.digits_to_words)
        context_menu.tk_popup(event.x_root, event.y_root)

    def clear_transcription(self):
        """Löscht den Inhalt des Transkriptionsbereichs."""
        if self.transcription_text:
            self.transcription_text.delete(1.0, tk.END)

    def copy_all_to_clipboard(self):
        """Kopiert den gesamten Inhalt des Transkriptionsbereichs in die Zwischenablage."""
        if self.transcription_text:
            all_text = self.transcription_text.get(1.0, tk.END)
            pyperclip.copy(all_text)
            self.update_status("Gesamter Text in die Zwischenablage kopiert", "green")

    def words_to_digits(self):
        """Wandelt Zahlwörter in Ziffern um."""
        if self.transcription_text:
            current_text = self.transcription_text.get(1.0, tk.END)
            converted_text = text_operations.words_to_digits(current_text)
            self.transcription_text.delete(1.0, tk.END)
            self.transcription_text.insert(tk.END, converted_text)
            self.update_status("Zahlwörter in Ziffern umgewandelt", "green")

    def digits_to_words(self):
        """Wandelt Ziffern in Zahlwörter um."""
        if self.transcription_text:
            current_text = self.transcription_text.get(1.0, tk.END)
            converted_text = text_operations.digits_to_words(current_text)
            self.transcription_text.delete(1.0, tk.END)
            self.transcription_text.insert(tk.END, converted_text)
            self.update_status("Ziffern in Zahlwörter umgewandelt", "green")

    def update_timer(self):
        """Aktualisiert den Timer während der Aufnahme."""
        start_time = time.time()
        while self.state.recording:
            elapsed_time = time.time() - start_time
            self.timer_var.set(f"Aufnahmezeit: {elapsed_time:.1f} s")
            time.sleep(0.1)

    def on_press(self, key):
        """
        Behandelt das Drücken einer Taste.

        Args:
            key: Die gedrückte Taste.
        """
        if key == keyboard.Key.f12 and not self.state.recording:
            self.state.recording = True
            self.update_status("Aufnahme läuft...", "red")
            self.state.recording_thread = threading.Thread(target=self.record_audio)
            self.state.recording_thread.start()

    def on_release(self, key):
        """
        Behandelt das Loslassen einer Taste.

        Args:
            key: Die losgelassene Taste.
        """
        if key == keyboard.Key.f12 and self.state.recording:
            self.state.recording = False
            self.update_status("Aufnahme beendet", "orange")
            if self.state.recording_thread:
                self.state.recording_thread.join()
            if self.state.timer_thread:
                self.state.timer_thread.join()
            self.timer_var.set("Aufnahmezeit: 0.0 s")

    def record_audio(self):
        """Nimmt Audio auf und transkribiert es."""
        self.state.timer_thread = threading.Thread(target=self.update_timer)
        self.state.timer_thread.start()
        duration = self.audio_processor.record_audio(self.state)
        if duration > 0:  # Nur fortfahren, wenn die Aufnahme erfolgreich war
            if duration >= MIN_RECORD_SECONDS:
                self.transcribe_and_update()
            else:
                print(f"Aufnahme zu kurz (< {MIN_RECORD_SECONDS} Sekunden). Verworfen.")
                self.state.audio_data.clear()
        else:
            print("Aufnahme fehlgeschlagen.")

    def transcribe_and_update(self):
        """Transkribiert das aufgenommene Audio und aktualisiert die GUI."""
        self.update_status("Transkribiere...", "orange")
        audio_np = np.frombuffer(b''.join(self.state.audio_data), dtype=np.int16).astype(np.float32) / 32768.0
        audio_resampled = self.audio_processor.resample_audio(audio_np, RATE, TARGET_RATE)
        text = self.transcriber.transcribe(audio_resampled, self.language_var.get())

        if self.transcription_text:
            current_position = self.transcription_text.index(tk.INSERT)
            self.transcription_text.insert(current_position, f"{text}")
            end_position = self.transcription_text.index(f"{current_position} + {len(text)}c")
            self.transcription_text.tag_add("highlight", current_position, end_position)
            self.transcription_text.see(end_position)
            self.root.after(HIGHLIGHT_DURATION, lambda: self.transcription_text.tag_remove("highlight", current_position, end_position))

        pyperclip.copy(text)
        self.update_status("Text transkribiert und in Zwischenablage kopiert", "green")
        self.transcription_timer_var.set(f"Transkriptionszeit: {self.state.transcription_time:.2f} s")

    def run(self):
        """Startet die Hauptschleife der GUI."""
        listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        listener.start()

        self.root.after(100, lambda: threading.Thread(target=lambda: self.load_model(WHISPER_MODEL), daemon=True).start())
        self.root.mainloop()

        listener.stop()
        self.audio_processor.p.terminate()


if __name__ == "__main__":
    state = WordweberState()
    audio_processor = AudioProcessor()
    transcriber = Transcriber(state)
    gui = WordweberGUI(state, audio_processor, transcriber)

    audio_processor.list_audio_devices()
    gui.run()
