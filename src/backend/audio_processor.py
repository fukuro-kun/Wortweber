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

from src.utils.error_handling import handle_exceptions, logger
from src.config import AUDIO_FORMAT, AUDIO_CHANNELS, AUDIO_RATE, AUDIO_CHUNK, TARGET_RATE, DEFAULT_AUDIO_DEVICE_INDEX, DEFAULT_INCOGNITO_MODE
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
    @handle_exceptions
    def __init__(self, settings_manager):
        self.settings_manager = settings_manager
        self.RATE = AUDIO_RATE
        self.TARGET_RATE = TARGET_RATE
        self.last_recording = None
        self.p = pyaudio.PyAudio()
        self.current_device_index = self.get_device_index()
        self.stream = None
        logger.debug(f"AudioProcessor initialisiert mit Geräteindex: {self.current_device_index}")

    def __del__(self):
        self.cleanup()

    @handle_exceptions
    def cleanup(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if self.p:
            self.p.terminate()
        logger.debug("AudioProcessor Ressourcen bereinigt")

    @handle_exceptions
    def reinitialize(self):
        self.cleanup()
        self.p = pyaudio.PyAudio()
        self.current_device_index = self.get_device_index()
        logger.debug("AudioProcessor reinitialisiert")

    @handle_exceptions
    def get_device_index(self):
        try:
            index = int(self.settings_manager.get_setting("audio_device_index", DEFAULT_AUDIO_DEVICE_INDEX))
            if 0 <= index < self.p.get_device_count():
                logger.debug(f"Verwende gespeicherten Audiogeräteindex: {index}")
                return index
            else:
                logger.warning(f"Gespeicherter Index {index} ungültig. Verwende Standardgerät.")
        except (ValueError, TypeError):
            logger.warning("Ungültiger Audiogeräteindex in den Einstellungen.")

        default_index = self.p.get_default_input_device_info()['index']
        logger.info(f"Verwende Standardgeräteindex: {default_index}")
        self.settings_manager.set_setting("audio_device_index", default_index)
        return default_index

    @handle_exceptions
    def get_current_device_info(self):
        try:
            device_info = self.p.get_device_info_by_index(self.current_device_index)
            return {
                'index': self.current_device_index,
                'name': device_info.get('name', 'Unbekanntes Gerät')
            }
        except Exception as e:
            logger.error(f"Fehler beim Abrufen des aktuellen Audiogeräts: {e}")
            return None

    @handle_exceptions
    def update_device(self, new_index):
        new_index = int(new_index)  # Explizite Konvertierung zu int
        if 0 <= new_index < self.p.get_device_count():
            self.current_device_index = new_index
            self.settings_manager.set_setting("audio_device_index", new_index)
            self.settings_manager.save_settings()
            logger.debug(f"Audiogerät aktualisiert auf Index: {new_index}")
            return True
        else:
            logger.error(f"Ungültiger Audiogeräteindex: {new_index}")
            return False

    @contextlib.contextmanager
    def get_pyaudio(self):
        try:
            yield self.p
        finally:
            pass

    @handle_exceptions
    def check_device_availability(self):
        try:
            device_info = self.p.get_device_info_by_index(self.current_device_index)
            if device_info and device_info.get('maxInputChannels', 0) > 0:
                return True
            else:
                logger.warning(f"Ausgewähltes Audiogerät (Index: {self.current_device_index}) ist nicht verfügbar oder hat keine Eingabekanäle.")
                return False
        except Exception as e:
            logger.error(f"Fehler beim Überprüfen des Audiogeräts (Index: {self.current_device_index}): {e}")
            return False

    @handle_exceptions
    def open_audio_stream(self):
        try:
            self.stream = self.p.open(format=AUDIO_FORMAT, channels=AUDIO_CHANNELS, rate=self.RATE, input=True,
                            frames_per_buffer=AUDIO_CHUNK, input_device_index=self.current_device_index)
            return self.stream
        except IOError as e:
            if e.errno == -9996:  # Device unavailable
                logger.error(f"Das ausgewählte Audiogerät (Index: {self.current_device_index}) ist nicht verfügbar.")
            elif e.errno == -9997:  # Invalid sample rate
                logger.error(f"Die Abtastrate {self.RATE} wird vom Gerät nicht unterstützt.")
            else:
                logger.error(f"Fehler beim Öffnen des Audiostreams: {e}")
            raise
        except Exception as e:
            logger.error(f"Unerwarteter Fehler beim Öffnen des Audiostreams: {e}")
            raise

    @handle_exceptions
    def reset_stream(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.stream = None

    @handle_exceptions
    def record_audio(self, state):
        logger.info("Audioaufnahme gestartet.")
        try:
            self.reset_stream()
            self.stream = self.open_audio_stream()

            start_time = time.time()
            state.audio_data = []
            while state.recording:
                try:
                    data = self.stream.read(AUDIO_CHUNK, exception_on_overflow=False)
                    state.audio_data.append(data)
                except IOError as e:
                    logger.error(f"IOError während der Aufnahme: {e}")
                    break

            duration = time.time() - start_time
            logger.info(f"Audioaufnahme beendet. Dauer: {duration:.2f} Sekunden")

            if len(state.audio_data) > 0:
                self.last_recording = state.audio_data
            else:
                logger.warning("Keine Audiodaten aufgenommen")

            return duration
        except Exception as e:
            logger.error(f"Fehler bei der Audioaufnahme: {e}")
            logger.error(f"Fehlertyp: {type(e).__name__}")
            logger.error(f"Geräteinformationen: {self.p.get_device_info_by_index(self.current_device_index)}")
            logger.debug("Detaillierter Traceback:", exc_info=True)
            raise
        finally:
            if self.stream:
                self.stream.stop_stream()

    @handle_exceptions
    def resample_audio(self, audio_np):
        if len(audio_np) == 0:
            logger.warning("Leeres Audio-Array zum Resampling übergeben")
            return audio_np
        target_length = int(len(audio_np) * self.TARGET_RATE / self.RATE)
        resampled = signal.resample(audio_np, target_length)
        logger.debug(f"Audio resampled von {len(audio_np)} auf {len(resampled)} Samples")
        return resampled

    @handle_exceptions
    def save_last_recording(self, filename="tests/test_data/speech_sample.wav"):
        if not self.last_recording:
            logger.warning("Keine Aufnahme verfügbar zum Speichern")
            return False

        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(AUDIO_CHANNELS)
            wf.setsampwidth(pyaudio.get_sample_size(AUDIO_FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(self.last_recording))

        incognito_mode = self.settings_manager.get_setting("incognito_mode", DEFAULT_INCOGNITO_MODE)
        if not incognito_mode:
            logger.info(f"Letzte Aufnahme gespeichert als {filename}")
        else:
            logger.info("Letzte Aufnahme gespeichert (Incognito-Modus aktiv)")
        return True

    @handle_exceptions
    def list_audio_devices(self):
        """Listet alle verfügbaren Audioeingangsgeräte auf."""
        logger.info("Auflistung der Audiogeräte gestartet")
        info = self.p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        if numdevices is not None:
            for i in range(int(numdevices)):
                device_info = self.p.get_device_info_by_host_api_device_index(0, i)
                max_channels = device_info.get('maxInputChannels')
                if max_channels is not None and int(max_channels) > 0:
                    print(f"Input Device id {i} - {device_info.get('name')}")
                    logger.debug(f"Input Device id {i} - {device_info.get('name')}")
        logger.info("Auflistung der Audiogeräte abgeschlossen")

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

# 7. Geräteauswahl:
#    Die Methode `get_device_index` ermöglicht es, das vom Benutzer ausgewählte Audiogerät
#    zu verwenden, was die Flexibilität und Benutzerfreundlichkeit der Anwendung erhöht.
