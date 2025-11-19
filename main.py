import wave, pyaudio, numpy

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 0.125

# Make random seed
def randomSeed():
    """
    Captures a small amount of audio data from the default microphone 
    and converts the raw sample values into a large string seed.
    """
    p = pyaudio.PyAudio()
    
    # Open the audio stream for recording
    stream = p.open(format=FORMAT, 
                    channels=CHANNELS, 
                    rate=RATE, 
                    input=True, 
                    frames_per_buffer=CHUNK)

    dataRaw = []
    seed = ""
    
    # Calculate the number of chunks to record for RECORD_SECONDS
    frames_to_record = int(RATE / CHUNK * RECORD_SECONDS)

    for _ in range(0, frames_to_record):
        # Read a chunk of audio data
        data = stream.read(CHUNK)
        # Convert raw bytes into a numpy array of signed 16-bit integers
        samples = numpy.frombuffer(data, dtype=numpy.int16)
        dataRaw.append(samples)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Concatenate all sample values into a single string
    for I in dataRaw:
        for J in I:
            # Append the absolute value of the sample to the seed string
            seed = seed + str(J).strip('-')

    return seed

if __name__ == '__main__':
    print("--- Generating Entropy Seed ---")
    generated_seed = randomSeed()
    print(f"Seed Length: {len(generated_seed)}")
    print(f"Generated Seed: {generated_seed[:50]}...")
    print("-------------------------------")
