## Streaming Latency Benchmarks

This folder contains real-time performance evaluation scripts for the Offline Hindi Voice Assistant.

The benchmark measures end-to-end system latency on actual hardware (Raspberry Pi 4).

---

## 📄 streaming_latency.py

This script performs a **live streaming latency benchmark** using microphone input.

It measures:

- 🎤 Speech Duration  
- 🧠 ASR + NLP Processing Latency  
- 🔊 TTS Playback Duration  
- ⏱ Full Completion Time (speech start → TTS finish)  
- 💻 CPU Usage  
- 🧠 Memory Usage  

---

## 🏆 Competition Metric

The primary evaluation metric is:

**Processing Latency**

This is defined as:

Time between:
> ASR final text detection  
and  
> TTS response generation start  

It represents the system’s actual decision speed.

---

## 📊 Metrics Explained

| Metric | Description |
|--------|-------------|
| Speech Duration | Time from first audio chunk to ASR final text |
| Processing Latency | Intent detection + response generation time |
| TTS Playback Duration | Time required to speak the response |
| Full Completion Time | Speech start → TTS playback finish |
| CPU Usage | % CPU used by the process |
| Memory Usage | RAM usage in MB |

---

## 🧪 How to Run Benchmark

### 1️⃣ Connect Microphone
Ensure your microphone is connected and working on Raspberry Pi.

You can verify with:
```bash
arecord -l
```


---

### 2️⃣ Run Benchmark Script

From project root:

``` bash
python -m benchmarks.streaming_latency_test
```

---

### 3️⃣ Speak a Test Command

After running, you will see:
```bash
Speak now...
```


Speak a clear Hindi command such as:

- "समय क्या हुआ है"
- "10 सेकंड का टाइमर लगाओ"
- "नमस्ते"
- "आज की तारीख क्या है"

The system will:
1. Detect speech
2. Convert speech to text (ASR)
3. Detect intent
4. Generate response
5. Speak response (TTS)
6. Print latency metrics

---

## 📁 Benchmark Results

Each run automatically saves a timestamped log file inside:

<RESULTS_DIR>/streaming_latency_YYYYMMDD_HHMMSS.log

Example: results/streaming_latency_20260219_184523.log

This file contains:
- All latency measurements
- CPU & memory stats
- Detected intent
- ASR output

---

## 🎯 Testing Best Practices

For consistent measurements:

- Use the same command each time
- Speak at normal speed
- Minimize background noise
- Run no other heavy processes
- Reboot Pi before official measurements (recommended)

Run 5–10 trials and report the average processing latency.

---

## 🖥 Hardware Used

Final measurements are performed on:

Raspberry Pi 4 (4GB RAM)  
Offline ASR (Vosk Hindi Model)  
Fully local NLP and TTS  

No internet is used during benchmarking.

