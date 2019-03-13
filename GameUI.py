import sys, pygame
pygame.init()

#helper functions and other definitions
buttons = pygame.sprite.RenderUpdates()
quitbuttons = pygame.sprite.Group()
startbuttons = pygame.sprite.Group()

obstacles = pygame.sprite.RenderUpdates()
playergrp = pygame.sprite.GroupSingle()

ubound = -1000000000000000
lbound = 1000000000000000

fontobj = pygame.font.SysFont("Arial",11, 1)

size = width, height = 640, 480
black = 0, 0, 0

class player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, players)
        self.image = pygame.surface(walkrect)
        self.image.blit(walk[0],walkrect)
        self.rect = walkrect
        self.rect.x = 10

class button(pygame.sprite.Sprite):
    def __init__(self, text="", location, shape):
        pygame.sprite.Sprite.__init__(buttons)
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
        if not state == None:
            self.state == state
        if not text == None:
            self.text = text

        #refill background
        bg = 240 - (self.state * 40)
        self.image.fill((bg,bg,bg))
        #redraw text
        textimg = fontobj.render(self.text, True,black,(bg,bg,bg))
        textrect = textimg.get_rect()
        textrect.center = self.rect.center
        self.image.blit(textimg, textrect)
        

    def collidepoint(self,pos):
        '''
        mouseover detection
        '''
        return self.rect.collidepoint(pos)


def maininit():
    '''
    Initialize the main menu
    '''
    #state switchings
    gamestate = 0
           
    #Set button locations
    for bttn in buttons.sprites:
        bttn.kill()

    newrect = button("New Game",(220, 150), (200, 50))
    newrect.add(startbuttons)
    quitrect = button("Quit", (220, 280), (200, 50))
    quitrect.add(quitbuttons)

def mainmenu(click = False):
    ''' 
    Looping Main Menu routine
    '''
    #click handling
    mpos = pygame.mouse.get_pos()
    
    for button in buttons.sprites():
        if button.collidepoint(mpos):
            if click:
                button.update(state=2)
                if startbuttons in button.groups():
                    calibinit()
                else:
                    xit = True
            else:
                button.update(state=1)
        else:
            button.update(state=0)

def calibinit():
    '''
    Calibration Screen Initialization
    '''
    for bttn in buttons.sprites:
        bttn.kill()
    #state switching
    gamestate = 1

    #establish buttons
    newrect = button("Confirm",(220, 150), (200, 50))
    newrect.add(startbuttons)
    quitrect = button("Cancel", (220, 280), (200, 50))
    quitrect.add(quitbuttons)


def calibscreen(click = False):
    '''
    Looping Calibration routine
    '''
    
    #click handling:
    mpos = pygame.mouse.get_pos()
    
    for button in buttons.sprites():
        if button.collidepoint(mpos):
            if click:
                button.update(state=2)
                if startbuttons in button.groups():
                    gameinit()
                else:
                    maininit()
            else:
                button.update(state=1)
        else:
            button.update(state=0)

def gameinit():
    '''
    game initialization function
    '''
    for bttn in buttons.sprites:
        bttn.kill()

    #state switching
    gamestate = 2

    player = pygame.sprite.Sprite(playergrp)

def gameunpause():
    '''
    Pause menu cleanup and state switching function
    '''
    for bttn in buttons.sprites:
        bttn.kill()

    gamestate=2

def gameexit():
    '''
    Game End function
    '''
    for bttn in buttons.sprites:
        bttn.kill()

    #state switching
    gamestate = 0

def gamescreen(click = False):
    '''
    Looping Game Screen routine
    '''

def pauseinit():
    '''
    Pause Menu Initialization routine
    '''
    for bttn in buttons.sprites:
        bttn.kill()

    #state switching
    gamestate = 3

    #establish buttons
    newrect = button("Continue Game",(220, 150), (200, 50))
    newrect.add(startbuttons)
    quitrect = button("Quit", (220, 280), (200, 50))
    quitrect.add(quitbuttons)

def pausemenu(click = False):
    '''
    Looping Pause Menu routine
    '''
    
    for button in buttons.sprites():
        if button.collidepoint(mpos):
            if click:
                button.update(state=2)
                if startbuttons in button.groups():
                    gameunpause()
                else:
                    gameexit()
            else:
                button.update(state=1)
        else:
            button.update(state=0)

#initialize game variables and constants
pygame.mouse.set_visible(False)
xit= False
gamestate = 0 
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

while 1:
    #initialize loop variables
    click = False
    #check events    
    for event in pygame.event.get():
        #quit detect
        if event.type == pygame.QUIT: xit = True
        #click detect
        if event.type == pygame.MOUSEBUTTONUP & event:
            cpos = pygame.mouse.get_pos()
            click = True
    if xit: break

    if gamestate == 0:
        mainmenu(click)
    elif gamestate == 1:
        calibscreen(click)
    elif gamestate == 2:
        gamescreen(click)
    elif gamestate == 3:
        pausemenu(click)
