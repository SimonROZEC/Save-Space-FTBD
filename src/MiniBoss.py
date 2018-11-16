import pygame
from globaldefines import *

from math import *

from BossLifeBar import *

from Laser import *
from Powerup import *
from Collider import *
from Textures import *

debug = False

OFFSET_LASER = pygame.math.Vector2(0, 20)

class BossState:
    def __init__(self, boss, prepare, update, end, render, init = None) :
        self.boss = boss
        
        self.p = prepare # update preparation du boss pour commencer l'etat + condition de fin de preparation
        
        self.u = update # mise a jour du boss pour un etat specifique
        self.r = render # affichage d'effets graphiques specifiques a l'etat

        self.e = end # condition de fin de l'etat et passage a l'etat suivant

        self.time = 0
        self.prepared = False # le boss a termine la phase de preparation de son etat
        if not init == None :
            init(self, boss)

    def update(self):
        self.time += 1
        if not self.prepared :
            self.p(self, self.boss)
        else :
            self.u(self, self.boss)
        
        self.e(self, self.boss)

    def render(self, window):
        self.r(self, window)

from MiniBossIA import states

class MiniBoss(pygame.sprite.Sprite):
    def __init__(self, lasers, powerups, player) :
        pygame.sprite.Sprite.__init__(self)

        self.type = 'MINIBOSS'

        self.pos = pygame.math.Vector2(CENTERX, -40)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.image = textures['MINIBOSS_SHIP']

        self.scale = 1

        self.colliders = [
            Collider(self, 24, pygame.math.Vector2(-50, 20)),
            Collider(self, 24, pygame.math.Vector2(50, 20)),
            Collider(self, 64, pygame.math.Vector2(0, -30))
        ]

        self.states = states(self)
        self.state = self.states['start']

        self.lasers = lasers
        self.powerups = powerups
        self.player = player

        self.lifeBar = BossLifeBar(10000)
    
    def set_state(self, name) :
        self.state = self.states[name]

    def fire(self, target, precision = 0.05)  :
        laser = Laser(self, self.pos + OFFSET_LASER, pi*0.5, 0.5, 1000, 1.5, precision)
        self.lasers.append(laser)

    def give_powerup(self, target, type) :
        self.powerups.append(Powerup(self.pos, target, type))

    def update(self, dt) :

        self.state.update()

        self.pos += self.vel

        # check collisions
        for laser in self.lasers :
            collider = laser.collider
            for col in self.colliders :
                if laser.owner.type == 'PLAYER' and col.collides(collider) : #collision
                    self.lifeBar.remove_life(laser.lifetime)
                    laser.destroy(self.lasers)
                    break

    def render(self, window) :
        self.state.render(window)
        window.blit(self.image, self.pos-texturesOffsets['MINIBOSS_SHIP'])
        
        self.lifeBar.render(window)
        if debug :
            for collider in self.colliders :
                collider.render(window)
    
    # methode securise pour target un point
    def target_point(self, target, speed) :
        d = (target - self.pos) * speed
        if d.length() < 2 :
            if self.dist_to_point(target) < 2 :
                self.pos = target
                return
            else :
                d.scale_to_length(2)
        self.pos += d

    def dist_to_point(self, target) :
        return (target-self.pos).length()