import pygame
from Textures import *

from math import *
from random import *
from MiniBoss import BossState
from Powerup import *


# Scene setup
def start_init(self, boss) :
  self.pos = pygame.math.Vector2(CENTERX, 140)

def start_prepare(self, boss) :
    boss.target_point(self.pos, 0.02)
    if boss.dist_to_point(self.pos) < 10 :
        self.prepared = True

def start_update(self, boss) :
    pass

def start_render(self, window) :
    pass

def start_end(self, boss) :
    if self.prepared :
      boss.set_state('phase1')
    pass

#################################################################################################
# First state, pos boss onto the right coords
def phase1_init(self, boss) :
    self.xlimit = -256
    self.point = pygame.math.Vector2(self.xlimit, HEIGHT)
    self.pointlimit = pygame.math.Vector2(WIDTH, 2 * HEIGHT)
    self.salve_id = 0
    self.pos = pygame.math.Vector2(CENTERX, 140)
    self.speed = 24
    self.cd = 30
def phase1_prepare(self, boss) :
    self.time = 0
    boss.target_point(self.pos, 0.02)
    if boss.dist_to_point(self.pos) < 10 :
        self.prepared = True
        boss.give_powerup(boss.pos + (uniform(-100, 100), uniform(500, 600)), 'PU_ENERGY')

# First phase
def phase1_update(self, boss) :
    boss.vel.x = cos(float(self.time) / 100.0) * 0.1
    boss.vel.y = cos(float(self.time) / 50.0) * 0.1
    self.cd -= 1
    if self.time % (FPS * 5) == 0:
      boss.give_powerup(boss.pos + (uniform(-100, 100), uniform(500, 600)), 'PU_ENERGY')
    if self.cd <= 0 :
        if self.time % 5 == 0 :
          boss.fire(0, self.point)
          if self.salve_id == 2 :
            boss.fire(0, self.pointlimit - self.point)

        if self.salve_id == 0 :
          self.point.x += self.speed
          if self.point.x >= WIDTH - self.xlimit :
            self.salve_id = 1
            self.cd = 20
        elif self.salve_id == 1 :
          self.point.x -= self.speed
          if self.point.x <= self.xlimit :
            self.salve_id = 2
            self.cd = 30
        elif self.salve_id == 2 :
          self.point.x += self.speed
          if self.point.x >= WIDTH - self.xlimit * 6:
            self.salve_id = 0
            self.point.x = self.xlimit
            self.cd = 50

def phase1_render(self, window) :
    pass

def phase1_end(self, boss) :
    if boss.lifeBar.life * boss.lifeBar.maxLife <= 1-1/6 :
        boss.set_state('phase2')
    pass

#################################################################################################
# Second state, pos boss onto the right coords
def phase2_init(self, boss) :
    self.angle = -pi * 0.5
    self.outpoint = (CENTERX, -32)
    self.angledir = 1
def phase2_prepare(self, boss) :
    # boss.pos = boss.pos.lerp((CENTERX, 400), 0.1)
    boss.target_point(self.outpoint, 0.1)
    d = boss.dist_to_point(self.outpoint)
    if d < 10 :
        self.prepared = True
        self.time = 0

def phase2_update(self, boss) :
    boss.pos.x = CENTERX + cos(self.angle) * CENTERY - 32
    boss.pos.y = CENTERY + sin(self.angle) * CENTERY - 32
    self.angle += pi * 0.01 * self.angledir
    
    if self.time % (FPS * 8) == 0 :
      self.angledir *= -1

    if self.time % 15 == 0:
        boss.fire(0.6, (CENTERX, CENTERY))
    if self.time % (FPS * 5) == 0 :
        pu = 'PU_ENERGY'
        if randint(0, 3) == 2 :
            pu = 'PU_HEALTH'
        boss.give_powerup((CENTERX, CENTERY), pu)

def phase2_render(self, window) :
    pass

def phase2_end(self, boss) :
    if boss.lifeBar.life * boss.lifeBar.maxLife <= 1-2/6 :
        boss.give_powerup(boss.pos + (uniform(-400, 400), uniform(-400, 100)), 'PU_ENERGY')
        boss.give_powerup(boss.pos + (uniform(-400, 400), uniform(-400, 100)), 'PU_HEALTH')
        boss.set_state('phase3')
    pass

#################################################################################################
def phase3_init(self, boss) :
    self.time = 0
    self.points = [
        pygame.math.Vector2(CENTERX, WIDTH - CENTERX * 0.4),
        pygame.math.Vector2(CENTERX * 0.4, 128),
        pygame.math.Vector2(WIDTH - CENTERX * 0.4, 128)
    ]
    self.pu_pos = pygame.math.Vector2(CENTERX, 304)
    self.target = 0
    self.delay = FPS
    self.count = 0

# Third state, pos boss onto the right coords
def phase3_prepare(self, boss) :
    # boss.pos = boss.pos.lerp((CENTERX, 400), 0.1)
    boss.target_point(self.points[0], 0.2)
    d = boss.dist_to_point(self.points[0])
    if d < 10 :
        self.prepared = True

# First phase
def phase3_update(self, boss) :
    d = boss.dist_to_point(self.points[self.target % 3])
    if d > 20 :
        boss.target_point(self.points[self.target % 3], 0.2)
    else:
        self.delay -= 1

        if self.delay <= 0 :
            old = self.target
            while self.target == old :
                self.target = randint(0, 2)
            self.delay = FPS
            self.time = 0
            self.count += 1
            if self.count % 6 == 0 :
                boss.give_powerup(self.pu_pos, 'PU_SHIELD')
            if (self.count+1) % 3 == 0:
                boss.give_powerup(self.pu_pos, 'PU_ENERGY')
        else :
            if self.delay < FPS*0.5 and self.time % 8 == 0:
                boss.fire(0.15, boss.player.pos)

def phase3_render(self, window) :
    pass

def phase3_end(self, boss) :
    if boss.lifeBar.life <= 1 :
        boss.set_state('end')
    pass

#################################################################################################
def end_init(self, boss) :
    self.time = 0
    self.center = pygame.math.Vector2(CENTERX, CENTERY)
    self.bottom = pygame.math.Vector2(CENTERX, HEIGHT)
    self.endanim = False
    self.smokeoff = pygame.math.Vector2(0, 0)
    self.smokeframe = 0
    self.laseroff = pygame.math.Vector2(0, 0)
    self.laserframe = 0
    
    self.boss = boss

# Third state, pos boss onto the right coords
def end_prepare(self, boss) :
    # boss.pos = boss.pos.lerp((CENTERX, 400), 0.1)
    boss.target_point(self.center, 0.1)
    d = boss.dist_to_point(self.center)
    if d < 10 :
        self.prepared = True
        for i in xrange(0, 8) :
            pu = 'PU_ENERGY'
            if randint(0, 1) == 0 :
                pu = 'PU_HEALTH'
            boss.give_powerup(boss.pos + (uniform(-200, 200), uniform(-200, 100)), pu)

# First phase
def end_update(self, boss) :
    boss.pos += pygame.math.Vector2(randint(-20, 21), randint(-20, 21)) * boss.scale
    boss.target_point(self.bottom, 0.001)
    boss.scale -= 0.005

def end_render(self, window) :
    self.smokeframe += 1
    self.laserframe += 1
    scale = abs(sin(self.time * 0.1))
    laserscale = abs(sin(self.time * 0.5))
    if scale <= 0.1 :
        self.smokeoff.x = randint(-10, 0)
        self.smokeoff.y = randint(-10, 0)
    else :
        coord = self.boss.pos + self.smokeoff * self.boss.scale * scale * 3
        window.blit(pygame.transform.rotozoom(textures['SMOKE'][self.smokeframe % 7], 0, self.boss.scale * scale * 3), coord + self.smokeoff)
    
    if laserscale <= 0.05 :
        self.laseroff.x = randint(-60, 60)
        self.laseroff.y = randint(-60, 60)
    else :
        coord = self.boss.pos + self.laseroff * self.boss.scale * laserscale
        window.blit(pygame.transform.rotozoom(textures['LASER_PLAYER_EXPLOSION'][self.laserframe % 4], 0, self.boss.scale * laserscale), coord - texturesOffsets['LASER_PLAYER_EXPLOSION'] * self.boss.scale * laserscale)
    
    
    pass

def end_end(self, boss) :
    if boss.scale <= 0.0 :
        self.endanim = True
    if self.endanim:
        boss.finish()
    pass

def states(boss) :
    return {
        'start'   : BossState(boss, start_prepare, start_update, start_end, start_render, start_init),
        'phase1' : BossState(boss, phase1_prepare, phase1_update, phase1_end, phase1_render, phase1_init),
        'phase2' : BossState(boss, phase2_prepare, phase2_update, phase2_end, phase2_render, phase2_init),
        'phase3': BossState(boss, phase3_prepare, phase3_update, phase3_end, phase3_render, phase3_init),
        'end' : BossState(boss, end_prepare, end_update, end_end, end_render, end_init)
    }