import sys, pygame, pitchdetection, time
from multiprocessing import Process

# humming/voice approx 100, 500
# whistle 1000, 3000
low_freq = 1000
high_freq = 3000

def GetPitch():
    # read the pitch file
    pitchfile = open("pitch.txt", "r")
    readpitch = pitchfile.readline()
    pitchfile.close()
    return readpitch


def GameLoop():
    pygame.init()

    calibration_length = 5
    size = width, height = 800, 800
    black = 0, 0, 0
    white = 255, 255, 255

    screen = pygame.display.set_mode(size)

    pygame.font.init()
    myfont = pygame.font.Font("Assets/JosefinSans-Regular.ttf", 30)

    checkpoint_time = time.time()
    curpitch = 0

    while time.time() - checkpoint_time < calibration_length:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        screen.fill(black)

        textsurface = myfont.render('Sing or hum a low note', False, white)
        screen.blit(textsurface, (width/2 - textsurface.get_width()/2, height/2 - textsurface.get_height()/2))

        time_remaining = str(calibration_length - int(time.time() - checkpoint_time))
        countdown = myfont.render(time_remaining, False, white)
        screen.blit(countdown, (width/2 - countdown.get_width()/2,
                                height/2 - countdown.get_height()/2 + textsurface.get_height()))

        readpitch = GetPitch()
        if readpitch is not "":
            curpitch = float(readpitch)

        global low_freq
        low_freq = curpitch

        frequency = myfont.render("Low: " + "{:.2f}".format(curpitch), False, white)
        screen.blit(frequency, (width/2 - frequency.get_width()/2,
                                height/2 - frequency.get_height()/2 +
                                textsurface.get_height() + countdown.get_height()))
        pygame.display.flip()

    checkpoint_time = time.time()
    curpitch = 0

    while time.time() - checkpoint_time < calibration_length:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        screen.fill(black)

        textsurface = myfont.render('Sing or hum a high note', False, white)
        screen.blit(textsurface, (width / 2 - textsurface.get_width() / 2, height / 2 - textsurface.get_height() / 2))

        time_remaining = str(calibration_length - int(time.time() - checkpoint_time))
        countdown = myfont.render(time_remaining, False, white)
        screen.blit(countdown, (width / 2 - countdown.get_width() / 2,
                                height / 2 - countdown.get_height() / 2 + textsurface.get_height()))

        set_low = myfont.render("Low: " + "{:.2f}".format(low_freq), False, white)
        screen.blit(set_low, (width / 2 - frequency.get_width() / 2,
                              height / 2 - frequency.get_height() / 2 +
                              textsurface.get_height() + countdown.get_height()))

        readpitch = GetPitch()
        if readpitch is not "":
            curpitch = float(readpitch)

        global high_freq
        high_freq = curpitch

        frequency = myfont.render("High: " + "{:.2f}".format(curpitch), False, white)
        screen.blit(frequency, (width / 2 - frequency.get_width() / 2,
                                height / 2 - frequency.get_height() / 2 +
                                textsurface.get_height() + countdown.get_height() + set_low.get_height()))
        pygame.display.flip()

    print(low_freq, high_freq)
    ball = pygame.image.load("intro_ball.gif")
    ballrect = ball.get_rect()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        readpitch = GetPitch()
        if readpitch is not "":
            curpitch = float(readpitch)

        if curpitch < low_freq:
            curpitch = low_freq
        if curpitch > high_freq:
            curpitch = high_freq

        curheight = height - int((curpitch-low_freq)/(high_freq-low_freq) * height)

        print(curpitch, curheight)

        # move the ball
        ballrect.center = (width/2, curheight)

        # draw
        screen.fill(black)
        screen.blit(ball, ballrect)
        pygame.display.flip()


if __name__ == '__main__':
    # pitchdetection.initpitch()

    a = Process(target=pitchdetection.pitchdetection, args=(50, 5000, .0001))
    a.start()
    b = Process(target=GameLoop)
    b.start()

    a.join()
    b.join()
