import random #random number generation
import sys #for exit
import pygame #to use pygame module
from pygame.locals import * #basic pygame imports


#Global variables for the game
FPS = 32 #frames per second
SCREENWIDTH =  289
SCREENHEIGHT = 511
SCREEN = pygame .display.set_mode((SCREENWIDTH,SCREENHEIGHT)) #To initialize a screen for display
GROUNDY = SCREENHEIGHT *  0.8 #80% of base image
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'gallery/sprites/bird.png'
BACKGROUND = 'gallery/sprites/background.jpg'
PIPE = 'gallery/sprites/pipe.png'

def welcomeScreen():
    """
    Shows welcome image to the screen
    """
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2) #To get the player in center
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT* 0.13)
    basex = 0
    while TRUE:
        for event in pygame.event.get():
            #If user clicks on cross button, close the game
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            #If the user presses up key or space, start the game for them

            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key== K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'],(0,0))
                SCREEN.blit(GAME_SPRITES['player'],(playerx,playery)) #From top left they will vary 
                SCREEN.blit(GAME_SPRITES['message'],(messagex,messagey))
                SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
                pygame.display.update() #Screen won't change unless any update is happened no matter how many blit function run
                FPSCLOCK.tick(FPS) #To control the frames of the game

def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0
    #Create two pipes for blitting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # my list of upper pipe
    upperPipes= [
        {'x': SCREENWIDTH+200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y': newPipe2[0]['y']},
    ]
    # my list if lower pipe
    lowerPipes= [
        {'x': SCREENWIDTH+200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y': newPipe2[1]['y']},
    ]

    pipeVelX = -4;

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8 #Velocity while flapping
    playerFlapped = False #It is true only when the bird is flapping

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0 : #If player is there in screen
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()


        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes) #If the player is crashed
        if crashTest:
            return

        #Recheck for score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width/2
            if pipeMidPos <= playerMidPos < pipeMidPos+4:
                score +=1
                print(f"Your score is {score}")
                GAME_SOUNDS['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY +=playerAccY
        if playerFlapped:
            playerFlapped= False
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight) #So the Player does not go to ground

        #Move pipes to the left
        for upperPipes, lowerPipes in zip(upperPipes,lowerPipes):
            upperPipes['x'] += pipeVelX
            lowerPipes['x'] += pipeVelX
        #Add a new pipe when a first pipe is about to cross the leftmost part of the screen
        if 0< upperPipes[0]['x']<5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])
    
        #if the pipe is out of the screen , remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes(0)

        #Lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'],(0, 0))
        for upperPipes, lowerPipes in zip(upperPipes,lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0],(upperPipes['x'],upperPipes['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1],(lowerPipes['x'],lowerPipes['y']))

        SCREEN.blit(GAME_SPRITES['base'],(basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx,playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width= GAME_SPRITES['numbers'][digit].get_width()
        xoffset = (SCREENWIDTH- width)/2
        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit],(xoffset, SCREENHEIGHT*0.12))
            xoffset +=  GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick= FPS



def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery > GROUNDY - 25 or playery< 0:
        GAME_SOUNDS['hit'].play()
        return True
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(palyery < pipeHeight+ pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
        GAME_SOUNDS['hit'].play
        return True
    for pipe in lowerPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if((palyery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
        GAME_SOUNDS['hit'].play
        return True
    
    return False


def getRandomPipe():
    """
    Generate positions for two pipes (one bottom straight and one top rotated)
    for blitting in the screen
    """
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.range(0,int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2 * offset))
    pipex = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipex, 'y': -y1}, #Upper Pipe
        {'x': pipey, 'y': y2}  #Lower Pipe

    ]
    return pipe







if __name__ == "__main__":
        #main function from where the game will start
        pygame.init() #initialize all pygame modules
        FPSCLOCK =  pygame.time.clock() #for controlling game FPS
        pygame.display.set_caption('Flappy Bird By Arihant')
        GAME_SPRITES['numbers'] = (
            pygame.image.load('gallery/sprites/0.png').convert_alpha(),  #convert_alpha will optimize image for game
            pygame.image.load('gallery/sprites/1.png').convert_alpha(), 
            pygame.image.load('gallery/sprites/2.png').convert_alpha(), 
            pygame.image.load('gallery/sprites/3.png').convert_alpha(), 
            pygame.image.load('gallery/sprites/4.png').convert_alpha(), 
            pygame.image.load('gallery/sprites/5.png').convert_alpha(), 
            pygame.image.load('gallery/sprites/6.png').convert_alpha(), 
            pygame.image.load('gallery/sprites/7.png').convert_alpha(), 
            pygame.image.load('gallery/sprites/8.png').convert_alpha(), 
            pygame.image.load('gallery/sprites/9.png').convert_alpha()
        )

        GAME_SPRITES['message'] = pygame.image.load('gallery/sprites/message.png').convert_alpha()
        GAME_SPRITES['base'] = pygame.image.load('gallery/sprites/base.png').convert_alpha()
        GAME_SPRITES['pipe'] = (
        
        pygame.transform.rotate(pygame.image.load( PIPE).convert_alpha(), 180),      #To rotate the pipe for top
        pygame.image.load('gallery/sprites/pipe.png').convert_alpha()
        )
        #GAME SOUNDS
        GAME_SOUNDS['die'] = pygame.mixer.sound('gallery/audio/die.wav')
        GAME_SOUNDS['hit'] = pygame.mixer.sound('gallery/audio/hit.wav')
        GAME_SOUNDS['point'] = pygame.mixer.sound('gallery/audio/point.wav')
        GAME_SOUNDS['swoosh'] = pygame.mixer.sound('gallery/audio/swoosh.wav')
        GAME_SOUNDS['wing'] = pygame.mixer.sound('gallery/audio/wing.wav')
        GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
        GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

        while TRUE :
            welcomeScreen() # Shows welcome screen to the user until he presses a button
            mainGame() #this is the main game function 
            






