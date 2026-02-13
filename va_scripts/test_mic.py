import soundfile as sf
from audio.audio_io import record_audio

audio = record_audio(5.0)

if audio is None:
    print("[Test] No live mic in this environment. Test skipped.")
    exit(0)

sf.write("test_input.wav", audio, 48000)
print("[Test] Audio saved to test_input.wav")
