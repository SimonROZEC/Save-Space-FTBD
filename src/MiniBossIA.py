import pygame
from globaldefines import *

from math import *
from random import *
from MiniBoss import BossState

# First state, pos boss onto the right coords
def start_prepare(self, boss) :
    boss.pos = boss.pos.lerp((220, 120), 0.02)
    if ((220, 120)-boss.pos).length() < 10 :
        self.prepared = True
    #pass

# First phase
def start_update(self, boss) :
    boss.vel.x = sin(float(self.time) / 100.0)
    boss.vel.y = cos(float(self.time) / 50.0)
    if self.time % 20 == 0:
        boss.fire((0, 0), 0.6)
    #pass

def start_render(self, window) :
    pass

def start_end(self, boss) :
    if boss.lifeBar.life * boss.lifeBar.maxLife <= 0.5 :
        boss.set_state('phase1')
    pass

#################################################################################################
# Second state, pos boss onto the right coords
def phase1_prepare(self, boss) :
    self.prepared = True
    #pass

# First phase
def phase1_update(self, boss) :
    boss.vel.x = sin(float(self.time) / 100.0)
    boss.vel.y = cos(float(self.time) / 50.0)
    if self.time % 5 == 0:
        boss.fire((0, 0), 0.1)
    #pass

def phase1_render(self, window) :
    pass

def phase1_end(self, boss) :
    pass

def states(boss) :
    return {
        'start'   : BossState(boss, start_prepare, start_update, start_end, start_render),
        'phase1' : BossState(boss, phase1_prepare, phase1_update, phase1_end, phase1_render),
        'phase2' : BossState(boss, start_prepare, start_update, start_end, start_render),
        'phase3': BossState(boss, start_prepare, start_update, start_end, start_render),
        'end' : BossState(boss, start_prepare, start_update, start_end, start_render)
    }