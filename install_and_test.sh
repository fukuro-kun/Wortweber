#!/bin/bash
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

# Funktion zum Überprüfen von Fehlern
check_error() {
    if [ $? -ne 0 ]; then
        echo "Fehler: $1"
        exit 1
    fi
}

# Stelle sicher, dass conda in der aktuellen Shell verfügbar ist
eval "$(conda shell.bash hook)"

# Erstellen einer neuen Conda-Umgebung
conda create -n wortweber python=3.11 -y
check_error "Conda-Umgebung konnte nicht erstellt werden"

# Aktivieren der Umgebung
conda activate wortweber
check_error "Conda-Umgebung konnte nicht aktiviert werden"

# Installation der Systemabhängigkeiten
echo "Bitte geben Sie Ihr Passwort ein, um Systemabhängigkeiten zu installieren:"
sudo apt-get update
sudo apt-get install -y portaudio19-dev python3-tk
check_error "Systemabhängigkeiten konnten nicht installiert werden"

# Installation der Python-Abhängigkeiten
pip install -r custom_requirements.txt
check_error "Python-Abhängigkeiten konnten nicht installiert werden"

# Kopieren der libstdc++.so.6 (falls erforderlich)
if [ ! -f $CONDA_PREFIX/lib/libstdc++.so.6 ]; then
    cp /usr/lib/x86_64-linux-gnu/libstdc++.so.6 $CONDA_PREFIX/lib/
    check_error "libstdc++.so.6 konnte nicht kopiert werden"
fi

# Test der Installation
python -c "import pyaudio, numpy, whisper, pynput, scipy, tqdm, tiktoken, numba; print('Alle Module erfolgreich importiert')"
check_error "Nicht alle Module konnten importiert werden"

# Ausführen des Hauptskripts
python src/wortweber.py
check_error "Hauptskript konnte nicht ausgeführt werden"

echo "Installation und Test erfolgreich abgeschlossen!"
echo "Sie können die Wortweber-Umgebung nun mit 'conda activate wortweber' aktivieren."

# Deaktivieren der Umgebung am Ende des Skripts
conda deactivate
