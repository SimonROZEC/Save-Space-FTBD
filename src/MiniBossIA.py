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
        boss.fire((0, 0), 0.4)   
    #pass

def start_end(self, boss) :
    pass

def start_render(self, window) :
    pass

def states(boss) :
    return {
        'start'   : BossState(boss, start_prepare, start_update, start_end, start_render),
        'phase1' : BossState(boss, start_prepare, start_update, start_end, start_render),
        'phase2' : BossState(boss, start_prepare, start_update, start_end, start_render),
        'phase3': BossState(boss, start_prepare, start_update, start_end, start_render),
        'end' : BossState(boss, start_prepare, start_update, start_end, start_render)
    }