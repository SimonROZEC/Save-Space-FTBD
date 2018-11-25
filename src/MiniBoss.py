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

        self.lifeBar = BossLifeBar(self, 12000)

        self.shieldcd = 0
        self.shield_duration = 0
        self.shield_tex = []
        self.shield_scale = 1.4
        self.shield_collider = Collider(self, 100, pygame.math.Vector2(0, 6))
        for t in textures['SHIELD'] :
          self.shield_tex.append(pygame.transform.rotozoom(t, 180, self.shield_scale).convert_alpha())

    def set_state(self, name) :
        self.state = self.states[name]

    def set_shield(self, duration) :
        self.shieldcd = duration
        self.shield_duration = duration

    def create_shield(self, duration) : # si un shield existe deja, ne reset pas le cd
        if self.shieldcd > 0 :
          return
        self.shieldcd = duration
        self.shield_duration = duration

    def remove_shield(self) :
        self.shieldcd = 0

    def fire(self, precision = 0.05, target = None)  :
        pos = self.pos + OFFSET_LASER
        laser = None
        if target == None :
            laser = Laser(self, pos, pi*0.5, 0.5, 1000, 1.5, precision)
        else :
            a = NULLVEC.angle_to(pos - target)
            laser = Laser(self, pos, radians(a) + pi, 0.5, 1000, 1.5, precision)
        self.lasers.append(laser)

    def give_powerup(self, target, type) :
        self.powerups.append(Powerup(self.pos, target, type))

    def update(self, dt) :

        self.state.update()
        self.shieldcd -= 1
        self.pos += self.vel

        # check collisions
        for laser in self.lasers :
            collider = laser.collider
            if self.shieldcd > 0 :
                if laser.owner.type == 'PLAYER' and self.shield_collider.collides(collider) :
                    laser.destroy(self.lasers)
            else :
                for col in self.colliders :
                    if laser.owner.type == 'PLAYER' and col.collides(collider) : #collision
                        self.lifeBar.remove_life(laser.lifetime)
                        laser.destroy(self.lasers)
                        break

    def render(self, window) :
        
        window.blit(pygame.transform.rotozoom(self.image, 0, self.scale), self.pos-texturesOffsets['MINIBOSS_SHIP']*self.scale)
        
        # print('shield ' + str(self.shieldcd))

        if self.shieldcd > 0 :
            shieldframe = min((self.shield_duration - self.shieldcd) * 0.3, 2)
            
            if self.shieldcd < FPS :
                if self.shieldcd % 5 <= 2 :
                    window.blit(self.shield_tex[int(shieldframe)], self.pos - texturesOffsets['SHIELD'] * self.shield_scale + (-2, 10))
            else :
                window.blit(self.shield_tex[int(shieldframe)], self.pos - texturesOffsets['SHIELD'] * self.shield_scale + (-2, 10))
            
        self.state.render(window)
        self.lifeBar.render(window)
        

        if debug :
            for collider in self.colliders :
                collider.render(window)
            if self.shieldcd > 0 :
                self.shield_collider.render(window)
    
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

    def finish(self) :
        self.lifeBar.life = 0

    def dist_to_point(self, target) :
        return (target-self.pos).length()