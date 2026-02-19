import os
import logging
from config.settings import LOG_PATH
from tts.hindi_tts import AsyncTTS
from pipeline.streaming_pipeline import StreamingAssistant


# Ensure log directory exists
log_dir = os.path.dirname(LOG_PATH)
if log_dir and not os.path.exists(log_dir):
    os.makedirs(log_dir, exist_ok=True)

# Configure logging
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
