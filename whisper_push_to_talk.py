# Dateiname: whisper_push_to_talk.py

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

# Unterdrücke Warnungen von ALSA
warnings.filterwarnings("ignore", category=UserWarning)

# Konstanten
CHUNK = 4096
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
TARGET_RATE = 16000
DEVICE_INDEX = 6
MIN_RECORD_SECONDS = 0.5

# Whisper-Modell laden
print("Lade Whisper-Modell...")
model = whisper.load_model("small")  # base, small, medium, large
print("Whisper-Modell geladen.")

# PyAudio-Objekt initialisieren
p = pyaudio.PyAudio()

# Globale Variablen
recording = False
audio_data = []
start_time = 0
recording_thread = None
status_var = None
transcription_text = None
timer_var = None
timer_thread = None

def list_audio_devices():
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range(0, numdevices):
        device_info = p.get_device_info_by_host_api_device_index(0, i)
        if device_info.get('maxInputChannels') > 0:
            print(f"Input Device id {i} - {device_info.get('name')}")

def update_timer():
    global start_time, timer_var
    while recording:
        elapsed_time = time.time() - start_time
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
    global audio_data
    if not audio_data:
        return "Keine Audiodaten aufgenommen."

    audio_np = np.frombuffer(b''.join(audio_data), dtype=np.int16).astype(np.float32) / 32768.0

    # Resampling
    audio_resampled = resample_audio(audio_np, RATE, TARGET_RATE)

    try:
        # Whisper-Konfiguration anpassen
        options = whisper.DecodingOptions(language="de", without_timestamps=True)
        result = model.transcribe(audio_resampled, **options.__dict__)
        return result["text"].strip()
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
    transcription_text.insert(tk.END, f"{text}\n\n")
    transcription_text.see(tk.END)
    pyperclip.copy(text)
    update_status("Text transkribiert und in Zwischenablage kopiert", "green")

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
        timer_var.set("Aufnahmezeit: 0.0 s")

def clear_transcription():
    transcription_text.delete(1.0, tk.END)

# Liste verfügbare Audiogeräte auf
list_audio_devices()

# GUI erstellen
root = tk.Tk()
root.title("Whisper Transkription")

# Hauptframe
main_frame = ttk.Frame(root, padding="10")
main_frame.grid(column=0, row=0, sticky="nsew")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Anweisungen
instruction_label = ttk.Label(main_frame, text="Drücken und halten Sie F12, um zu sprechen")
instruction_label.grid(column=0, row=0, columnspan=2, pady=10)

# Timer
timer_var = tk.StringVar()
timer_var.set("Aufnahmezeit: 0.0 s")
timer_label = ttk.Label(main_frame, textvariable=timer_var)
timer_label.grid(column=0, row=1, columnspan=2, pady=5)

# Status
status_var = tk.StringVar()
status_label = ttk.Label(main_frame, textvariable=status_var)
status_label.grid(column=0, row=2, columnspan=2, pady=5)
update_status("Bereit", "green")

# Transkriptionsbereich
transcription_frame = ttk.LabelFrame(main_frame, text="Transkription")
transcription_frame.grid(column=0, row=3, columnspan=2, sticky="nsew", pady=10)
main_frame.columnconfigure(0, weight=1)
main_frame.rowconfigure(3, weight=1)

transcription_text = scrolledtext.ScrolledText(transcription_frame, wrap=tk.WORD, width=80, height=20)
transcription_text.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

# Gelbe Hintergrundfarbe beim Markieren
transcription_text.config(selectbackground="yellow", selectforeground="black")

# Buttons
clear_button = ttk.Button(main_frame, text="Transkription löschen", command=clear_transcription)
clear_button.grid(column=0, row=4, pady=10)

quit_button = ttk.Button(main_frame, text="Beenden", command=root.quit)
quit_button.grid(column=1, row=4, pady=10)

# Tastaturlistener starten
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

# GUI-Loop starten
root.mainloop()

# Aufräumen
listener.stop()
p.terminate()
