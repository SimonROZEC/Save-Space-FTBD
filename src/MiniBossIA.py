import pygame
from math import *
from random import *
from MiniBoss import BossState

def start_prepare(self, boss) :
    boss.pos = boss.pos.lerp((160, 150), 0.05)
    if ((160, 150)-boss.pos).length() < 1 :
        self.prepared = True
    pass

def start_update(self, boss) :
    boss.vel.x = sin(float(self.time) / 100.0)
    boss.vel.y = cos(float(self.time) / 50.0)
    if self.time % 30 == 0:
        boss.fire((0, 0), 0.4)
        
    pass

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