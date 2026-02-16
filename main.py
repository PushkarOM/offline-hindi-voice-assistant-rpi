import logging
from config.settings import LOG_PATH
from tts.hindi_tts import AsyncTTS
from pipeline.streaming_pipeline import StreamingAssistant


logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s | %(message)s"
)


def main():
    # Initialize shared TTS engine
    tts = AsyncTTS()

    # Startup message
    tts.speak("नमस्ते, सहायक शुरू हो गया है")
    tts.queue.join()  # wait until startup speech finishes

    # Start streaming assistant
    assistant = StreamingAssistant(tts=tts)
    assistant.run()


if __name__ == "__main__":
    main()
