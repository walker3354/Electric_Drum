import multiprocessing
import subprocess
import torchaudio
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write


def run_script1():
    subprocess.call(['python3', 'drumAndSensor.py'])

def run_script2():
    subprocess.call(['python3', 'recordAudio.py'])

if __name__ == "__main__":
    # Creating multiple processes
    proc1 = multiprocessing.Process(target=run_script1)
    proc2 = multiprocessing.Process(target=run_script2)

    # Initiating processes
    proc1.start()
    proc2.start()

    # Waiting until processes finish
    proc1.join()
    proc2.join()

    print("Both scripts completed.")



print("music generating...")
model = MusicGen.get_pretrained('melody')
model.set_generation_params(duration=15)  # generate 8 seconds.
wav = model.generate_unconditional(4)    # generates 4 unconditional audio samples
descriptions = ['Use this tempo to create a simple, upbeat pop beat. Take heavy influence from the melody in the given audio. Make sure the melody audio sample given has notable influence.']
wav = model.generate(descriptions)  # generates 3 samples.

melody, sr = torchaudio.load("/home/csl/Downloads/electricdrum/output.wav")
# generates using the melody from the given audio and the provided descriptions.
wav = model.generate_with_chroma(descriptions, melody[None], sr)
#melody[None].expand(3, -1, -1) is you want three
for idx, one_wav in enumerate(wav):
    # Will save under {idx}.wav, with loudness normalization at -14 db LUFS.
    audio_write(f'{idx}', one_wav.cpu(), model.sample_rate, strategy="loudness")

    print("done!")

