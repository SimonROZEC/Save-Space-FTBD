from math import *
from random import *

from Collider import *


class IAPlayer():
    def __init__(self, player) :
        self.player = player
        self.IACollider = Collider(self.player, 100, pygame.math.Vector2(50, 40))
    
    def processInput(self, boss, inputs) :
        if(self.isPlayerBelowBoss(boss)) :
            inputs['fire'] = True
        else :
            inputs['fire'] = False

        pass


    def isPlayerBelowBoss(self, boss) :
        maxX = 0
        minX = 999999

        for collider in boss.colliders :
            maxX = max(maxX, collider.getX() + collider.getWidth())
            minX = min(minX, collider.getX())

        if( self.player.collider.getX() > minX 
        and ( self.player.collider.getX() + self.player.collider.getWidth() ) < maxX ) :
            return True
        return False

    def debug(self, window) :
        self.IACollider.render(window)