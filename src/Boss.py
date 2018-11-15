import pygame
from math import *
from Laser import *
from Collider import *

debug = False

OFFSET_LASER_LEFT = pygame.math.Vector2(16, 48)
OFFSET_LASER_RIGHT = pygame.math.Vector2(83-16, 48)

class Boss(pygame.sprite.Sprite):
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)

        self.pos = pygame.math.Vector2(150 / 2, 16)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.image = pygame.image.load('./res/Images/Enemies/boss.png').convert_alpha()
        
        self.fire = [pygame.image.load('./res/Images/Effects/fire' + str(i) + '.png').convert_alpha() for i in range(15, 18)]
        self.anim = 0

        self.firecd = 0
        self.colliders = [
            Collider(self, 48, pygame.math.Vector2(38, 150)),
            Collider(self, 48, pygame.math.Vector2(257 - 38, 150)),
            Collider(self, 96, pygame.math.Vector2(257 / 2, 40))
        ]

        self.time = 0
        
    def update(self, dt, lasers) :
        self.time += 1
        
        # window border forcefield
        if (self.pos.x < 0) :
            self.acc.x = 0.1
        if (self.pos.x > 600 - 99) :
            self.acc.x = -0.1
        if (self.pos.y < 0) :
            self.acc.y = 0.1
        if (self.pos.y > 800 - 75) :
            self.acc.y = -0.1

        self.vel.x = sin(float(self.time) / 100.0)

        # limit player speed
        if self.vel.length() > 20 :
            self.vel.scale_to_length(20)

        self.pos += self.vel

        # check collisions
        for laser in lasers :
            collider = laser.collider
            for col in self.colliders :
                if col.collides(collider) : #collision
                    laser.destroy(lasers)
                    break

    def render(self, window) :
        window.blit(self.image, self.pos)
        if debug :
            for collider in self.colliders :
                collider.render(window)
        