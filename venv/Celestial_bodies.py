import math
import pygame
import Constants
import random

def conv(res, x, y, x_offset, y_offset):
    return (int(Constants.scale*x+res[0]/2 + x_offset), int(res[1]/2-Constants.scale*y + y_offset))


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

    def draw(self, resolution, screen, x_offset, y_offset):
        pos = conv(resolution, self.pos_x, self.pos_y, x_offset, y_offset)
        pygame.draw.circle(screen, (255, 255, 255), pos, max(2,int(self.Radius*Constants.scale)), min(2,int(self.Radius*Constants.scale)))

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
    Points = []

    def __init__(self, name, m, r, x, y, vx, vy):
        self.Name = name
        self.Mass = m
        self.Radius = r
        self.pos_x = x
        self.pos_y = y
        self.velocity_x = vx
        self.velocity_y = vy
        self.Points = self.generatePoints()

    def generatePoints(self):
        points = []
        offset = 2000
        n_of_points = random.randint(3, 12)
        angle_step = 2 * math.pi / n_of_points
        for i in range(n_of_points):
            r = self.Radius + random.randint(-offset, +offset)
            gamma = i * angle_step + random.uniform(-0.5, 0.5)
            point = [r * math.cos(gamma), r * math.sin(gamma)]
            points.append(point)
        return points

    def draw(self, resolution, screen, x_offset, y_offset):
        pts = []
        white = (255, 255, 255)
        for i in range(len(self.Points)):
            pts.append(conv(resolution, self.Points[i][0] + self.pos_x, self.Points[i][1] + self.pos_y, x_offset, y_offset))

        pygame.draw.polygon(screen, white, pts, 3)