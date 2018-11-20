import pygame

#defines
WIDTH = 600
HEIGHT = 800
FPS = 60

CENTERX = WIDTH*0.5
CENTERY = HEIGHT*0.5

NULLVEC = pygame.math.Vector2(0, 0)

#strange aliases
try:
    xrange
except NameError:
    xrange = range

# methode securise pour lerp un point
def target_point(start, target, speed) :
    d = (target - start) * speed
    if d.length() < 2 :
        if dist_to_point(start, target) < 2 :
            return target
        else :
            d.scale_to_length(2)
    return start + d


def dist_to_point(start, target) :
    return (target-start).length()