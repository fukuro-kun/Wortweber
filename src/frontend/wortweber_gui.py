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
import tkinter as tk
from tkinter import ttk, scrolledtext
import ttkthemes
from src.backend.wortweber_backend import WordweberBackend
import threading
from pynput import keyboard
from pynput.keyboard import Key, Controller as KeyboardController
import pyperclip
import time
import json
import os
import logging
import itertools
from src.config import WHISPER_MODEL, WHISPER_MODELS, SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE, HIGHLIGHT_DURATION
from src.backend.text_processor import words_to_digits, digits_to_words

class WordweberGUI:
    def __init__(self, backend: WordweberBackend):
        self.backend = backend
        self.root = ttkthemes.ThemedTk()
        self.root.title("Wortweber Transkription")
        self.auto_copy_var = tk.BooleanVar(value=True)

        self.themes = sorted(ttkthemes.THEMES)
        self.current_theme_index = 0
        self.current_theme = tk.StringVar(value=self.themes[self.current_theme_index])

        self.language_var = tk.StringVar(value=DEFAULT_LANGUAGE)
        self.model_var = tk.StringVar(value=WHISPER_MODEL)

        self.settings_file = "user_settings.json"
        self.model_loaded = threading.Event()
        self.loading_animation = None

        self.last_window_save_time = 0
        self.last_saved_position = None

        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.debug("WordweberGUI initialisiert")

        self.setup_ui()
        self.load_settings()

    def setup_ui(self):
        self.root.geometry("800x600")

        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.setup_left_frame(main_frame)
        self.setup_right_frame(main_frame)
        self.setup_transcription_area(main_frame)
        self.setup_buttons(main_frame)

        self.root.bind("<Configure>", self.on_window_configure)

        logging.debug("UI Setup abgeschlossen")

    def setup_left_frame(self, parent):
        left_frame = ttk.Frame(parent)
        left_frame.grid(column=0, row=0, sticky="nw")

        self.notebook = ttk.Notebook(left_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        options_tab = ttk.Frame(self.notebook)
        self.themes_tab = ttk.Frame(self.notebook)

        self.notebook.add(options_tab, text="Optionen")
        self.notebook.add(self.themes_tab, text="Themes")

        self.setup_options_tab(options_tab)
        self.setup_themes_tab(self.themes_tab)

    def setup_options_tab(self, parent):
        language_frame = ttk.LabelFrame(parent, text="Sprache")
        language_frame.pack(fill=tk.X, pady=5)
        for lang_code, lang_name in SUPPORTED_LANGUAGES.items():
            ttk.Radiobutton(language_frame, text=lang_name, variable=self.language_var, value=lang_code, command=self.on_language_change).pack(side=tk.LEFT, padx=5)

        model_frame = ttk.Frame(parent)
        model_frame.pack(fill=tk.X, pady=5)

        ttk.Label(model_frame, text="Whisper-Modell:").grid(column=0, row=0, padx=(0, 5))

        model_dropdown = ttk.Combobox(model_frame, textvariable=self.model_var, values=WHISPER_MODELS, state="readonly", width=10)
        model_dropdown.grid(column=1, row=0)
        model_dropdown.bind("<<ComboboxSelected>>", self.on_model_change)

        self.loading_label = ttk.Label(model_frame, text="Modell wird geladen...", foreground="blue")
        self.loading_label.grid(column=2, row=0, padx=(10, 0))
        self.loading_label.grid_remove()

        self.setup_delay_options(parent)
        self.setup_input_mode(parent)

    def setup_themes_tab(self, parent):
        theme_frame = ttk.Frame(parent, padding="10")
        theme_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(theme_frame, text="Theme Auswahl", font=("Arial", 12, "bold")).pack(pady=(0, 10))

        self.theme_var = tk.StringVar(value=self.themes[0])
        self.theme_dropdown = ttk.Combobox(theme_frame, textvariable=self.theme_var, values=self.themes, state="readonly")
        self.theme_dropdown.pack(fill=tk.X, pady=(0, 20))
        self.theme_dropdown.bind("<<ComboboxSelected>>", self.on_theme_change)

        ttk.Label(theme_frame, text="Wählen Sie ein Theme aus der Dropdown-Liste aus.", wraplength=200).pack()

    def on_theme_change(self, event):
        selected_theme = self.theme_var.get()
        self.change_theme(selected_theme)

    def change_theme(self, theme_name):
        self.root.set_theme(theme_name)
        self.theme_var.set(theme_name)
        self.save_settings()
        logging.debug(f"Theme geändert zu: {theme_name}")

    def setup_delay_options(self, parent):
        delay_frame = ttk.LabelFrame(parent, text="Verzögerungsmodus")
        delay_frame.pack(fill=tk.X, pady=5)

        self.delay_mode_var = tk.StringVar(value="no_delay")
        self.no_delay_radio = ttk.Radiobutton(delay_frame, text="Keine Verzögerung", variable=self.delay_mode_var, value="no_delay")
        self.no_delay_radio.pack(anchor=tk.W)

        char_delay_frame = ttk.Frame(delay_frame)
        char_delay_frame.pack(anchor=tk.W, fill=tk.X)
        self.char_delay_radio = ttk.Radiobutton(char_delay_frame, text="Zeichenweise", variable=self.delay_mode_var, value="char_delay")
        self.char_delay_radio.pack(side=tk.LEFT)
        self.char_delay_entry = ttk.Entry(char_delay_frame, width=5)
        self.char_delay_entry.pack(side=tk.LEFT, padx=(5, 0))
        self.char_delay_entry.insert(0, "10")
        self.char_delay_label = ttk.Label(char_delay_frame, text="ms")
        self.char_delay_label.pack(side=tk.LEFT)

        self.clipboard_radio = ttk.Radiobutton(delay_frame, text="Zwischenablage", variable=self.delay_mode_var, value="clipboard")
        self.clipboard_radio.pack(anchor=tk.W)

    def setup_input_mode(self, parent):
        input_mode_frame = ttk.LabelFrame(parent, text="Eingabemodus")
        input_mode_frame.pack(fill=tk.X, pady=5)

        self.input_mode_var = tk.StringVar(value="textfenster")
        ttk.Radiobutton(input_mode_frame, text="Ins Textfenster", variable=self.input_mode_var, value="textfenster", command=self.toggle_delay_options).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(input_mode_frame, text="An Systemcursor-Position", variable=self.input_mode_var, value="systemcursor", command=self.toggle_delay_options).pack(side=tk.LEFT, padx=5)

    def setup_right_frame(self, parent):
        right_frame = ttk.Frame(parent)
        right_frame.grid(column=1, row=0, sticky="ne")

        ttk.Label(right_frame, text="Drücken und halten Sie F12, um zu sprechen").grid(column=0, row=0, pady=5)

        self.timer_var = tk.StringVar(value="Aufnahmezeit: 0.0 s")
        ttk.Label(right_frame, textvariable=self.timer_var).grid(column=0, row=1, pady=5)

        self.transcription_timer_var = tk.StringVar(value="Transkriptionszeit: 0.00 s")
        ttk.Label(right_frame, textvariable=self.transcription_timer_var).grid(column=0, row=2, pady=5)

        self.auto_copy_checkbox = ttk.Checkbutton(right_frame, text="Automatisch in Zwischenablage kopieren",
                                                  variable=self.auto_copy_var)
        self.auto_copy_checkbox.grid(column=0, row=3, pady=5, sticky="w")

        self.status_var = tk.StringVar()
        self.status_label = ttk.Label(right_frame, textvariable=self.status_var)
        self.status_label.grid(column=0, row=4, pady=5)
        self.update_status("Initialisiere...", "blue")

    def setup_transcription_area(self, parent):
        transcription_frame = ttk.LabelFrame(parent, text="Transkription")
        transcription_frame.grid(column=0, row=1, columnspan=2, sticky="nsew", pady=10)
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(1, weight=1)

        self.transcription_text = scrolledtext.ScrolledText(transcription_frame, wrap=tk.WORD, width=80, height=20)
        self.transcription_text.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        self.transcription_text.bind("<Button-3>", self.create_context_menu)
        self.transcription_text.tag_configure("highlight", background="yellow")
        self.transcription_text.config(
            insertbackground="red",
            insertwidth=2,
            selectbackground="yellow",
            selectforeground="black"
        )

    def setup_buttons(self, parent):
        button_frame = ttk.Frame(parent)
        button_frame.grid(column=0, row=2, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Transkription löschen", command=self.clear_transcription).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Alles kopieren", command=self.copy_all_to_clipboard).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Beenden", command=self.root.quit).pack(side=tk.LEFT, padx=5)

    def update_status(self, message: str, color: str = "black"):
        self.status_var.set(message)
        self.status_label.config(foreground=color)
        self.root.update()

    def on_language_change(self, *args):
        self.save_settings()
        logging.debug(f"Sprache geändert zu: {self.language_var.get()}")

    def on_model_change(self, *args):
        self.loading_label.grid()
        self.start_loading_animation()
        self.root.update()
        threading.Thread(target=self.load_model, args=(self.model_var.get(),), daemon=True).start()
        self.save_settings()
        logging.debug(f"Modell geändert zu: {self.model_var.get()}")

    def start_loading_animation(self):
        self.loading_animation = threading.Thread(target=self._animate_loading, daemon=True)
        self.loading_animation.start()

    def _animate_loading(self):
        for c in itertools.cycle(['|', '/', '-', '\\']):
            if self.model_loaded.is_set():
                break
            self.loading_label.config(text=f"Modell wird geladen... {c}")
            time.sleep(0.1)
        self.loading_label.config(text="Modell geladen!")
        self.root.after(2000, self.loading_label.grid_remove)

    def load_model(self, model_name: str):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                logging.info(f"Versuche Modell zu laden: {model_name} (Versuch {attempt + 1})")
                self.backend.load_transcriber_model(model_name)
                self.loading_label.grid_remove()
                self.update_status("Bereit", "green")
                self.model_loaded.set()
                logging.info(f"Modell erfolgreich geladen: {model_name}")
                return
            except Exception as e:
                logging.error(f"Fehler beim Laden des Modells: {e}")
                if attempt < max_retries - 1:
                    time.sleep(1)  # Kurze Pause vor dem nächsten Versuch
                else:
                    self.update_status("Fehler beim Laden des Modells", "red")
        self.model_loaded.set()  # Stoppe die Animation auch im Fehlerfall

    def create_context_menu(self, event):
        context_menu = tk.Menu(self.root, tearoff=0)
        context_menu.add_command(label="Ausschneiden", command=self.cut_selected)
        context_menu.add_command(label="Kopieren", command=self.copy_selected)
        context_menu.add_command(label="Einfügen", command=self.paste)
        context_menu.add_command(label="Löschen", command=self.delete_selected)
        context_menu.add_separator()
        context_menu.add_command(label="Alles auswählen", command=self.select_all)
        context_menu.add_separator()
        context_menu.add_command(label="Zahlwörter nach Ziffern", command=self.words_to_digits)
        context_menu.add_command(label="Ziffern nach Zahlwörtern", command=self.digits_to_words)
        context_menu.tk_popup(event.x_root, event.y_root)

    def copy_selected(self):
        self.transcription_text.event_generate("<<Copy>>")

    def paste(self):
        self.transcription_text.event_generate("<<Paste>>")

    def select_all(self):
        self.transcription_text.tag_add(tk.SEL, "1.0", tk.END)

    def clear_transcription(self):
        self.transcription_text.delete(1.0, tk.END)
        self.save_settings()

    def copy_all_to_clipboard(self):
        all_text = self.transcription_text.get(1.0, tk.END)
        pyperclip.copy(all_text)
        self.update_status("Gesamter Text in die Zwischenablage kopiert", "green")

    def on_press(self, key):
        if key == keyboard.Key.f12 and not self.backend.state.recording:
            if not self.model_loaded.is_set():
                self.update_status("Modell wird noch geladen. Bitte warten.", "orange")
                return
            try:
                if self.backend.check_audio_device():
                    self.backend.start_recording()
                    self.update_status("Aufnahme läuft...", "red")
                    self.start_timer()
                else:
                    self.update_status("Audiogerät nicht verfügbar", "red")
            except Exception as e:
                logging.error(f"Fehler beim Starten der Aufnahme: {e}")
                self.update_status("Fehler beim Starten der Aufnahme", "red")

    def on_release(self, key):
        if key == keyboard.Key.f12 and self.backend.state.recording:
            self.backend.stop_recording()
            self.update_status("Aufnahme beendet", "orange")
            self.stop_timer()
            self.transcribe_and_update()

    def start_timer(self):
        self.start_time = time.time()
        self.update_timer()

    def stop_timer(self):
        self.timer_var.set("Aufnahmezeit: 0.0 s")

    def update_timer(self):
        if self.backend.state.recording:
            elapsed_time = time.time() - self.start_time
            self.timer_var.set(f"Aufnahmezeit: {elapsed_time:.1f} s")
            self.root.after(100, self.update_timer)

    def transcribe_and_update(self):
        self.update_status("Transkribiere...", "orange")
        text = self.backend.process_and_transcribe(self.language_var.get())

        if self.input_mode_var.get() == "textfenster":
            current_position = self.transcription_text.index(tk.INSERT)
            self.transcription_text.insert(current_position, text)
            end_position = self.transcription_text.index(f"{current_position} + {len(text)}c")
            self.transcription_text.tag_add("highlight", current_position, end_position)
            self.transcription_text.see(end_position)
            self.root.after(HIGHLIGHT_DURATION, lambda: self.transcription_text.tag_remove("highlight", current_position, end_position))
        else:
            delay_mode = self.delay_mode_var.get()

            if delay_mode == "no_delay":
                keyboard = KeyboardController()
                keyboard.type(text)
            elif delay_mode == "char_delay":
                try:
                    delay = float(self.char_delay_entry.get()) / 1000
                except ValueError:
                    delay = 0.01  # Fallback to 10ms if invalid input
                keyboard = KeyboardController()
                for char in text:
                    keyboard.type(char)
                    time.sleep(delay)
            elif delay_mode == "clipboard":
                pyperclip.copy(text)
                keyboard = KeyboardController()
                with keyboard.pressed(Key.ctrl):
                    keyboard.press('v')
                    keyboard.release('v')

        if self.auto_copy_var.get():
            pyperclip.copy(text)
            self.update_status("Text transkribiert und in Zwischenablage kopiert", "green")
        else:
            self.update_status("Text transkribiert", "green")

        self.transcription_timer_var.set(f"Transkriptionszeit: {self.backend.state.transcription_time:.2f} s")
        self.save_settings()

    def toggle_delay_options(self):
        state = 'disabled' if self.input_mode_var.get() == "textfenster" else 'normal'
        for widget in [self.no_delay_radio, self.char_delay_radio, self.char_delay_entry, self.clipboard_radio]:
            widget.configure(state=state)
        self.char_delay_label.configure(state=state)

    def cut_selected(self):
        self.transcription_text.event_generate("<<Cut>>")
        self.save_settings()

    def delete_selected(self):
        self.transcription_text.event_generate("<<Clear>>")
        self.save_settings()

    def words_to_digits(self):
        try:
            selected_text = self.transcription_text.get(tk.SEL_FIRST, tk.SEL_LAST)
            converted_text = words_to_digits(selected_text)
            self.transcription_text.delete(tk.SEL_FIRST, tk.SEL_LAST)
            self.transcription_text.insert(tk.INSERT, converted_text)
            self.save_settings()
        except tk.TclError:
            # No text selected
            pass

    def digits_to_words(self):
        try:
            selected_text = self.transcription_text.get(tk.SEL_FIRST, tk.SEL_LAST)
            converted_text = digits_to_words(selected_text)
            self.transcription_text.delete(tk.SEL_FIRST, tk.SEL_LAST)
            self.transcription_text.insert(tk.INSERT, converted_text)
            self.save_settings()
        except tk.TclError:
            # No text selected
            pass

    def save_settings(self):
        settings = {
            "language": self.language_var.get(),
            "model": self.model_var.get(),
            "theme": self.theme_var.get(),
            "window_size": self.root.geometry(),
            "input_mode": self.input_mode_var.get(),
            "delay_mode": self.delay_mode_var.get(),
            "char_delay": self.char_delay_entry.get(),
            "auto_copy": self.auto_copy_var.get(),
            "text_content": self.transcription_text.get("1.0", tk.END).strip()
        }
        with open(self.settings_file, "w") as f:
            json.dump(settings, f)
        logging.debug(f"Einstellungen gespeichert: {settings}")

    def load_settings(self):
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, "r") as f:
                    settings = json.load(f)
                logging.debug(f"Geladene Einstellungen: {settings}")

                self.language_var.set(settings.get("language", DEFAULT_LANGUAGE))
                self.model_var.set(settings.get("model", WHISPER_MODEL))
                self.theme_var.set(settings.get("theme", self.themes[0]))
                self.root.geometry(settings.get("window_size", "800x600"))
                self.input_mode_var.set(settings.get("input_mode", "textfenster"))
                self.delay_mode_var.set(settings.get("delay_mode", "no_delay"))
                self.char_delay_entry.delete(0, tk.END)
                self.char_delay_entry.insert(0, settings.get("char_delay", "10"))
                self.auto_copy_var.set(settings.get("auto_copy", True))

                self.transcription_text.delete("1.0", tk.END)
                self.transcription_text.insert("1.0", settings.get("text_content", ""))

                self.change_theme(self.theme_var.get())

                logging.debug("Einstellungen erfolgreich angewendet")
            except json.JSONDecodeError:
                logging.error("Fehler beim Laden der Einstellungen. Verwende Standardeinstellungen.")
        else:
            logging.debug("Keine Einstellungsdatei gefunden. Verwende Standardeinstellungen.")

    def on_window_configure(self, event):
        if event.widget == self.root:
            current_time = time.time()
            current_position = self.root.geometry()

            if (current_position != self.last_saved_position and
                current_time - self.last_window_save_time > 1):
                self.save_settings()
                self.last_window_save_time = current_time
                self.last_saved_position = current_position

    def run(self):
        logging.debug("Starte Anwendung")
        listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        listener.start()

        self.root.after(100, lambda: threading.Thread(target=self.load_model, args=(self.model_var.get(),), daemon=True).start())
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

        listener.stop()

    def on_closing(self):
        logging.debug("Anwendung wird geschlossen")
        self.save_settings()
        self.root.destroy()
