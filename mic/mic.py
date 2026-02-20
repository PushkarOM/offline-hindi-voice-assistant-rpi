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
import time

# =========================
# Audio Configuration
# =========================
SAMPLE_RATE = 16000
CHANNELS = 1
DURATION_TEST = 5  # seconds
CHUNK = 1024

# =========================
# High-Pass Filter (EMI / Hum Reduction)
# Removes low-frequency noise (50/60Hz)
# =========================
def highpass_filter(data, cutoff=100, fs=16000, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
    return signal.lfilter(b, a, data)

# =========================
# Real-Time Volume Meter
# =========================
plt.ion()
fig, ax = plt.subplots()
bar = ax.bar([0], [0])
ax.set_ylim(0, 50000)
ax.set_xticks([])
ax.set_ylabel("Volume Level")

print("Real-time Mic Monitor Started... Speak into mic")

def audio_callback(indata, frames, time_info, status):
    global bar
    if status:
        print(status)

    audio_data = indata[:, 0]

    # Noise Reduction
    filtered = highpass_filter(audio_data)

    # RMS Volume
    rms = np.sqrt(np.mean(filtered**2))
    bar[0].set_height(rms)
    plt.pause(0.001)

# =========================
# Start Real-Time Monitoring
# =========================
with sd.InputStream(callback=audio_callback,
                    channels=CHANNELS,
                    samplerate=SAMPLE_RATE,
                    blocksize=CHUNK):
    print("Monitoring for 10 seconds...")
    sd.sleep(10000)

# =========================
# Short Test Recording
# =========================
print("Recording test audio for", DURATION_TEST, "seconds...")
recording = sd.rec(int(DURATION_TEST * SAMPLE_RATE),
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

print("Test recording saved:", filename)

# =========================
# Playback
# =========================
print("Playing recorded test audio...")
sd.play(recording, SAMPLE_RATE)
sd.wait()

# =========================
# Delete Test File
# =========================
os.remove(filename)
print("Test file removed.")

print("Process Completed.")
