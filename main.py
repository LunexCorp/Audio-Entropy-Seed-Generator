import argparse
import hashlib
import sys
import os
import numpy as np
import sounddevice as sd
import base64

def record_audio(duration, samplerate, channels, dtype):
    print('[INFO] Recording...')
    audio = sd.rec(
        int(duration * samplerate),
        samplerate=samplerate,
        channels=channels,
        dtype=dtype
    )
    sd.wait()
    return np.squeeze(audio)

def extract_raw(samples, bit_depth):
    # Convert audio data to bytes according to bit depth
    if bit_depth == 16:
        int_samples = (samples * 32767).astype(np.int16)
        return int_samples.tobytes()
    elif bit_depth == 8:
        int_samples = ((samples + 1) * 127.5).astype(np.uint8)
        return int_samples.tobytes()
    else:
        raise ValueError("Unsupported bit depth for raw output")

def extract_sha256(samples, bit_depth):
    print('[INFO] Processing entropy with SHA-256...')
    raw_bytes = extract_raw(samples, bit_depth)
    h = hashlib.sha256()
    h.update(raw_bytes)
    return h.digest()  # Return raw bytes

def extract_xor(samples, bit_depth):
    print('[INFO] Processing entropy with XOR reduction...')
    raw_bytes = extract_raw(samples, bit_depth)
    # Reduce all bytes with xor
    result = 0
    for b in raw_bytes:
        result ^= b
    # Repeat result to fill 32 bytes (256 bits)
    out = bytes([result] * 32)
    return out

def von_neumann_unbias(bitstream):
    out = []
    i = 0
    while i < len(bitstream) - 1:
        pair = bitstream[i:i+2]
        if pair == [0,1]:
            out.append(1)
        elif pair == [1,0]:
            out.append(0)
        # else (0,0) or (1,1): skip
        i += 2
    return out

def extract_von_neumann(samples, bit_depth):
    print('[INFO] Processing entropy with Von Neumann unbiasing...')
    raw_bytes = extract_raw(samples, bit_depth)
    bits = []
    for b in raw_bytes:
        for i in reversed(range(8)):
            bits.append((b >> i) & 1)
    unbiased_bits = von_neumann_unbias(bits)
    # Pad to nearest byte
    while len(unbiased_bits) % 8 != 0:
        unbiased_bits.append(0)
    # Convert back to bytes
    result_bytes = bytearray()
    for i in range(0, len(unbiased_bits), 8):
        byte = 0
        for j in range(8):
            byte = (byte << 1) | unbiased_bits[i + j]
        result_bytes.append(byte)
    out_bytes = bytes(result_bytes)
    # Output up to 32 bytes (for consistency with sha256)
    return out_bytes[:32] if len(out_bytes) >= 32 else out_bytes

def save_output(data, output_path, mode='wb'):
    with open(output_path, mode) as f:
        f.write(data)

def main():
    parser = argparse.ArgumentParser(description="Audio Entropy Seed Generator")
    parser.add_argument('--duration', type=float, default=5, help='Length of audio capture in seconds (default: 5)')
    parser.add_argument('--samplerate', type=int, default=44100, help='Sample rate in Hz (default: 44100)')
    parser.add_argument('--bits', type=int, default=16, choices=[8,16], help='Bit depth (default: 16)')
    parser.add_argument('--channels', type=int, default=1, help='Number of audio channels (default: 1/mono)')
    parser.add_argument('--algorithm', type=str, choices=['sha256', 'von', 'raw', 'xor'], default='sha256',
                        help='Entropy extraction algorithm: sha256, von, xor, or raw (default: sha256)')
    parser.add_argument('--output', type=str, default=None, help='File to save the generated seed (default: none)')
    parser.add_argument('--format', type=str, choices=['hex','base64','raw'], default='hex',
                        help='Output format (default: hex, only applies to sha256/xor/von)')
    args = parser.parse_args()

    if args.bits == 16:
        dtype = 'int16'
    elif args.bits == 8:
        dtype = 'uint8'
    else:
        print("Unsupported bit depth. Only 8 or 16 allowed.")
        sys.exit(1)

    try:
        samples = record_audio(args.duration, args.samplerate, args.channels, dtype)
    except Exception as e:
        print(f'[ERROR] Recording failed: {e}')
        sys.exit(1)

    if args.algorithm == 'sha256':
        seed_bytes = extract_sha256(samples, args.bits)
        label = 'Seed (hex)' if args.format == 'hex' else 'Seed (base64)'
    elif args.algorithm == 'xor':
        seed_bytes = extract_xor(samples, args.bits)
        label = 'Seed (hex)' if args.format == 'hex' else 'Seed (base64)'
    elif args.algorithm == 'von':
        seed_bytes = extract_von_neumann(samples, args.bits)
        label = 'Seed (hex)' if args.format == 'hex' else 'Seed (base64)'
    elif args.algorithm == 'raw':
        print('[INFO] Outputting raw waveform data...')
        seed_bytes = extract_raw(samples, args.bits)
        label = 'Raw waveform bytes'
    else:
        print('[ERROR] Unknown algorithm choice.')
        sys.exit(1)

    # Output or save the result
    if args.output:
        if args.algorithm == 'raw' or args.format == 'raw':
            save_output(seed_bytes, args.output, 'wb')
            print(f'[INFO] Seed saved as raw bytes to: {args.output}')
        elif args.format == 'hex':
            hex_string = seed_bytes.hex()
            save_output((hex_string + '\n').encode(), args.output, 'wb')
            print(f'[INFO] Seed (hex) saved to: {args.output}')
        elif args.format == 'base64':
            b64 = base64.b64encode(seed_bytes)
            save_output((b64.decode() + '\n').encode(), args.output, 'wb')
            print(f'[INFO] Seed (base64) saved to: {args.output}')
    else:
        print('-------------------------------')
        if args.algorithm == 'raw' or args.format == 'raw':
            print(f'{label}: (raw byte output; not printed)')
            print(f'Length: {len(seed_bytes)} bytes')
        elif args.format == 'hex':
            print(f'{label}: {seed_bytes.hex()}')
            print(f'Entropy bits: {len(seed_bytes)*8}')
        elif args.format == 'base64':
            b64 = base64.b64encode(seed_bytes).decode()
            print(f'{label}: {b64}')
            print(f'Entropy bits: {len(seed_bytes)*8}')
        print('-------------------------------')

if __name__ == '__main__':
    main()
