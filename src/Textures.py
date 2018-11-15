import pygame
from globaldefines import *

textures = {
            'LASER_PLAYER': [pygame.image.load('./res/Images/Lasers/laserGreen' + str(i) + '.png').convert_alpha() for i in range(3, 4)],
            'LASER_ENEMY': [pygame.image.load('./res/Images/Lasers/laserRed' + str(i) + '.png').convert_alpha() for i in range(3, 4)],
            'LASER_PLAYER_EXPLOSION' : [pygame.image.load('./res/Images/Lasers/expGreen' + str(i) + '.png').convert_alpha() for i in range(1, 5)],
            'LASER_ENEMY_EXPLOSION' : [pygame.image.load('./res/Images/Lasers/laserRed' + str(i) + '.png').convert_alpha() for i in range(21, 25)],
            'PLAYER_SHIP' : pygame.image.load('./res/Images/playerShip1_green.png').convert_alpha(),
            'PLAYER_THRUSTER' : [pygame.image.load('./res/Images/Effects/fire' + str(i) + '.png').convert_alpha() for i in range(15, 18)],
            'PLAYER_LIFE_ICON' : pygame.image.load('./res/Images/UI/playerLife1_green.png').convert_alpha(),
            'BACKGROUND' : pygame.image.load('./res/Images/Background/darkPurple.png').convert(),
            'MINIBOSS_SHIP' : pygame.image.load('./res/Images/Enemies/miniboss.png').convert_alpha(),
            'BOSS_SHIP' : pygame.image.load('./res/Images/Enemies/boss.png').convert_alpha()
        }

#approx
texturesOffsets = {
    'LASER_PLAYER':             (4.5, 0),
    'LASER_ENEMY':              (4.5, 0),
    'LASER_PLAYER_EXPLOSION' :  (5, 5),
    'LASER_ENEMY_EXPLOSION' :   (0, 0),
    'PLAYER_SHIP' :             (50, 38),
    'PLAYER_THRUSTER' :         (0, 0),
    'PLAYER_LIFE_ICON' :        (0, 0),
    'BACKGROUND' :              (128, 128),
    'MINIBOSS_SHIP' :           (80, 60),
    'BOSS_SHIP' :               (0, 0),
}

def drawTexture(window, texture, posXY) :
    window.blit(texture, posXY)

def createTextTexture(text, fontPath, fontSize, color) :
    font = pygame.font.Font(fontPath, fontSize)
    texture = font.render(text, True, color)
    return texture
