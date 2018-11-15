import pygame
from math import *
from Laser import *
from Collider import *
from LoadImages import *

debug = False

OFFSET_LASER_LEFT = pygame.math.Vector2(82, 175)
OFFSET_LASER_RIGHT = pygame.math.Vector2(164, 170)

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

from BossIA import states

class Boss(pygame.sprite.Sprite):
    def __init__(self, lasers) :
        pygame.sprite.Sprite.__init__(self)

        self.type = 'BOSS'

        self.pos = pygame.math.Vector2(150 * 0.5, 200)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.image = images['BOSS_SHIP']

        self.colliders = [
            Collider(self, 48, pygame.math.Vector2(38, 150)),
            Collider(self, 48, pygame.math.Vector2(257 - 38, 150)),
            Collider(self, 96, pygame.math.Vector2(257 * 0.5, 40))
        ]

        self.states = states(self)
        self.state = self.states['start']

        self.lasers = lasers
    
    def fire(self) :
        l1 = Laser(self, self.pos + OFFSET_LASER_LEFT, pi*0.5, 0.5, 1000)
        l2 = Laser(self, self.pos + OFFSET_LASER_RIGHT, pi*0.5, 0.5, 1000)
        self.lasers.append(l2)
        self.lasers.append(l1)

    def update(self, dt) :

        self.state.update()

        self.pos += self.vel

        # check collisions
        for laser in self.lasers :
            
            collider = laser.collider
            for col in self.colliders :
                if laser.owner.type == 'PLAYER' and col.collides(collider) : #collision
                    print(laser.owner.type)
                    laser.destroy(self.lasers)
                    break

    def render(self, window) :
        window.blit(self.image, self.pos)
        if debug :
            for collider in self.colliders :
                collider.render(window)
        