import logging
import time
from audio.input_stream import MicStream
from asr.streaming_asr import StreamingASR
from nlp.intent_parser import detect_intent
from tts.responses import generate_response



class StreamingAssistant:

    def __init__(self, tts):
        
        self.state = "IDLE"
        self.active_since = None
        self.active_timeout = 10 # seconds
        self.unknown_count = 0
        self.max_unknown = 2
        
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

            # TIMEOUT CHECK (only if assitant is Active)
            if self.state == "ACTIVE" and self.active_since:
                if time.time() - self.active_since > self.active_timeout:
                    self.tts.speak("कोई निर्देश नहीं मिला, स्लीप मोड में जा रही हूँ")
                    self.state = "IDLE"
                    self.active_since = None
                    self.unknown_count = 0

            if text:

                logging.info(f"ASR: {text}")
                intent, processed_text  = detect_intent(text)
                logging.info(f"Intent, Processed Text : {intent} , {processed_text}")
                logging.info(f"State: {self.state}")

                # IDLE MODE
                if self.state == "IDLE":
                    if intent == "WAKE":
                        response = generate_response("WAKE", text, processed_text)
                        self.tts.speak(response)
                        self.state = "ACTIVE"
                        self.active_since = time.time()
                    self.asr.reset()
                    continue

                # ACTIVE MODE
                if self.state == "ACTIVE":

                    if intent == "UNKNOWN":
                        self.unknown_count += 1
                        self.active_since = time.time()

                        if self.unknown_count <= self.max_unknown:
                            self.tts.speak("माफ़ कीजिए, दोबारा कहिए")
                            time.sleep(2)
                        else:
                            response = generate_response(intent, text, processed_text)
                            self.tts.speak(response)
                            self.state = "IDLE"
                            self.active_since = None
                            self.unknown_count = 0
                    
                        self.asr.reset()
                        continue


                    response = generate_response(intent, text, processed_text, self.tts)
                    self.tts.speak(response)

                    # force sleep
                    if intent == "EXIT":    
                        self.state = "IDLE"
                        self.active_since = None
                        self.asr.reset()
                        continue
                    
                    # Reset, timer and unknown_command after valid command
                    self.unknown_count = 0
                    self.active_since = time.time()
                    self.asr.reset()
