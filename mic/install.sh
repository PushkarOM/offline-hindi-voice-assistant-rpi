# No use the latest version of the RPi OS thus INMP441 does not support or dected by the RPi.
# For the L/R connected with GPIO to GND Default channel will be the Left.

#  Used to enable the I2S (I2C & SPI) interface in Raspberry Pi.
sudo raspi-config

# Used to add the line dtparam=i2s=on to activate I2S in the boot configuration.
sudo nano /boot/config.txt

# Restart the system to apply configuration changes.
sudo reboot

# Used to verify that the INMP441 microphone is detected.
arecord -l

# Used to record digital audio from the INMP441 microphone.
arecord -D plughw:1,0 -f S32_LE -r 16000 test.wav
