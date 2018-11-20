from math import *
from random import *

from Collider import *
from globaldefines import *

class IAPlayer():
    def __init__(self, player, powerups) :
        self.player = player
        self.powerup = powerups
        self.IACollider = Collider(self.player, 70, pygame.math.Vector2(50, 40))
    


    def processInput(self, boss, lasers, inputs) :
        
        if( self.isPlayerBelowBoss(boss) ) :
            if(self.player.energybar.energy > 0 and boss.shieldcd <= 0 ) :
                inputs['fire'] = True
        else :  
            if ( self.player.vel.length() < 1 and self.player.vel.length() > -1 ) :         
                if ( (boss.colliders[1].getX() - self.player.collider.getX()) > 0 ) :
                    inputs['right'] = True
                else :
                    inputs['left'] = True

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
    #TODO
    # pickup energy
    # when shielded can ignore lasers

        goodPu = None
        for pu in self.powerup :
            if goodPu == None  :
                goodPu = pu
                pass

            if( pu.collider.getY() < 300 ) :
                pass

            #if( pygame.math.Vector2(pu.collider.getX(), pu.collider.getX()).length() < goodPu.collider.get )

        if( angle != 0 ) :
            
            if( angle >= 0 and angle < 90 ) :
                if( angle < 70 and angle > 20 ) :
                    print('down')                 
                    inputs['down'] = True
            
                if( angle < 45 ) :   
                    print(' and right')       
                    inputs['right'] = True
                    inputs['left'] = True if inputs['left'] else False
                else :
                    print(' and right')
                    inputs['left'] = True

            elif( angle >= 90 and angle < 180 ) :
                print('left')                 
                inputs['left'] = True
                inputs['right'] = True if inputs['right'] else False

            elif( angle <= 0 and angle > -90 ) :
                print('right')                 
                inputs['right'] = True
                inputs['left'] = True if inputs['left'] else False

            elif( angle <= -90 and angle > -180 ) :
                print('left')
                inputs['left'] = True
                inputs['right'] = True if inputs['right'] else False
            
            #print( vecPlayer - lastVec)
        
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