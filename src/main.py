#imports
import pygame
from queue import Queue

from globaldefines import *

# init sdl
pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("-#- Space Shooter -#-")

clock = pygame.time.Clock()

# textures 
from Textures import *

#strange aliases
try:
    xrange
except NameError:
    xrange = range

# struct
keys = None

from Player import *
from MiniBoss import *
from Laser import *


##
# Return false if game was closed py player, true if player lost
#
def main() :   
    lasers = []
    bossAndAddQueue = Queue()

    # struct
    keys = {
        'up'   : False,
        'down' : False,
        'left' : False,
        'right': False,
        'fire' : False
    }

    player = Player()

    bossAndAddQueue.put(MiniBoss(lasers, player))
    #bossAndAddQueue.put(Meteorite())
    #bossAndAddQueue.put(Boss(lasers, player))

    backgroundOffset = 0
    background = textures['BACKGROUND']

    running = True
    currentEnemy = bossAndAddQueue.get()

    while running :
        # time since last frame, should be 1/FPS
        # or less of the game is lagging
        dt = clock.tick(FPS)

        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                return False

            elif event.type == pygame.KEYDOWN :
                if event.key == pygame.K_UP :
                    keys['up'] = True
                elif event.key == pygame.K_DOWN :
                    keys['down'] = True
                elif event.key == pygame.K_LEFT :
                    keys['left'] = True
                elif event.key == pygame.K_RIGHT :
                    keys['right'] = True
                elif event.key == pygame.K_a :
                    keys['fire'] = True

            elif event.type == pygame.KEYUP :
                if event.key == pygame.K_UP :
                    keys['up'] = False
                elif event.key == pygame.K_DOWN :
                    keys['down'] = False
                elif event.key == pygame.K_LEFT :
                    keys['left'] = False
                elif event.key == pygame.K_RIGHT :
                    keys['right'] = False
                elif event.key == pygame.K_a :
                    keys['fire'] = False

        
        # move back ground according to player poss
        offx = - player.pos.x * 0.125
        offy = - player.pos.y * 0.125
        backgroundOffset += 3
        for x in xrange(-256, WIDTH, 256) :
            for y in xrange(-256, HEIGHT, 256) :
                window.blit(background, (x+offx, y+backgroundOffset%256))

        # for each laser check if should die
        for laser in lasers :
            laser.update(dt, lasers)

        player.update(keys, dt, lasers, currentEnemy)
        
        currentEnemy.update(dt)
        
        if(player.lifebar.lifes == 0) :
            running = False
            pass

        if(currentEnemy.lifeBar.life <= 0) :
            if(not bossAndAddQueue.empty()) :
                currentEnemy = bossAndAddQueue.get()
                pass
            else :
                print('you won !')
                return True
                #quit()

        # blit order is important
        for laser in lasers :
            laser.render(window)
        
        player.render(window)

        currentEnemy.render(window)

        for laserParts in laser_particles :
            laserParts.render(window)
      
        # frame buffer ?
        pygame.display.flip()
    return True


def startAnim(player) :
    coordsBack = pygame.math.Vector2(CENTERX, CENTERY + 100) - texturesOffsets['PLAYER_SHIP']
    coordsEnd = pygame.math.Vector2(CENTERX, - 1000) - texturesOffsets['PLAYER_SHIP']
    background = textures['BACKGROUND']

    framecount = 0
    currentCoord = coordsBack

    while True :
        clock.tick(FPS)

        if not ((currentCoord - player.pos).length() < 10) :
            player.pos = player.pos.lerp(currentCoord, 0.05)
        else :
            currentCoord = coordsEnd

        if((coordsEnd - player.pos).length() < 10) :
            return True

        # move back ground according to player poss
        offx = - sin(framecount*0.01) * 30

        for x in xrange(-256, WIDTH, 256) :
            for y in xrange(-256, HEIGHT, 256) :
                window.blit(background, (x+offx, y+framecount%256))

        player.render(window)
        pygame.display.flip()

        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                return False

        framecount += 1
    return True

## Menu
def menu() :
    background = textures['BACKGROUND']

    textTexture = createTextTexture('Press space to start', './res/Fonts/kenvector_future_thin.ttf', 30, (0, 0, 0))

    player = Player(False)
    startCoord = pygame.math.Vector2(CENTERX, HEIGHT+100) - texturesOffsets['PLAYER_SHIP']
    player.pos = startCoord

    goalCoord = pygame.math.Vector2(CENTERX, CENTERY) - texturesOffsets['PLAYER_SHIP']

    while True :
        clock.tick(FPS)
         
        for x in xrange(-256, WIDTH, 256) :
            for y in xrange(-256, HEIGHT, 256) :
                window.blit(background, (x, y))

        if not ((goalCoord - player.pos).length() < 10) :
            player.pos = player.pos.lerp(goalCoord, 0.05)
        else :
            break       

        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                return

        player.render(window)

        pygame.display.flip()

    framecount = 0
    frameCounter = 0
    while True :
        clock.tick(FPS)
        
        # move back ground according to player poss
        offx = - sin(frameCounter*0.01) * 30

        for x in xrange(-256, WIDTH, 256) :
            for y in xrange(-256, HEIGHT, 256) :
                window.blit(background, (x+offx, y+frameCounter%256))

        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                return
            elif event.type == pygame.KEYDOWN :
                if event.key == pygame.K_SPACE :   
                    if(not startAnim(player)) :
                        return False

                    if (main()) :
                        return True 
                    else :
                        return False

        player.render(window)

        if(framecount < 30) :
            drawTexture(window, textTexture, (WIDTH*0.5-180, HEIGHT*0.7))
        elif (framecount < 60) :
            pass
        else :
            framecount = 0

        pygame.display.flip()

        framecount += 1
        frameCounter += 1

while menu() :
    frameCount = 0

    background = textures['BACKGROUND']
    textTexture = createTextTexture('You lost', './res/Fonts/kenvector_future_thin.ttf', 30, (0, 0, 0))

    coordTextStart = pygame.math.Vector2(-500, CENTERY)
    coordMiddleText = pygame.math.Vector2(CENTERX - 75, CENTERY)

    coordText = coordTextStart

    while True :
        clock.tick(FPS)

        for x in xrange(-256, WIDTH, 256) :
            for y in xrange(-256, HEIGHT, 256) :
                drawTexture(window, background, (x, y))
        
        if((coordText - coordMiddleText).length() >= 3) :
            coordText = coordText.lerp(coordMiddleText, 0.05)
        else :
            break

        drawTexture(window, textTexture, coordText)
        pygame.display.flip()

        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                quit()

        frameCount += 1
