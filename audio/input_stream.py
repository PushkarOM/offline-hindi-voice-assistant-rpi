import subprocess
import numpy as np

class MicStream:
    def __init__(self, device="hw:2,0"):
        self.device = device

    def start(self):
        self.process = subprocess.Popen(
            [
                "arecord",
                "-D", self.device,
                "-f", "S32_LE",
                "-r", "48000",
                "-c", "2"
            ],
            stdout=subprocess.PIPE,
            bufsize=0
        )

    def read_chunk(self, frames=4000):
        # Each frame = 2 channels × 4 bytes (S32)
        bytes_per_frame = 2 * 4
        raw = self.process.stdout.read(frames * bytes_per_frame)

        if not raw:
            return None

        # Convert to numpy int32
        audio = np.frombuffer(raw, dtype=np.int32)

        # Reshape to (n_frames, 2 channels)
        audio = audio.reshape(-1, 2)

        # Take only one channel (left)
        mono = audio[:, 0]

        # Downsample 48kHz → 16kHz (simple decimation)
        mono_16k = mono[::3]

        # Convert int32 → int16
        mono_16k = (mono_16k >> 16).astype(np.int16)

        return mono_16k.tobytes()

    def stop(self):
        self.process.terminate()
