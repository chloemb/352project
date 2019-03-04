import pyaudio
import aubio
import time
import numpy as np
import matplotlib.pyplot as plt

# humming/voice 800, 100, 1000
# whistle 800, 1000, 4000
lowest_freq = 1000
highest_freq = 3000
smoothing_threshold = (highest_freq - lowest_freq)/2

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

start = time.time()

prevsteadypitch = 0.0
prevpitch = 0.0



while True:
    data = stream.read(1024)
    samples = np.fromstring(data, dtype=aubio.float_type)
    pitch = pDetection(samples)[0]
    # Compute the energy (volume) of the
    # current frame.
    # volume = np.sum(samples ** 2) / len(samples)
    # Format the volume output so that at most
    # it has six decimal numbers.
    # volume = "{:.6f}".format(volume)

    if not pitch < lowest_freq and not pitch > highest_freq:
        if prevsteadypitch < lowest_freq and pitch < highest_freq:
            prevsteadypitch = pitch
        elif abs(prevsteadypitch - pitch) < smoothing_threshold and prevsteadypitch != 0 and pitch != 0:
            prevsteadypitch = pitch

    pitchfile = open("pitch.txt", "w+")
    pitchfile.write(str(prevsteadypitch))
    pitchfile.close()

    # samplenum += 1
    # plotx.append(samplenum)
    # ploty.append(prevsteadypitch)


    prevpitch = pitch

    print(prevsteadypitch)
    # print(volume)


# plt.plot(plotx, ploty)
# plt.show()