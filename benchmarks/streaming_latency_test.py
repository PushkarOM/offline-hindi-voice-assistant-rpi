import time
import os
import psutil
from datetime import datetime

from audio.input_stream import MicStream
from asr.streaming_asr import StreamingASR
from nlp.intent_parser import detect_intent
from tts.responses import generate_response
from tts.hindi_tts import AsyncTTS
from config.settings import RESULTS_DIR


def now():
    return time.perf_counter()


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def log_to_file(lines):
    ensure_dir(RESULTS_DIR)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = f"{RESULTS_DIR}/streaming_latency_{ts}.log"
    with open(path, "w") as f:
        f.write("\n".join(lines))
    return path


def main():
    output = []
    output.append("=== Streaming Latency Benchmark (Competition Mode) ===")

    process = psutil.Process(os.getpid())
    process.cpu_percent(interval=None)

    mic = MicStream()
    asr = StreamingASR()
    tts = AsyncTTS()

    mic.start()
    print("Speak now...")

    speech_start_time = None
    command_detect_time = None
    final_text = None

    # --- ASR Phase ---
    while True:
        chunk = mic.read_chunk()
        if not chunk:
            continue

        # Mark first audio chunk as speech start
        if speech_start_time is None:
            speech_start_time = now()

        text = asr.process_chunk(chunk)

        if text:
            final_text = text
            command_detect_time = now()
            asr.reset()
            break

    # --- Intent Phase ---
    intent = detect_intent(final_text)
    intent_time = now()

    # --- TTS Phase ---
    response = generate_response(intent, text)
    tts_start_time = now()
    tts.speak(response)

    # Wait for playback to finish
    tts.queue.join()
    tts_end_time = now()

    mic.stop()

    cpu = process.cpu_percent(interval=None)
    mem = process.memory_info().rss / (1024 * 1024)

    # ----- Calculations -----
    speech_duration = (command_detect_time - speech_start_time) * 1000
    processing_latency = (tts_start_time - command_detect_time) * 1000
    tts_playback_time = (tts_end_time - tts_start_time) * 1000
    full_completion = (tts_end_time - speech_start_time) * 1000

    output.extend([
        f"CPU usage                 : {cpu:.1f} %",
        f"Memory usage              : {mem:.1f} MB",
        "",
        f"Speech duration           : {speech_duration:.1f} ms",
        f"Processing latency        : {processing_latency:.1f} ms  <-- Competition Metric",
        f"TTS playback duration     : {tts_playback_time:.1f} ms",
        f"Full completion time      : {full_completion:.1f} ms",
        "",
        f"ASR Output : {final_text}",
        f"Intent     : {intent}"
    ])

    for line in output:
        print(line)

    log_path = log_to_file(output)
    print(f"\n[Saved] {log_path}")


if __name__ == "__main__":
    main()
