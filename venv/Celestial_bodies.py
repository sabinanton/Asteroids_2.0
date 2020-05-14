import math
import pygame
import Constants
import random

def conv(scale, res, x, y, x_offset, y_offset):
    return (int(scale*x+res[0]/2 + x_offset), int(res[1]/2-scale*y + y_offset))

def rotate(x, y, tetha):
    return [int(x*math.cos(-tetha) - y*math.sin(-tetha)), int(x*math.sin(-tetha) + y*math.cos(-tetha))]

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

    def draw(self, resolution, screen, x_offset, y_offset, scale, color):
        pos = conv(scale, resolution, self.pos_x, self.pos_y, x_offset, y_offset)
        pygame.draw.circle(screen, color, pos, max(2,int(self.Radius*scale)), min(2,int(self.Radius*scale)))

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
    tetha = 0
    omega = 0
    Points = []

    def __init__(self, name, m, r, x, y, vx, vy, tetha, omega):
        self.Name = name
        self.Mass = m
        self.Radius = r
        self.pos_x = x
        self.pos_y = y
        self.velocity_x = vx
        self.velocity_y = vy
        self.tetha = tetha
        self.omega = omega
        self.Points = self.generatePoints()

    def generatePoints(self):
        points = []
        offset = 80000000
        n_of_points = random.randint(5, 16)
        angle_step = 2 * math.pi / n_of_points
        for i in range(n_of_points):
            r = self.Radius + random.randint(-offset, +offset)
            gamma = i * angle_step + random.uniform(-0.35, 0.35) + self.tetha
            point = [r * math.cos(gamma), r * math.sin(gamma)]
            points.append(point)
        return points

    def draw(self, resolution, screen, x_offset, y_offset, scale, color):
        pts = []
        white = (255, 255, 255)
        for i in range(len(self.Points)):
            t = self.tetha
            pts.append(conv(scale, resolution, self.Points[i][0]*math.cos(t)-self.Points[i][1]*math.sin(t) + self.pos_x, self.Points[i][1]*math.cos(t)+self.Points[i][0]*math.sin(t) + self.pos_y, x_offset, y_offset))

        pygame.draw.polygon(screen, color, pts, 3)

class SpaceShip:
    Name = 'Planet'
    Mass = 0
    Radius = 0
    pos_x = 0
    pos_y = 0
    velocity_x = 0
    velocity_y = 0
    acceleration_x = 0
    acceleration_y = 0
    tetha = 0
    omega = 0
    scale = 1

    def __init__(self, name, m, x, y, vx, vy, tetha, omega, scale):
        self.Name = name
        self.Mass = m
        self.pos_x = x
        self.pos_y = y
        self.velocity_x = vx
        self.velocity_y = vy
        self.tetha = tetha
        self.omega = omega
        self.scale = scale


    def T_accelerate(self, acc, Step):
        self.velocity_x += acc*math.cos(self.tetha + math.pi/2) * Step
        self.velocity_y += acc*math.sin(self.tetha + math.pi/2) * Step
    def Rotate(self, dir, shot):
        self.tetha += dir*shot

    def draw(self, resolution, screen, game_scale, x_offset, y_offset, color):
        L_body = 10 * self.scale * game_scale
        D_body = 5 * self.scale * game_scale
        h_top = 2 * self.scale * game_scale
        D_e = 5 * self.scale * game_scale
        l_e = 2 * self.scale * game_scale
        d_tube = 1 * self.scale * game_scale
        l_tube = 2.5 * self.scale * game_scale
        l_stube = 3 * self.scale * game_scale
        t = self.tetha
        body_points = [rotate(-D_body/2, -L_body/2, t), rotate(D_body/2, -L_body/2, t), rotate(D_body/2, L_body/2, t), rotate(-D_body/2, L_body/2, t)]
        body = []
        pos = conv(game_scale, resolution, self.pos_x, self.pos_y, x_offset, y_offset)
        for i in range(4):
           body.append([pos[0] + body_points[i][0], pos[1] + body_points[i][1]])
        pygame.draw.polygon(screen, color, body, 3)