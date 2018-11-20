from math import *
from random import *

from Collider import *
from globaldefines import *

class IAPlayer():
    def __init__(self, player) :
        self.player = player
        self.IACollider = Collider(self.player, 70, pygame.math.Vector2(50, 40))
    


    def processInput(self, boss, lasers, inputs) :
        
        if( self.isPlayerBelowBoss(boss) ) :
            inputs['fire'] = True
      

        vecPlayer = pygame.math.Vector2( self.player.collider.getX(), self.player.collider.getY() )
        angle = 0
        for laser in lasers :
            if(laser.owner.type == 'PLAYER'):
                break

            if self.IACollider.collides( laser.collider ) : #collision
                vecLaser = pygame.math.Vector2( laser.collider.getX(), laser.collider.getY() )
                angle = (angle + NULLVEC.angle_to(vecPlayer - vecLaser)) * 0.5

        if( angle != 0 ) :
            if( angle >= 0 and angle < 60 ) :
                inputs['right'] = True
            elif( angle >= 60 and angle < 120 ) :
                inputs['left'] = True
            elif( angle >= 120 and angle < 180 ) :
                inputs['down'] = True
            elif( angle <= 0 and angle > -60 ) :
                inputs['right'] = True   
            elif( angle <= -60 and angle > -120 ) :
                inputs['up'] = True    
            elif( angle <= 120 and angle > -180 ) :
                inputs['left'] = True


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