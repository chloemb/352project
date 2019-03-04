import pyaudio
import aubio
import time
import numpy as np


def initpitch():
    global currentpitch
    currentpitch = 0


def pitchdetection(highest_freq, lowest_freq):
    smoothing_threshold = (highest_freq - lowest_freq) / 2

    # PyAudio object.
    p = pyaudio.PyAudio()

    # Open stream.
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1, rate=44100, input=True,
                    frames_per_buffer=1024)

    # Aubio's pitch detection.
    pDetection = aubio.pitch("default", 2048,
                             2048 // 2, 44100)

    # Set unit.
    pDetection.set_unit("Hz")
    pDetection.set_silence(-40)

    # Plotting
    # samplenum = 0
    # fig = plt.figure()
    # plotx = []
    # ploty = []

    prevsteadypitch = 0.0

    while True:
        data = stream.read(1024)
        samples = np.fromstring(data, dtype=aubio.float_type)
        pitch = pDetection(samples)[0]

        if not pitch < lowest_freq and not pitch > highest_freq:
            if prevsteadypitch < lowest_freq and pitch < highest_freq:
                prevsteadypitch = pitch
            elif abs(prevsteadypitch - pitch) < smoothing_threshold and prevsteadypitch != 0 and pitch != 0:
                prevsteadypitch = pitch

        pitchfile = open("pitch.txt", "w+")
        pitchfile.write(str(prevsteadypitch))
        pitchfile.close()


def getcurpitch():
    global currentpitch
    return currentpitch
