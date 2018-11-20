import pygame
from globaldefines import *

from math import *
from random import *

from Collider import *
from Textures import *

debug = False

powerup_particles = []

class PowerupPicked(pygame.sprite.Sprite):
    def __init__(self, owner, pos) :
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.anim = 0
        self.frames = textures['PU_PARTICLE']
        
    def render(self, window) :
        
        self.anim += 0.25
        window.blit(self.frames[int(min(self.anim, 2))],self.pos-texturesOffsets['PU_PARTICLE'])

        if self.anim >= 3 :
            powerup_particles.remove(self)

class Powerup(pygame.sprite.Sprite):
    def __init__(self, pos, target, type) :
        pygame.sprite.Sprite.__init__(self)
        
        self.prepared = False
        self.velB = pygame.math.Vector2(0, 0.1)
        self.vel = self.velB
        self.acc = pygame.math.Vector2(0, 0)
        self.target = target
        self.pos = pygame.math.Vector2(pos[0], pos[1])
        # self.angle = degrees(-dir) - 90
        # self.vel = pygame.math.Vector2(speed * cos(dir), speed * sin(dir))
        self.type = type
        self.image = textures[type]

        self.collider = Collider(self, 12, pygame.math.Vector2(0, 0))
        self.scale = 1

    def update(self, dt, powerups) :
        if self.prepared :
            maxW = texturesOffsets['PU'][0]
            if self.pos.x < 0 + maxW  :
                self.acc.x = 0.1
            elif self.pos.x > WIDTH - maxW :
                self.acc.x = -0.1
            else :
                self.acc.x = 0
            self.vel.x *= 0.8
            self.vel += self.acc
            self.pos += self.vel * dt
        else :
            self.pos = target_point(self.pos, self.target, 0.2)
            if dist_to_point(self.pos, self.target) < 10 :
                self.prepared = True

    def render(self, window) :
        window.blit(self.image ,self.pos - texturesOffsets['PU'])
        if debug : 
            self.collider.render(window)

    def destroy(self, powerups) :
        powerup_particles.append(PowerupPicked(self, self.pos))
        powerups.remove(self)

PU_TYPES = ['PU_ENERGY', 'PU_HEALTH', 'PU_SHIELD']

def get_random_type() :
    return PU_TYPES[randint(0, 2)]