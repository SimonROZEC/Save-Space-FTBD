from math import *
from random import *

from Collider import *
from globaldefines import *

class IAPlayer():
    def __init__(self, player, powerups) :
        self.player = player
        self.powerup = powerups
        self.IACollider = Collider(self.player, 75, pygame.math.Vector2(50, 40))
        self.inputsDelays = {
            'up'   : 0,
            'down' : 0,
            'left' : 0,
            'right': 0,
            'fire' : 0
        }

    def smallStep(self, keysCode, delay, pressed) :
        self.inputsDelays['up'] = self.inputsDelays[keysCode] - 1
        self.inputsDelays['down'] = self.inputsDelays[keysCode] - 1
        self.inputsDelays['left'] = self.inputsDelays[keysCode] - 1
        self.inputsDelays['right'] = self.inputsDelays[keysCode] - 1
        self.inputsDelays['fire'] = self.inputsDelays[keysCode] - 1

        print(keysCode)
        print(self.inputsDelays[keysCode])

        if(( self.inputsDelays[keysCode] < 0 and pressed) or delay == 0 ) :
            self.inputsDelays[keysCode] = delay
            return True
        return False

    def processInput(self, boss, lasers, inputs) :
        
        if( self.isPlayerBelowBoss(boss) ) :
            if(self.player.energybar.energy > 10 and boss.shieldcd <= 0 ) :          
                inputs['fire'] = True
        else :  
            if ( self.player.vel.length() < 5 and self.player.vel.length() > -5 ) :         
                if ( (boss.colliders[1].getX() - self.player.collider.getX()) > 0 ) :
                    inputs['right'] = self.smallStep('right', 2, True)
                else :
                    inputs['left'] = self.smallStep('left', 2, True)
        
        if( self.player.pos.y > (boss.pos.y + 450) ) :
            inputs['up'] = self.smallStep('up', 10, True)
        elif( self.player.pos.y < (boss.pos.y + 400) and (self.player.pos.y < (HEIGHT - 100)) ) :
            inputs['down'] = self.smallStep('down', 0, True)

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
            if goodPu == None :
                goodPu = pu
                pass

            if pu.collider.getY() < 300 :
                pass

            #if( pygame.math.Vector2(pu.collider.getX(), pu.collider.getX()).length() < goodPu.collider.get )
        defaultDelay = 15
        if( angle != 0 ) :
            
            if( angle >= 0 and angle < 90 ) :
                if( angle < 70 and angle > 20 ) :
                    print('down')          
                    inputs['down'] = self.smallStep('down', defaultDelay, True);
            
                if( angle < 45 ) :   
                    print(' and right')                           
                    inputs['right'] = self.smallStep('right', defaultDelay, True);
                    inputs['left'] = False if inputs['right'] else inputs['left']

                else :
                    print(' and left')
                    inputs['left'] = self.smallStep('left', defaultDelay, True);
                    inputs['right'] = False if inputs['left'] else inputs['right']

            elif( angle >= 90 and angle < 180 ) :
                print('left')                 
                inputs['left'] = self.smallStep('left', defaultDelay, True);
                inputs['right'] = False if inputs['left'] else inputs['right']

            elif( angle <= 0 and angle > -90 ) :
                print('right')                 
                inputs['right'] = self.smallStep('right', defaultDelay, True);
                inputs['left'] = False if inputs['right'] else inputs['left']

            elif( angle <= -90 and angle > -180 ) :
                print('left')
                inputs['left'] = self.smallStep('left', defaultDelay, True);
                inputs['right'] = False if inputs['left'] else inputs['right']

            
            #print( vecPlayer - lastVec)
        
    def isPlayerBelowBoss(self, boss) :
        maxX = 0
        minX = 999999

        padding = 25

        for collider in boss.colliders :  
            maxX = max(maxX, collider.getX() + collider.getWidth())
            minX = min(minX, collider.getX())

        if( self.player.collider.getX() > ( minX - padding )
        and ( self.player.collider.getX() + self.player.collider.getWidth() ) < ( maxX + padding ) ) :
            return True
        return False

    def debug(self, window) :
        self.IACollider.render(window)