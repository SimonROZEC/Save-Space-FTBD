# collider en cercle
import pygame
from math import *

collider_color = (255, 0, 0)

class Collider :
    def __init__(self, parent, radius, offset) :
        self.radius = radius
        self.parent = parent
        self.offset = offset

    def collides(self, other) :
        sp = self.parent.pos + self.offset * self.parent.scale
        op = other.parent.pos + other.offset * other.parent.scale
        return self.radius *self.parent.scale + other.radius * other.parent.scale > hypot(sp.x-op.x, sp.y-op.y)

    def getX(self) :
        return self.parent.pos.x + self.offset.x * self.parent.scale

    def getY(self) :
        return self.parent.pos.y + self.offset.y * self.parent.scale

    def getWidth(self) :
        return self.radius * 2

    def render(self, window) :
        pygame.draw.circle(window, collider_color, (int(self.parent.pos.x + self.offset.x * self.parent.scale ), int(self.parent.pos.y + self.offset.y * self.parent.scale)), int(self.radius * self.parent.scale), 0)