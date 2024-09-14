# src/backend/audio_processor.py

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

from src.utils.error_handling import handle_exceptions, logger
from src.config import AUDIO_FORMAT, AUDIO_CHANNELS, AUDIO_RATE, AUDIO_CHUNK, DEVICE_INDEX, TARGET_RATE
import pyaudio
import numpy as np
from scipy import signal
import time
import warnings
import os
import wave
import contextlib

# Unterdrücke RuntimeWarnings, die oft bei Audiooperationen auftreten können
warnings.filterwarnings("ignore", category=RuntimeWarning)

class AudioProcessor:
    """
    Diese Klasse ist verantwortlich für die Verarbeitung von Audioaufnahmen.
    Sie bietet Methoden zur Auflistung von Audiogeräten, zur Aufnahme von Audio
    und zur Verarbeitung der aufgenommenen Audiodaten.
    """

    @handle_exceptions
    def __init__(self):
        """
        Initialisiert den AudioProcessor.
        Setzt die Aufnahme- und Zielrate und initialisiert die PyAudio-Instanz.
        """
        self.RATE = AUDIO_RATE
        self.TARGET_RATE = TARGET_RATE
        self.last_recording = None
        self.p = pyaudio.PyAudio()
        logger.info("AudioProcessor initialisiert")

    def __del__(self):
        """
        Destruktor für die AudioProcessor-Klasse.
        Stellt sicher, dass die PyAudio-Instanz ordnungsgemäß beendet wird.
        """
        if hasattr(self, 'p'):
            self.p.terminate()
        logger.info("AudioProcessor beendet")

    @contextlib.contextmanager
    def get_pyaudio(self):
        """
        Kontextmanager für die PyAudio-Instanz.
        Stellt sicher, dass die PyAudio-Ressourcen ordnungsgemäß freigegeben werden.

        :yield: Die PyAudio-Instanz
        """
        try:
            yield self.p
        finally:
            pass  # Die Terminierung erfolgt im Destruktor

    @handle_exceptions
    def list_audio_devices(self):
        """
        Listet alle verfügbaren Audioeingangsgeräte auf.
        Diese Methode ist nützlich, um die korrekten Geräte-IDs für die Aufnahme zu identifizieren.
        """
        logger.info("Auflistung der Audiogeräte gestartet")
        info = self.p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        if numdevices is not None:
            for i in range(int(numdevices)):
                device_info = self.p.get_device_info_by_host_api_device_index(0, i)
                max_channels = device_info.get('maxInputChannels')
                if max_channels is not None and int(max_channels) > 0:
                    print(f"Input Device id {i} - {device_info.get('name')}")
                    logger.info(f"Input Device id {i} - {device_info.get('name')}")
        logger.info("Auflistung der Audiogeräte abgeschlossen")

    @handle_exceptions
    def record_audio(self, state):
        """
        Nimmt Audio auf, basierend auf dem gegebenen Zustand.

        :param state: Ein Objekt, das den aktuellen Aufnahmezustand repräsentiert.
        :return: Die Dauer der Aufnahme in Sekunden.

        Diese Methode öffnet einen Audiostream, nimmt Audiodaten auf und speichert sie im state-Objekt.
        Sie läuft, bis state.recording auf False gesetzt wird.
        """
        logger.info("Audioaufnahme gestartet")
        try:
            stream = self.p.open(format=AUDIO_FORMAT, channels=AUDIO_CHANNELS, rate=self.RATE, input=True,
                            frames_per_buffer=AUDIO_CHUNK, input_device_index=DEVICE_INDEX)

            start_time = time.time()
            state.audio_data = []
            while state.recording:
                data = stream.read(AUDIO_CHUNK, exception_on_overflow=False)
                state.audio_data.append(data)

            stream.stop_stream()
            stream.close()
            duration = time.time() - start_time
            logger.info(f"Audioaufnahme beendet. Dauer: {duration:.2f} Sekunden")

            self.last_recording = state.audio_data
            return duration
        except Exception as e:
            logger.error(f"Fehler bei der Audioaufnahme: {e}")
            logger.error(f"Fehlertyp: {type(e).__name__}")
            logger.error(f"Geräteinformationen: {self.p.get_device_info_by_index(DEVICE_INDEX)}")
            raise

    @handle_exceptions
    def resample_audio(self, audio_np):
        """
        Resampled das Audioarray auf die Zielrate.

        :param audio_np: Ein NumPy-Array mit den Audiodaten.
        :return: Ein NumPy-Array mit den resampled Audiodaten.

        Diese Methode verwendet scipy.signal.resample, um die Abtastrate des Audios anzupassen.
        """
        if len(audio_np) == 0:
            logger.warning("Leeres Audio-Array zum Resampling übergeben")
            return audio_np
        target_length = int(len(audio_np) * self.TARGET_RATE / self.RATE)
        resampled = signal.resample(audio_np, target_length)
        logger.debug(f"Audio resampled von {len(audio_np)} auf {len(resampled)} Samples")
        return resampled

    @handle_exceptions
    def save_last_recording(self, filename="tests/test_data/speech_sample.wav"):
        """
        Speichert die letzte Aufnahme als Testdatei.

        :param filename: Der Pfad und Name der zu speichernden Datei.
        :return: True, wenn die Aufnahme erfolgreich gespeichert wurde, sonst False.
        """
        if not self.last_recording:
            logger.warning("Keine Aufnahme verfügbar zum Speichern")
            return False

        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(AUDIO_CHANNELS)
            wf.setsampwidth(pyaudio.get_sample_size(AUDIO_FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(self.last_recording))

        logger.info(f"Letzte Aufnahme gespeichert als {filename}")
        return True

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

# 5. Testaufnahme-Speicherung:
#    Die Methode `save_last_recording` ermöglicht es, die zuletzt aufgenommene Audiodatei
#    für Testzwecke zu speichern. Dies ist nützlich für die Entwicklung und das Debugging
#    der Audioaufnahme- und Verarbeitungsfunktionen.

# 6. Ressourcenmanagement:
#    Die Verwendung des Kontextmanagers `get_pyaudio` stellt sicher, dass die PyAudio-Ressourcen
#    ordnungsgemäß initialisiert und freigegeben werden, auch im Falle von Fehlern.
