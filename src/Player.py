import pygame
from globaldefines import *

from math import *
from Laser import *
from Collider import *
from Textures import *

debug = True

OFFSET_LASER_LEFT = pygame.math.Vector2(16, 20)
OFFSET_LASER_RIGHT = pygame.math.Vector2(83-16, 20)

class PlayerLifebar(pygame.sprite.Sprite):
    def __init__(self, lifeBarEnabeled) :
        pygame.sprite.Sprite.__init__(self)
        self.lifes = 5
        self.icon = textures['PLAYER_LIFE_ICON']
        self.lifeBarEnabeled = lifeBarEnabeled

    def remove_life(self) :
        if self.lifes > 0 :
            self.lifes -= 1

    def render(self, window) :
        if(self.lifeBarEnabeled) :
            for i in range(self.lifes) :
                window.blit(self.icon, (10 + i*36, 800 - 40))

class Player(pygame.sprite.Sprite):
    def __init__(self, hasLifeBar = True) :
        pygame.sprite.Sprite.__init__(self)
        self.type = 'PLAYER'

        self.pos = pygame.math.Vector2(CENTERX, CENTERY) - texturesOffsets['PLAYER_SHIP']
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)

        self.image = textures['PLAYER_SHIP']
        self.fire = textures['PLAYER_THRUSTER']
        self.anim = 0

        self.firecd = 0
        self.invulframe = 0

        self.collider = Collider(self, 32, pygame.math.Vector2(50, 40))

        self.lifebar = PlayerLifebar(hasLifeBar)
        self.time = 0
        self.scale = 1

    def update(self, keys, dt, lasers, boss) :
        self.time += 0.5

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

        # window border forcefield
        if (self.pos.x < 0) :
            self.acc.x = 0.1
        if (self.pos.x > 600 - 99) :
            self.acc.x = -0.1
        if (self.pos.y < 0) :
            self.acc.y = 0.1
        if (self.pos.y > 800 - 75) :
            self.acc.y = -0.1

        # boss collision 
        for c in boss.colliders :
            if self.collider.collides(c) :
                force = self.pos - boss.pos
                if boss.type == 'MINIBOSS' :
                    force -= (80, 20)
                else :
                    force -= (128, 20)

                force.scale_to_length(2)
                self.acc += force
                if self.invulframe <= 0 :
                    self.lifebar.remove_life()
                    self.invulframe = 30 # duree de la frame d'invulnerabilite

        # laser collision
        for laser in lasers :
            #tous les lasers qui sont pas ceux du joueur
            if(laser.owner.type == 'PLAYER'):
                break

            if self.collider.collides(laser.collider) : #collision
                self.lifebar.remove_life()
                laser.destroy(lasers)


        self.vel += self.acc * dt

        # limit player speed
        if self.vel.length() > 15 :
            self.vel.scale_to_length(15)

        self.pos += self.vel

        # create lasers
        if keys['fire'] and self.firecd <= 0:
            self.firecd = 8
            speed = 1
            if self.vel.y < 0 :
                speed += -self.vel.y * 0.05
            dec = 0.02 * self.vel.x
            l1 = Laser(self, self.pos + OFFSET_LASER_LEFT, -pi*0.5+dec, speed,100)
            l2 = Laser(self, self.pos + OFFSET_LASER_RIGHT, -pi*0.5+dec, speed, 100)
            lasers.append(l2)
            lasers.append(l1)

        self.invulframe -= 1
        self.firecd -= 1

    def render(self, window) :
        offx = self.vel.x * 2 if self.vel.x > 0 else 0
        scalex = 99 - abs(2 * int(self.vel.x))
        if self.invulframe <= 0 or self.time % 2 == 0 :
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

        self.lifebar.render(window)

        if debug :
            self.collider.render(window)
        