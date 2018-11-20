import pygame
from Textures import *

from math import *
from random import *
from MiniBoss import BossState
from Powerup import *


# Scene setup
def start_init(self, boss) :
    self.start_pos = pygame.math.Vector2(CENTERX, -150)
    self.current_pos = self.start_pos + (0, 0)

def start_prepare(self, boss) :
    boss.pos = boss.pos.lerp((CENTERX, 240), 0.015)
    self.current_pos = self.current_pos.lerp((CENTERX, 130), 0.015)
    if ((CENTERX, 230)-boss.pos).length() < 10 :
        self.prepared = True
        
    #pass

def start_update(self, boss) :
    self.current_pos = self.current_pos.lerp(self.start_pos, 0.03)
    #pass

def start_render(self, window) :
    coord = self.current_pos - texturesOffsets['BOSS_SHIP']
    window.blit(textures['BOSS_SHIP'], coord)
    pass

def start_end(self, boss) :
    if self.prepared and (self.start_pos-self.current_pos).length() < 10 :
        boss.set_state('phase1')
    pass

#################################################################################################
# First state, pos boss onto the right coords
def phase1_init(self, boss) :
    self.time = 0

def phase1_prepare(self, boss) :
    boss.pos = boss.pos.lerp((CENTERX, 120), 0.03)
    if ((CENTERX, 120)-boss.pos).length() < 10 :
        boss.give_powerup(boss.pos + (uniform(-400, 400), uniform(200, 400)), 'PU_ENERGY')
        self.prepared = True
    #pass

# First phase
def phase1_update(self, boss) :
    boss.vel.x = sin(float(self.time) / 100.0)
    boss.vel.y = cos(float(self.time) / 50.0)
    if self.time % 20 == 0:
        boss.fire(0.8)
    if (self.time + FPS*2) % (FPS * 5) == 0 :
        pu = 'PU_ENERGY'
        if randint(0, 5) == 2 :
            pu = 'PU_HEALTH'
        boss.give_powerup(boss.pos + (uniform(-200, 200), uniform(-200, -400)), pu)
    if (self.time+1) % (FPS * 10) == 0 :
        boss.create_shield(FPS*3)
    #pass

def phase1_render(self, window) :
    pass

def phase1_end(self, boss) :
    if boss.lifeBar.life * boss.lifeBar.maxLife <= 0.66 :
        boss.set_state('phase2')
    pass

#################################################################################################
# Second state, pos boss onto the right coords
def phase2_prepare(self, boss) :
    # boss.pos = boss.pos.lerp((CENTERX, 400), 0.1)
    boss.target_point((CENTERX, 400), 0.1)
    d = boss.dist_to_point((CENTERX, 400))
    # print('dist : ' + str(d))
    if d < 10 :
        # print("ok" + str(self.time))
        self.prepared = True
        self.time = 0
    #pass

# First phase
def phase2_update(self, boss) :
    boss.vel.x = cos(float(self.time) / 100.0)
    boss.vel.y = sin(float(self.time) / 50.0)
    if self.time % 50 == 0:
        boss.fire(1)
    if self.time % 10 == 0:
        boss.fire(0.02)
    
    if self.time % (FPS * 5) == 0 :
        boss.give_powerup(boss.pos + (uniform(-200, 200), 0), 'PU_SHIELD')

    if (self.time + FPS*2) % (FPS * 10) == 0 :
        boss.give_powerup(boss.pos + (uniform(-200, 200), uniform(-200, -400)), 'PU_ENERGY')
    #pass

def phase2_render(self, window) :
    pass

def phase2_end(self, boss) :
    if boss.lifeBar.life * boss.lifeBar.maxLife <= 0.33 :
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
        'phase2' : BossState(boss, phase2_prepare, phase2_update, phase2_end, phase2_render),
        'phase3': BossState(boss, phase3_prepare, phase3_update, phase3_end, phase3_render, phase3_init),
        'end' : BossState(boss, end_prepare, end_update, end_end, end_render, end_init)
    }