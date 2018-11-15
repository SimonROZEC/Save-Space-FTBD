import pygame

images = {
    'LASER_PLAYER': [pygame.image.load('./res/Images/Lasers/laserGreen' + str(i) + '.png').convert_alpha() for i in range(0, 4)],
    'LASER_ENEMY': [pygame.image.load('./res/Images/Lasers/laserRed' + str(i) + '.png').convert_alpha() for i in range(0, 4)],
    'LASER_PLAYER_EXPLOSION' : [pygame.image.load('./res/Images/Lasers/expGreen' + str(i) + '.png').convert_alpha() for i in range(1, 5)],
    'LASER_ENEMY_EXPLOSION' : [pygame.image.load('./res/Images/Lasers/laserRed' + str(i) + '.png').convert_alpha() for i in range(21, 25)],
    'PLAYER_SHIP' : pygame.image.load('./res/Images/playerShip1_green.png').convert_alpha(),
    'PLAYER_THRUSTER' : [pygame.image.load('./res/Images/Effects/fire' + str(i) + '.png').convert_alpha() for i in range(15, 18)],
    'PLAYER_LIFE_ICON' : pygame.image.load('./res/Images/UI/playerLife1_green.png').convert_alpha(),
    'BACKGROUND' : pygame.image.load('./res/Images/Background/darkPurple.png').convert(),
    'MINIBOSS_SHIP' : pygame.image.load('./res/Images/Enemies/miniboss.png').convert_alpha(),
    'BOSS_SHIP' : pygame.image.load('./res/Images/Enemies/boss.png').convert_alpha()
}