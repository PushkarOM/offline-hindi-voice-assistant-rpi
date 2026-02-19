import json
import os
from vosk import KaldiRecognizer, Model
from nlp.intents import INTENTS

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "model",
    "vosk-model-small-hi-0.22"
)

_model = None


def load_model():
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise RuntimeError("Vosk Hindi model not found")
        _model = Model(MODEL_PATH)
    return _model

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
