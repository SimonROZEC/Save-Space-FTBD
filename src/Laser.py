import pygame
from math import *
from random import *

class Laser(pygame.sprite.Sprite):
    def __init__(self, owner, pos, dir, speed, lifetime = 60) :
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        precision = uniform(-0.1, 0.1)
        dir += precision
        self.angle = degrees(-dir) - 90
        self.vel = pygame.math.Vector2(speed * cos(dir), speed * sin(dir))

        self.frames = [pygame.image.load('./res/Images/Lasers/laserGreen' + str(i) + '.png').convert_alpha() for i in range(10, 14)]
        self.anim = 0
        
        self.maxlife = lifetime
        self.lifetime = lifetime

    def update(self, dt, lasers) :
        
        if self.lifetime <= 0 or self.pos.y < -13 :
            lasers.remove(self)

        self.lifetime -= 1

        if self.anim < 3 :
            self.anim += 0.25

        self.pos += self.vel * dt

    def render(self, window) :
        window.blit(pygame.transform.rotozoom(self.frames[int(self.anim)], self.angle, (float(self.lifetime)/float(self.maxlife))),self.pos)
        
