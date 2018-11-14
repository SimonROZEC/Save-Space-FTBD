import pygame
from math import *
from Laser import *

OFFSET_LASER_LEFT = pygame.math.Vector2(16, 48)
OFFSET_LASER_RIGHT = pygame.math.Vector2(83-16, 48)

class Player(pygame.sprite.Sprite):
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        self.pos = pygame.math.Vector2(400, 300)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)

        self.image = pygame.image.load('./res/Images/playerShip1_green.png').convert_alpha()
        self.fire = [pygame.image.load('./res/Images/Effects/fire' + str(i) + '.png').convert_alpha() for i in range(15, 18)]
        self.anim = 0

        self.firecd = 0

    def update(self, keys, dt, lasers) :
        if keys['up'] :
            self.acc.y = -0.1
        elif keys['down'] :
            self.acc.y = 0.04
        else :
            self.acc.y = 0
            self.vel.y *= 0.90

        if keys['right']:
            self.acc.x = 0.1
        elif keys['left']:
            self.acc.x = -0.1
        else :
            self.acc.x = 0
            self.vel.x *= 0.90
        
        # create lasers
        if keys['fire'] and self.firecd <= 0:
            self.firecd = 8
            speed = 1
            if self.vel.y < 0 :
                speed += -self.vel.y * 0.05
            l1 = Laser(self, self.pos + OFFSET_LASER_LEFT, -pi*0.5, speed, 30)
            l2 = Laser(self, self.pos + OFFSET_LASER_RIGHT, -pi*0.5, speed, 30)
            lasers.append(l2)
            lasers.append(l1)
        self.firecd -= 1

        # window border forcefield
        if (self.pos.x < 0) :
            self.acc.x = 0.1
        if (self.pos.x > 600 - 99) :
            self.acc.x = -0.1
        if (self.pos.y < 0) :
            self.acc.y = 0.1
        if (self.pos.y > 800 - 75) :
            self.acc.y = -0.1

        self.vel += self.acc * dt

        # limit player speed
        if self.vel.length() > 20 :
            self.vel.scale_to_length(20)

        

        self.pos += self.vel

        

    def render(self, window) :
        offx = self.vel.x * 2 if self.vel.x > 0 else 0
        scalex = 99 - abs(2 * int(self.vel.x))
        window.blit(pygame.transform.scale(self.image, (scalex, 75)), self.pos+(offx, 0))
        
        if (self.acc.y < 0) :
            z = self.vel.x * 0.01
            window.blit(pygame.transform.rotozoom(self.fire[self.anim],0, 1+z), self.pos+(offx+18, 58))
            window.blit(pygame.transform.rotozoom(self.fire[self.anim], 0, 1-z), self.pos+(scalex+offx-18-14, 58))
        elif (self.acc.y > 0) :
            window.blit(pygame.transform.rotate(self.fire[self.anim], 180), self.pos+(offx + scalex/2-14/2, -31))
        
        if (self.acc.x > 0) :
            window.blit(pygame.transform.rotate(self.fire[self.anim], 270), self.pos+(offx + -34, 50-14/2))
        elif (self.acc.x < 0) :
            window.blit(pygame.transform.rotate(self.fire[self.anim], 90), self.pos+(scalex + 3, 50-14/2))

        self.anim = (self.anim + 1) % 3
        