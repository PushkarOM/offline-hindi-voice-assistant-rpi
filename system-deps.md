# 🖥 System Dependencies (Raspberry Pi)

Install the following system-level packages **before creating the Python virtual environment**.

These are required for:
- Python development
- Microphone input (PortAudio / ALSA)
- Offline Text-to-Speech (eSpeak-NG)

---

## 📦 Install Required Packages

```bash
sudo apt update

sudo apt install -y \
  python3 \
  python3-venv \
  python3-dev \
  python3-pip \
  build-essential \
  portaudio19-dev \
  alsa-utils \
  espeak-ng
```
