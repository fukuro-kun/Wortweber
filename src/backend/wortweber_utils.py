# Wortweber - Echtzeit-Sprachtranskription mit KI
# Copyright (C) 2024 fukuro-kun
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.



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
