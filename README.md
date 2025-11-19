# Audio Entropy Seed Generator

This project provides a simple Python script that captures a brief snippet of microphone audio and converts the raw waveform data into a large numeric string suitable for use as an entropy seed.

## Features

* Records a tiny audio sample (default: 0.125 seconds)
* Converts raw 16-bit PCM microphone input into a long deterministic numeric string
* Produces a variable-length seed based on real-world noise
* Lightweight and easy to integrate into other applications

## How It Works

1. The script opens the default microphone via **PyAudio**.
2. It records a few audio frames using the configured sample rate and buffer size.
3. Raw audio bytes are converted into NumPy arrays of 16-bit signed integers.
4. Each sample value has its sign removed and is appended to a growing string.
5. The resulting numeric string can be used as an entropy source.

## Requirements

* Python 3.x
* `pyaudio`
* `numpy`
* Microphone input available

Install dependencies:

```bash
pip install pyaudio numpy
```

## Usage

Run the script directly:

```bash
python yourscript.py
```

You will see output similar to:

```
--- Generating Entropy Seed ---
Seed Length: 58200
Generated Seed: 1209219283...
-------------------------------
```

## Configuration

You can adjust the recording behavior by modifying these variables:

* `CHUNK` – number of frames per buffer
* `RATE` – audio sample rate
* `RECORD_SECONDS` – length of audio capture
* `CHANNELS` – number of audio channels (default: mono)

## Example Output Explained

The seed is a plain concatenation of absolute sample values from the audio. Length depends on:

```
seed_length ≈ (RATE × RECORD_SECONDS)
```

Small changes in ambient noise result in different seed values.

## Notes

This method provides a lightweight form of entropy, but it is **not** intended as a cryptographically secure RNG replacement on its own. Combine with additional entropy sources if you need strong randomness.
