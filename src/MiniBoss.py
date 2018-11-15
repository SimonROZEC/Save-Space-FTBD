import pygame
from globaldefines import *

from math import *
from Laser import *
from Collider import *
from Textures import *

debug = True

OFFSET_LASER = pygame.math.Vector2(72, 64)

class BossState:
    def __init__(self, boss, prepare, update, end, render) :
        self.boss = boss
        self.p = prepare # update preparation du boss pour commencer l'etat + condition de fin de preparation
        self.u = update # mise a jour du boss pour un etat specifique
        self.r = render # affichage d'effets graphiques specifiques a l'etat
        self.e = end # condition de fin de l'etat et passage a l'etat suivant
        self.time = 0
        self.prepared = False # le boss a termine la phase de preparation de son etat
    
    def update(self):
        self.time += 1
        if self.prepared :
            self.u(self, self.boss)
        else :
            self.p(self, self.boss)
        
        self.e(self, self.boss)

    def render(self, window):
        self.r(self, window)

from MiniBossIA import states

class MiniBoss(pygame.sprite.Sprite):
    def __init__(self, lasers) :
        pygame.sprite.Sprite.__init__(self)

        self.type = 'MINIBOSS'

        self.pos = pygame.math.Vector2(300-80, -120)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.image = textures['MINIBOSS_SHIP']

        self.scale = 1

        self.colliders = [
            Collider(self, 24, pygame.math.Vector2(30, 80)),
            Collider(self, 24, pygame.math.Vector2(130, 80)),
            Collider(self, 64, pygame.math.Vector2(80, 30))
        ]

        self.states = states(self)
        self.state = self.states['start']

        self.lasers = lasers
    
    def fire(self, target, precision = 0.05)  :
        laser = Laser(self, self.pos + OFFSET_LASER, pi*0.5, 0.5, 1000, 1.5, precision)
        self.lasers.append(laser)

    def update(self, dt) :

        self.state.update()

        self.pos += self.vel

        # check collisions
        for laser in self.lasers :
            collider = laser.collider
            for col in self.colliders :
                if laser.owner.type == 'PLAYER' and col.collides(collider) : #collision
                    laser.destroy(self.lasers)
                    break

    def render(self, window) :
        window.blit(self.image, self.pos)
        if debug :
            for collider in self.colliders :
                collider.render(window)
        