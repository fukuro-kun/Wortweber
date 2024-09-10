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
from config import *
import pyaudio
import numpy as np
import whisper
import tkinter as tk
from tkinter import scrolledtext, ttk
from pynput import keyboard
import threading
import time
import warnings
from scipy import signal
import pyperclip

# Am Anfang der Datei
print("Starte Wortweber...")

# Unterdrücke Warnungen von ALSA
warnings.filterwarnings("ignore", category=UserWarning)

# Konstanten aus der Konfiguration
CHUNK = AUDIO_CHUNK
FORMAT = getattr(pyaudio, AUDIO_FORMAT)
CHANNELS = AUDIO_CHANNELS
RATE = AUDIO_RATE

# Whisper-Modelle
WHISPER_MODELS = ["tiny", "base", "small", "medium", "large"]

# Globale Variablen
recording = False
audio_data = []
start_time = 0
recording_thread = None
status_var = None
transcription_text = None
timer_var = None
timer_thread = None
language_var = None
model_var = None
transcription_timer_var = None
transcription_time = 0
model = None
loading_label = None

# PyAudio-Objekt initialisieren
p = pyaudio.PyAudio()

def load_whisper_model(model_name):
    global model
    print(f"Lade Spracherkennungsmodell: {model_name}")
    model = whisper.load_model(model_name)
    print("Spracherkennungsmodell geladen.")
    if loading_label:
        loading_label.grid_remove()
    update_status("Bereit", "green")

def list_audio_devices():
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    if numdevices is not None:
        for i in range(int(numdevices)):
            device_info = p.get_device_info_by_host_api_device_index(0, i)
            max_channels = device_info.get('maxInputChannels')
            if max_channels is not None and int(max_channels) > 0:
                print(f"Input Device id {i} - {device_info.get('name')}")

def update_timer():
    global start_time, timer_var
    while recording:
        elapsed_time = time.time() - start_time
        if timer_var is not None:
            timer_var.set(f"Aufnahmezeit: {elapsed_time:.1f} s")
        time.sleep(0.1)

def record_audio():
    global recording, audio_data, start_time, timer_thread
    try:
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True,
                        frames_per_buffer=CHUNK, input_device_index=DEVICE_INDEX)

        print("Aufnahme gestartet.")
        start_time = time.time()
        audio_data = []
        timer_thread = threading.Thread(target=update_timer)
        timer_thread.start()
        while recording:
            data = stream.read(CHUNK, exception_on_overflow=False)
            audio_data.append(data)

        stream.stop_stream()
        stream.close()
        duration = time.time() - start_time
        print(f"Aufnahme beendet. Dauer: {duration:.2f} Sekunden")

        if duration >= MIN_RECORD_SECONDS:
            transcribe_and_update()
        else:
            print(f"Aufnahme zu kurz (< {MIN_RECORD_SECONDS} Sekunden). Verworfen.")
            audio_data.clear()
    except Exception as e:
        print(f"Fehler bei der Audioaufnahme: {e}")

def resample_audio(audio_np, orig_sr, target_sr):
    resampled = signal.resample(audio_np, int(len(audio_np) * target_sr / orig_sr))
    return resampled

def transcribe_audio():
    global audio_data, language_var, transcription_time
    if not audio_data:
        return "Keine Audiodaten aufgenommen."

    audio_np = np.frombuffer(b''.join(audio_data), dtype=np.int16).astype(np.float32) / 32768.0

    # Resampling
    audio_resampled = resample_audio(audio_np, RATE, TARGET_RATE)

    try:
        # Whisper-Konfiguration anpassen
        if language_var is not None:
            options = whisper.DecodingOptions(language=language_var.get(), without_timestamps=True)
            start_time = time.time()
            result = model.transcribe(audio_resampled, **options.__dict__)
            transcription_time = time.time() - start_time
            return result["text"].strip()
        else:
            return "Sprachauswahl nicht verfügbar."
    except Exception as e:
        return f"Fehler bei der Transkription: {e}"

def update_status(message, color="black"):
    if status_var:
        status_var.set(message)
        status_label.config(foreground=color)
        root.update()

def transcribe_and_update():
    update_status("Transkribiere...", "orange")
    text = transcribe_audio()
    if transcription_text is not None:
        # Aktuelle Cursorposition speichern
        current_position = transcription_text.index(tk.INSERT)

        # Text an der Cursorposition einfügen (ohne zusätzlichen Zeilenumbruch)
        transcription_text.insert(current_position, f"{text}")

        # Neu eingefügten Text markieren
        end_position = transcription_text.index(f"{current_position} + {len(text)}c")
        transcription_text.tag_add("highlight", current_position, end_position)

        # Sicherstellen, dass der neue Text sichtbar ist
        transcription_text.see(end_position)

        # Timer starten, um die Hervorhebung nach 2 Sekunden zu entfernen
        root.after(2000, lambda: transcription_text.tag_remove("highlight", current_position, end_position))

    pyperclip.copy(text)
    update_status("Text transkribiert und in Zwischenablage kopiert", "green")
    if transcription_timer_var is not None:
        transcription_timer_var.set(f"Transkriptionszeit: {transcription_time:.2f} s")

def on_press(key):
    global recording, recording_thread
    if key == keyboard.Key.f12 and not recording:
        recording = True
        update_status("Aufnahme läuft...", "red")
        recording_thread = threading.Thread(target=record_audio)
        recording_thread.start()

def on_release(key):
    global recording, recording_thread, timer_thread
    if key == keyboard.Key.f12 and recording:
        recording = False
        update_status("Aufnahme beendet", "orange")
        if recording_thread:
            recording_thread.join()
        if timer_thread:
            timer_thread.join()
        if timer_var is not None:
            timer_var.set("Aufnahmezeit: 0.0 s")

def clear_transcription():
    if transcription_text is not None:
        transcription_text.delete(1.0, tk.END)

def copy_all_to_clipboard():
    if transcription_text is not None:
        all_text = transcription_text.get(1.0, tk.END)
        pyperclip.copy(all_text)
        update_status("Gesamter Text in die Zwischenablage kopiert", "green")

def on_model_change(*args):
    global loading_label
    if loading_label:
        loading_label.grid_remove()
    loading_label = ttk.Label(main_frame, text="Modell wird geladen...", foreground="blue")
    loading_label.grid(column=0, row=2, columnspan=2, pady=5)
    root.update()
    threading.Thread(target=lambda: load_whisper_model(model_var.get()), daemon=True).start()

# Liste verfügbare Audiogeräte auf
list_audio_devices()

# GUI erstellen
root = tk.Tk()
root.title("Wortweber Transkription")

# Stil konfigurieren
style = ttk.Style()
style.theme_use('clam')
style.configure('TLabelframe', borderwidth=0)  # Entfernt Rahmen von LabelFrames
style.configure('TCombobox', selectbackground='#0078D7', selectforeground='white')

# Hauptframe
main_frame = ttk.Frame(root, padding="10")
main_frame.grid(column=0, row=0, sticky="nsew")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Linke Seite: Sprachauswahl und Modellauswahl
left_frame = ttk.Frame(main_frame)
left_frame.grid(column=0, row=0, sticky="nw")

# Sprachauswahl
language_var = tk.StringVar(value=DEFAULT_LANGUAGE)
language_frame = ttk.LabelFrame(left_frame, text="Sprache")
language_frame.grid(column=0, row=0, pady=5, sticky="ew")
for lang_code, lang_name in SUPPORTED_LANGUAGES.items():
    ttk.Radiobutton(language_frame, text=lang_name, variable=language_var, value=lang_code).pack(side=tk.LEFT, padx=5)

# Modellauswahl
model_var = tk.StringVar(value=WHISPER_MODEL)
model_frame = ttk.LabelFrame(left_frame, text="Whisper-Modell")
model_frame.grid(column=0, row=1, pady=5, sticky="ew")
model_dropdown = ttk.Combobox(model_frame, textvariable=model_var, values=WHISPER_MODELS, state="readonly")
model_dropdown.pack(side=tk.LEFT, padx=5)
model_var.trace("w", on_model_change)

# Rechte Seite: Anweisungen, Timer und Status
right_frame = ttk.Frame(main_frame)
right_frame.grid(column=1, row=0, sticky="ne")

# Anweisungen
instruction_label = ttk.Label(right_frame, text="Drücken und halten Sie F12, um zu sprechen")
instruction_label.grid(column=0, row=0, pady=5)

# Timer
timer_var = tk.StringVar()
timer_var.set("Aufnahmezeit: 0.0 s")
timer_label = ttk.Label(right_frame, textvariable=timer_var)
timer_label.grid(column=0, row=1, pady=5)

# Transkriptionstimer
transcription_timer_var = tk.StringVar()
transcription_timer_var.set("Transkriptionszeit: 0.00 s")
transcription_timer_label = ttk.Label(right_frame, textvariable=transcription_timer_var)
transcription_timer_label.grid(column=0, row=2, pady=5)

# Status
status_var = tk.StringVar()
status_label = ttk.Label(right_frame, textvariable=status_var)
status_label.grid(column=0, row=3, pady=5)
update_status("Initialisiere...", "blue")

# Transkriptionsbereich
transcription_frame = ttk.LabelFrame(main_frame, text="Transkription")
transcription_frame.grid(column=0, row=1, columnspan=2, sticky="nsew", pady=10)
main_frame.columnconfigure(0, weight=1)
main_frame.rowconfigure(1, weight=1)

transcription_text = scrolledtext.ScrolledText(transcription_frame, wrap=tk.WORD, width=80, height=20)
transcription_text.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

# Cursor-Farbe und -Breite anpassen
transcription_text.config(insertbackground="red", insertwidth=2)

# Gelbe Hintergrundfarbe beim Markieren
transcription_text.config(selectbackground="yellow", selectforeground="black")

# Tag für Hervorhebung des neu eingefügten Texts erstellen
transcription_text.tag_configure("highlight", background="light green")

# Buttons
button_frame = ttk.Frame(main_frame)
button_frame.grid(column=0, row=2, columnspan=2, pady=10)

clear_button = ttk.Button(button_frame, text="Transkription löschen", command=clear_transcription)
clear_button.pack(side=tk.LEFT, padx=5)

copy_all_button = ttk.Button(button_frame, text="Alles kopieren (Zwischenablage)", command=copy_all_to_clipboard)
copy_all_button.pack(side=tk.LEFT, padx=5)

quit_button = ttk.Button(button_frame, text="Beenden", command=root.quit)
quit_button.pack(side=tk.LEFT, padx=5)

# Whisper-Modell laden
loading_label = ttk.Label(main_frame, text="Modell wird geladen...", foreground="blue")
loading_label.grid(column=0, row=3, columnspan=2, pady=5)
root.update()

# Tastaturlistener starten
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

# GUI-Loop starten
root.after(100, lambda: threading.Thread(target=lambda: load_whisper_model(WHISPER_MODEL), daemon=True).start())
root.mainloop()

# Aufräumen
listener.stop()
p.terminate()
