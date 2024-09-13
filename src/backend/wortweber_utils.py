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

"""
Dieses Modul enthält Hilfsfunktionen für die Wortweber-Anwendung,
insbesondere für die Überprüfung von GPU-Ressourcen.
"""

import torch
from typing import Tuple

def check_gpu_resources() -> Tuple[bool, float]:
    """
    Überprüft die Verfügbarkeit und den freien Speicher der GPU.

    Returns:
        tuple: (bool: GPU verfügbar, float: verfügbarer Speicher in GB)
    """
    if torch.cuda.is_available():
        device = torch.device("cuda")
        gpu_properties = torch.cuda.get_device_properties(device)
        total_memory = gpu_properties.total_memory / (1024 ** 3)  # Konvertierung zu GB
        allocated_memory = torch.cuda.memory_allocated(device) / (1024 ** 3)
        free_memory = total_memory - allocated_memory
        return True, free_memory
    else:
        return False, 0.0

# Beispielnutzung und Test
if __name__ == "__main__":
    gpu_available, free_memory = check_gpu_resources()
    if gpu_available:
        print(f"GPU verfügbar mit {free_memory:.2f} GB freiem Speicher")
    else:
        print("Keine GPU verfügbar")

# Zusätzliche Erklärungen:
# 1. Die Funktion nutzt die torch.cuda-Bibliothek zur GPU-Erkennung und Speicherabfrage.
# 2. Die Speicherwerte werden in GB umgerechnet für bessere Lesbarkeit.
# 3. Der Rückgabewert ist ein Tuple mit einem Boolean für GPU-Verfügbarkeit und einem Float für den freien Speicher.
# 4. Der __main__-Block ermöglicht einen schnellen Test der Funktion bei direkter Ausführung des Skripts.
