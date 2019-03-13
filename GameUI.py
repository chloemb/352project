import sys, pygame, pitchdetection, threading
pygame.init()

#helper functions and other definitions
buttons = pygame.sprite.RenderUpdates()
quitbuttons = pygame.sprite.GroupSingle()
startbuttons = pygame.sprite.GroupSingle()

obstacles = pygame.sprite.RenderUpdates()
playergrp = pygame.sprite.GroupSingle()

debuginfo = pygame.sprite.RenderUpdates()

ubound = -1000000000000000
lbound = 1000000000000000

fontobj = pygame.font.SysFont("Arial",11, 1)
pygame.font.init()
myfont = pygame.font.Font("Assets/JosefinSans-Regular.ttf", 30)

size = width, height = 640, 480
black = 0, 0, 0
white = 255,255,255

#initialize game variables and constants
pygame.mouse.set_visible(True)
xit= False
gamestate = 0
lowfreq = 0
highfreq = 3000
volumethreshold = .001
curpitch = 0
calibstate = 0

'''
0 = Main Menu Loop
1 = Calibration Screen Loop
2 = Game Loop
3 = Pause Menu Loop
'''
#load walker frames
walk = []
for i in range(8): 
    walk.append(pygame.image.load("./placeholderwalking/Walk-3-" + str(i) + ".png"))
walkrect = walk[0].get_rect()

screen = pygame.display.set_mode(size)
bgd = pygame.Surface(size)

class debug_text(pygame.sprite.Sprite):
    def __init__(self, location, text=""):
        super().__init__(debuginfo)
        self.text = text
        self.image = fontobj.render(self.text, True,(255,255,255),black)
        self.rect = self.image.get_rect()

    def update(self):
        self.image = fontobj.render(self.text, True,(255,255,255),black)
        self.rect = self.image.get_rect()

class player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(players)
        self.image = pygame.surface(walkrect)
        self.image.blit(walk[0],walkrect)
        self.rect = walkrect
        self.rect.x = 10

class button(pygame.sprite.Sprite):
    def __init__(self, location, shape, text=""):
        super().__init__(buttons)
        #set initial state
        self.state = 0 # 0 normal, 1 hover, 2 clicked
        self.text = text
        #create image canvas and fill image with background color
        self.image = pygame.Surface(shape)
        #get rect for button and set location of button
        self.rect = pygame.Surface.get_rect(self.image)
        self.rect.topleft = location
        #write text to the button
        self.update()

    def update(self, state = None, text = None):
        '''
        Appearance updating helper function, used for updates and for initialization
        '''
        #update state variables
        if state != None:
            self.state = state
        if text != None:
            self.text = text

        #refill background
        bg = 240 - (self.state * 40)
        self.image.fill((bg,bg,bg))
        #redraw text
        textimg = fontobj.render(self.text, True,black,(bg,bg,bg))
        textrect = textimg.get_rect()
 
        textrect.center = (self.rect.width//2,self.rect.height//2)
        self.image.blit(textimg, textrect)
        

    def collidepoint(self,pos):
        '''
        mouseover detection
        '''
        return self.rect.collidepoint(pos)

def drawscreen(redrawlist = []):
    
    debuginfo.clear(screen,bgd)
    debuginfo.update()
    redrawlist = redrawlist + debuginfo.draw(screen)
    redrawlist = redrawlist + buttons.draw(screen)
    pygame.display.update(redrawlist)

def maininit():
    '''
    Initialize the main menu
    '''
           
    #Set button locations
    for bttn in buttons.sprites():
        bttn.kill()

    newrect = button((220, 150), (200, 50), "New Game")
    newrect.add(startbuttons)
    quitrect = button((220, 280), (200, 50), "Quit")
    quitrect.add(quitbuttons)

def mainmenu(click = False):
    ''' 
    Looping Main Menu routine
    '''
    #click handling
    mpos = pygame.mouse.get_pos()
    debug = ""
    newstate = 0
    for button in buttons.sprites():
        if button.collidepoint(mpos):
            debug = button.text
            if click:
                button.update(state=2)
                if button in startbuttons:
                    newstate = 1
                elif button in quitbuttons:
                    newstate = -1
            else:
                button.update(state=1)
        else:
            button.update(state=0)

    return debug, newstate

def calibinit():
    '''
    Calibration Screen Initialization
    '''
    #establish buttons
    newrect = button((220, 150), (200, 50), "Confirm Low Note")
    newrect.add(startbuttons)
    quitrect = button((220, 280), (200, 50), "Cancel")
    quitrect.add(quitbuttons)
    
def calibscreen(click, calib):
    '''
    Looping Calibration routine
    '''
    global calibstate

    #click handling:
    mpos = pygame.mouse.get_pos()
    debug = ""
    newstate = 1
    for button in buttons.sprites():
        if button.collidepoint(mpos):
            debug = button.text
            if click:
                button.update(state=2)
                if button in startbuttons:
                    if calib[0]:
                        newstate = 2
                        calib = (True, True)
                    else:
                        button.update(text="Confirm High Note")
                        quitbuttons.sprite.update(text = "Redo Low Note")
                        print("switching calibstate to 1")
                        calibstate = 1
                        calib = (True,False)
                elif button in quitbuttons:
                    if calib[0]:
                        startbuttons.sprite.update(text="Confirm Low Note")
                        quitbuttons.sprite.update(text = "Cancel")
                        print("switching calibstate to 0")
                        calibstate = 0
                        calib = (False,False)
                    else:
                        newstate = 0
            else:
                button.update(state=1)
        else:
            button.update(state=0)

    '''
    Calibration prompts
    '''
    
    if calibstate is 0:
        CalibLow()
    else:
        CalibHigh()

    return debug, newstate, calib

def CalibLow():
    global curpitch, lowfreq
    topmargin = 10

    readpitch = GetPitch()
    if readpitch is not "":
        curpitch = float(readpitch)
    lowfreq = curpitch

    screen.fill(black)
    textsurface = myfont.render('Sing or hum a low note', False, white)
    screen.blit(textsurface, (width / 2 - textsurface.get_width() / 2, topmargin))
    frequency = myfont.render("{:.2f}".format(curpitch), False, white)
    screen.blit(frequency, (width / 2 - frequency.get_width() / 2, topmargin +  textsurface.get_height()))
    pygame.display.flip()

def CalibHigh():
    global curpitch, highfreq
    topmargin = 10

    readpitch = GetPitch()
    if readpitch is not "":
        curpitch = float(readpitch)
    highfreq = curpitch

    screen.fill(black)
    textsurface = myfont.render('Sing or hum a high note', False, white)
    screen.blit(textsurface, (width / 2 - textsurface.get_width() / 2, topmargin))
    frequency = myfont.render("{:.2f}".format(curpitch), False, white)
    screen.blit(frequency, (width / 2 - frequency.get_width() / 2, topmargin + textsurface.get_height()))
    pygame.display.flip()
    
def gameinit():
    '''
    game initialization function
    '''
    screen.fill(black)
    pauserect = button((625,0), (15, 15), "II")
    pauserect.add(quitbuttons)
    player = pygame.sprite.Sprite(playergrp)

def gameunpause():
    '''
    Pause menu cleanup and state switching function
    '''
    pauserect = button((625,0), (15, 15), "II")
    pauserect.add(quitbuttons)

def gameexit():
    '''
    Game End function
    '''

    playergrp.sprite.kill
    #state switching

def gamescreen(click = False):
    '''
    Looping Game Screen routine
    '''
    debug = ""
    newstate = 2
    mpos = pygame.mouse.get_pos()
    for button in buttons.sprites():
        if button.collidepoint(mpos):
            debug = button.text
            if click:
                button.update(state=2)
                if button in quitbuttons:
                    newstate = 3
            else:
                button.update(state=1)
        else:
            button.update(state=0)

    debug += " Frequency settings: " + str(lowfreq) + " " + str(highfreq)

    return debug, newstate

def pauseinit():
    '''
    Pause Menu Initialization routine
    '''
    #establish buttons
    newrect = button((220, 150), (200, 50), "Continue Game")
    newrect.add(startbuttons)
    quitrect = button((220, 280), (200, 50), "Quit")
    quitrect.add(quitbuttons)

def pausemenu(click = False):
    '''
    Looping Pause Menu routine
    '''
    newstate = 3
    debug = ""
    
    mpos = pygame.mouse.get_pos()
    for button in buttons.sprites():
        if button.collidepoint(mpos):
            debug = button.text
            if click:
                button.update(state=2)
                if button in startbuttons:
                    newstate = 2
                elif button in quitbuttons:
                    newstate = 0
            else:
                button.update(state=1)
        else:
            button.update(state=0)
    return debug, newstate

def GetPitch():
    # read the pitch file
    pitchfile = open("pitch.txt", "r")
    readpitch = pitchfile.readline()
    pitchfile.close()
    return readpitch


if __name__ == '__main__':
    t1 = threading.Thread(target=pitchdetection.pitchdetection, args=[lowfreq, highfreq, volumethreshold])
    t1.start()

# def GameLoop():

#first time initialization
maininit()
dbinfo = debug_text((0,0))
calib = (False, False)
#game while loop
newstate = 0
while 1:
    #initialize loop variables
    click = False
    #check events
    for event in pygame.event.get():
        #quit detect
        if event.type == pygame.QUIT: xit = True
        #click detect
        if event.type == pygame.MOUSEBUTTONUP:
            click = True
    if xit: break

    debug = ""
    if newstate != gamestate:
        #clear buttons
        buttons.clear(screen,bgd)
        for bttn in buttons.sprites():
            bttn.kill()
        if newstate == 0:
            maininit()
        elif newstate == 1:
            calib = (False, False)
            calibinit()
        elif newstate == 2:
            if gamestate == 1:
                gameinit()
            if gamestate == 3:
                gameunpause()
        elif newstate == 3:
            pauseinit()
        else: break

    gamestate = newstate


    if gamestate == 0:
        debug, newstate = mainmenu(click)
    elif gamestate == 1:
        debug, newstate, calib = calibscreen(click, calib)
    elif gamestate == 2:
        debug, newstate = gamescreen(click)
    elif gamestate == 3:
        debug, newstate = pausemenu(click)

    debug = str(pygame.mouse.get_pos()) + debug
    dbinfo.text = debug
    drawscreen()
