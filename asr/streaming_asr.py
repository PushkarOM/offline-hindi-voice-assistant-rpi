import json
from vosk import KaldiRecognizer
from asr.hindi_asr import load_model


class StreamingASR:
    def __init__(self):
        self.model = load_model()
        self.rec = KaldiRecognizer(self.model, 16000)
        self.rec.SetWords(True)

    def process_chunk(self, chunk):
        if self.rec.AcceptWaveform(chunk):
            result = json.loads(self.rec.Result())
            return result.get("text", "")
        return None

    def reset(self):
        self.rec = KaldiRecognizer(self.model, 16000)
        self.rec.SetWords(True)
