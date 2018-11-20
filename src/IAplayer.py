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
        else :            
            self.player.vel += pygame.math.Vector2((boss.colliders[1].getX()-self.player.collider.getX())*0.001, 0)

        vecPlayer = pygame.math.Vector2( self.player.collider.getX(), self.player.collider.getY() )
        lastVec = None
        angle = 0
        for laser in lasers :
            if(laser.owner.type == 'PLAYER'):
                break

            if self.IACollider.collides( laser.collider ) : #collision
                vecLaser = pygame.math.Vector2( laser.collider.getX(), laser.collider.getY() )
                angle = (angle + NULLVEC.angle_to(vecPlayer - vecLaser)) * 0.5
                lastVec = vecLaser

        if( angle != 0 ) :
            
            if( angle >= 0 and angle < 90 ) :
                if( angle < 70 and angle > 20 ) :
                    print('down')                 
                    inputs['down'] = True
            
                if( angle < 45 ) :   
                    print(' and right')                 
                    inputs['right'] = True
                else :
                    print(' and right')
                    inputs['left'] = True

            elif( angle >= 90 and angle < 180 ) :
                print('left')                 
                inputs['left'] = True

            elif( angle <= 0 and angle > -90 ) :
                print('right')                 
                inputs['right'] = True

            elif( angle <= -90 and angle > -180 ) :
                print('left')
                inputs['left'] = True
                        
            print( vecPlayer - lastVec)
        
        
         
            

    def isPlayerBelowBoss(self, boss) :
        maxX = 0
        minX = 999999

        padding = 50

        for collider in boss.colliders :  
            maxX = max(maxX, collider.getX() + collider.getWidth())
            minX = min(minX, collider.getX())

        if( self.player.collider.getX() > ( minX - padding )
        and ( self.player.collider.getX() + self.player.collider.getWidth() ) < ( maxX + padding ) ) :
            return True
        return False

    def debug(self, window) :
        self.IACollider.render(window)