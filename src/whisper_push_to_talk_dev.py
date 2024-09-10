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
normalize_numbers_var = None
language_var = None

# Whisper-Modell laden
print("Lade Whisper-Modell...")
model = whisper.load_model("small")  # base, small, medium, large
print("Whisper-Modell geladen.")

# PyAudio-Objekt initialisieren
p = pyaudio.PyAudio()

def detect_pause(audio_chunk, threshold=PAUSE_THRESHOLD, min_pause_duration=MIN_PAUSE_DURATION):
    """
    Erkennt Pausen in einem Audio-Chunk basierend auf der Amplitude.

    :param audio_chunk: NumPy-Array des Audio-Chunks
    :param threshold: Schwellenwert für die Amplitudenerkennung
    :param min_pause_duration: Minimale Pausendauer in Sekunden
    :return: True, wenn eine Pause erkannt wurde, sonst False

    Hinweis bitte nicht entfernen - Wichtige Dokumentation.
    """
    # Konvertiere das Audio-Chunk in ein NumPy-Array, falls es noch nicht eines ist
    if not isinstance(audio_chunk, np.ndarray):
        audio_chunk = np.frombuffer(audio_chunk, dtype=np.int16).astype(np.float32) / 32768.0

    # Berechne die RMS-Amplitude (Root Mean Square) für kleine Fenster
    window_size = int(RATE * PAUSE_WINDOW_SIZE)
    chunks = np.array_split(audio_chunk, len(audio_chunk) // window_size)
    # Diese Änderung fügt `np.maximum(np.mean(window**2), 1e-10)` hinzu, um sicherzustellen, dass wir nie versuchen, die Quadratwurzel aus einer negativen Zahl oder Null zu ziehen.
    rms = np.array([np.sqrt(np.maximum(np.mean(chunk**2), 1e-10)) for chunk in chunks])

    # Finde Bereiche, wo die RMS unter dem Schwellenwert liegt
    is_pause = rms < threshold

    # Prüfe, ob die Pause lang genug ist
    pause_samples = int(min_pause_duration * (len(rms) / (len(audio_chunk) / RATE)))
    if np.sum(is_pause) >= pause_samples:
        return True
    return False

def list_audio_devices():
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    if numdevices is not None:
        for i in range(0, numdevices):
            device_info = p.get_device_info_by_host_api_device_index(0, i)
            if device_info.get('maxInputChannels') is not None and device_info.get('maxInputChannels') > 0:
                print(f"Input Device id {i} - {device_info.get('name')}")

def update_timer():
    global start_time, timer_var
    while recording:
        elapsed_time = time.time() - start_time
        if timer_var is not None:
            timer_var.set(f"Aufnahmezeit: {elapsed_time:.1f} s")
        time.sleep(0.1)

def record_audio():
    global recording, audio_queue, start_time, timer_thread
    try:
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True,
                        frames_per_buffer=CHUNK, input_device_index=DEVICE_INDEX)

        print("Aufnahme gestartet.")
        start_time = time.time()
        current_chunk = []
        chunk_start_time = time.time()
        timer_thread = threading.Thread(target=update_timer)
        timer_thread.start()

        while recording:
            data = stream.read(CHUNK, exception_on_overflow=False)
            current_chunk.append(data)

            audio_np = np.frombuffer(b''.join(current_chunk), dtype=np.int16)
            chunk_duration = time.time() - chunk_start_time

            if detect_pause(audio_np) or chunk_duration >= MAX_CHUNK_DURATION:
                if chunk_duration >= MIN_CHUNK_DURATION:
                    audio_queue.put(b''.join(current_chunk))

                    # Überlappung für den nächsten Chunk
                    overlap_samples = int(CHUNK_OVERLAP * RATE)
                    current_chunk = current_chunk[-overlap_samples:]

                    chunk_start_time = time.time() - CHUNK_OVERLAP
                elif chunk_duration < MIN_CHUNK_DURATION:
                    continue

        if current_chunk:
            audio_queue.put(b''.join(current_chunk))

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

    Diese Funktion läuft in einem separaten Thread und führt folgende Schritte aus:
    1. Holt Audio-Chunks aus der audio_queue
    2. Konvertiert die Audio-Daten in das richtige Format für Whisper
    3. Führt die Transkription mit Whisper durch
    4. Verarbeitet den transkribierten Text, um Überlappungen zu entfernen
    5. Sendet den neuen Text an die GUI zur Anzeige

    Die Funktion läuft, bis ein None-Objekt in der Queue empfangen wird, was das Ende der Aufnahme signalisiert.
    """
    global last_transcribed_text
    full_transcription = ""
    while True:
        chunk = audio_queue.get()
        if chunk is None:
            break

        audio_np = np.frombuffer(chunk, dtype=np.int16).astype(np.float32) / 32768.0

        if RATE != TARGET_RATE:
            audio_resampled = resample_audio(audio_np, RATE, TARGET_RATE)
        else:
            audio_resampled = audio_np

        try:
            options = whisper.DecodingOptions(language=language_var.get(), without_timestamps=True)
            result = model.transcribe(audio_resampled, **options.__dict__)
            new_text = result["text"].strip()

            # Finde den neuen Teil des Texts
            if full_transcription:
                # Finde den längsten gemeinsamen Suffix/Präfix
                overlap = find_overlap(full_transcription, new_text)
                new_text = new_text[overlap:]

            if new_text:
                full_transcription += " " + new_text
                transcription_queue.put(new_text)
                update_transcription_gui(new_text)
        except Exception as e:
            print(f"Fehler bei der Transkription: {e}")

    transcription_queue.put(None)  # Signal für das Ende der Transkription

def find_overlap(a, b):
    """Findet die Länge des längsten gemeinsamen Suffix von a und Präfix von b."""
    min_len = min(len(a), len(b))
    for i in range(min_len, 0, -1):
        if a[-i:] == b[:i]:
            return i
    return 0

def normalize_numbers(text):
    """Konvertiert Zahlwörter in Ziffern und umgekehrt, um Konsistenz zu gewährleisten."""
    if language_var.get() == "de":
        number_words = {
            'null': '0', 'eins': '1', 'zwei': '2', 'drei': '3', 'vier': '4', 'fünf': '5',
            'sechs': '6', 'sieben': '7', 'acht': '8', 'neun': '9', 'zehn': '10',
            'elf': '11', 'zwölf': '12', 'dreizehn': '13', 'vierzehn': '14', 'fünfzehn': '15'
        }
    else:  # Englisch
        number_words = {
            'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5',
            'six': '6', 'seven': '7', 'eight': '8', 'nine': '9', 'ten': '10',
            'eleven': '11', 'twelve': '12', 'thirteen': '13', 'fourteen': '14', 'fifteen': '15'
        }

    words = text.split()
    normalized = []
    for word in words:
        if word.lower() in number_words:
            normalized.append(number_words[word.lower()])
        elif word.isdigit() and int(word) <= 15:
            normalized.append(list(number_words.keys())[list(number_words.values()).index(word)])
        else:
            normalized.append(word)
    return ' '.join(normalized)

def update_transcription_gui(text):
    if text and transcription_text is not None:
        if normalize_numbers_var.get():
            text = normalize_numbers(text)
        transcription_text.insert(tk.END, f"{text} ")
        transcription_text.see(tk.END)
        root.update_idletasks()  # Aktualisiert die GUI sofort

def resample_audio(audio_np, orig_sr, target_sr):
    resampled = signal.resample(audio_np, int(len(audio_np) * target_sr / orig_sr))
    return resampled

def update_status(message, color="black"):
    if status_var:
        status_var.set(message)
        status_label.config(foreground=color)
        root.update()

def on_press(key):
    global recording, recording_thread, processing_thread
    if key == keyboard.Key.f12 and not recording:
        recording = True
        update_status("Aufnahme läuft...", "red")
        recording_thread = threading.Thread(target=record_audio)
        processing_thread = threading.Thread(target=process_audio_chunks)
        recording_thread.start()
        processing_thread.start()

def on_release(key):
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
    while True:
        text = transcription_queue.get()
        if text is None:
            break
        # Die GUI-Aktualisierung wird jetzt in update_transcription_gui gehandhabt
    update_status("Transkription abgeschlossen", "green")

def clear_transcription():
    if transcription_text is not None:
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
language_var = tk.StringVar(value="de")
language_frame = ttk.LabelFrame(main_frame, text="Sprache")
language_frame.grid(column=0, row=3, columnspan=3, pady=5, sticky="ew")
ttk.Radiobutton(language_frame, text="Deutsch", variable=language_var, value="de").pack(side=tk.LEFT, padx=5)
ttk.Radiobutton(language_frame, text="Englisch", variable=language_var, value="en").pack(side=tk.LEFT, padx=5)

# Zahlennormalisierung
normalize_numbers_var = tk.BooleanVar(value=False)
ttk.Checkbutton(main_frame, text="Zahlennormalisierung", variable=normalize_numbers_var).grid(column=0, row=4, columnspan=3, pady=5)

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
