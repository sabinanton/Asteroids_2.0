import math
import pygame
import Constants

def conv(res, x, y):
    return (int(Constants.scale*x+res[0]/2), int(res[1]/2-Constants.scale*y))


class Planet:
    Name = 'Planet'
    Mass = 0
    Radius = 0
    pos_x = 0
    pos_y = 0
    velocity_x = 0
    velocity_y = 0
    acceleration_x = 0
    acceleration_y = 0
    def __init__(self, name, m, r, x, y, vx, vy):
        self.Name = name
        self.Mass = m
        self.Radius = r
        self.pos_x = x
        self.pos_y = y
        self.velocity_x = vx
        self.velocity_y = vy

    def draw(self, resolution, screen):
        pos = conv(resolution, self.pos_x, self.pos_y)
        pygame.draw.circle(screen, (255, 255, 255), pos, int(self.Radius*Constants.scale), min(2,int(self.Radius*Constants.scale)))

class Asteroid:
    Name = 'Planet'
    Mass = 0
    Radius = 0
    pos_x = 0
    pos_y = 0
    velocity_x = 0
    velocity_y = 0
    acceleration_x = 0
    acceleration_y = 0

    def __init__(self, name, m, r, x, y, vx, vy):
        self.Name = name
        self.Mass = m
        self.Radius = r
        self.pos_x = x
        self.pos_y = y
        self.velocity_x = vx
        self.velocity_y = vy

    def draw(self, resolution, screen):
        pos = conv(resolution, self.pos_x, self.pos_y)
        pygame.draw.circle(screen, (255, 255, 255), pos, int(self.Radius * Constants.scale),
                           min(2, int(self.Radius * Constants.scale)))