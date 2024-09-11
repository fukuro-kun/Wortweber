import unittest
import pyaudio
import wave
import os
import numpy as np
from src.config import CHUNK, FORMAT, CHANNELS, RATE, DEVICE_INDEX

class TestAudioRecording(unittest.TestCase):
    def setUp(self):
        self.p = pyaudio.PyAudio()
        self.RECORD_SECONDS = 2
        self.WAVE_OUTPUT_FILENAME = "test_output.wav"

    def tearDown(self):
        self.p.terminate()
        if os.path.exists(self.WAVE_OUTPUT_FILENAME):
            os.remove(self.WAVE_OUTPUT_FILENAME)

    def test_audio_recording(self):
        stream = self.p.open(format=FORMAT,
                             channels=CHANNELS,
                             rate=RATE,
                             input=True,
                             input_device_index=DEVICE_INDEX,
                             frames_per_buffer=CHUNK)

        print("* recording")

        frames = []

        for _ in range(0, int(RATE / CHUNK * self.RECORD_SECONDS)):
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)

        print("* done recording")

        stream.stop_stream()
        stream.close()

        wf = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        # Verify that the file was created and contains audio data
        self.assertTrue(os.path.exists(self.WAVE_OUTPUT_FILENAME))
        with wave.open(self.WAVE_OUTPUT_FILENAME, 'rb') as wf:
            self.assertEqual(wf.getnchannels(), CHANNELS)
            self.assertEqual(wf.getframerate(), RATE)
            audio_data = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16)
            self.assertGreater(len(audio_data), 0)
            self.assertNotEqual(np.max(np.abs(audio_data)), 0)  # Ensure there's some non-zero audio data

if __name__ == '__main__':
    unittest.main()
