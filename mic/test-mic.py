import pyaudio
import numpy as np

# Audio configuration
FORMAT = pyaudio.paInt32   # INMP441 usually works in 32-bit
CHANNELS = 1               # Mono mic
RATE = 16000               # Sample rate
CHUNK = 1024               # Buffer size

p = pyaudio.PyAudio()

# Open stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("🎤 Mic Test Started... Speak into microphone")

try:
    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)
        audio_data = np.frombuffer(data, dtype=np.int32)

        # Calculate RMS (volume level)
        rms = np.sqrt(np.mean(audio_data**2))
        print("Volume Level:", int(rms))

except KeyboardInterrupt:
    print("\nTest Stopped")

stream.stop_stream()
stream.close()
p.terminate()
