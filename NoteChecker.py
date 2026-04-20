
import numpy as np

import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
#fft_result = np.fft.fft(signal)

#parameters
fs = 44100  # Sample rate, aka how many snapshots of "audio" to take every second
seconds = 1  # Duration of raudio recording

print("Recording started...")

#2. Start recording into a NumPy array
myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)# only using 1 as we are using just the mono mic of my lapotop to record

# 3. Wait for recording to finish
sd.wait()

print("Recording finished. Saving file...")

# 4. Save as WAV file
write('output.wav', fs, myrecording)

# print(myrecording.shape)
# print("First 10 instances")
# print(myrecording[:11])
# print("Last 10 instances")
# print(myrecording[-10:])
audio_signal = myrecording.squeeze() # to make the audio file 1d as we are only using 1 channel to reccord the audio

#to do now
# now need to analyze the recorded audio,
# convert the frequency to note and then
# output  the result

#plotting the waveform of the audion recorded using matlab , funstuff
plt.plot(myrecording)
plt.title("Waveform")
plt.show()

#FFT , to do waveform analhysis
N = len(audio_signal)
fft_result = np.fft.fft(audio_signal)
freqs = np.fft.fftfreq(N, 1/fs)

# keep only positive frequencies
positive_freqs = freqs[:N//2]
magnitudes = np.abs(fft_result[:N//2])

# find peak frequency, as we only need the peaks to detect the audios
peak_index = np.argmax(magnitudes)
dominant_freq = positive_freqs[peak_index]

print(f"Detected Frequency: {dominant_freq:.2f} Hz")

# -now that frequency is noted, converting it to note
if dominant_freq > 0:
    note_number = 69 + 12 * np.log2(dominant_freq / 440.0)# formula to conveert
    note_number = int(round(note_number))

    notes = ['C', 'C#', 'D', 'D#', 'E', 'F',
             'F#', 'G', 'G#', 'A', 'A#', 'B'] # array for all notes

    note = notes[note_number % 12]
    octave = note_number // 12 - 1

    print(f"Note: {note}{octave}")
else:
    print("No valid frequency detected")