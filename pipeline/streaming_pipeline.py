import logging
from audio.input_stream import MicStream
from asr.streaming_asr import StreamingASR
from nlp.intent_parser import detect_intent
from tts.responses import generate_response



class StreamingAssistant:

    def __init__(self, tts):
        self.tts = tts
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

                intent, processed_text = detect_intent(text)
                logging.info(f"Processed Text: {processed_text}")
                logging.info(f"Intent: {intent}")

                response = generate_response(intent, text, processed_text)
                self.tts.speak(response)

                self.asr.reset()
