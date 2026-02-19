import pyaudio

SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK = 1024
FORMAT = pyaudio.paInt16

RECORD_SECONDS = 2.0
    
LOG_PATH = "logs/assistant.log"

USE_MIC = True
MIC_DURATION = 3.0


TMP_DIR = "benchmarks/tmp"
RESULTS_DIR = "benchmarks/results"
