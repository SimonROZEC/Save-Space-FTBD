#imports
import pygame
import requests
from queue import Queue

# API INFOS
URL = 'https://spaceshooter-api.herokuapp.com'
token = ''
name = ''

# init sdl
pygame.init()

from globaldefines import *
from IAplayer import *

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
from Enemy import *
from Asteroids import *
from Upgrade import *

##
# Return false if game was closed py player, true if player lost
#
def main() :   
    lasers = []
    enemies = []
    powerups = []
    upgrades = []
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
    ia = IAPlayer(player, powerups)
    PLAYER_IS_IA = False
    
    bossAndAddQueue.put(MiniBoss(lasers, powerups, player))
    bossAndAddQueue.put(Asteroids(lasers, powerups, player, enemies, upgrades))
    bossAndAddQueue.put(Boss(lasers, powerups, player, enemies))
    
    #bossAndAddQueue.put(Meteorite())
    #bossAndAddQueue.put(Boss(lasers, player))

    backgroundOffset = 0
    background = textures['BACKGROUND']

    running = True
    currentEnemy = bossAndAddQueue.get()

    ########### TIMING
    clear_segments()
    start_timer() # init du debut de la run

    ###########
    
    global token

    res = requests.post(URL+'/register_run', data=[])
    token = res.json()["token"]

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
        for enemy in enemies :
            enemy.update(dt, enemies, lasers, player)
        for laser in lasers :
            laser.update(dt, lasers)
        for powerup in powerups :
            powerup.update(dt, powerups)
        for upgrade in upgrades :
            upgrade.update(dt, upgrades)

        player.update(keys, dt, lasers, currentEnemy, powerups, enemies, upgrades)
        
        currentEnemy.update(dt)
        
        if(player.lifebar.lifes == 0) :
            running = False
            pass

        if(currentEnemy.lifeBar.life <= 0) :
            if(not bossAndAddQueue.empty()) :
                currentEnemy = bossAndAddQueue.get()
                print('One boss done')
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
        for upgrade in upgrades :
            upgrade.render(window)

        for enemy in enemies :
            enemy.render(window)

        player.render(window)
        currentEnemy.render(window)
        
        

        

        for laserParts in laser_particles :
            laserParts.render(window)
      
        #if(PLAYER_IS_IA) :
            #ia.debug(window)

        for powerupParts in powerup_particles :
            powerupParts.render(window)
        for upgradeParts in upgrade_particles :
            upgradeParts.render(window)

        #window.blit(timeT, )
        tm = str ( get_time()) # arrondi au centieme
        display_text(window, 'time : ' + tm, 4, 26, (255, 255, 255))
        offtm = 0
        for t in segments :
            offtm += 1
            if offtm < 10 :
                tms = str(t)
                alpha = 255 / (offtm)
                display_text_min_alpha(window, tms, 4, 48 + offtm * 12, (255, 200, 0), alpha)

        # frame buffer ?
        pygame.display.flip()

    ## TODO
    # faire une anim de fin de vie pour le joueur
    player.doDeath(window)
    return 'playerLost'

#
def startAnim(player) :
    global time
    global offx

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
        offx += - sin(time*0.01) * 0.2
        time += 1
        for x in xrange(-256, WIDTH, 256) :
            for y in xrange(-256, HEIGHT, 256) :
                window.blit(background, (x+offx, y+time%256))

        player.render(window)
        pygame.display.flip()

        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                return 'playerQuit'

        framecount += 1
    # should not be reachable
    return 'animEnded'

offx = 0

## Menu
def menu() :
    global time
    global offx
    background = textures['BACKGROUND']

    textTexture = createTextTexture('< Press space to start > ', './res/Fonts/kenvector_future_thin.ttf', 30, WHITE)

    player = Player(False)
    startCoord = pygame.math.Vector2(CENTERX, HEIGHT+100) - texturesOffsets['PLAYER_SHIP']
    player.pos = startCoord

    goalCoord = pygame.math.Vector2(CENTERX, CENTERY) - texturesOffsets['PLAYER_SHIP']

    ## anim de debut de menu
    while True :
        clock.tick(FPS)
        for x in xrange(-256, WIDTH, 256) :
            for y in xrange(-256, HEIGHT, 256) :
                window.blit(background, (x, y+time%256))

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
    ytime = time
    while True :
        clock.tick(FPS)
        
        # move back ground according to player poss
        offx += - sin(time*0.01) * 0.2
        time += 1

        for x in xrange(-256, WIDTH, 256) :
            for y in xrange(-256, HEIGHT, 256) :
                window.blit(background, (x+offx, y+ytime%256))
        
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                return
            elif event.type == pygame.KEYDOWN :
                if event.key == pygame.K_SPACE :
                    time = ytime 
                    if(startAnim(player) == 'playerQuit') :
                        return 'playerQuit'
                    return main()
        
        player.render(window)

        if(framecount < 30) :
            drawTexture(window, textTexture, (CENTERX - textTexture.get_width() * 0.5, HEIGHT*0.7))
        elif (framecount < 60) :
            pass
        else :
            framecount = 0
        pygame.display.flip()

        framecount += 1
        frameCounter += 1


fadeEnded = False
alpha = 255.0
alphasurf = pygame.Surface((WIDTH, HEIGHT))
alphasurf.fill((0, 0, 0))
alphasurf.set_alpha(alpha)
stringLabelFinal = "We need your name captain :"
stringLabel = ""
stringcursor = 0
canWrite = False
textLabel = createTextTexture(stringLabel, './res/Fonts/kenvector_future_thin.ttf', 25, WHITE)
nameTexture = createTextTexture('{  }', './res/Fonts/kenvector_future_thin.ttf', 30, GREEN)
background = textures['BACKGROUND']
time = 0
namemaxsize = 10
namesize = 0

yname = CENTERY
velyname = -10
nameSelected = False

while yname > -200 :
    clock.tick(FPS)

    if nameSelected :
      yname -= velyname
      velyname += 1.5

    for x in xrange(-256, WIDTH, 256) :
        for y in xrange(-256, HEIGHT, 256) :
            drawTexture(window, background, (x, y+time%256))

    if not canWrite :
      
      if stringcursor % 1 == 0 :
        stringLabel += stringLabelFinal[int(stringcursor)]
      stringcursor += 0.5
      textLabel = createTextTexture(stringLabel, './res/Fonts/kenvector_future_thin.ttf', 25, WHITE)
      if stringcursor == 27 :
        canWrite = True

    if not nameSelected :
      drawTexture(window, textLabel, (CENTERX - textLabel.get_width() / 2, CENTERY - 50))
    if canWrite :
      drawTexture(window, nameTexture, (CENTERX - nameTexture.get_width() / 2, yname))

    if not fadeEnded :
      alphasurf.set_alpha(alpha)
      alpha -= 2
      window.blit(alphasurf, (0, 0))
      if alpha <= 0 :
        fadeEnded = True

    pygame.display.flip()
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            quit()
        elif event.type == pygame.KEYDOWN :
            if event.key == pygame.K_RETURN:
                nameSelected = True
            elif event.key == pygame.K_BACKSPACE and canWrite :
                name = name[:-1]
                namesize = len(name)
                nameTexture = createTextTexture('{ ' + name + ' }', './res/Fonts/kenvector_future_thin.ttf', 30, GREEN)
            elif canWrite :
                if namesize < namemaxsize :
                  name += event.unicode
                  namesize += 1
                  nameTexture = createTextTexture('{ ' + name + ' }', './res/Fonts/kenvector_future_thin.ttf', 30, GREEN)
    time += 1

while True :
    retVal = menu()
    run_end = add_segment("end") # arrondi au centieme
    textTexture = None

    frameCount = 0
    background = textures['BACKGROUND']

    if(retVal == 'playerQuit') :
        quit()
    elif (retVal == 'playerWon') :
        req = URL+'/validate_run/' + token + '/' + name + '/' + str(run_end)
        res = requests.post(req, data=[]) # record time
        textTexture = createTextTexture('You WON !!', './res/Fonts/kenvector_future_thin.ttf', 30, WHITE)
    elif (retVal == 'playerLost') :
        textTexture = createTextTexture('You lost...', './res/Fonts/kenvector_future_thin.ttf', 30, WHITE)
    
    res = requests.get(URL+'/ranking', data=[]).json()

    coordTextStart = pygame.math.Vector2(-500, 16)
    coordMiddleText = pygame.math.Vector2(CENTERX - 75, 16)

    coordText = coordTextStart

    while True :
        clock.tick(FPS)

        for x in xrange(-256, WIDTH, 256) :
            for y in xrange(-256, HEIGHT, 256) :
                drawTexture(window, background, (x, y+time%256))
        
        if((coordText - coordMiddleText).length() >= 3) :
            coordText = coordText.lerp(coordMiddleText, 0.05)
        elif frameCount > FPS * 10:
            break

        drawTexture(window, textTexture, coordText)
        
        if retVal == 'playerWon' :
          display_text_med(window, 'you have defeated the boss in ' + str(run_end) + ' sec', coordText.x - CENTERX + 88, 64, GREEN)
        elif retVal == 'playerLost':
          display_text_med(window, 'the boss destroyed you in ' + str(run_end) + ' sec', coordText.x - CENTERX + 88, 64, RED)

        display_text(window, 'HIGHSCORES', coordText.x - 20, CENTERY - 100, WHITE)
        offy = CENTERY - 40
        for tm in res :
          if tm['time'] == str(run_end) :
            col = GREEN
          else :
            col = WHITE
          display_text_med(window, tm['name'] + ' : ' + tm['time'], coordText.x - 20, offy, col)
          offy += 32
        
        pygame.display.flip()

        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                quit()

        frameCount += 1

