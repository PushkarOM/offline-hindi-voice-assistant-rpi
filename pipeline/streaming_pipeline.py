import logging
from audio.input_stream import MicStream
from asr.streaming_asr import StreamingASR
from nlp.intent_parser import detect_intent
from tts.responses import RESPONSES
from tts.hindi_tts import speak


class StreamingAssistant:

    def __init__(self):
        self.mic = MicStream()
        self.asr = StreamingASR()

    def run(self):
        self.mic.start()

        while True:
            chunk = self.mic.read_chunk()

            if chunk is None:
                continue

            text = self.asr.process_chunk(chunk)

            if text:
                logging.info(f"ASR: {text}")

                intent = detect_intent(text)
                logging.info(f"Intent: {intent}")

                response = RESPONSES.get(intent, RESPONSES["UNKNOWN"])
                speak(response)

                self.asr.reset()
