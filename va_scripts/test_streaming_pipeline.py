from pipeline.streaming_pipeline import StreamingAssistant


def main():
    assistant = StreamingAssistant()

    print("🚀 Starting streaming pipeline test...")
    print("Press Ctrl+C to exit.\n")

    try:
        assistant.run()
    except KeyboardInterrupt:
        print("\nStopping assistant...")


if __name__ == "__main__":
    main()
