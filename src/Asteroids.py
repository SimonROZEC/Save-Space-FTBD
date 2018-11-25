import pygame
from globaldefines import *

from math import *

from BossLifeBar import *

from Laser import *
from Powerup import *
from Collider import *
from Textures import *

debug = False

class Asteroid(pygame.sprite.Sprite) :
    def __init__(self, boss, pos, player, enemies) :
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.type = 'ASTEROID'
        self.boss = boss
        self.player = player
        self.enemies = enemies
        self.collider = Collider(self, 40, pygame.math.Vector2(0, 0))
        self.scale = 1
        self.image = textures['ASTEROID'][randint(0, 2)]
        self.rotatespeed = uniform(-0.2, 0.2)
        self.angle = 0
        self.vel = pygame.math.Vector2(0, 2)
        self.acc = pygame.math.Vector2(0, 0)

    def update(self, dt, enemies, lasers, player) :
      self.vel += self.acc
      self.pos += self.vel
      self.angle += self.rotatespeed

      self.acc.x = 0
      self.acc.y = 0

      for enemy in enemies :
          if not enemy.type == 'ASTEROID' or enemy == self :
            continue
          collider = self.collider
          if collider.collides(enemy.collider) :
              force = self.pos + texturesOffsets['ASTEROID'] - enemy.pos
              force.scale_to_length(0.2)
              self.acc += force
      
      if self.collider.collides(player.collider) :
              force = self.pos + texturesOffsets['ASTEROID'] - (player.pos +texturesOffsets['PLAYER_SHIP'])
              force.scale_to_length(0.4)
              self.acc += force


      # check collisions
      for laser in lasers :
          collider = laser.collider
          if laser.owner.type == 'PLAYER' and self.collider.collides(collider) : #collision
              laser.destroy(lasers)
              
    def render(self, window) :
      tex = pygame.transform.rotate(self.image, self.angle)
      window.blit(tex, self.pos-(tex.get_width() * 0.5, tex.get_height() * 0.5))
      if debug :
        self.collider.render(window)


class Asteroids(pygame.sprite.Sprite):
    def __init__(self, lasers, powerups, player, enemies) :
        pygame.sprite.Sprite.__init__(self)

        self.type = 'ASTEROIDS'

        self.pos = pygame.math.Vector2(CENTERX, 0)
        self.scale = 1

        self.colliders = []

        self.lasers = lasers
        self.powerups = powerups
        self.player = player
        self.enemies = enemies
        self.time = 0

        self.lifeBar = BossLifeBar(self, FPS * 30)

    def give_powerup(self, target, type) :
        self.powerups.append(Powerup(self.pos, target, type))

    def update(self, dt) :
        self.time += 1
        self.lifeBar.life -= 1
        if self.time % (FPS) == 0:
          self.enemies.append(Asteroid(self, pygame.math.Vector2(uniform(0, WIDTH), -50), self.player, self.enemies))

    def render(self, window) :
        self.lifeBar.render(window)