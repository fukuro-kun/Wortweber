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

# src/wortweber.py
import sys
import os

# Füge den Projektordner zum Python-Pfad hinzu
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.backend.wortweber_backend import WordweberBackend
from src.frontend.wortweber_gui import WordweberGUI

def main():
    backend = WordweberBackend()
    backend.list_audio_devices()
    gui = WordweberGUI(backend)
    gui.run()

if __name__ == "__main__":
    main()
