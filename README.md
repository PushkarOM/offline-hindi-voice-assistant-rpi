# 🗣 Offline Hindi Voice Assistant (ARM Edge Deployment)

A fully offline, privacy-preserving Hindi Voice Assistant optimized for ARM-based edge devices such as the Raspberry Pi 4.

Built as part of the **Bharat AI-SoC Student Challenge 2026**, this project demonstrates an end-to-end embedded speech pipeline executing entirely on-device without any cloud dependency.

---

## 🚀 Project Overview

The system implements a real-time streaming speech pipeline:

Microphone → Audio Stream → Vosk ASR → NLP Engine → State Manager → Action Layer → TTS → Speaker

All processing is performed locally on the Raspberry Pi CPU, ensuring:

- ✅ Complete offline operation  
- 🔒 Data privacy  
- ⚡ Low latency  
- 🧠 Edge AI deployment feasibility  

---

## 🎯 Key Features

- Fully offline Hindi speech recognition
- Streaming-based low-latency ASR
- Rule-based NLP with cosine similarity fallback
- Wake-word activation
- Timer and basic command support
- Modular architecture
- Streaming benchmark mode for performance evaluation

---

## 🧠 Speech Pipeline Components

### 1️⃣ Automatic Speech Recognition (ASR)

- Engine: **Vosk (Small Hindi Model)**
- Sampling Rate: 16 kHz
- Streaming inference
- Optimized for ARM CPU

Why Vosk?
- Lightweight (~50 MB model)
- Fully offline
- ARM compatible
- Low memory footprint

---

### 2️⃣ Intent Recognition (NLP)

Two-step detection mechanism:

**Step 1 – Rule-Based Matching**
- Text normalization
- Filler word removal
- Regex-based pattern extraction
- Keyword mapping

**Step 2 – Cosine Similarity Fallback**
- TF-IDF vectorization
- Semantic similarity comparison
- Handles transcription variations (e.g., nukta differences)

This hybrid approach improves robustness without heavy transformer models, making it suitable for edge deployment.

---

### 3️⃣ Text-to-Speech (TTS)

- Engine: **eSpeak-NG**
- Fully offline
- Low-latency response generation
- Hindi-compatible output

---

## 💻 Hardware Requirements

- Raspberry Pi 4 Model B (4GB recommended)
- USB or I2S Microphone (e.g., INMP441)
- Speaker (3.5mm jack or HDMI)
- microSD card (16GB+)
- Stable power supply

---

## 🛠 System Setup (Raspberry Pi)

Before running the assistant, ensure that the Raspberry Pi audio interface is properly configured.

### 🎙 I2S Microphone Configuration

If using an I2S microphone (e.g., INMP441) or Google Voice HAT, update the Raspberry Pi boot configuration:

Open the configuration file:

```bash
sudo nano /boot/config.txt
```

Add the Following Lines :

```bash
dtparam=i2s=on
dtoverlay=googlevoicehat-soundcard
```

Save and Reboot, After reboot verify if the sound card is detected :

```bash
arecord -l
```

### 2️⃣ USB Microphone Setup (Recommended)

If using a USB microphone:
- No dtoverlay configuration is required.
- Simply plug in the USB microphone.
- Reboot (optional but recommended).

Verify detection:
```bash
arecord -l
```

You should see something similar to:
```bash
card 1: Device [USB Audio Device], device 0
```


For maximum compatibility across different hardware setups, configure the microphone device in the code as:
[Input Stream](./audio/input_stream.py)

```bash
device="default"  # if usb
```

#### if dtoverlay used with a different mic module

```bash
device="plughw:CARD=sndrpigooglevoi,DEV=0" 
```

### Installing System Level Packages

Before installing Python dependencies, you must install required system-level packages.

👉 See detailed setup instructions here:  
[System Dependencies Guide](./system-deps.md)


---


## 🧰 Software Requirements

- Raspberry Pi OS (64-bit recommended)
- Python 3.10+
- PyAudio
- Vosk
- eSpeak-NG
- NumPy
- scikit-learn (for cosine similarity)

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ⚙️ Running the Assistant
Start the assistant:

```bash
python main.py
```

---

## 📊 Sample Streaming Benchmark Output
For Benchmarks Refer to the 
[Benchmarks Guide](./benchmarks/README.md)


```bash
=== Streaming Latency Benchmark (Competition Mode) ===
CPU usage                 : 53.4 %
Memory usage              : 162.0 MB

Speech duration           : 4565.9 ms
Processing latency        : 253.4 ms
TTS playback duration     : 3342.8 ms
Full completion time      : 8162.1 ms

ASR Output : 10 सेकेंड का टाइमर लगा
Intent     : TIMER
```
---

## 🗂 Project Structure

```bash
tree -I "venv|__pycache__|model"
.
├── LICENSE
├── README.md
├── asr
│   ├── __init__.py
│   └── streaming_asr.py
├── audio
│   ├── __init__.py
│   └── input_stream.py
├── benchmarks
│   ├── README.md
│   ├── results
│   └── streaming_latency_test.py
├── config
│   ├── __init__.py
│   ├── env.py
│   └── settings.py
├── logs
│   └── assistant.log
├── main.py
├── nlp
│   ├── __init__.py
│   ├── intent_parser.py
│   ├── intents.py
│   └── number_normalizer.py
├── pipeline
│   └── streaming_pipeline.py
├── requirements.txt
├── system-deps.md
└── tts
    ├── __init__.py
    ├── hindi_tts.py
    └── responses.py

9 directories, 23 files
```

---

## 🔬 Optimization Highlights

- Lightweight ASR model selection
- Streaming inference instead of batch processing
- Event-driven state management
- Minimal background processes=
- ARM CPU-friendly architecture

Designed specifically for Edge AI deployment on AI-SoC platforms.

---

## 🔒 Privacy & Edge AI

- No internet usage
- No cloud APIs
- No data transmission
- All inference performed locally

Ensures privacy-preserving intelligent interaction.

---

## 🎥 Demo Video

👉 [Watch Demo on YouTube](https://youtu.be/ryDRLKcCcr8?si=5ujjtuz32ikEVcwN)

---

## 📚 References

- Vosk Speech Recognition Toolkit  
- eSpeak-NG Documentation  
- Raspberry Pi 4 Specifications  
- ARM Architecture Reference Manual  

---

## 👨‍💻 Authors

**Pushkar Chaturvedi**  
**Rishabh Jain**  

#### Mentor : **Mr Ajay Kumar** (JUET) 

Jaypee University of Engineering & Technology  
Bharat AI-SoC Student Challenge 2026

---
