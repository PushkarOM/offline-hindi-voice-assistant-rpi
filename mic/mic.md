# INMP441 MEMS High Precision

## INMP441 Micro Electro Mechanical System High Precision Omnidirectional Microphone Module (I2S)

- The **INMP441** is a high-performance, low-power, digital-output, omnidirectional MEMS microphone with a bottom port.  

- The complete INMP441 solution consists of a MEMS sensor, signal conditioning, analog-to-digital converter, anti-aliasing filter, power management, and an industry-standard **24-bit I2S interface**.

- The I2S interface allows the INMP441 to be directly connected to digital processors such as DSPs and microcontrollers without the need for an external audio codec.  

- The INMP441 has a high signal-to-noise ratio and is an excellent choice for near-field applications. It features a flat wideband frequency response, resulting in high-definition natural sound.

## Interface Definition

- **SCK**: Serial data clock for I2S interface  
- **WS**: Serial data word selection for I2S interface  
- **L/R**: Left/Right channel selection  
- When set to **low**, the microphone outputs a signal on the **left channel** of the I2S frame  
- When set to **high**, the microphone outputs a signal on the **right channel**  
- **SD**: Serial data output of the I2S interface  
- **VCC**: Input power, **1.8V to 3.3V**  
- **GND**: Power ground  

## INMP441 Connection with ESP32

| INMP441 Pin | ESP32 Pin |
|------------|-----------|
| SCK        | GPIO14    |
| SD         | GPIO32    |
| WS         | GPIO15    |
| L/R        | GND       |
| GND        | GND       |
| VDD        | VDD3.3    |

## INMP441 Connection with Raspberry Pi 4

| INMP441 Pin | Raspberry Pi 4 Pin | GPIO |
|------------|-------------------|------|
| **SCK**    | Pin 12            | GPIO18 (PCM_CLK) |
| **WS**     | Pin 35            | GPIO19 (PCM_FS)  |
| **SD**     | Pin 38            | GPIO20 (PCM_DIN) |
| **L/R**    | Pin 6             | GND |
| **VDD**    | Pin 1 or 17       | 3.3V |
| **GND**    | Pin 6             | GND |

## Features

- Digital I2S interface with high-precision **24-bit data**  
- High signal-to-noise ratio: **61 dBA**  
- High sensitivity: **−26 dBFS**  
- Stable frequency response from **60 Hz to 15 kHz**  
- Low power consumption: **1.4 mA**  
- High PSR: **−75 dBFS** 

## Product Specifications

| Parameter                    | Value            |
|------------------------------|------------------|
| Frequency Range (Hz)         | 60 to 15000      |
| S/N Ratio (dB)               | 61 dBA           |
| High Sensitivity             | −26 dBFS         |
| Current Consumption (mA)     | 1.4 mA           |
| High PSR                     | −75 dBFS         |
| Shipping Weight              | 0.02 kg          |
| Shipping Dimensions          | 6 × 5 × 3 cm     |






