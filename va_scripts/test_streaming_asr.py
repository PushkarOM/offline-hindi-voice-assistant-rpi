from audio.input_stream import MicStream
from asr.streaming_asr import StreamingASR


def main():
    mic = MicStream()
    asr = StreamingASR()

    mic.start()

    print("🎙 Speak... (Ctrl+C to stop)")

    try:
        while True:
            chunk = mic.read_chunk()
            if not chunk:
                continue

            text = asr.process_chunk(chunk)

            if text:
                print(f"\n✅ Final: {text}")
                asr.reset()

    except KeyboardInterrupt:
        print("\nStopping...")

    finally:
        mic.stop()


if __name__ == "__main__":
    main()
