import pygame

try:
    xrange
except NameError:
    xrange = range

WIDTH = 600
HEIGHT = 800
FPS = 60

pygame.init()
clock = pygame.time.Clock()

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

from LoadImages import *

from Player import *
from Boss import *
from Laser import *

keys = {
    'up'   : False,
    'down' : False,
    'left' : False,
    'right': False,
    'fire' : False
}

background = images['BACKGROUND']

def main() :

    lasers = []

    p = Player()
    b = Boss(lasers)
    


    running = True
    offset = 0

    while running :
        dt = clock.tick(FPS)

        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                running = False
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

        offset += 2
        offx = - p.pos.x / 8
        offy = - p.pos.y / 8
        for x in xrange(-256, WIDTH, 256) :
            for y in xrange(-256, HEIGHT, 256) :
                window.blit(background, (x+offx, y+offset%256))

        for l in lasers :
            l.update(dt, lasers)
            l.render(window)

        p.update(keys, dt, lasers, b)
        p.render(window)
        
        b.update(dt)
        b.render(window)

        for li in laser_particles :
            li.render(window)

        pygame.display.flip()

main()