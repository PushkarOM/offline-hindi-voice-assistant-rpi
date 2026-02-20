# -----------------------------------------------
# sudo apt install portaudio19-dev
# pip install sounddevice numpy scipy matplotlib
# -----------------------------------------------

import sounddevice as sd
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
import wave
import os

# =========================
# Configuration
# =========================
SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK = 1024
TEST_DURATION = 5
VAD_THRESHOLD = 0.0005

# =========================
# 50 Hz Notch Filter
# =========================
def notch_filter(data, fs, freq=50.0, Q=30):
    b, a = signal.iirnotch(freq, Q, fs)
    return signal.lfilter(b, a, data)

# =========================
# LMS Adaptive Filter
# =========================
class LMSFilter:
    def __init__(self, mu=0.00001, taps=32):
        self.mu = mu
        self.taps = taps
        self.w = np.zeros(taps)
        self.x = np.zeros(taps)

    def adapt(self, d):
        y = np.dot(self.w, self.x)
        e = d - y
        self.w += 2 * self.mu * e * self.x
        self.x = np.roll(self.x, 1)
        self.x[0] = d
        return e

lms = LMSFilter()

# =========================
# Real-Time Plot Setup
# =========================
plt.ion()
fig, (ax1, ax2) = plt.subplots(2, 1)

# Volume bar
bar = ax1.bar([0], [0])
ax1.set_ylim(0, 0.01)
ax1.set_xticks([])
ax1.set_ylabel("Energy")
ax1.set_title("Real-Time Volume")

# Spectrogram
spec_data = np.zeros((100, CHUNK//2))
img = ax2.imshow(spec_data,
                 aspect='auto',
                 origin='lower',
                 extent=[0, SAMPLE_RATE/2, 0, 100])
ax2.set_ylabel("Time")
ax2.set_xlabel("Frequency (Hz)")
ax2.set_title("Real-Time Spectrogram")

print("System Started with Spectrogram...")

# =========================
# Audio Callback
# =========================
def audio_callback(indata, frames, time_info, status):
    global spec_data

    if status:
        print(status)

    audio = indata[:, 0]

    # Notch Filter
    filtered = notch_filter(audio, SAMPLE_RATE)

    # Adaptive LMS
    cleaned = np.array([lms.adapt(sample) for sample in filtered])

    # VAD
    energy = np.mean(cleaned**2)
    if energy > VAD_THRESHOLD:
        print("Voice Detected")

    # Update Volume Bar
    bar[0].set_height(energy)

    # Spectrogram (FFT)
    fft_data = np.abs(np.fft.rfft(cleaned))
    fft_data = fft_data / np.max(fft_data + 1e-6)

    spec_data = np.roll(spec_data, -1, axis=0)
    spec_data[-1, :] = fft_data

    img.set_data(spec_data)

    plt.pause(0.001)

# =========================
# Real-Time Monitoring (15 sec)
# =========================
with sd.InputStream(callback=audio_callback,
                    channels=CHANNELS,
                    samplerate=SAMPLE_RATE,
                    blocksize=CHUNK):
    sd.sleep(15000)

print("Monitoring finished.")

# =========================
# Short Test Recording
# =========================
print("Recording test audio...")
recording = sd.rec(int(TEST_DURATION * SAMPLE_RATE),
                   samplerate=SAMPLE_RATE,
                   channels=CHANNELS,
                   dtype='int16')
sd.wait()

filename = "test_audio.wav"

with wave.open(filename, 'w') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(2)
    wf.setframerate(SAMPLE_RATE)
    wf.writeframes(recording.tobytes())

print("Playing test recording...")
sd.play(recording, SAMPLE_RATE)
sd.wait()

os.remove(filename)
print("Test file removed. Process Completed.")
