import sys, pygame
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

ubound = -1000000000000000
lbound = 1000000000000000

debugfont = pygame.font.SysFont("Consolas", 12, 1)
buttonfont = pygame.font.SysFont("Arial", 24, 1)
headerfont = pygame.font.SysFont("Verdana",48, 1)
subheaderfont = pygame.font.SysFont("Verdana",24, 1)

size = width, height = 640, 480
black = 0, 0, 0
white = 255, 255, 255
#initialize game variables and constants
curheight = 0
pygame.mouse.set_visible(True)
xit= False
gamestate = 0 
'''
0 = Main Menu Loop
1 = Calibration Screen Loop
2 = Game Loop
3 = Pause Menu Loop
'''

screen = pygame.display.set_mode(size)
bgd = pygame.image.load("./Assets/bground.png")

screen.blit(bgd, (0,0))
pygame.display.update()

class menu_title(pygame.sprite.Sprite):
    def __init__(self, center, titleType, text=""):
        super().__init__(menuobjects)
        self.text = text
        if titleType == "Header":
            self.font = headerfont
        elif titleType == "Subheader":
            self.font = subheaderfont
        self.center = center
        self.update()

    def update(self, text = None):
        if text != None:
            self.text = text
        self.image = self.font.render(self.text, True, white)
        self.rect = self.image.get_rect()
        self.rect.center = self.center

class debug_text(pygame.sprite.Sprite):
    def __init__(self, location, text=""):
        super().__init__(debuginfo)
        self.text = text
        self.loca = location
        self.update()

    def update(self):
        self.image = debugfont.render(self.text, True, white)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.loca

class player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(playeracc,playerupd)
        self.image = pygame.image.load("./Assets/rocket.png")
        self.rect = self.image.get_rect()
        self.rect.x = 15
        self.rect.centery = 240

    def update(self):
        self.rect.centery = curheight[1]

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
        textimg = buttonfont.render(self.text, True,black,(bg,bg,bg))
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
    menuobjects.clear(screen,bgd)
    redrawlist = redrawlist + menuobjects.draw(screen)
    redrawlist = redrawlist + debuginfo.draw(screen)
    redrawlist = redrawlist + buttons.draw(screen)
    redrawlist = redrawlist + playerupd.draw(screen)
    pygame.display.update(redrawlist)

def maininit():
    '''
    Initialize the main menu
    '''
           
    #Set button locations
    for bttn in buttons.sprites():
        bttn.kill()

    mainheader = menu_title((320, 100),"Header","Main Menu")
    mainheader.add(menutitle)
    newrect = button((220, 200), (200, 50), "New Game")
    newrect.add(startbuttons)
    quitrect = button((220, 300), (200, 50), "Quit")
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
    mainheader = menu_title((320, 80),"Header","Calibrate High Note")
    mainheader.add(menutitle)
    pitchheader = menu_title((320, 150), "Subheader", "Pitch: Note_Goes_Here Hz")
    pitchheader.add(menupitch)
    newrect = button((220, 200), (200, 50), "Confirm")
    newrect.add(startbuttons)
    quitrect = button((220, 300), (200, 50), "Cancel")
    quitrect.add(quitbuttons)
    
def calibscreen(click, calib):
    '''
    Looping Calibration routine
    '''

    #insert real time instantaneous pitch detection code here
    #
    #
    pitch = "Note_Goes_Here"

    menupitch.sprite.update("Pitch: " + pitch + " Hz")
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
                        menutitle.sprite.update("Confirm Low Note")
                        quitbuttons.sprite.update(text = "Redo High Note")
                        calib = (True,False)
                elif button in quitbuttons:
                    if calib[0]:
                        menutitle.sprite.update("Confirm High Note")
                        quitbuttons.sprite.update(text = "Cancel")
                        calib = (False,False)
                    else:
                        newstate = 0
            else:
                button.update(state=1)
        else:
            button.update(state=0)

    return debug, newstate, calib
    
def gameinit():
    '''
    game initialization function
    '''

    pauserect = button((620,5), (15, 15), "I")
    pauserect.add(quitbuttons)
    p = player()

def gameunpause():
    '''
    Pause menu cleanup and state switching function
    '''
    pauserect = button((620,5), (15, 15), "I")
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
    playerupd.clear(screen,bgd)
    playerupd.update()

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

    return debug, newstate

def pauseinit():
    '''
    Pause Menu Initialization routine
    '''
    #establish buttons
    mainheader = menu_title((320, 100),"Header","Game Paused")
    mainheader.add(menutitle)
    newrect = button((220, 200), (200, 50), "Continue Game")
    newrect.add(startbuttons)
    quitrect = button((220, 300), (200, 50), "Quit")
    quitrect.add(quitbuttons)

def pausemenu(click = False):
    '''
    Looping Pause Menu routine
    '''
    newstate = 3
    debug = ""
    
    mpos = pygame.mouse.get_pos().x
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
        #clear buttons and old header
        menuobjects.clear(screen, bgd)
        for header in menuobjects:
            header.kill()
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
    curheight = pygame.mouse.get_pos()

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