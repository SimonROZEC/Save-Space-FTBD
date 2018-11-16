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
            'PLAYER_ENERGY_ICON' : pygame.transform.scale(pygame.image.load('./res/Images/Lasers/laserBlue04.png').convert_alpha(), (13, 26)),
            'BACKGROUND' : pygame.image.load('./res/Images/Background/darkPurple.png').convert(),
            'MINIBOSS_SHIP' : pygame.image.load('./res/Images/Enemies/miniboss.png').convert_alpha(),
            'BOSS_SHIP' : pygame.image.load('./res/Images/Enemies/boss.png').convert_alpha(),
            'PU_ENERGY' : pygame.image.load('./res/Images/Power-ups/powerupGreen_bolt.png').convert_alpha(),
            'PU_HEALTH' : pygame.image.load('./res/Images/Power-ups/powerupGreen_health.png').convert_alpha(),
            'PU_SHIELD' : pygame.image.load('./res/Images/Power-ups/powerupGreen_shield.png').convert_alpha(),
            'PU_PARTICLE' : [pygame.image.load('./res/Images/Effects/star' + str(i) + '.png').convert_alpha() for i in range(1, 4)],
            'SHIELD' : [pygame.image.load('./res/Images/Effects/shield' + str(i) + '.png').convert_alpha() for i in range(1, 4)],
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
    'BOSS_SHIP' :               (128, 113),
    'PU' :                      (17, 17),
    'PU_PARTICLE' :             (12, 12),
    'SHIELD' :                  (144 * 0.5, 137 * 0.5)
}

def drawTexture(window, texture, posXY) :
    window.blit(texture, posXY)

def createTextTexture(text, fontPath, fontSize, color) :
    font = pygame.font.Font(fontPath, fontSize)
    texture = font.render(text, True, color)
    return texture

def blit_alpha(target, source, location, opacity):
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)        
    target.blit(temp, location)

def drawRoundedRect(surface,rect,color,radius=0.4):
    rect         = pygame.Rect(rect)
    color        = pygame.Color(*color)
    alpha        = color.a
    color.a      = 0
    pos          = rect.topleft
    rect.topleft = 0,0
    rectangle    = pygame.Surface(rect.size,pygame.SRCALPHA)
    circle       = pygame.Surface([min(rect.size)*3]*2,pygame.SRCALPHA)
    pygame.draw.ellipse(circle,(0,0,0),circle.get_rect(),0)
    circle       = pygame.transform.smoothscale(circle,[int(min(rect.size)*radius)]*2)
    radius              = rectangle.blit(circle,(0,0))
    radius.bottomright  = rect.bottomright
    rectangle.blit(circle,radius)
    radius.topright     = rect.topright
    rectangle.blit(circle,radius)
    radius.bottomleft   = rect.bottomleft
    rectangle.blit(circle,radius)
    rectangle.fill((0,0,0),rect.inflate(-radius.w,0))
    rectangle.fill((0,0,0),rect.inflate(0,-radius.h))
    rectangle.fill(color,special_flags=pygame.BLEND_RGBA_MAX)
    rectangle.fill((255,255,255,alpha),special_flags=pygame.BLEND_RGBA_MIN)
    return surface.blit(rectangle,pos)