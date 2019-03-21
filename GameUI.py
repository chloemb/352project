import sys, pygame, pitchdetection, threading, random, math
pygame.init()

#helper functions and other definitions
buttons = pygame.sprite.RenderUpdates()
quitbuttons = pygame.sprite.GroupSingle()
startbuttons = pygame.sprite.GroupSingle()

obstacles = pygame.sprite.RenderUpdates()
playerupd = pygame.sprite.RenderUpdates()
playeracc = pygame.sprite.GroupSingle()

menuobjects = pygame.sprite.RenderUpdates()
menutitle = pygame.sprite.GroupSingle()
menupitch = pygame.sprite.GroupSingle()

debuginfo = pygame.sprite.RenderUpdates()

size = width, height = 640, 480
bheight = height//10
bwidth = width//3
centerx = width//2
black = 0, 0, 0
white = 255,255,255
lightblue = 200, 200, 255
darkblue = 0, 0, 70

pygame.font.init()
debugfont = pygame.font.Font("./Assets/Consolas.ttf", height//40)
buttonfont = pygame.font.Font("./Assets/Verdana.ttf", height//24)
headerfont = pygame.font.Font("./Assets/Verdana.ttf", height//11)
subheaderfont = pygame.font.Font("./Assets/Verdana.ttf", height//20)

#initialize game variables and constants
curheight = 0
pygame.mouse.set_visible(True)
xit= False
gamestate = 0
lowfreq = 0
highfreq = 4000
volumethreshold = .001
curpitch = 0
curheight = 0
curtarget = 0
calibstate = 0

movethreshold = 5
playerspeed = 40

'''
0 = Main Menu Loop
1 = Calibration Screen Loop
2 = Game Loop
3 = Pause Menu Loop
4 = Game Over Loop
'''

screen = pygame.display.set_mode(size)
icon = pygame.image.load("./Assets/icon.png")
pygame.display.set_icon(icon)
bgd = pygame.transform.smoothscale(pygame.image.load("./Assets/bground.png"), size)
screen.blit(bgd, (0, 0))
pygame.display.update()
frames = pygame.time.Clock()
ticker = 0

class obstacle(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__(obstacles)
        self.image = pygame.image.load("./Assets/astrd.png")
        self.rect = self.image.get_rect()
        self.rect.left = width + 5
        self.rect.centery = random.randint(24, height-24)
        self.radius = 20
        self.speed = speed

    def update(self):
        if self.rect.right < 0:
            self.kill()
        else:
            self.rect.x -= self.speed

class menu_title(pygame.sprite.Sprite):
    def __init__(self, center, titleType, text=""):
        super().__init__(menuobjects)
        self.text = text
        if titleType == "Header":
            self.font = headerfont
            self.add(menutitle)
        elif titleType == "Subheader":
            self.font = subheaderfont
            self.add(menupitch)
        self.center = center
        self.update()

    def update(self, text=None):
        if text != None:
            self.text = text
        self.image = self.font.render(self.text, True, lightblue)
        self.rect = self.image.get_rect()
        self.rect.center = self.center


class debug_text(pygame.sprite.Sprite):
    def __init__(self, location, text=""):
        super().__init__(debuginfo)
        self.text = text
        self.update()

    def update(self):
        self.image = debugfont.render(self.text, True,(255,255,255),black)
        self.rect = self.image.get_rect()


class player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(playeracc,playerupd)
        self.image = pygame.image.load("./Assets/rocket.png")
        self.rect = self.image.get_rect()
        self.rect.x = 15
        self.rect.centery = height//2
        self.radius = 20

    def update(self):
        self.rect.centery = curheight

class button(pygame.sprite.Sprite):
    def __init__(self, location, shape, groups, text=""):
        super().__init__(buttons,groups)
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
        if state != None: self.state = state
        if text != None: self.text = text

        #refill background
        b = 240 - (self.state * 40)
        r = g = b-60
        rgb = (r,g,b)
        self.image.fill(rgb)
        #redraw text
        textimg = buttonfont.render(self.text, True,darkblue,rgb)
        textrect = textimg.get_rect()
        textrect.center = (self.rect.width//2,self.rect.height//2)
        self.image.blit(textimg, textrect)
        

    def collidepoint(self,pos):
        '''
        mouseover detection
        '''
        return self.rect.collidepoint(pos)


def drawscreen(redrawlist = []):
    debuginfo.clear(screen, bgd)
    debuginfo.update()
    menuobjects.clear(screen, bgd)
    obstacles.clear(screen, bgd)
    redrawlist += obstacles.draw(screen)
    redrawlist += menuobjects.draw(screen)
    redrawlist += debuginfo.draw(screen)
    redrawlist += buttons.draw(screen)
    redrawlist += playerupd.draw(screen)
    pygame.display.update(redrawlist)


def addbutton(group, text, ypos):
    brect = pygame.rect.Rect(0,0,bwidth,bheight)
    brect.center = (centerx,ypos)
    button(brect.topleft, brect.size, group, text)

def menubuttons(starttext, quittext):
    addbutton(startbuttons, starttext, height//2)
    addbutton(quitbuttons, quittext, (height*7)//10)

def menutitles(kind, headertext, subheadertext=None):
    if kind == "single":
        menu_title((centerx, height//4), "Header", headertext)
    else:
        menu_title((centerx, height//6), "Header", headertext)
        menu_title((centerx, height//3 ), "Subheader", subheadertext)
        

def maininit():
    '''
    Initialize the main menu
    '''
           
    #Set button locations
    for bttn in buttons.sprites():
        bttn.kill()

    menutitles("single", "Main Menu")
    menubuttons("New Game", "Quit")

def mainmenu(click):
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
    global calibstate
    calibstate = 0
    menutitles("double","Sing or Hum a Low Note", "Pitch: Note_Goes_Here Hz")
    menubuttons("Confirm", "Cancel")
    
def calibscreen(click):
    '''
    Looping Calibration routine
    '''

    # Calibration
    global calibstate
    pitch = "Note_Goes_Here"
    if calibstate is 0:
        menutitle.sprite.update("Sing or Hum a Low Note")
        CalibLow()
        pitch = lowfreq
    elif calibstate is 1:
        menutitle.sprite.update("Sing or Hum a High Note")
        CalibHigh()
        pitch = highfreq

    menupitch.sprite.update("Pitch: " + "{:.2f}".format(pitch) + " Hz")

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
                    if calibstate == 1:
                        newstate = 2
                    else:
                        quitbuttons.sprite.update(text = "Redo Low Note")
                        calibstate = 1
                elif button in quitbuttons:
                    if calibstate == 1:
                        quitbuttons.sprite.update(text = "Cancel")
                        calibstate = 0
                    else:
                        newstate = 0
            else:
                button.update(state=1)
        else:
            button.update(state=0)

    return debug, newstate

def CalibLow():
    global curpitch, lowfreq
    readpitch = GetPitch()
    if readpitch is not "":
        curpitch = float(readpitch)
    lowfreq = curpitch

def CalibHigh():
    global curpitch, highfreq
    readpitch = GetPitch()
    if readpitch is not "":
        curpitch = float(readpitch)
    highfreq = curpitch


def pausebutton():
    button((width-20, 5), (15, 15), quitbuttons, "|")

def gameinit():
    '''
    game initialization function
    '''
    global ticker
    ticker = 0
    pausebutton()
    player()

def gameunpause():
    '''
    Pause menu cleanup and state switching function
    '''
    pausebutton()

def gamescreen(click):
    '''
    Looping Game Screen routine
    '''
    global curpitch, curheight, curtarget, ticker

    speed = ticker//200 + 2
    obstacles.update()
    if not ticker % (100//speed):
        obstacle(speed)
    ticker += 1

    debug = ""
    newstate = 2
    if pygame.sprite.spritecollideany(playeracc.sprite,obstacles, pygame.sprite.collide_circle) != None:
        newstate = 4

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

    readpitch = GetPitch()
    if readpitch is not "":
        curpitch = float(readpitch)

    curpitch = max(min(curpitch, highfreq), lowfreq)

    potarget = height - int(math.log(curpitch/lowfreq, 2) / math.log(highfreq/lowfreq, 2) * height)

    if abs(potarget - curheight) > movethreshold:
        curtarget = potarget

    # Height to move the player object to
    if abs(curtarget - curheight) >= playerspeed:
        if curheight > curtarget:
            curheight -= playerspeed
        elif curheight < curtarget:
            curheight += playerspeed
    else:
        curheight = curtarget

    playerupd.clear(screen, bgd)
    playerupd.update()

    debug += " Frequency settings: " + "{:.2f}".format(lowfreq) + " " + "{:.2f}".format(highfreq) + \
             " Current pitch: " + "{:.2f}".format(curpitch) + " Current target: " + str(curtarget)
    return debug, newstate


def gameexit():
    '''
    Game End function
    '''
    obstacles.empty()
    playerupd.clear(screen, bgd)
    playeracc.sprite.kill()
    
    #state switching
    menutitles("double", "Game Over", "Score: " + str(ticker))
    menubuttons("Main Menu", "Quit")

def overscreen(click):
    '''
    Game Over Screen
    '''
    newstate = 4
    debug = ""
    
    mpos = pygame.mouse.get_pos()
    for button in buttons.sprites():
        if button.collidepoint(mpos):
            debug = button.text
            if click:
                button.update(state=2)
                if button in startbuttons:
                    newstate = 0
                elif button in quitbuttons:
                    newstate = -1
            else:
                button.update(state=1)
        else:
            button.update(state=0)
    return debug, newstate


def pauseinit():
    '''
    Pause Menu Initialization routine
    '''
    # establish buttons
    menutitles("single", "Game Paused")
    menubuttons("Continue Game", "Quit")

def pausemenu(click):
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
                    newstate = 4
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


#first time initialization
maininit()
dbinfo = debug_text((0,0))
newstate = 0

#game while loop
while not xit:
    #initialize loop variables
    click = False
    #check events
    for event in pygame.event.get():
        #quit detect
        if event.type == pygame.QUIT: xit = True
        #click detect
        if event.type == pygame.MOUSEBUTTONUP:
            click = True

    debug = ""
    if newstate != gamestate:
        # clear buttons and old header
        menuobjects.clear(screen, bgd)
        for header in menuobjects:
            header.kill()
        buttons.clear(screen, bgd)
        for bttn in buttons.sprites():
            bttn.kill()
        if newstate == 0:
            maininit()
        elif newstate == 1:
            calibinit()
        elif newstate == 2:
            if gamestate == 1:
                gameinit()
            if gamestate == 3:
                gameunpause()
        elif newstate == 3:
            pauseinit()
        elif newstate == 4:
            gameexit()
        else: xit = True

    gamestate = newstate

    if gamestate == 0:
        debug, newstate = mainmenu(click)
    elif gamestate == 1:
        debug, newstate = calibscreen(click)
    elif gamestate == 2:
        debug, newstate = gamescreen(click)
    elif gamestate == 3:
        debug, newstate = pausemenu(click)
    elif gamestate == 4:
        debug, newstate = overscreen(click)

    debug = str(pygame.mouse.get_pos()) + debug
    dbinfo.text = debug
    drawscreen()

t1.run = False
t1.join()
pygame.display.quit()