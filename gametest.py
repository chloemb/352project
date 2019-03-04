import sys, pygame, pyaudio, aubio, time, numpy as np, matplotlib.pyplot as plt

# humming/voice 800, 100, 1000si
# whistle 800, 1000, 4000
lowest_freq = 1000
highest_freq = 3000

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

# Game
pygame.init()

size = width, height = 320, 800
speed = [2, 2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

ball = pygame.image.load("intro_ball.gif")
ballrect = ball.get_rect()

curpitch = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    # read the pitch file
    pitchfile = open("/Users/chloe/Desktop/352project/pitch.txt", "r")
    readpitch = pitchfile.readline()
    if readpitch is not "":
        curpitch = float(readpitch)

    # calculate the height
    curheight = height - int((curpitch-lowest_freq)/(highest_freq-lowest_freq) * height)

    # move the ball
    ballrect.center = (160, curheight)

    # draw
    screen.fill(black)
    screen.blit(ball, ballrect)
    pygame.display.flip()


