import pygame
from Textures import *

from math import *
from random import *
from MiniBoss import BossState
from Powerup import *

SEG_LENGTH = 1.0/6.0 

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
        if self.time % 6 == 0 :
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
    if boss.lifeBar.life * boss.lifeBar.maxLife <= 1-SEG_LENGTH:
        boss.set_state('phase2')
        add_segment("Boss 1st phase")
    pass

#################################################################################################
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
    self.angle += pi * 0.005 * self.angledir

    if self.time % (FPS * 8) == 0 :
      self.angledir *= -1

    if self.time % 14 == 0:
        boss.fire(0.3, (CENTERX, CENTERY))
    if self.time % (FPS * 5) == 0 :
        pu = 'PU_ENERGY'
        if randint(0, 3) == 2 :
            pu = 'PU_HEALTH'
        boss.give_powerup((CENTERX, CENTERY), pu)

def phase2_render(self, window) :
    pass

def phase2_end(self, boss) :
    print (boss.lifeBar.life * boss.lifeBar.maxLife)
    print(1-2*SEG_LENGTH)
    if boss.lifeBar.life * boss.lifeBar.maxLife <= 1-2*SEG_LENGTH :
        boss.give_powerup(boss.pos + (uniform(-400, 400), uniform(-400, 100)), 'PU_ENERGY')
        boss.give_powerup(boss.pos + (uniform(-400, 400), uniform(-400, 100)), 'PU_HEALTH')
        boss.set_state('phase3')
        add_segment("Boss 2nd phase")
    pass

#################################################################################################
#################################################################################################
def phase3_init(self, boss) :
    self.time = 0
    self.points = [
        pygame.math.Vector2(CENTERX, CENTERY),
        pygame.math.Vector2(CENTERX * 0.4, CENTERY - 64),
        pygame.math.Vector2(WIDTH - CENTERX * 0.4, CENTERY - 64)
    ]
    self.boss_pos = pygame.math.Vector2(CENTERX, 140)
    self.target = 0
    self.delay = FPS
    self.count = 0

    self.protectors = []
    self.shielded = False
    

# Third state, pos boss onto the right coords
def phase3_prepare(self, boss) :

    if not self.shielded :
      boss.create_shield(FPS * 2000)
      self.shielded = True
    # boss.pos = boss.pos.lerp((CENTERX, 400), 0.1)
    boss.target_point(self.boss_pos, 0.01)
    d = boss.dist_to_point(self.boss_pos)
    if d < 10 :
        self.prepared = True
        self.time = 0
        for p in self.points :
            self.protectors.append(boss.spawn_enemy(p - pygame.math.Vector2(0, CENTERY + 64), p))

# First phase
def phase3_update(self, boss) :
    
    boss.vel.x = cos(float(self.time) / 75.0) * 0.1
    boss.vel.y = cos(float(self.time) / 50.0) * 0.1
    
    if self.shielded :
      remshield = True
      for p in self.protectors :
        if not p.dead :
          remshield = False
          break
      
      if remshield and self.shielded:
        boss.set_shield(FPS + 2)
        self.shielded = False

      if self.time % (FPS * 8) == 0 :
        boss.doublefire(0.0, boss.player.pos)

      if self.time % (FPS * 5) == 0 :
        pu = 'PU_ENERGY'
        if randint(0, 4) == 2 :
            pu = 'PU_SHIELD'
        boss.give_powerup(boss.pos + (uniform(-400, 400), uniform(250, 300)), pu)

    else :
        if self.time % (FPS * 5) == 0:
            boss.give_powerup(boss.pos + (uniform(-50, 50), uniform(250, 300)), 'PU_ENERGY')

        if self.time % (FPS * 4) < (FPS * 3) :
            if self.time % 8 == 0 :
                boss.doublefire(0.2, boss.player.pos + texturesOffsets['PLAYER_SHIP'])
        
def phase3_render(self, window) :
    pass

def phase3_end(self, boss) :
    if boss.lifeBar.life * boss.lifeBar.maxLife <= 1-3 * SEG_LENGTH :
        boss.set_state('phase4')
        boss.give_powerup(self.boss_pos + (uniform(-50, 50), uniform(-50, 50)), 'PU_ENERGY')
        boss.give_powerup(self.boss_pos + (uniform(-50, 50), uniform(-50, 50)), 'PU_HEALTH')
        boss.give_powerup(self.boss_pos + (uniform(-200, 200), uniform(400, 500)), 'PU_HEALTH')
        add_segment("Boss 3rd phase")
    pass

#################################################################################################
#################################################################################################
def phase4_init(self, boss) :
    self.time = 0
    self.hidepoint = pygame.math.Vector2(CENTERX, -240)
    self.target = 0
    self.chargeCount = 0
    self.left = pygame.math.Vector2(-300, 240)
    self.right = pygame.math.Vector2(WIDTH + 300, 240)
    self.center = pygame.math.Vector2(CENTERX, CENTERY)
    
# 4th state, pos boss onto the right coords
def phase4_prepare(self, boss) :
    boss.target_point(self.hidepoint, 0.01)
    d = boss.dist_to_point(self.hidepoint)
    if d < 10 :
        boss.remove_shield()
        self.prepared = True
        self.time = 0
        a = uniform(0, 2 * pi)
        boss.pos = pygame.math.Vector2(CENTERX + cos(a + pi) * (CENTERY + 200), CENTERY + sin(a + pi) * (CENTERY + 200))
        self.target = pygame.math.Vector2(CENTERX + cos(a) * (CENTERY + 200), CENTERY + sin(a) * (CENTERY + 200))
        boss.doublefire(0.1, self.center)
        if 1 == 1 :
          boss.give_powerup(self.center, 'PU_SHIELD')

# First phase
def phase4_update(self, boss) :
    
    if self.chargeCount <= 2 :
        boss.target_point(self.target, 0.014)
        d = boss.dist_to_point(self.target)
        if d < 20 :
          self.chargeCount += 1
          a = uniform(0, 2 * pi)
          boss.pos = pygame.math.Vector2(CENTERX + cos(a + pi) * (CENTERY + 300), CENTERY + sin(a + pi) * (CENTERY + 300))
          self.target = pygame.math.Vector2(CENTERX + cos(a) * (CENTERY + 300), CENTERY + sin(a) * (CENTERY + 300))
          if randint(0, 3) == 1 :
            boss.give_powerup(self.center, 'PU_SHIELD')
    else :
        if self.chargeCount < 10000 :
            boss.pos = self.left + pygame.math.Vector2(0, 0)
            self.chargeCount = 10000
            self.time = 0
        elif self.chargeCount == 10000 :
            boss.target_point(self.right, 0.005)
            d = boss.dist_to_point(self.right)
            boss.pos.y += sin(self.time * 0.01)
            self.time += 1

            if self.time % 20 == 0 :
              boss.alternfire(0)
            
            if d < 20 :
              self.chargeCount = 0
              a = uniform(0, 2 * pi)
              boss.give_powerup(self.center, 'PU_ENERGY')
              boss.pos = pygame.math.Vector2(CENTERX + cos(a + pi) * (CENTERY + 200), CENTERY + sin(a + pi) * (CENTERY + 200))
              self.target = pygame.math.Vector2(CENTERX + cos(a) * (CENTERY + 200), CENTERY + sin(a) * (CENTERY + 200))

def phase4_render(self, window) :
    pass

def phase4_end(self, boss) :
    if boss.lifeBar.life * boss.lifeBar.maxLife <= 1-4 * SEG_LENGTH :
        boss.set_state('phase5')
        boss.give_powerup(self.center + (uniform(-50, 50), uniform(-50, 50)), 'PU_ENERGY')
        boss.give_powerup(self.center + (uniform(-50, 50), uniform(-50, 50)), 'PU_HEALTH')
        add_segment("Boss 4th phase")
    pass

#################################################################################################
#################################################################################################
# First state, pos boss onto the right coords
def phase5_init(self, boss) :
    self.spread = 32
    self.width = 64
    self.target = pygame.math.Vector2(randint(self.spread, WIDTH-self.spread), HEIGHT)
    self.bosspos = pygame.math.Vector2(CENTERX, 120)
    self.angler = pi
    self.anglel = 0
    self.posr = self.bosspos + pygame.math.Vector2(cos(self.angler) * CENTERX, sin(self.angler) * CENTERX)
    self.posl = self.bosspos + pygame.math.Vector2(cos(self.anglel) * CENTERX, sin(self.anglel) * CENTERX)
    self.speed = 24
    self.cd = 30
    

def phase5_prepare(self, boss) :
    boss.target_point(self.bosspos, 0.02)
    if boss.dist_to_point(self.bosspos) < 10 :
        self.prepared = True
        self.time = 0
        boss.give_powerup(boss.pos + (uniform(-100, 100), uniform(500, 600)), 'PU_ENERGY')

# First phase
def phase5_update(self, boss) :
    boss.vel.x = cos(float(self.time) / 100.0) * 0.1
    boss.vel.y = cos(float(self.time) / 50.0) * 0.1
    
    self.angler += 0.05
    self.anglel -= 0.05
    self.posr = boss.pos + pygame.math.Vector2(cos(self.angler) * CENTERX, sin(self.angler) * CENTERX)
    self.posl = boss.pos + pygame.math.Vector2(cos(self.anglel) * CENTERX, sin(self.anglel) * CENTERX)
    print("t : " + str(self.target.x) + "  " + str(self.target.y))
    ax = NULLVEC.angle_to(boss.pos - self.target)
    p = boss.pos + pygame.math.Vector2(cos(ax) * CENTERX, sin(ax) * CENTERX)
    
    if self.time % 35 > (FPS * .1) :
        if self.time % 1 == 0:
            boss.fire(0, self.posl)
            boss.fire(0, self.posr)
            boss.fire(0, p)

def phase5_render(self, window) :
    pass

def phase5_end(self, boss) :
    if boss.lifeBar.life <= 1 :
        boss.set_state('end')
        add_segment("Boss killed !")
    pass

#################################################################################################
#################################################################################################
#################################################################################################
#################################################################################################
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
        'phase4': BossState(boss, phase4_prepare, phase4_update, phase4_end, phase4_render, phase4_init),
        'phase5': BossState(boss, phase5_prepare, phase5_update, phase5_end, phase5_render, phase5_init),
        'end' : BossState(boss, end_prepare, end_update, end_end, end_render, end_init)
    }