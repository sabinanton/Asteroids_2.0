import math
import pygame
import Constants
import random
import numpy as np

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
        offset = 190000000
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
    trajectory = []
    Engine_fired = False
    Left_stube_fired = False
    Right_stube_fired = False

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
        self.Engine_fired = False
        self.Left_stube_fired = 0
        self.Right_stube_fired = 0
        self.trajectory = []


    def T_accelerate(self, acc, Step):
        self.velocity_x += acc*math.cos(self.tetha + math.pi/2) * Step
        self.velocity_y += acc*math.sin(self.tetha + math.pi/2) * Step
        self.Engine_fired = True
    def a_impulse(self, acc, dir, Step):
        self.velocity_x += -dir * acc * math.cos(self.tetha + math.pi / 2) * Step
        self.velocity_y += -dir * acc * math.sin(self.tetha + math.pi / 2) * Step
        self.Left_stube_fired = dir
        self.Right_stube_fired = dir
    def Rotate(self, dir, shot):
        self.omega += dir*shot
        self.Left_stube_fired = dir
        self.Right_stube_fired = -dir

    def compute_distance(self, object):
        r = math.sqrt((self.pos_y - object.pos_y)**2 + (self.pos_x - object.pos_x)**2)
        theta = math.atan2(self.pos_y - object.pos_y, self.pos_x - object.pos_x)
        self.trajectory.append([r, theta])
        if len(self.trajectory) > 35: self.trajectory.pop(0)

    def compute_trajectory(self):
        if len(self.trajectory) >= 35:
            a = []
            b = []
            tr = self.trajectory
            for i in range(len(tr)):
                a.append([1, tr[i][0]*math.cos(tr[i][1]), tr[i][0]*math.sin(tr[i][1])])
                b.append([tr[i][0]])
            A = np.array(a)
            A_T = np.transpose(A)
            B = np.array(b)
            res = np.linalg.inv(A_T.dot(A)).dot(A_T.dot(B))
            phi = math.atan2(res[2], res[1])
            e = res[1]/(math.cos(phi))
            print(e)
            return [res[0], e, phi]

    def draw_trajectory(self, resolution, screen, scale, x_offset, y_offset, color, samples):
        pts = []
        N = samples
        step = 2*math.pi/N
        trajectory = self.compute_trajectory()
        if trajectory != None:
            for i in range(N):
                r = trajectory[0]/(1 - trajectory[1]*math.cos(i*step-trajectory[2]))
                point = conv(scale, resolution, r*math.cos(i*step), r*math.sin(i*step), x_offset, y_offset)
                pts.append(point)
            pygame.draw.polygon(screen, color, pts, 2)

    def draw(self, resolution, screen, game_scale, x_offset, y_offset, color):
        L_body = 10 * self.scale * game_scale
        D_body = 5 * self.scale * game_scale
        h_top = 2 * self.scale * game_scale
        D_e = 5 * self.scale * game_scale
        l_e = 3 * self.scale * game_scale
        d_tube = 1 * self.scale * game_scale
        l_tube = 2.5 * self.scale * game_scale
        l_stube = 3 * self.scale * game_scale
        blue = (200,200,255)
        t = self.tetha
        body_points = [rotate(-D_body/2, -L_body/2, t), rotate(D_body/2, -L_body/2, t),
                       rotate(D_body/2, L_body/2, t), rotate(-D_body/2, L_body/2, t)]
        thrsuter_points = [rotate(0, L_body/2, t), rotate(-D_e/2, L_body/2 + l_e, t), rotate(D_e/2, L_body/2 + l_e, t)]
        body = []
        pos = conv(game_scale, resolution, self.pos_x, self.pos_y, x_offset, y_offset)
        for i in range(4):
           body.append([pos[0] + body_points[i][0], pos[1] + body_points[i][1]])
        pygame.draw.polygon(screen, color, body, 3)
        thruster = []
        for i in range(3):
            thruster.append([pos[0] + thrsuter_points[i][0], pos[1] + thrsuter_points[i][1]])
        if self.Engine_fired :
            fire_points = [rotate(0, L_body / 2 + l_e*3, t), rotate(-D_e / 4, L_body / 2 + l_e, t),
                               rotate(D_e / 4, L_body / 2 + l_e, t)]
            fire = []
            for i in range(3):
                fire.append([pos[0] + fire_points[i][0], pos[1] + fire_points[i][1]])
            pygame.draw.polygon(screen, blue, fire, 6)
            self.Engine_fired = False
        pygame.draw.polygon(screen, color, thruster, 3)
        left_tube_points = [rotate(-D_body/2, -d_tube/2, t), rotate(-D_body/2, d_tube/2, t),
                            rotate(-D_body/2 - l_tube, d_tube/2, t), rotate(-D_body/2 - l_tube, -d_tube/2, t)]
        left_tube = []
        for i in range(4):
           left_tube.append([pos[0] + left_tube_points[i][0], pos[1] + left_tube_points[i][1]])
        pygame.draw.polygon(screen, color, left_tube, 2)
        right_tube_points = [rotate(D_body / 2, -d_tube / 2, t), rotate(D_body / 2, d_tube / 2, t),
                            rotate(D_body / 2 + l_tube, d_tube / 2, t), rotate(D_body / 2 + l_tube, -d_tube / 2, t)]
        right_tube = []
        for i in range(4):
            right_tube.append([pos[0] + right_tube_points[i][0], pos[1] + right_tube_points[i][1]])
        pygame.draw.polygon(screen, color, right_tube, 2)
        left_stube_points = [rotate(-D_body / 2 - l_tube/2, -l_tube / 2, t),
                             rotate(-D_body / 2 -l_tube/2, l_tube / 2, t),
                            rotate(-D_body / 2 - l_tube/2 - d_tube, l_tube / 2, t),
                             rotate(-D_body / 2 - l_tube/2 - d_tube, -l_tube / 2, t)]
        left_stube = []
        for i in range(4):
           left_stube.append([pos[0] + left_stube_points[i][0], pos[1] + left_stube_points[i][1]])
        pygame.draw.polygon(screen, color, left_stube, 2)
        right_stube_points = [rotate(D_body / 2 + l_tube / 2, -l_tube / 2, t),
                             rotate(D_body / 2 + l_tube / 2, l_tube / 2, t),
                             rotate(D_body / 2 + l_tube / 2 + d_tube, l_tube / 2, t),
                             rotate(D_body / 2 + l_tube / 2 + d_tube, -l_tube / 2, t)]
        right_stube = []
        for i in range(4):
            right_stube.append([pos[0] + right_stube_points[i][0], pos[1] + right_stube_points[i][1]])
        pygame.draw.polygon(screen, color, right_stube, 2)
        if self.Left_stube_fired:
            left_stube_fire_points = [rotate(-D_body / 2 - l_tube/2 - d_tube/2, -self.Left_stube_fired*l_tube / 2, t),
                                rotate(-D_body / 2 - l_tube/2 - d_tube/2 - d_tube/3, -self.Left_stube_fired*l_tube/2*3, t),
                                  rotate(-D_body / 2 - l_tube / 2 - d_tube / 2 + d_tube / 3,
                                         -self.Left_stube_fired * l_tube / 2 * 3, t) ]
            left_stube_fire = []
            for i in range(3):
                left_stube_fire.append([pos[0] + left_stube_fire_points[i][0], pos[1] + left_stube_fire_points[i][1]])
            pygame.draw.polygon(screen, color, left_stube_fire, 3)
            self.Left_stube_fired = 0
        if self.Right_stube_fired:
            right_stube_fire_points = [rotate(D_body / 2 + l_tube/2 + d_tube/2, -self.Right_stube_fired*l_tube / 2, t),
                                rotate(D_body / 2 + l_tube/2 + d_tube/2 + d_tube/3, -self.Right_stube_fired*l_tube/2*3, t),
                                  rotate(D_body / 2 + l_tube / 2 + d_tube / 2 - d_tube / 3,
                                         -self.Right_stube_fired * l_tube / 2 * 3, t) ]
            right_stube_fire = []
            for i in range(3):
                right_stube_fire.append([pos[0] + right_stube_fire_points[i][0], pos[1] + right_stube_fire_points[i][1]])
            pygame.draw.polygon(screen, color, right_stube_fire, 3)
            self.Right_stube_fired = 0