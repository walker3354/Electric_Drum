import sounddevice as sd
import soundfile as sf

duration = 18
  # Recording duration in seconds
samplerate = 44100  # Specify the desired samplerate

# Set the default audio input device to the system default (system audio output)
default_input_device = sd.default.device[1]

# Record the system audio
print("recording")
recording = sd.rec(int(duration * samplerate), channels=2, dtype='float32', blocking=True, device=default_input_device)

# Save the recording to a file (example using WAV format)
output_file = 'output.wav'
sf.write(output_file, recording, samplerate)

print(f"System audio recorded and saved to '{output_file}'.")
