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

from src.config import FORMAT, CHANNELS, RATE, CHUNK, DEVICE_INDEX, TARGET_RATE
import pyaudio
import numpy as np
from scipy import signal
import time
import warnings
import logging

warnings.filterwarnings("ignore", category=RuntimeWarning)

class AudioProcessor:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.RATE = RATE
        self.TARGET_RATE = TARGET_RATE

    def list_audio_devices(self):
        info = self.p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        if numdevices is not None:
            for i in range(int(numdevices)):
                device_info = self.p.get_device_info_by_host_api_device_index(0, i)
                max_channels = device_info.get('maxInputChannels')
                if max_channels is not None and int(max_channels) > 0:
                    print(f"Input Device id {i} - {device_info.get('name')}")

    def record_audio(self, state):
        try:
            stream = self.p.open(format=FORMAT, channels=CHANNELS, rate=self.RATE, input=True,
                                 frames_per_buffer=CHUNK, input_device_index=DEVICE_INDEX)

            print("Aufnahme gestartet.")
            start_time = time.time()
            state.audio_data = []
            while state.recording:
                data = stream.read(CHUNK, exception_on_overflow=False)
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
        if len(audio_np) == 0:
            return audio_np
        target_length = int(len(audio_np) * self.TARGET_RATE / self.RATE)
        resampled = signal.resample(audio_np, target_length)
        return resampled
