import pygame
from math import *
from random import *

from Collider import *

from LoadImages import *

debug = False

laser_particles = []

class LaserImpact(pygame.sprite.Sprite):
    def __init__(self, owner, pos, lifetime = 30) :
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        if owner.owner.type == 'PLAYER' :
            self.frames = images['LASER_PLAYER_EXPLOSION']
        else :
            self.frames = images['LASER_ENEMY_EXPLOSION']
        self.anim = 0
        r = randint(10, 30)
        self.maxlife = r
        self.lifetime = self.maxlife

        self.scale = uniform(0.1, 0.2 + self.lifetime/(owner.maxlife + 1))

    def render(self, window) :
        
        self.anim += 0.25
        self.anim = self.anim % len(self.frames)

        self.lifetime -= 1
        window.blit(pygame.transform.rotozoom(self.frames[int(self.anim)], 0, (float(self.lifetime)/float(self.maxlife) + self.scale)),self.pos-(19*self.scale, 19*self.scale))


class Laser(pygame.sprite.Sprite):
    def __init__(self, owner, pos, dir, speed, lifetime = 60) :
        pygame.sprite.Sprite.__init__(self)
        
        self.owner = owner
        self.pos = pos
        precision = uniform(-0.05, 0.05)
        dir += precision
        self.angle = degrees(-dir) - 90
        self.vel = pygame.math.Vector2(speed * cos(dir), speed * sin(dir))
        if owner.type == 'PLAYER' :
            self.frames = images['LASER_PLAYER']
        else :
            self.frames = images['LASER_ENEMY']
        
        self.anim = 0
        
        r = randint(0, 15)
        self.maxlife = lifetime + r
        self.lifetime = self.maxlife

        self.collider = Collider(self, 4, pygame.math.Vector2(4, 4))

    def update(self, dt, lasers) :
        
        if self.lifetime <= 0 or self.pos.y < -13 or self.pos.y > 813:
            lasers.remove(self)

        self.lifetime -= 1

        if self.anim < 3 :
            self.anim += 0.25

        self.pos += self.vel * dt

    def render(self, window) :
        window.blit(pygame.transform.rotozoom(self.frames[int(self.anim)], self.angle, (float(self.lifetime)/float(self.maxlife))),self.pos)
        if debug : 
            self.collider.render(window)

    def destroy(self, lasers) :
            laser_particles.append(LaserImpact(self, self.pos, self.lifetime + 1))
            lasers.remove(self)
