# NOTE!:
#------------------------------------------------------------------------------------------------
# No use the latest version of the RPi OS thus INMP441 does not support or dected by the RPi.
# For the L/R connected with GPIO to GND Default channel will be the Left.
#------------------------------------------------------------------------------------------------

# Pre Request:
# -------------------------------------------------
# Upgrade & Update 
sudo apt-get update && sudo apt-get upgrade -y

# Virtual enviroment.
python3 -m venv env

# Active the enviroment.
source env/bin/activate

# Upgrade pip if not.
pip install --upgrade pip

# Deactivation enviroment.
deactivate
# ------------------------------------------------

# All this library will be in enviroment folder:
#--------------------------------------------------------------------------------
# INMP441 works via ALSA (Advanced Linux Sound Architecture) for globel.
sudo apt-get install alsa-utils 

# PyAudio library used for recording audio stream, real time audio capture.
sudo apt install portaudio19-dev  # Globel
# or 
pip install pyaudio               # in env

# Converting raw audio to arrays, Signal math operations.
pip install numpy

# Filtering, FFT, Digital signal processing.
pip install scipy
#--------------------------------------------------------------------------------

# Used to enable the I2S (I2C & SPI) interface in Raspberry Pi.
sudo raspi-config

# Used to add the line dtparam=i2s=on to activate I2S in the boot configuration.
sudo nano /boot/config.txt

# Restart the system to apply configuration changes.
sudo reboot

# Used to verify that the INMP441 microphone is detected.
arecord -l

# Used to record digital audio from the INMP441 microphone.
arecord -D plughw:1,0 -f S32_LE -r 16000 test.wav

