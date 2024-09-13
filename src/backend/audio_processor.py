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

# src/backend/audio_processor.py

from src.config import AUDIO_FORMAT, AUDIO_CHANNELS, AUDIO_RATE, AUDIO_CHUNK, DEVICE_INDEX, TARGET_RATE
import pyaudio
import numpy as np
from scipy import signal
import time
import warnings
import logging

# Unterdrücke RuntimeWarnings, die oft bei Audiooperationen auftreten können
warnings.filterwarnings("ignore", category=RuntimeWarning)

class AudioProcessor:
    """
    Diese Klasse ist verantwortlich für die Verarbeitung von Audioaufnahmen.
    Sie bietet Methoden zur Auflistung von Audiogeräten, zur Aufnahme von Audio
    und zur Verarbeitung der aufgenommenen Audiodaten.
    """

    def __init__(self):
        """
        Initialisiert den AudioProcessor.
        Erstellt eine PyAudio-Instanz und setzt die Aufnahme- und Zielrate.
        """
        self.p = pyaudio.PyAudio()
        self.RATE = AUDIO_RATE
        self.TARGET_RATE = TARGET_RATE

    def list_audio_devices(self):
        """
        Listet alle verfügbaren Audioeingangsgeräte auf.
        Diese Methode ist nützlich, um die korrekten Geräte-IDs für die Aufnahme zu identifizieren.
        """
        info = self.p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        if numdevices is not None:
            for i in range(int(numdevices)):
                device_info = self.p.get_device_info_by_host_api_device_index(0, i)
                max_channels = device_info.get('maxInputChannels')
                if max_channels is not None and int(max_channels) > 0:
                    print(f"Input Device id {i} - {device_info.get('name')}")

    def record_audio(self, state):
        """
        Nimmt Audio auf, basierend auf dem gegebenen Zustand.

        :param state: Ein Objekt, das den aktuellen Aufnahmezustand repräsentiert.
        :return: Die Dauer der Aufnahme in Sekunden.

        Diese Methode öffnet einen Audiostream, nimmt Audiodaten auf und speichert sie im state-Objekt.
        Sie läuft, bis state.recording auf False gesetzt wird.
        """
        try:
            stream = self.p.open(format=AUDIO_FORMAT, channels=AUDIO_CHANNELS, rate=self.RATE, input=True,
                                 frames_per_buffer=AUDIO_CHUNK, input_device_index=DEVICE_INDEX)

            print("Aufnahme gestartet.")
            start_time = time.time()
            state.audio_data = []
            while state.recording:
                data = stream.read(AUDIO_CHUNK, exception_on_overflow=False)
                state.audio_data.append(data)

            stream.stop_stream()
            stream.close()
            duration = time.time() - start_time
            print(f"Aufnahme beendet. Dauer: {duration:.2f} Sekunden")

            return duration
        except Exception as e:
            logging.error(f"Fehler bei der Audioaufnahme: {e}")
            logging.error(f"Fehlertyp: {type(e).__name__}")
            logging.error(f"Geräteinformationen: {self.p.get_device_info_by_index(DEVICE_INDEX)}")
            return 0

    def resample_audio(self, audio_np):
        """
        Resampled das Audioarray auf die Zielrate.

        :param audio_np: Ein NumPy-Array mit den Audiodaten.
        :return: Ein NumPy-Array mit den resampled Audiodaten.

        Diese Methode verwendet scipy.signal.resample, um die Abtastrate des Audios anzupassen.
        """
        if len(audio_np) == 0:
            return audio_np
        target_length = int(len(audio_np) * self.TARGET_RATE / self.RATE)
        resampled = signal.resample(audio_np, target_length)
        return resampled

# Zusätzliche Erklärungen:

# 1. PyAudio:
#    PyAudio wird verwendet, um auf die Audiogeräte des Systems zuzugreifen und Audiostreams zu öffnen.
#    Es bietet eine plattformübergreifende Schnittstelle für Audioein- und -ausgabe.

# 2. Resampling:
#    Das Resampling ist notwendig, da das Whisper-Modell eine bestimmte Eingabeabtastrate erwartet (16000 Hz).
#    Die Funktion `signal.resample` aus scipy wird verwendet, um die Abtastrate anzupassen, ohne die Audiodauer zu ändern.

# 3. Fehlerbehandlung:
#    Die ausführliche Fehlerprotokollierung in `record_audio` hilft bei der Diagnose von Problemen,
#    insbesondere bei Schwierigkeiten mit spezifischen Audiogeräten oder Treibern.

# 4. Zustandsbasierte Aufnahme:
#    Die Verwendung eines state-Objekts ermöglicht eine flexible Kontrolle der Aufnahmedauer
#    und eine einfache Integration mit der Benutzeroberfläche.
