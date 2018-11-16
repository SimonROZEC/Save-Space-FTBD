import pygame
from Textures import *

from math import *
from random import *
from MiniBoss import BossState
from Powerup import *

# methode securise pour lerp un point
def target_point(start, target, speed) :
    d = (target - start) * speed
    if d.length() < 2 :
        if dist_to_point(start, target) < 2 :
            return target
        else :
            d.scale_to_length(2)
    return start + d

def dist_to_point(start, target) :
    return (target-start).length()

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
        self.prepared = True
    #pass

# First phase
def phase1_update(self, boss) :
    boss.vel.x = sin(float(self.time) / 100.0)
    boss.vel.y = cos(float(self.time) / 50.0)
    if self.time % 20 == 0:
        boss.fire((0, 0), 0.6)
    #pass

def phase1_render(self, window) :
    pass

def phase1_end(self, boss) :
    if boss.lifeBar.life * boss.lifeBar.maxLife <= 0.5 :
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
    #pass

# First phase
def phase2_update(self, boss) :
    boss.vel.x = sin(float(self.time) / 100.0)
    boss.vel.y = cos(float(self.time) / 50.0)
    if self.time % 20 == 0:
        boss.fire((0, 0), 1)
    if self.time % 10 == 0:
        boss.fire((0, 0), 0.02)
    if self.time % 60 == 0 :
        boss.give_powerup((uniform(0, WIDTH), -34), get_random_type())
    #pass

def phase2_render(self, window) :
    pass

def phase2_end(self, boss) :
    pass

def states(boss) :
    return {
        'start'   : BossState(boss, start_prepare, start_update, start_end, start_render, start_init),
        'phase1' : BossState(boss, phase1_prepare, phase1_update, phase1_end, phase1_render),
        'phase2' : BossState(boss, phase2_prepare, phase2_update, phase2_end, phase2_render),
        'phase3': BossState(boss, phase1_prepare, phase1_update, phase1_end, phase1_render),
        'end' : BossState(boss, start_prepare, start_update, start_end, start_render)
    }