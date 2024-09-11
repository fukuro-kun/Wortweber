from src.config import FORMAT, CHANNELS, RATE, CHUNK, DEVICE_INDEX, TARGET_RATE
import pyaudio
import numpy as np
from scipy import signal
import time
import warnings
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
            print(f"Fehler bei der Audioaufnahme: {e}")
            print(f"Fehlertyp: {type(e).__name__}")
            print(f"Geräteinformationen: {self.p.get_device_info_by_index(DEVICE_INDEX)}")
            return 0

    def resample_audio(self, audio_np):
        if len(audio_np) == 0:
            return audio_np
        target_length = max(2, int(len(audio_np) * self.TARGET_RATE / self.RATE))
        resampled = signal.resample(audio_np, target_length)
        print(f"Debug: Resampling from {len(audio_np)} to {len(resampled)} samples")
        return resampled

    def process_audio(self, state):
        print(f"Debug: Raw audio data: {state.audio_data}")
        audio_np = np.frombuffer(b''.join(state.audio_data), dtype=np.int16)
        print(f"Debug: Audio as int16: {audio_np}")
        audio_float = audio_np.astype(np.float32) / 32767.0
        print(f"Debug: Normalized audio: {audio_float}")
        resampled = self.resample_audio(audio_float)
        print(f"Debug: Resampled audio: {resampled}")
        if len(resampled) < 2:
            print("Warning: Resampled audio has less than 2 samples. Padding with zeros.")
            resampled = np.pad(resampled, (0, 2 - len(resampled)), 'constant')
        return resampled # Stellen Sie sicher, dass dies ein numpy array ist
