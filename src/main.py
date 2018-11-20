#imports
import pygame
from queue import Queue




# init sdl
pygame.init()

from globaldefines import *
from IAPlayer import *

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("-#- Space Shooter -#-")

clock = pygame.time.Clock()

# textures 
from Textures import *


# struct
keys = None

from Player import *
from MiniBoss import *
from Boss import *
from Laser import *
from Powerup import *

##
# Return false if game was closed py player, true if player lost
#
def main() :   
    lasers = []
    powerups = []
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

    # IA
    ia = IAPlayer(player)
    PLAYER_IS_IA = False

    
    bossAndAddQueue.put(MiniBoss(lasers, powerups, player))
    bossAndAddQueue.put(Boss(lasers, powerups, player))
    #bossAndAddQueue.put(Meteorite())
    #bossAndAddQueue.put(Boss(lasers, player))

    backgroundOffset = 0
    background = textures['BACKGROUND']

    running = True
    currentEnemy = bossAndAddQueue.get()

    ########### TIMING
    start_timer() # init du debut de la run

    ###########


    while running :
        # time since last frame, should be 1/FPS
        # or less of the game is lagging
        dt = clock.tick(FPS)

        #timeT = createTextTexture('Time : ' + str(pygame.time.get_ticks() * 0.001), './res/Fonts/kenvector_future_thin.ttf', 30, (255, 255, 255))

        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                return 'playerQuit'
            elif(not PLAYER_IS_IA) :
                
                if event.type == pygame.KEYDOWN :
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
                    elif event.key == pygame.K_RETURN :
                        add_segment("enter segment") # TODO REMOVE
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
                        
        if(PLAYER_IS_IA) : 
            keys =  {
                'up'   : False,
                'down' : False,
                'left' : False,
                'right': False,
                'fire' : False
            }             
            ia.processInput(currentEnemy, lasers, keys)

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
        for powerup in powerups :
            powerup.update(dt, powerups)

        player.update(keys, dt, lasers, currentEnemy, powerups)
        
        currentEnemy.update(dt)
        
        if(player.lifebar.lifes == 0) :
            running = False
            pass

        if(currentEnemy.lifeBar.life <= 0) :
            if(not bossAndAddQueue.empty()) :
                currentEnemy = bossAndAddQueue.get()
                ### segment time

                pass
            else :                
                return 'playerWon'
                ### final time 

        # blit order is important
        for laser in lasers :
            laser.render(window)
        for powerup in powerups :
            powerup.render(window)

        player.render(window)

        currentEnemy.render(window)

        for laserParts in laser_particles :
            laserParts.render(window)
      
        #if(PLAYER_IS_IA) :
            #ia.debug(window)

        for powerupParts in powerup_particles :
            powerupParts.render(window)

        #window.blit(timeT, )
        tm = str ( get_time())[:-1] # arrondi au centieme
        display_text(window, 'time : ' + tm, 4, 26, (255, 255, 255))
        offtm = 0
        for t in segments :
            
            offtm += 1
            if offtm < 10 :
                tms = str(t)[:-1]
                alpha = 255 / (offtm)
                display_text_min_alpha(window, tms, 4, 50 + offtm * 12, (255, 200, 0), alpha)
            
        
        # frame buffer ?
        pygame.display.flip()

    ## TODO
    # faire une anim de fin de vie pour le joueur
    player.doDeath(window)

    return 'playerLost'

#
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
            return 'animEnded'

        # move back ground according to player poss
        offx = - sin(framecount*0.01) * 30

        for x in xrange(-256, WIDTH, 256) :
            for y in xrange(-256, HEIGHT, 256) :
                window.blit(background, (x+offx, y+framecount%256))

        player.render(window)
        pygame.display.flip()

        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                return 'playerQuit'

        framecount += 1
    # should not be reachable
    return 'animEnded'

## Menu
def menu() :
    background = textures['BACKGROUND']

    textTexture = createTextTexture('Press space to start', './res/Fonts/kenvector_future_thin.ttf', 30, (0, 0, 0))

    player = Player(False)
    startCoord = pygame.math.Vector2(CENTERX, HEIGHT+100) - texturesOffsets['PLAYER_SHIP']
    player.pos = startCoord

    goalCoord = pygame.math.Vector2(CENTERX, CENTERY) - texturesOffsets['PLAYER_SHIP']

    ## anim de debut de menu
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
                return 'playerQuit'

        player.render(window)

        pygame.display.flip()

    #anim d'attente
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
                    if(startAnim(player) == 'playerQuit') :
                        return 'playerQuit'
                    return main()

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



while True :
    run_end = str ( get_time())[:-1] # arrondi au centieme

    retVal = menu()

    textTexture = None

    frameCount = 0
    background = textures['BACKGROUND']

    color = (200, 0, 0)

    if(retVal == 'playerQuit') :
        quit()
    elif (retVal == 'playerWon') :
        textTexture = createTextTexture('You WON !!', './res/Fonts/kenvector_future_thin.ttf', 30, (0, 0, 0))
        color = (0, 200, 0)
    elif (retVal == 'playerLost') :
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
        
        display_text(window, 'time : ' + run_end, coordText.x, coordText.y + 32, color)

        pygame.display.flip()

        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                quit()

        frameCount += 1

