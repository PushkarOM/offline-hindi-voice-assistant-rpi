## Project Description

Students will build an embedded speech pipeline performing:

* Speech-to-text using a lightweight ASR model (e.g., Coqui STT or fine-tuned wav2vec2 for Hindi).
* Command parsing and intent recognition in Python.
* Text-to-speech responses using local TTS (eSpeak-NG or Festival).
* End-to-end execution on the Raspberry Pi CPU with no cloud dependency.

## Key Requirements

### Hardware

* Raspberry Pi 4 (or similar Arm SBC)
* USB microphone
* Speaker via 3.5 mm jack or HDMI

### Software

* Python with PyAudio for audio I/O
* Coqui STT or fine-tuned wav2vec2 for ASR
* eSpeak-NG or Festival for TTS
* Custom Python logic for intent recognition and command execution

## Performance Targets

* Sub-2-second response time per command
* Accurate recognition for 10–15 Hindi commands
* Robust, fully offline operation

## Deliverables

* Source code for the full voice assistant pipeline
* Documentation of any model fine-tuning or optimization steps
* Demo video showing responses to multiple commands
* Short report on architecture, challenges in Hindi ASR/TTS, and performance metrics

## Learning Outcomes

* Hands-on experience with embedded speech AI and offline ASR/TTS
* Understanding challenges of regional language processing
* Integrating ASR, simple NLP/intent logic, and TTS on a constrained platform
