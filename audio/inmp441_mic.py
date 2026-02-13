import subprocess
import numpy as np
import tempfile
import soundfile as sf


def record_inmp441(duration_sec=2.0, device="hw:2,0"):
    with tempfile.NamedTemporaryFile(suffix=".wav") as tmp:
        cmd = [
            "arecord",
            "-D", device,
            "-f", "S32_LE",
            "-r", "48000",
            "-c", "2",
            "-d", str(int(duration_sec)),
            tmp.name
        ]

        subprocess.run(cmd, check=True)

        audio, _ = sf.read(tmp.name, dtype="int16")
        return audio
