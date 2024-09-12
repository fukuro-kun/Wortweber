import tkinter as tk
from tkinter import ttk
from src.frontend.transcription_panel import TranscriptionPanel
from src.frontend.options_panel import OptionsPanel
from src.frontend.status_panel import StatusPanel

class MainWindow:
    def __init__(self, root, gui):
        self.root = root
        self.gui = gui

        self.setup_ui()

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.transcription_panel = TranscriptionPanel(main_frame, self.gui)
        self.options_panel = OptionsPanel(main_frame, self.gui)
        self.status_panel = StatusPanel(main_frame, self.gui)

        self.options_panel.grid(column=0, row=0, sticky="nw")
        self.status_panel.grid(column=1, row=0, sticky="ne")
        self.transcription_panel.grid(column=0, row=1, columnspan=2, sticky="nsew")

        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
