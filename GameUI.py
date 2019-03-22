import sys, pygame, pitchdetection, threading, random, math
pygame.init()

#game settings
size = width, height = 640, 480
lowfreq = 0
highfreq = 4000
volumethreshold = .005
movethreshold = 5
playerspeed = height//12

#Set up sprite groups
## Buttons
buttons = pygame.sprite.RenderUpdates()
quitbuttons = pygame.sprite.GroupSingle()
startbuttons = pygame.sprite.GroupSingle()

## Obstacles and Player
obstacles = pygame.sprite.RenderUpdates()
playerupd = pygame.sprite.RenderUpdates()
playeracc = pygame.sprite.GroupSingle()

## Text Sprites
textobjects = pygame.sprite.RenderUpdates()
menutitle = pygame.sprite.GroupSingle()
subheader = pygame.sprite.GroupSingle()
score = pygame.sprite.GroupSingle()

#### Debug text
#debuginfo = pygame.sprite.RenderUpdates()

# Set up fonts for text
pygame.font.init()
#debugfont = pygame.font.Font("./Assets/Consolas.ttf", height//40)
buttonfont = pygame.font.Font("./Assets/Verdana.ttf", height//24)
headerfont = pygame.font.Font("./Assets/Verdana.ttf", height//11)
subheaderfont = pygame.font.Font("./Assets/Verdana.ttf", height//20)
scorefont = pygame.font.Font("./Assets/Roboto-Black.ttf", height//20)

#initialize game constants
bheight = height//10
bwidth = width//3
centerx = width//2
black = 0, 0, 0
white = 255,255,255
lightblue = 200, 200, 255
darkblue = 0, 0, 70

#initialize state variables
curheight = 0
curpitch = 0
curheight = 0
curtarget = 0
calibstate = 0
xit= False
ticker = 0
gamestate = 0

'''
Gamestate Key
0 = Main Menu Loop
1 = Calibration Screen Loop
2 = Game Loop
3 = Pause Menu Loop
4 = Game Over Loop
'''

#set up game screen
screen = pygame.display.set_mode(size)
bgd = pygame.transform.smoothscale(pygame.image.load("./Assets/bground.png"), size)
screen.blit(bgd, (0, 0))
pygame.display.set_icon(pygame.image.load("./Assets/icon.png"))
pygame.display.set_caption("Cosmic Scale")
pygame.display.update()

#Set up obstacle sprite class
class obstacle(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__(obstacles)
        self.image = pygame.image.load("./Assets/astrd.png")
        self.rect = self.image.get_rect()
        self.rect.left = width + 5
        self.rect.centery = random.randint(24, height-24)
        self.radius = 22
        self.speed = speed

    def update(self):
        if self.rect.right < 0:
            self.kill()
        else:
            self.rect.x -= self.speed

#Set up player sprite class
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

#set up button sprite class
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


#set up multipurpose formatted text sprite class
class fancytext(pygame.sprite.Sprite):
    def __init__(self, center, titleType, text=""):
        super().__init__(textobjects)
        self.text = text
        self.type = titleType
        if titleType == "Header":
            self.font = headerfont
            self.add(menutitle)
        elif titleType == "Subheader":
            self.font = subheaderfont
            self.add(subheader)
        elif titleType == "Score":
            self.font = scorefont
            self.add(score)
        self.center = center
        self.update()

    def update(self, text=None):
        if text != None:
            self.text = text
        self.image = self.font.render(self.text, True, lightblue)
        self.rect = self.image.get_rect()
        if self.type == "Score":
            self.rect.bottomright = self.center
        else:
            self.rect.center = self.center

###set up debug text sprite class
##class debug_text(pygame.sprite.Sprite):
##    def __init__(self, location, text=""):
##        super().__init__(debuginfo)
##        self.text = text
##        self.update()
##
##    def update(self):
##        self.image = debugfont.render(self.text, True, white,black)
##        self.rect = self.image.get_rect()

'''
Runtime Helper Functions
'''
#screen redraw function
def drawscreen(redrawlist = []):
    ##debuginfo.clear(screen, bgd)
    ##debuginfo.update()
    textobjects.clear(screen, bgd)
    obstacles.clear(screen, bgd)
    redrawlist += obstacles.draw(screen)
    redrawlist += textobjects.draw(screen)
    ##redrawlist += debuginfo.draw(screen)
    redrawlist += buttons.draw(screen)
    redrawlist += playerupd.draw(screen)
    pygame.display.update(redrawlist)

#button adding function
def addbutton(group, text, ypos):
    brect = pygame.rect.Rect(0,0,bwidth,bheight)
    brect.center = (centerx,ypos)
    button(brect.topleft, brect.size, group, text)

#menu button adder
def menubuttons(starttext, quittext):
    addbutton(startbuttons, starttext, height//2)
    addbutton(quitbuttons, quittext, (height*7)//10)

#menu title adder
def menutitles(kind, headertext, subheadertext=None):
    if kind == "single":
        fancytext((centerx, height//4), "Header", headertext)
    else:
        fancytext((centerx, height//6), "Header", headertext)
        fancytext((centerx, height//3 ), "Subheader", subheadertext)
        
'''
Runtime Main Functions
'''
def menuinit(upper, lower, header, subheader = None):
    '''
    Universal Menu Initializer
    '''
    menubuttons(upper, lower)

    if subheader != None:
        menutitles("double", header, subheader)
    else:
        menutitles("single", header)


def menuloop(click, nex, prev, calib=False):

    if calib:
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

        subheader.sprite.update("Pitch: " + "{:.2f}".format(pitch) + " Hz")

    mpos = pygame.mouse.get_pos()
    #debug = ""
    newstate = gamestate

    for button in buttons.sprites():
        if button.collidepoint(mpos):
            #debug = button.text
            if click:
                button.update(state=2)
                if button in startbuttons:
                    if calib:
                        if calibstate == 1:
                            newstate = nex
                        else:
                            quitbuttons.sprite.update(text = "Redo Low Note")
                            calibstate = 1
                    else:
                        newstate = nex
                elif button in quitbuttons:
                    if calib:
                        if calibstate == 1:
                            quitbuttons.sprite.update(text = "Cancel")
                            calibstate = 0
                        else:
                            newstate = prev
                    else:
                        newstate = prev
            else:
                button.update(state=1)
        else:
            button.update(state=0)
    return newstate


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

    score.update("Score:" + str(ticker))

    #debug = ""
    newstate = 2
    if pygame.sprite.spritecollideany(playeracc.sprite,obstacles, pygame.sprite.collide_circle) != None:
        newstate = 4

    mpos = pygame.mouse.get_pos()
    if quitbuttons.sprite.collidepoint(mpos):
        #debug = quitbuttons.sprite.text
        if click:
            quitbuttons.sprite.update(state=2)
            newstate = 3
        else:
            quitbuttons.sprite.update(state=1)
    else:
        quitbuttons.sprite.update(state=0)

    readpitch = GetPitch()
    if readpitch is not "":
        curpitch = float(readpitch)

    clampedpitch = max(min(curpitch, highfreq), lowfreq)

    potarget = height - int(math.log(clampedpitch/lowfreq, 2) / math.log(highfreq/lowfreq, 2) * height)

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

    #debug += " Frequency settings: " + "{:.2f}".format(lowfreq) + " " + "{:.2f}".format(highfreq) + \
    #         " Current pitch: " + "{:.2f}".format(curpitch) + " Current target: " + str(curtarget)
    return newstate


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
menuinit("New Game", "Quit", "Cosmic Scale")
#dbinfo = debug_text((0,0))
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

    #debug = ""
    #check for newscreen initialization
    if newstate != gamestate:
        # clear buttons and old header
        textobjects.clear(screen, bgd)
        for header in textobjects:
            header.kill()
        buttons.clear(screen, bgd)
        for bttn in buttons.sprites():
            bttn.kill()

        if newstate == 0:
            menuinit("New Game", "Quit", "Cosmic Scale")
        elif newstate == 1:
            calibstate = 0
            menuinit("Confirm", "Cancel", "Sing or Hum a Low Note", "Pitch: Note_Goes_Here Hz")
        elif newstate == 2:
            if gamestate == 1:
                ticker = 0
                player()
            button((width-20, 5), (15, 15), quitbuttons, "|")
            fancytext((width-5, height-5), "Score", str(ticker))
        elif newstate == 3:
            menuinit("Continue Game", "Quit", "Game Paused")
        elif newstate == 4:
            obstacles.empty()
            playerupd.clear(screen, bgd)
            playeracc.sprite.kill()
            menuinit("Main Menu", "Quit", "Game Over", "Score: " + str(ticker))
        else: xit = True

    gamestate = newstate

    if gamestate == 0:
        newstate = menuloop(click, 1,-1)
    elif gamestate == 1:
        newstate = menuloop(click, 2, 0, True)
    elif gamestate == 2:
        newstate = gamescreen(click)
    elif gamestate == 3:
        newstate = menuloop(click, 2, 4)
    elif gamestate == 4:
        newstate = menuloop(click, 0, -1)

    #debug = str(pygame.mouse.get_pos()) + debug
    #dbinfo.text = debug
    drawscreen()

t1.run = False
t1.join()
pygame.display.quit()