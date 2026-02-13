import time
import os
import psutil
from datetime import datetime

from audio.input_stream import MicStream
from asr.streaming_asr import StreamingASR
from nlp.intent_parser import detect_intent
from tts.responses import RESPONSES
from tts.hindi_tts import speak
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
    output.append("=== Streaming Latency Benchmark ===")

    process = psutil.Process(os.getpid())
    process.cpu_percent(interval=None)

    mic = MicStream()
    asr = StreamingASR()

    mic.start()

    print("Speak now...")

    t0 = now()
    final_text = None

    while True:
        chunk = mic.read_chunk()
        if not chunk:
            continue

        text = asr.process_chunk(chunk)

        if text:
            final_text = text
            break

    t1 = now()

    intent = detect_intent(final_text)
    t2 = now()

    response = RESPONSES.get(intent, RESPONSES["UNKNOWN"])
    speak(response)
    t3 = now()

    mic.stop()

    cpu = process.cpu_percent(interval=None)
    mem = process.memory_info().rss / (1024 * 1024)

    output.extend([
        f"CPU usage         : {cpu:.1f} %",
        f"Memory usage      : {mem:.1f} MB",
        f"ASR latency       : {(t1 - t0) * 1000:.1f} ms",
        f"Intent latency    : {(t2 - t1) * 1000:.2f} ms",
        f"TTS latency       : {(t3 - t2) * 1000:.1f} ms",
        f"End-to-End latency: {(t3 - t0) * 1000:.1f} ms",
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
