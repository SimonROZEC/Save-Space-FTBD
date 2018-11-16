import pygame
from globaldefines import *

from math import *
from random import *

from Collider import *
from Textures import *

debug = False

class Powerup(pygame.sprite.Sprite):
    def __init__(self, pos, dir, speed, type) :
        pygame.sprite.Sprite.__init__(self)
        
        self.pos = pygame.math.Vector2(pos[0], pos[1])
        self.angle = degrees(-dir) - 90
        self.vel = pygame.math.Vector2(speed * cos(dir), speed * sin(dir))
        self.type = type
        self.image = textures[type]

        self.collider = Collider(self, 12, pygame.math.Vector2(0, 0))
        self.scale = 1

    def update(self, dt, powerups) :
        self.pos += self.vel * dt

    def render(self, window) :
        window.blit(self.image ,self.pos - texturesOffsets['PU'])
        if debug : 
            self.collider.render(window)

    def destroy(self, powerups) :
            powerups.remove(self)
