import logging
from config.settings import LOG_PATH
from tts.hindi_tts import speak
from pipeline.streaming_pipeline import StreamingAssistant


logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s | %(message)s"
)


def main():
    speak("नमस्ते, सहायक शुरू हो गया है")

    assistant = StreamingAssistant()
    assistant.run()


if __name__ == "__main__":
    main()
