import pygame
from globaldefines import *

from math import *
from random import *

from Collider import *
from Textures import *
from Laser import *

debug = False

class Enemy(pygame.sprite.Sprite):
    def __init__(self, owner, pos, speed, firerate, health, target = None, endstop = False) :
        pygame.sprite.Sprite.__init__(self)
        print('enemy !!!')
        self.type = 'ENEMY'
        self.owner = owner
        self.pos = pos
        self.vel = pygame.math.Vector2(0, speed)
        self.image = textures['ENEMY_SHIP']
        self.speed = speed
        self.targeted = True if target == None else False
        self.endstop = endstop # le vaisseau s'arrête après avoir atteint sa target
        self.target = target

        self.health = health
        self.dead = False
        
        self.scale = 1
        self.time = 0
        self.anim = 0
        self.collider = Collider(self, 42, pygame.math.Vector2(0, 0))

    def update(self, dt, enemies, lasers, player) :
        if self.pos.y > HEIGHT + texturesOffsets['ENEMY_SHIP'].y * 2 :
          self.destroy(enemies)
          return

        if self.targeted :
          if not self.endstop :
            self.pos += self.vel * dt # move down
          else : # Idle
            self.vel.x = cos(float(self.time) / 100.0) * 0.15
            self.vel.y = cos(float(self.time) / 50.0) * 0.15
            self.pos += self.vel
        else :# go to target
          self.time = 0
          self.target_point(self.target, self.speed * 0.05)
          d = self.dist_to_point(self.target)
          if d < 10 :
              self.targeted = True
        self.time += 1

        # check collisions
        for laser in lasers :
            collider = laser.collider
            if laser.owner.type == 'PLAYER' and self.collider.collides(collider) : #collision
                self.health -= laser.lifetime
                laser.destroy(lasers)
                if self.health <= 0 :
                    for i in range(0, 5) :
                        l = Laser(player, self.pos + (uniform(-40, 40), uniform(-40, 40)), 0, 0, randint(10, 50))
                        lasers.append(l)
                        l.destroy(lasers)
                    self.destroy(enemies)
                    return

    def render(self, window) :
        if not (self.targeted and self.endstop) :
          window.blit(pygame.transform.rotate(textures['PLAYER_THRUSTER'][self.anim],180), self.pos-(32, 70))
          window.blit(pygame.transform.rotate(textures['PLAYER_THRUSTER'][self.anim], 180), self.pos-(-18, 70))
        else :
          window.blit(pygame.transform.rotate(textures['PLAYER_THRUSTER'][self.anim],180), self.pos-(32, 50))
          window.blit(pygame.transform.rotate(textures['PLAYER_THRUSTER'][self.anim], 180), self.pos-(-18, 50))

        window.blit(self.image ,self.pos - texturesOffsets['ENEMY_SHIP'])

        if debug : 
            self.collider.render(window)

        self.anim = (self.anim + 1) % 3

    def destroy(self, enemies) :
            self.dead = True
            enemies.remove(self)

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