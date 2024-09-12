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
from src.backend.wortweber_backend import WordweberBackend
from src.frontend.main_window import MainWindow
from src.frontend.settings_manager import SettingsManager
from src.frontend.input_processor import InputProcessor
import logging

class WordweberGUI:
    def __init__(self, backend: WordweberBackend):
        self.backend = backend
        self.root = tk.Tk()
        self.root.title("Wortweber Transkription")

        self.settings_manager = SettingsManager()
        self.input_processor = InputProcessor(self)

        self.main_window = MainWindow(self.root, self)

        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.debug("WordweberGUI initialisiert")

    def run(self):
        logging.debug("Starte Anwendung")
        self.input_processor.start_listener()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def on_closing(self):
        logging.debug("Anwendung wird geschlossen")
        self.settings_manager.save_settings()
        if self.backend.transcriber.model is not None:
            del self.backend.transcriber.model
        self.root.destroy()

if __name__ == "__main__":
    backend = WordweberBackend()
    gui = WordweberGUI(backend)
    gui.run()
