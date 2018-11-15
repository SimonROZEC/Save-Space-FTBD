import pygame
from Player import *

WIDTH = 400
HEIGHT = 800

pygame.init()

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

keys = {
    'up'   : False,
    'down' : False,
    'left' : False,
    'right': False,
    'fire' : False
}

background = pygame.image.load('../res/Images/Background/blue.png')

def main() :
    p = Player()
    
    running = True

    while running :
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
            elif event.type == pygame.KEYUP :
                if event.key == pygame.K_UP :
                    keys['up'] = False
                elif event.key == pygame.K_DOWN :
                    keys['down'] = False
                elif event.key == pygame.K_LEFT :
                    keys['left'] = False
                elif event.key == pygame.K_RIGHT :
                    keys['right'] = False


        for x in xrange(0, WIDTH, 256) :
            for y in xrange(0, HEIGHT, 256) :
                window.blit(background, (x, y))

        p.update(keys)
        p.render(window)
        pygame.display.flip()

main()