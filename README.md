# Audio Entropy Seed Generator

**Audio Entropy Seed Generator** is a utility designed to capture ambient audio and convert it into a high-entropy random seed for cryptographic, security, or data-generation applications. It uses your microphone to collect unbiased environmental noise and processes it into binary data, governed by robust entropy extraction algorithms.

> **Key Features:**
> - **True Hardware-Based Entropy**: Gathers unpredictable randomness from real-world sound.
> - **Multiple Extraction Algorithms**: Choose from various algorithms to process raw input for reliability.
> - **Configurable Recording**: Customize sample rate, bit depth, and duration.
> - **Cross-Platform Support**: Works on major operating systems (Python 3.x compatible).

---

## Table of Contents

- [Features](#features)
- [How it Works](#how-it-works)
- [Installation](#installation)
- [Usage](#usage)
- [Entropy Extraction Algorithms](#entropy-extraction-algorithms)
- [Example](#example)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Real-World, Unbiased Randomness**
- **Configurable Audio Capture (Sample Rate, Bit Depth, Duration)**
- **Algorithm Selection for Raw or Processed Seeds**
- **Optional Save-to-File**
- **No Third-Party Cloud Dependencies (Runs Offline)**

---

## How it Works

Audio Entropy Seed Generator records audio from your default microphone, then applies entropy extraction techniques to eliminate bias and convert the captured sound waves into high-quality random data.

1. Records a user-configurable duration of ambient sound.
2. Optionally normalizes, de-noises, and processes raw waveform data.
3. Chooses an extraction algorithm (e.g., SHA-256, Von Neumann, XOR, or raw byte dumps).
4. Outputs a hex or base64-encoded seed suitable for cryptography, randomization, or system entropy pools.

---

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/LunexCorp/Audio-Entropy-Seed-Generator.git
   cd Audio-Entropy-Seed-Generator
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```
   *Typical dependencies include `sounddevice`, `numpy`, and `scipy`. See the requirements for full details.*

3. **(Optional) Create a Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

---

## Usage

Run the script from the command line:

```bash
python3 audio_entropy_seed.py [options]
```

**Common Options:**
- `--duration <seconds>`: *(Optional)* Length of audio capture (default: 5 seconds)
- `--samplerate <hz>`: *(Optional)* Sample rate in Hz (default: 44100)
- `--bits <depth>`: *(Optional)* Bit depth (default: 16)
- `--algorithm <name>`: *(Optional)* Extraction method (`sha256`, `raw`, `xor`, etc.)
- `--output <file>`: *(Optional)* File to save the generated seed

**Examples:**

Record 8 seconds of audio and generate a SHA-256 seed:

```bash
python3 audio_entropy_seed.py --duration 8 --algorithm sha256
```

Record 3 seconds and save the raw bytes to file:

```bash
python3 audio_entropy_seed.py --duration 3 --algorithm raw --output my_seed.bin
```

---

## Entropy Extraction Algorithms

The utility supports multiple ways to derive entropy from captured audio:

| Algorithm    | Description                                       |
|--------------|---------------------------------------------------|
| SHA-256      | Hashes waveform data to produce a 256-bit seed    |
| Von Neumann  | Applies Von Neumann unbiasing to raw bits         |
| XOR          | Bitwise reduces samples for fast extraction       |
| Raw Bytes    | Outputs captured waveform data verbatim           |

See the script for algorithm details and options, or add your own extractor!

---

## Example

Suppose you want to generate a high-entropy seed for your cryptographic application:

1. Launch the script with your preferred options:
   ```bash
   python3 audio_entropy_seed.py --duration 10 --algorithm sha256
   ```

2. Make some spontaneous noises or let ambient sound fill the input.

3. The program will output something like:
   ```
   [INFO] Recording...
   [INFO] Processing entropy...
   Seed (hex): e3b7040e...b1cf9ae3
   Entropy bits: 256
   ```

---

## Contributing

Contributions are welcome! If you have suggestions, find a bug, or want to add new extraction algorithms, please open an issue or submit a pull request.

---
