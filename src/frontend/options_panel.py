from tkinter import ttk
import tkinter as tk
from src.config import SUPPORTED_LANGUAGES, WHISPER_MODELS

class OptionsPanel(ttk.Frame):
    def __init__(self, parent, gui):
        super().__init__(parent)
        self.gui = gui
        self.setup_ui()
        self.toggle_delay_options()

    def setup_ui(self):
        self.setup_language_frame()
        self.setup_model_frame()
        self.setup_delay_options()
        self.setup_input_mode()

    def setup_language_frame(self):
        language_frame = ttk.LabelFrame(self, text="Sprache")
        language_frame.pack(fill=tk.X, pady=5)
        self.language_var = tk.StringVar(value=self.gui.settings_manager.get_setting("language"))
        for lang_code, lang_name in SUPPORTED_LANGUAGES.items():
            ttk.Radiobutton(language_frame, text=lang_name, variable=self.language_var, value=lang_code, command=self.on_language_change).pack(side=tk.LEFT, padx=5)

    def setup_model_frame(self):
        model_frame = ttk.Frame(self)
        model_frame.pack(fill=tk.X, pady=5)
        ttk.Label(model_frame, text="Whisper-Modell:").grid(column=0, row=0, padx=(0, 5))
        self.model_var = tk.StringVar(value=self.gui.settings_manager.get_setting("model"))
        model_dropdown = ttk.Combobox(model_frame, textvariable=self.model_var, values=WHISPER_MODELS, state="readonly", width=10)
        model_dropdown.grid(column=1, row=0)
        model_dropdown.bind("<<ComboboxSelected>>", self.on_model_change)

    def setup_delay_options(self):
        delay_frame = ttk.LabelFrame(self, text="Verzögerungsmodus")
        delay_frame.pack(fill=tk.X, pady=5)
        self.delay_mode_var = tk.StringVar(value=self.gui.settings_manager.get_setting("delay_mode"))
        self.no_delay_radio = ttk.Radiobutton(delay_frame, text="Keine Verzögerung", variable=self.delay_mode_var, value="no_delay", command=self.on_delay_mode_change)
        self.no_delay_radio.pack(anchor=tk.W)
        char_delay_frame = ttk.Frame(delay_frame)
        char_delay_frame.pack(anchor=tk.W, fill=tk.X)
        self.char_delay_radio = ttk.Radiobutton(char_delay_frame, text="Zeichenweise", variable=self.delay_mode_var, value="char_delay", command=self.on_delay_mode_change)
        self.char_delay_radio.pack(side=tk.LEFT)
        self.char_delay_entry = ttk.Entry(char_delay_frame, width=5)
        self.char_delay_entry.pack(side=tk.LEFT, padx=(5, 0))
        self.char_delay_entry.insert(0, self.gui.settings_manager.get_setting("char_delay"))
        self.char_delay_entry.bind("<FocusOut>", self.on_char_delay_change)
        ttk.Label(char_delay_frame, text="ms").pack(side=tk.LEFT)
        self.clipboard_radio = ttk.Radiobutton(delay_frame, text="Zwischenablage", variable=self.delay_mode_var, value="clipboard", command=self.on_delay_mode_change)
        self.clipboard_radio.pack(anchor=tk.W)

        self.delay_widgets = [self.no_delay_radio, self.char_delay_radio, self.char_delay_entry, self.clipboard_radio]

    def on_delay_mode_change(self):
        self.gui.settings_manager.set_setting("delay_mode", self.delay_mode_var.get())
        self.gui.settings_manager.save_settings()

    def setup_input_mode(self):
        input_mode_frame = ttk.LabelFrame(self, text="Eingabemodus")
        input_mode_frame.pack(fill=tk.X, pady=5)
        self.input_mode_var = tk.StringVar(value=self.gui.settings_manager.get_setting("input_mode"))
        ttk.Radiobutton(input_mode_frame, text="Ins Textfenster", variable=self.input_mode_var, value="textfenster", command=self.on_input_mode_change).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(input_mode_frame, text="An Systemcursor-Position", variable=self.input_mode_var, value="systemcursor", command=self.on_input_mode_change).pack(side=tk.LEFT, padx=5)

    def on_language_change(self):
        self.gui.settings_manager.set_setting("language", self.language_var.get())
        self.gui.settings_manager.save_settings()

    def on_model_change(self, event):
        self.gui.settings_manager.set_setting("model", self.model_var.get())
        self.gui.load_model_async(self.model_var.get())

    def on_input_mode_change(self):
        self.gui.settings_manager.set_setting("input_mode", self.input_mode_var.get())
        self.gui.settings_manager.save_settings()
        self.toggle_delay_options()

    def toggle_delay_options(self, *args):
        state = 'normal' if self.input_mode_var.get() == "systemcursor" else 'disabled'
        for widget in self.delay_widgets:
            widget.configure(state=state)

    def on_char_delay_change(self, *args):
        self.gui.settings_manager.set_setting("char_delay", self.char_delay_entry.get())
        self.gui.settings_manager.save_settings()
