import pygame
from globaldefines import *

from math import *
import random
from BossLifeBar import *

from Laser import *
from Powerup import *
from Collider import *
from Textures import *
from Upgrade import *

debug = False

class Station(pygame.sprite.Sprite) :
    def __init__(self, player, enemies, type, upgrades) :
        pygame.sprite.Sprite.__init__(self)

        self.dir = 1
        if randint(0, 10) < 5 :
          self.dir = -1
        if self.dir == 1 :
          self.pos = pygame.math.Vector2(-300, CENTERY+uniform(-150, 50))
        else :
          self.pos = pygame.math.Vector2(WIDTH+300, CENTERY+uniform(-150, 50))
          
        self.type = type
        self.player = player
        self.upgrades = upgrades
        self.enemies = enemies
        self.scale = 1
        self.collider = Collider(self, 60, pygame.math.Vector2(0, 0))
        self.health = 2000
        self.image = textures['STATION_' + type]
        self.rotatespeed = 0.05
        if randint(0, 10) < 5 :
          self.rotatespeed *= -1

        self.angle = 0
        self.vel = pygame.math.Vector2(1*self.dir, 0)
    def update(self, dt, enemies, lasers, player) :
      
      if self.pos.x > WIDTH + 300 :
          enemies.remove(self)
          return

      self.angle += self.rotatespeed
      self.pos += self.vel

      # check collisions
      for laser in lasers :
          collider = laser.collider
          if laser.owner.type == 'PLAYER' and self.collider.collides(collider) : #collision
                self.health -= laser.lifetime
                laser.destroy(lasers)
                if self.health <= 0 :
                    for i in range(0, 20) :
                        l = Laser(player, self.pos + (uniform(-100, 100), uniform(-100, 100)), 0, 0, randint(10, 50))
                        lasers.append(l)
                        l.destroy(lasers)
                    enemies.remove(self)
                    self.upgrades.append(Upgrade(self.pos, self.pos+(uniform(-200, 200), uniform(-50, 50)), self.type))

                    #TODO GIVE UPGRADE TO PLAYER
              
    def render(self, window) :
      tex = pygame.transform.rotate(self.image, self.angle)
      window.blit(tex, self.pos-(tex.get_width() * 0.5, tex.get_height() * 0.5))
      if debug :
        self.collider.render(window)


class Asteroid(pygame.sprite.Sprite) :
    def __init__(self, boss, pos, player, enemies) :
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.type = 'ASTEROID'
        self.boss = boss
        self.player = player
        self.enemies = enemies
        self.scale = uniform(0.8, 1.4)
        self.collider = Collider(self, 40*self.scale, pygame.math.Vector2(0, 0))
        self.forcefield = Collider(self, 40 * self.scale * 2.5, pygame.math.Vector2(0, 0))

        self.image = pygame.transform.rotozoom(textures['ASTEROID'][randint(0, 2)], 0, self.scale).convert_alpha()
        self.rotatespeed = uniform(-0.2, 0.2)
        self.angle = 0
        self.vel = pygame.math.Vector2(0, 2)
        self.acc = pygame.math.Vector2(0, 0)

    def update(self, dt, enemies, lasers, player) :
      
      if self.pos.y > HEIGHT + texturesOffsets['ASTEROID'].y * 2 :
          enemies.remove(self)
          return

      self.vel.x *= 0.9
      self.vel += self.acc
      self.pos += self.vel
      self.angle += self.rotatespeed

      self.acc.x = 0
      self.acc.y = 0

      if self.vel.y > 3 :
        self.vel.y = 3

      for enemy in enemies :
          if not enemy.type == 'ASTEROID' or enemy == self :
            continue
          collider = self.forcefield
          if collider.collides(enemy.forcefield) :
              force = self.pos + texturesOffsets['ASTEROID'] - enemy.pos
              force.scale_to_length(0.05)
              self.acc += force  

      if self.collider.collides(player.collider) :
              force = (self.pos) - (player.pos + texturesOffsets['PLAYER_SHIP'])
              force.scale_to_length(0.4)
              self.acc += force

      # check collisions
      for laser in lasers :
          collider = laser.collider
          if laser.owner.type == 'PLAYER' and self.collider.collides(collider) : #collision
              laser.destroy(lasers)
              force = self.pos + texturesOffsets['ASTEROID'] - laser.pos
              force.scale_to_length(0.1)
              self.acc += force
              
    def render(self, window) :
      tex = pygame.transform.rotate(self.image, self.angle)
      window.blit(tex, self.pos-(tex.get_width() * 0.5, tex.get_height() * 0.5))
      if debug :
        pass
        #self.forcefield.render(window)

UPGRADE_TYPES = ['ECO', 'RANGE', 'REACTOR']

class Asteroids(pygame.sprite.Sprite):
    def __init__(self, lasers, powerups, player, enemies, upgrades) :
        pygame.sprite.Sprite.__init__(self)

        self.type = 'ASTEROIDS'

        self.pos = pygame.math.Vector2(CENTERX, 0)
        self.scale = 1

        self.colliders = []

        self.upgrades = upgrades
        self.lasers = lasers
        self.powerups = powerups
        self.player = player
        self.enemies = enemies
        self.time = 0
        self.lifeBar = BossLifeBar(self, FPS * 40)
        self.diff = 30

    def give_powerup(self, target, type) :
        self.powerups.append(Powerup(self.pos, target, type))

    def update(self, dt) :
        self.time += 1
        self.lifeBar.life -= 1
        if self.lifeBar.life > FPS * 5 :
          if self.time % (self.diff) == 0:
            self.enemies.append(Asteroid(self, pygame.math.Vector2(uniform(0, WIDTH), -50), self.player, self.enemies))
          if self.time == FPS * 10 :
            self.enemies.append(Station(self.player, self.enemies, UPGRADE_TYPES[0], self.upgrades))
          if self.time == FPS * 20 :
            self.enemies.append(Station(self.player, self.enemies, UPGRADE_TYPES[1], self.upgrades))
          if self.time == FPS * 30 :
            self.enemies.append(Station(self.player, self.enemies, UPGRADE_TYPES[2], self.upgrades))
          if self.time % (FPS * 25) == 0 :
            self.diff = 24

    def render(self, window) :
        self.lifeBar.render(window)