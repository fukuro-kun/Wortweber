# Dateiname: src/whisper_push_to_talk_dev.py

from config import *
import numpy as np
import whisper
import tkinter as tk
from tkinter import scrolledtext, ttk
from pynput import keyboard
import threading
import time
import warnings
import pyaudio
from queue import Queue
from scipy import signal
import pyperclip
import logging

# Logging-Konfiguration
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Unterdrücke Warnungen von ALSA
warnings.filterwarnings("ignore", category=UserWarning)

print(RESAMPLING_NOTE)  # Druckt den wichtigen Hinweis beim Starten des Skripts

# Konstanten aus der Konfiguration
CHUNK = AUDIO_CHUNK
FORMAT = getattr(pyaudio, AUDIO_FORMAT)
CHANNELS = AUDIO_CHANNELS
RATE = AUDIO_RATE

# Globale Variablen
recording = False
audio_queue = Queue()
transcription_queue = Queue()
processing_thread = None
start_time = 0
recording_thread = None
status_var = None
transcription_text = None
timer_var = None
timer_thread = None
last_transcribed_text = ""
language_var = None

# Whisper-Modell laden
print("Lade Whisper-Modell...")
model = whisper.load_model(WHISPER_MODEL)
print("Whisper-Modell geladen.")

# PyAudio-Objekt initialisieren
p = pyaudio.PyAudio()

def list_audio_devices():
    """Listet alle verfügbaren Audio-Eingabegeräte auf."""
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    if numdevices is not None:
        for i in range(0, int(numdevices)):
            device_info = p.get_device_info_by_host_api_device_index(0, i)
            max_channels = device_info.get('maxInputChannels')
            if max_channels is not None and int(max_channels) > 0:
                print(f"Input Device id {i} - {device_info.get('name')}")

def update_timer():
    """Aktualisiert den Timer in der GUI während der Aufnahme."""
    global start_time, timer_var
    while recording:
        elapsed_time = time.time() - start_time
        if timer_var is not None:
            timer_var.set(f"Aufnahmezeit: {elapsed_time:.1f} s")
        time.sleep(0.1)

def record_audio():
    """
    Nimmt Audio auf und sendet es zur Verarbeitung.
    """
    global recording, audio_queue, start_time, timer_thread
    try:
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True,
                        frames_per_buffer=CHUNK, input_device_index=DEVICE_INDEX)

        print("Aufnahme gestartet.")
        start_time = time.time()
        timer_thread = threading.Thread(target=update_timer)
        timer_thread.start()

        while recording:
            data = stream.read(CHUNK, exception_on_overflow=False)
            audio_queue.put(data)

        stream.stop_stream()
        stream.close()
        duration = time.time() - start_time
        print(f"Aufnahme beendet. Dauer: {duration:.2f} Sekunden")

    except Exception as e:
        print(f"Fehler bei der Audioaufnahme: {e}")
    finally:
        audio_queue.put(None)  # Signal für das Ende der Aufnahme

def process_audio_chunks():
    """
    Verarbeitet die aufgenommenen Audio-Chunks und führt die Transkription durch.
    """
    audio_data = []
    while True:
        chunk = audio_queue.get()
        if chunk is None:
            break
        audio_data.append(chunk)

    if len(audio_data) > 0:
        audio_np = np.frombuffer(b''.join(audio_data), dtype=np.int16).astype(np.float32) / 32768.0

        if RATE != TARGET_RATE:
            audio_resampled = resample_audio(audio_np, RATE, TARGET_RATE)
        else:
            audio_resampled = audio_np

        try:
            options = whisper.DecodingOptions(language=language_var.get(), without_timestamps=True)
            result = model.transcribe(audio_resampled, **options.__dict__)
            transcribed_text = result["text"].strip()
            logging.debug(f"Whisper-Ausgabe: {transcribed_text}")
            transcription_queue.put(transcribed_text)
            update_transcription_gui(transcribed_text)
        except Exception as e:
            logging.error(f"Fehler bei der Transkription: {e}")

    transcription_queue.put(None)  # Signal für das Ende der Transkription

def update_transcription_gui(text):
    """Aktualisiert die Transkription in der GUI."""
    if text and transcription_text is not None:
        transcription_text.insert(tk.END, f"{text}\n\n")
        transcription_text.see(tk.END)
        root.update_idletasks()  # Aktualisiert die GUI sofort

def resample_audio(audio_np, orig_sr, target_sr):
    """Resampled das Audio auf die Ziel-Samplerate."""
    resampled = signal.resample(audio_np, int(len(audio_np) * target_sr / orig_sr))
    return resampled

def update_status(message, color="black"):
    """Aktualisiert die Statusanzeige in der GUI."""
    if status_var:
        status_var.set(message)
        status_label.config(foreground=color)
        root.update()

def on_press(key):
    """Callback-Funktion für das Drücken der Aufnahmetaste (F12)."""
    global recording, recording_thread, processing_thread
    if key == keyboard.Key.f12 and not recording:
        recording = True
        update_status("Aufnahme läuft...", "red")
        recording_thread = threading.Thread(target=record_audio)
        processing_thread = threading.Thread(target=process_audio_chunks)
        recording_thread.start()
        processing_thread.start()

def on_release(key):
    """Callback-Funktion für das Loslassen der Aufnahmetaste (F12)."""
    global recording, recording_thread, processing_thread, timer_thread
    if key == keyboard.Key.f12 and recording:
        recording = False
        update_status("Aufnahme beendet", "orange")
        if recording_thread:
            recording_thread.join()
        if processing_thread:
            processing_thread.join()
        if timer_thread:
            timer_thread.join()
        if timer_var is not None:
            timer_var.set("Aufnahmezeit: 0.0 s")
        update_transcription()

def update_transcription():
    """Aktualisiert die Transkription in der GUI nach Beendigung der Aufnahme."""
    while True:
        text = transcription_queue.get()
        if text is None:
            break
    update_status("Transkription abgeschlossen", "green")

def clear_transcription():
    """Löscht den aktuellen Transkriptionstext in der GUI."""
    if transcription_text is not None:
        transcription_text.delete(1.0, tk.END)

# Liste verfügbare Audiogeräte auf
list_audio_devices()

# GUI erstellen
root = tk.Tk()
root.title("Whisper Transkription (Entwicklungsversion)")

# Hauptframe
main_frame = ttk.Frame(root, padding="10")
main_frame.grid(column=0, row=0, sticky="nsew")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Anweisungen
instruction_label = ttk.Label(main_frame, text="Drücken und halten Sie F12, um zu sprechen")
instruction_label.grid(column=0, row=0, columnspan=3, pady=10)

# Timer
timer_var = tk.StringVar()
timer_var.set("Aufnahmezeit: 0.0 s")
timer_label = ttk.Label(main_frame, textvariable=timer_var)
timer_label.grid(column=0, row=1, columnspan=3, pady=5)

# Status
status_var = tk.StringVar()
status_label = ttk.Label(main_frame, textvariable=status_var)
status_label.grid(column=0, row=2, columnspan=3, pady=5)
update_status("Bereit", "green")

# Sprachauswahl
language_var = tk.StringVar(value=DEFAULT_LANGUAGE)
language_frame = ttk.LabelFrame(main_frame, text="Sprache")
language_frame.grid(column=0, row=3, columnspan=3, pady=5, sticky="ew")
for lang_code, lang_name in SUPPORTED_LANGUAGES.items():
    ttk.Radiobutton(language_frame, text=lang_name, variable=language_var, value=lang_code).pack(side=tk.LEFT, padx=5)

# Transkriptionsbereich
transcription_frame = ttk.LabelFrame(main_frame, text="Transkription")
transcription_frame.grid(column=0, row=5, columnspan=3, sticky="nsew", pady=10)
main_frame.columnconfigure(0, weight=1)
main_frame.rowconfigure(5, weight=1)

transcription_text = scrolledtext.ScrolledText(transcription_frame, wrap=tk.WORD, width=80, height=20)
transcription_text.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

# Gelbe Hintergrundfarbe beim Markieren
transcription_text.config(selectbackground="yellow", selectforeground="black")

# Buttons
clear_button = ttk.Button(main_frame, text="Transkription löschen", command=clear_transcription)
clear_button.grid(column=0, row=6, pady=10)

quit_button = ttk.Button(main_frame, text="Beenden", command=root.quit)
quit_button.grid(column=2, row=6, pady=10)

# Tastaturlistener starten
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

# GUI-Loop starten
root.mainloop()

# Aufräumen
listener.stop()
p.terminate()
