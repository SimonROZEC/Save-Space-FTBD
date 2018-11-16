from Textures import *

class BossLifeBar(pygame.sprite.Sprite):
    def __init__(self, lifeCount, lifeBarEnabeled = True) :
        pygame.sprite.Sprite.__init__(self)
        self.life = lifeCount
        self.maxLife = 1.0/self.life
        self.icon = textures['PLAYER_LIFE_ICON']
        self.lifeBarEnabeled = True

        self.takingDamageAnim = 0

    def remove_life(self, damage) :
        if self.life > 0 :
            self.life -= damage
            self.takingDamageAnim = 2

    def render(self, window) :
        if(self.lifeBarEnabeled) :
            drawRoundedRect(window,(0, 0, WIDTH, 10),(50, 50, 50),0.5)
            drawRoundedRect(window,(0,4,WIDTH,6),(255,0,0),0.5)
            # pygame.draw.rect(window, (255, 0, 0), [0, 2, WIDTH, 10])
            if(self.takingDamageAnim > 0) :
                # pygame.draw.rect(window, (255, 255, 255), [0, 2, WIDTH, 10])
                drawRoundedRect(window,(0, 2, WIDTH, 10),(255, 255, 255),0.5)
                self.takingDamageAnim -= 1
            else :
                drawRoundedRect(window,(0, 4, WIDTH*(self.life*self.maxLife), 6),(0, 200, 0),0.5)
                # pygame.draw.rect(window, (0, 255, 0), [0, 2, WIDTH*(self.life*self.maxLife), 10])
            
            # pygame.draw.rect(window, (0, 0, 0), [0, 2, WIDTH, 10], 3)

            