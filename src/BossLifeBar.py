from Textures import *

class BossLifeBar(pygame.sprite.Sprite):
    def __init__(self, owner, lifeCount, lifeBarEnabeled = True) :
        pygame.sprite.Sprite.__init__(self)
        self.owner = owner
        self.life = lifeCount
        self.maxLife = 1.0/self.life
        self.icon = textures['PLAYER_LIFE_ICON']
        self.lifeBarEnabeled = True

        self.takingDamageAnim = 0
        self.red = (172,57,57)
        self.green = (113, 201, 55)
        if owner.type == 'ASTEROIDS' :
          self.green = (62,136,161)
          self.red = (161, 161, 161)
        
    def remove_life(self, damage) :
        if self.life > 0 :
            self.life -= damage
            self.takingDamageAnim = 2
            if self.life <= 0 :
                self.life = 1

    def isDead(self) :
      return self.life <= 1

    def render(self, window) :

        if(self.lifeBarEnabeled) :
            drawRoundedRect(window,(0, 0, WIDTH, 24),(72, 72, 72),0.25)
            drawRoundedRect(window,(4,4,WIDTH-8,16),self.red,0.75)
            # pygame.draw.rect(window, (255, 0, 0), [0, 2, WIDTH, 10])
            if(self.takingDamageAnim > 0) :
                # pygame.draw.rect(window, (255, 255, 255), [0, 2, WIDTH, 10])
                drawRoundedRect(window,(0, 0, WIDTH, 24),(255, 255, 255),0.25)
                self.takingDamageAnim -= 1
            else :
                drawRoundedRect(window,(4, 4, (WIDTH-8)*(self.life*self.maxLife), 16),self.green,0.75)
                # pygame.draw.rect(window, (0, 255, 0), [0, 2, WIDTH*(self.life*self.maxLife), 10])
            
            # pygame.draw.rect(window, (0, 0, 0), [0, 2, WIDTH, 10], 3)

            