# collider en cercle
import pygame
from math import *

collider_color = (255, 0, 0)

class Collider :
    def __init__(self, parent, radius, offset) :
        self.radius = radius
        self.parent = parent
        self.offset = offset

    def colliding(self, other) :
        sp = self.parent.pos + self.offset
        op = other.parent.pos + other.offset
        return self.radius + other.radius < math.hypot(sp.x-op.x, sp.y-op.y)

    def render(self, window) :
        pygame.draw.circle(window, collider_color, (int(self.parent.pos.x + self.offset.x), int(self.parent.pos.y + self.offset.y)), int(self.radius), 0)