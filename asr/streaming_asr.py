import json
from vosk import KaldiRecognizer
from asr.hindi_asr import load_model
from nlp.intents import INTENTS


# Extract only single-word commands
COMMANDS = []
for phrases in INTENTS.values():
    for phrase in phrases:
        if " " not in phrase:  # single word only
            COMMANDS.append(phrase)


class StreamingASR:
    def __init__(self):
        self.model = load_model()
        self.rec = KaldiRecognizer(self.model, 16000)
        self.rec.SetWords(True)

    def process_chunk(self, chunk):
        # Final result
        if self.rec.AcceptWaveform(chunk):
            result = json.loads(self.rec.Result())
            text = result.get("text", "").strip()
            if text:
                return text

        # Partial result for early detection
        partial = json.loads(self.rec.PartialResult())
        partial_text = partial.get("partial", "").strip()

        if partial_text:
            for cmd in COMMANDS:
                if cmd in partial_text:
                    return cmd

        return None

    def reset(self):
        self.rec = KaldiRecognizer(self.model, 16000)
        self.rec.SetWords(True)
