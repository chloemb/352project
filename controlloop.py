import sys, pygame, pitchdetection
from multiprocessing import Process

# humming/voice 800, 100, 1000si
# whistle 800, 1000, 4000
low_freq = 100
high_freq = 500


def GameLoop():
    pygame.init()

    size = width, height = 320, 800
    black = 0, 0, 0

    screen = pygame.display.set_mode(size)

    ball = pygame.image.load("intro_ball.gif")
    ballrect = ball.get_rect()

    curpitch = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        # read the pitch file
        pitchfile = open("pitch.txt", "r")
        readpitch = pitchfile.readline()
        pitchfile.close()
        if readpitch is not "":
            curpitch = float(readpitch)

        # calculate the height
        curheight = height - int((curpitch-low_freq)/(high_freq-low_freq) * height)

        # move the ball
        ballrect.center = (160, curheight)

        # draw
        screen.fill(black)
        screen.blit(ball, ballrect)
        pygame.display.flip()


if __name__ == '__main__':
    pitchdetection.initpitch()

    a = Process(target=pitchdetection.pitchdetection, args=(high_freq, low_freq))
    a.start()
    b = Process(target=GameLoop)
    b.start()

    a.join()
    b.join()
