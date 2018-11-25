import pygame
from globaldefines import *

from math import *
from random import *

from Collider import *
from Textures import *

debug = False

laser_particles = []

class LaserImpact(pygame.sprite.Sprite):
    def __init__(self, owner, pos, lifetime = 30) :
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        if owner.owner.type == 'PLAYER' :
            self.frames = textures['LASER_PLAYER_EXPLOSION']
        else :
            self.frames = textures['LASER_ENEMY_EXPLOSION']
        self.anim = 0
        r = randint(5, 15)
        self.maxlife = r
        self.lifetime = self.maxlife

        self.scale = uniform(0.1, 0.2 + self.lifetime/(owner.maxlife + 1))

    def render(self, window) :
        
        self.anim += 0.25
        self.anim = self.anim % len(self.frames)

        self.lifetime -= 1
        scale = float(self.lifetime)/float(self.maxlife) + self.scale
        window.blit(pygame.transform.rotozoom(self.frames[int(self.anim)], 0, scale),self.pos-(24*scale, 24*scale))

        if self.lifetime <= 0 :
            laser_particles.remove(self)


class Laser(pygame.sprite.Sprite):
    def __init__(self, owner, pos, dir, speed, lifetime = 60, scale = 1, precision = 0.05) :
        pygame.sprite.Sprite.__init__(self)
        
        self.owner = owner
        self.pos = pos
        precision = uniform(-precision, precision)
        dir += precision
        self.angle = degrees(-dir) - 90
        self.vel = pygame.math.Vector2(speed * cos(dir), speed * sin(dir))
        if owner.type == 'PLAYER' :
            self.frames = textures['LASER_PLAYER']
        else :
            self.frames = textures['LASER_ENEMY']
        
        self.anim = 0
        self.scalefactor = scale
        self.scale = scale

        r = randint(0, 15)
        self.maxlife = lifetime + r
        self.lifetime = self.maxlife

        self.collider = Collider(self, 4, pygame.math.Vector2(0, 0))

    def update(self, dt, lasers) :
        
        if self.lifetime <= 0 or self.pos.y < -500 or self.pos.y > HEIGHT+500 or self.pos.x < -300 or self.pos.x > WIDTH + 300:
            lasers.remove(self)

        self.lifetime -= 1

        if self.anim < len(self.frames) - 1 :
            self.anim += 1

        self.pos += self.vel * dt

    def render(self, window) :
        self.scale = (float(self.lifetime)/float(self.maxlife)) * self.scalefactor
        sf = pygame.transform.rotozoom(self.frames[int(self.anim)], self.angle, self.scale)
        window.blit(sf ,self.pos - (sf.get_width() * 0.5, sf.get_height() * 0.5))
        if debug : 
            self.collider.render(window)

    def destroy(self, lasers) :
            laser_particles.append(LaserImpact(self, self.pos, self.lifetime + 1))
            lasers.remove(self)
