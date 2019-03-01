import sys, pygame
pygame.init()



#initialize game variables and constants
pygame.mouse.set_visible(False)
xit= False
gamestate = 0 # 0 = Main Menu, 2 = Game Screen, 3 = Pause Menu
#load walker frames
walk = []
for i in range(8): 
    walk.append(pygame.image.load("./placeholderwalking/Walk-3-" + str(i) + ".png"))
walkrect = walk[0].get_rect()

size = width, height = 640, 480
black = 0, 0, 0

screen = pygame.display.set_mode(size)

#helper functions and other definitions
buttons = pygame.sprite.RenderUpdates()

players = pygame.sprite.GroupSingle()

class player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, players)
        self.image = pygame.surface(walkrect)
        self.image.blit(walk[0],walkrect)
        self.rect = walkrect
        self.rect.x = 10

class button(pygame.sprite.Sprite):
    def __init__(self, text="", location, shape):
        pygame.sprite.Sprite.__init__(self,buttons)
        self.text = text
        self.image = pygame.Surface(shape)
        self.image.fill((240,240,240))
        self.rect = pygame.Surface.get_rect(self.image)
        self.rect.topleft = location
        self.state = 0 # 0 normal, 1 hover, 2 clicked
    
    def update(self, state = None, text = None):
        if not state == None:
            self.state == state
        if not text == None:
            self.text = text
        rgb = 240 - (state * 40)
        self.image.fill((rgb,rgb,rgb))
        

    def collidepoint(self,pos):
        '''
        mouseover detection
        '''
        return self.rect.collidepoint(pos)


def maininit():
    '''
    Initialize the main menu
    '''
           
    #Set button locations

    newrect = button("New Game",(220, 150), (200, 50))
    quitrect = button("Quit", (220, 280), (200, 50))


def mainmenu(click = False):
    ''' 
    looping mainmenu routine
    '''
    state = 1
    mpos = pygame.mouse.get_pos()

    if click: state = 2
    
    for button in buttons.sprites():
        if button.collidepoint(mpos):
            button.update(state=state)
    

def pausemenu(click = False, click_position = None):
    #looping pausemenu routine

def gameinit():
    #game initialization function
    player = pygame.sprite.Sprite(players)


def gameexit():
    #game end function

def gamescreen(click = False, click_position = None):
    #looping gamescreen processing

while 1:
    #initialize loop variables
    click = False
    #check events    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: xit = True
        if event.type == pygame.MOUSEBUTTONUP & event:
            cpos = pygame.mouse.get_pos()
            click = True
    if xit: break
