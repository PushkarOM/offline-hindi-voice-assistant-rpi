import subprocess

class MicStream:
    def __init__(self, device="plughw:CARD=sndrpigooglevoi,DEV=0"):
        # Store ALSA device name
        self.device = device

    def start(self):
        # Start arecord process to capture raw audio from mic
         self.process = subprocess.Popen(
            [
                "arecord",
                "-D", self.device,
                "-f", "S16_LE",
                "-r", "16000",
                "-c", "1",
                "--buffer-size=8000",
                "--period-size=2000"
            ],
            stdout=subprocess.PIPE,
            bufsize=0
        )


    def read_chunk(self, frames=2000):
        bytes_per_frame = 2  # mono 16-bit

        # Read raw audio bytes from process
        raw = self.process.stdout.read(frames * bytes_per_frame)

        if not raw:
            return None

        return raw

    def stop(self):
        # Stop recording process
        self.process.terminate()
