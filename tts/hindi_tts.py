import subprocess
import tempfile
import os
import threading
from queue import Queue
from config.env import is_wsl


class AsyncTTS:
    def __init__(self):
        self.queue = Queue()
        self.thread = threading.Thread(target=self._worker, daemon=True)
        self.thread.start()

    def _worker(self):
        while True:
            text = self.queue.get()
            if text is None:
                break

            try:
                self._speak_blocking(text)
            except Exception as e:
                print(f"TTS error: {e}")

            self.queue.task_done()

    def _speak_blocking(self, text):
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            wav_path = f.name

        subprocess.run([
            "espeak-ng",
            "-v", "hi",
            "-s", "150",
            "-a", "200",
            "-w", wav_path,
            text
        ], check=True)

        if not is_wsl():
            subprocess.run(["aplay", wav_path])
        else:
            print(f"[WSL] Audio generated: {wav_path}")

        os.remove(wav_path)

    def speak(self, text):
        self.queue.put(text)

    def stop(self):
        self.queue.put(None)
        self.thread.join()
