import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        self.pos = pygame.math.Vector2(400, 300)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)

        self.image = pygame.image.load('./Images/playerShip1_green.png')

    def update(self, keys) :
        if keys['up'] :
            self.acc.y -= 0.04
        elif keys['down'] :
            self.acc.y += 0.04
        else :
            self.acc.y = 0
            self.vel *= 0.9

        self.vel += self.acc

        if self.vel.length() > 5 :
            self.vel.scale_to_length(5)

        self.pos += self.vel

        

    def render(self, window) :
        window.blit(self.image, self.pos)
        