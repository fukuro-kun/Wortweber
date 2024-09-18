#!/bin/bash
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
#
# Funktion zum Überprüfen von Fehlern
check_error() {
    if [ $? -ne 0 ]; then
        echo "Fehler: $1"
        exit 1
    fi
}

# Erstellen des wortweber.sh Skripts
echo '#!/bin/bash
eval "$(conda shell.bash hook)"
conda activate wortweber
python -m src.wortweber
conda deactivate' > wortweber.sh
chmod +x wortweber.sh
check_error "wortweber.sh konnte nicht erstellt werden"

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
sudo apt-get install -y portaudio19-dev python3-tk xclip
check_error "Systemabhängigkeiten konnten nicht installiert werden"

# Installation der Python-Abhängigkeiten
pip install -r requirements.txt
check_error "Python-Abhängigkeiten konnten nicht installiert werden"

# Kopieren der libstdc++.so.6 (falls erforderlich)
if [ ! -f $CONDA_PREFIX/lib/libstdc++.so.6 ]; then
    cp /usr/lib/x86_64-linux-gnu/libstdc++.so.6 $CONDA_PREFIX/lib/
    check_error "libstdc++.so.6 konnte nicht kopiert werden"
fi

# Test der Installation
python -c "import pyaudio, numpy, whisper, pynput, scipy, tqdm, tiktoken, numba, pyperclip; print('Alle Module erfolgreich importiert')"
check_error "Nicht alle Module konnten importiert werden"

# Test der xclip-Installation
if ! command -v xclip &> /dev/null
then
    echo "xclip konnte nicht gefunden werden. Bitte installieren Sie es manuell mit 'sudo apt-get install xclip'"
    exit 1
fi

# Ausführen des Hauptskripts
python -m src.wortweber
check_error "Hauptskript konnte nicht ausgeführt werden"

echo "Installation und Test erfolgreich abgeschlossen!"
echo "Sie können die Wortweber-Anwendung nun mit './wortweber.sh' starten."

# Deaktivieren der Umgebung am Ende des Skripts
conda deactivate
