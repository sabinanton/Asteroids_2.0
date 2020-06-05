import math
import pygame
import Constants
import random
import numpy as np
import  collections

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

    def __init__(self, name, m, r, x, y, vx, vy, tetha, omega, type):
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
        self.Type = type
        self.white = (255,255,255)
        self.blue = (150, 150, 255)
        self.red = (255, 130, 100)
        self.map_white = (150, 150, 150)
        self.black = (0, 0, 0)
        self.green = (30, 255, 30)
        self.yellow = (255, 255, 0)
        self.content = random.randint(50,200)
        self.capacity = self.content

    def accelerate(self, ax, ay, ang,  step):
        self.velocity_x += ax * step
        self.velocity_y += ay * step
        self.omega += ang * step
        #self.pos_x += self.velocity_x * step
        #self.pos_y += self.velocity_y * step
        #self.tetha += self.omega * step

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
        if color == None:
            if self.Type == "normal": color = self.white
            if self.Type == "normal_map": color = self.map_white
            if self.Type == "minerals": color = self.blue
            if self.Type == "rare_gases": color = self.green
        white = (255, 255, 255)
        for i in range(len(self.Points)):
            t = self.tetha
            pts.append(conv(scale, resolution, self.Points[i][0]*math.cos(t)-self.Points[i][1]*math.sin(t) + self.pos_x, self.Points[i][1]*math.cos(t)+self.Points[i][0]*math.sin(t) + self.pos_y, x_offset, y_offset))

        try: pygame.draw.polygon(screen, color, pts, 3)
        except : "TypeError: points must be number pairs"

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
    Number_of_missiles = 3
    missiles = collections.deque([])
    laser_length = 0
    Left_stube_fired = False
    Right_stube_fired = False
    Laser_fired = False

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
        self.Number_of_missiles = 30
        self.blackhole = 1
        self.missiles = []
        self.laser_length = 0
        self.Laser_fired = False
        self.collision = False
        self.health = 100
        self.deltaV = 10000
        self.Radius = 6.5 * self.scale
        self.hangar_angle = 60 * math.pi / 180
        self.hangar_open = False
        self.Minerals = 0
        self.Rare_Gases = 0
        self.Minerals_Capacity = 1000
        self.Rare_Gases_Capacity = 1000
        self.Laser_power = 100
        self.velocity = math.sqrt(self.velocity_x**2+self.velocity_y**2)
        self.acceleration = math.sqrt(self.acceleration_x**2 + self.acceleration_y**2)


    def T_accelerate(self, Thrust, Step):
        acc = Thrust / self.Mass
        if self.deltaV > 0:
            self.velocity_x += acc*math.cos(self.tetha + math.pi/2) * Step
            self.velocity_y += acc*math.sin(self.tetha + math.pi/2) * Step
            self.Engine_fired = True
            self.Mass -= 50
    def a_impulse(self, Thrust, dir, Step):
        acc = Thrust / self.Mass
        if self.deltaV > 0:
            self.velocity_x += -dir * acc * math.cos(self.tetha + math.pi / 2) * Step
            self.velocity_y += -dir * acc * math.sin(self.tetha + math.pi / 2) * Step
            self.Left_stube_fired = dir
            self.Right_stube_fired = dir
            self.Mass -= 10
    def Rotate(self, dir, Thrust):
        shot = Thrust * 5 * self.scale / self.Mass
        if self.deltaV > 0:
            self.omega += dir*shot
            self.Left_stube_fired = dir
            self.Right_stube_fired = -dir
    def fire_missile(self, speed):
        if self.Number_of_missiles:
            t = self.tetha + math.pi/2
            x = self.pos_x + self.scale*3*math.cos(t)
            y = self.pos_y + 3*self.scale*math.sin(t)
            vx = self.velocity_x + speed*math.cos(t)
            vy = self.velocity_y + speed*math.sin(t)
            missile = Missile(x, y, vx, vy, self.tetha + math.pi, self.scale*1)
            self.missiles.append(missile)
            self.Number_of_missiles -= 1

    def compute_trajectory(self, object):
        v = math.sqrt((self.velocity_x)**2 + (self.velocity_y)**2)
        r = math.sqrt((self.pos_x)**2 + (self.pos_y)**2)
        H = (self.pos_x - object.pos_x) * (self.velocity_y) - \
            (self.pos_y - object.pos_y) * (self.velocity_x)
        gamma = math.atan2(self.velocity_y, self.velocity_x) - math.atan2(self.pos_y, self.pos_x)
        v_r = v*math.cos(gamma)
        v_t = abs(v*H/(v*r))
        p = (H)**2/(Constants.m_sun*Constants.G)
        v0 = math.sqrt(Constants.G * Constants.m_sun/p)
        theta = math.atan2(v_r/v0, v_t/v0 - 1)

        e = (v_t/v0 - 1)/math.cos(theta)

        if H<0: theta = -theta
        phi = math.atan2((self.pos_y), (self.pos_x)) - theta + math.pi
        return [p, e, phi]

    def draw_trajectory(self, resolution, screen, scale, x_offset, y_offset, color, samples, object):
        pts = []
        N = samples
        step = 2*math.pi/N
        trajectory = self.compute_trajectory(object)
        if trajectory != None:
            for i in range(N):
                r = abs(trajectory[0]/(1 - trajectory[1]*math.cos(i*step - trajectory[2])))
                gamma = math.atan2(self.pos_y, self.pos_x)
                point = conv(scale, resolution, r*math.cos(i*step), r*math.sin(i*step), x_offset, y_offset)
                pts.append(point)
        try: pygame.draw.polygon(screen, color, pts, 1)
        except: "TypeError: points must be number pairs"


    def draw(self, resolution, screen, game_scale, x_offset, y_offset, color):
        L_body = 10 * self.scale * game_scale
        D_body = 5 * self.scale * game_scale
        h_top = 2 * self.scale * game_scale
        D_e = 5 * self.scale * game_scale
        l_e = 3 * self.scale * game_scale
        d_tube = 1 * self.scale * game_scale
        l_tube = 2.5 * self.scale * game_scale
        l_stube = 3 * self.scale * game_scale
        hangar_door = int(3 * self.scale * game_scale)
        blue = (200,200,255)
        t = self.tetha
        laser_start_point = rotate(0, -L_body/2, t)
        body_points = [rotate(-D_body/2, -L_body/2, t), rotate(D_body/2, -L_body/2, t),
                       rotate(D_body/2, L_body/2, t), rotate(-D_body/2, L_body/2, t)]
        thrsuter_points = [rotate(0, L_body/2, t), rotate(-D_e/2, L_body/2 + l_e, t), rotate(D_e/2, L_body/2 + l_e, t)]
        body = []
        pos = conv(game_scale, resolution, self.pos_x, self.pos_y, x_offset, y_offset)

        if self.Laser_power>0:
            laser_start = [pos[0] + laser_start_point[0], pos[1] + laser_start_point[1]]
            l = self.laser_length * game_scale
            T = -(t + math.pi/2)
            if self.laser_length !=0 :pygame.draw.line(screen, color, laser_start,
                                                [int(laser_start[0] + l * math.cos(T)), int(laser_start[1] + l * math.sin(T))])


        #self.laser_length = 0
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
        hangar_door_1_points = [[0,0], rotate(0, hangar_door, self.hangar_angle)]
        hangar_door_2_points = [[0,0], rotate(0, hangar_door, math.pi + self.hangar_angle)]
        hangar_door_1 = [rotate(-D_body/2 + hangar_door_1_points[0][0], -L_body/2 - hangar_door_1_points[0][1], t),
                         rotate(-D_body/2 + hangar_door_1_points[1][0], -L_body/2 - hangar_door_1_points[1][1], t)]
        hangar_door_2 = [rotate(D_body / 2 + hangar_door_2_points[0][0], -L_body / 2 + hangar_door_2_points[0][1], t),
                         rotate(D_body / 2 + hangar_door_2_points[1][0], -L_body / 2 + hangar_door_2_points[1][1], t)]
        h1 = []
        h2 = []
        for i in range(2):
            h1.append([pos[0] + hangar_door_1[i][0], pos[1] + hangar_door_1[i][1]])
            h2.append([pos[0] + hangar_door_2[i][0], pos[1] + hangar_door_2[i][1]])
        if self.hangar_open:
            if self.hangar_angle > -60 * math.pi / 180:
                self.hangar_angle -= 3 * math.pi / 180
        else:
            if self.hangar_angle < 60 * math.pi / 180:
                self.hangar_angle += 3 * math.pi / 180
        pygame.draw.line(screen, color, h1[0], h1[1], 4)
        pygame.draw.line(screen, color, h2[0], h2[1], 4)
            

class Missile:
    Name = 'Planet'
    Mass = 0
    pos_x = 0
    pos_y = 0
    velocity_x = 0
    velocity_y = 0
    acceleration_x = 0
    acceleration_y = 0
    tetha = 0
    omega = 0
    scale = 1

    def __init__(self, pos_x, pos_y, v_x, v_y, tetha, scale):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.velocity_x = v_x
        self.velocity_y = v_y
        self.tetha = tetha
        self.omega = 0
        self.acceleration_x = 0
        self.acceleration_y = 0
        self.Mass = 400000
        self.scale = scale
        self.Radius = 500000

    def draw(self, resolution, screen, game_scale, x_offset, y_offset, color):
        t = self.tetha
        L_body = 5*game_scale*self.scale
        W_body = 1*game_scale*self.scale
        body_points = [rotate(-W_body / 2, -L_body / 2, t), rotate(W_body / 2, -L_body / 2, t),
                       rotate(W_body / 2, L_body / 2, t), rotate(0, L_body / 2 * 1.4, t), rotate(-W_body / 2, L_body / 2, t)]
        body = []
        pos = conv(game_scale, resolution, self.pos_x, self.pos_y, x_offset, y_offset)
        for i in range(5):
            body.append([pos[0] + body_points[i][0], pos[1] + body_points[i][1]])
        try: pygame.draw.polygon(screen, color, body, 3)
        except: "TypeError: points must be number pairs"

class Particle:
    life = 0
    pos_x = 0
    pos_y = 0
    velocity_x = 0
    velocity_y = 0
    acceleration_x = 0
    acceleration_y = 0

    def __init__(self, life, pos_x, pos_y, v_x, v_y, type):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.velocity_x = v_x
        self.velocity_y = v_y
        self.acceleration_x = 0
        self.acceleration_y = 0
        self.life = life
        self.Type = type
        self.white = (255, 255, 255)
        self.blue = (150, 150, 255)
        self.red = (255, 130, 100)
        self.map_white = (150, 150, 150)
        self.black = (0, 0, 0)
        self.green = (30, 255, 30)
        self.yellow = (255, 255, 0)

    def draw(self, resolution, screen, game_scale, x_offset, y_offset, color):
        if color == None:
            if self.Type == "normal": color = self.white
            if self.Type == "normal_map": color = self.map_white
            if self.Type == "minerals": color = self.blue
            if self.Type == "rare_gases": color = self.green
        p = conv(game_scale, resolution, self.pos_x, self.pos_y, x_offset, y_offset)
        try: 
            if self.life >0 : pygame.draw.circle(screen, color, [p[0], p[1]], 1, 1)
        except: "OverflowError: Python int too large to convert to C long"

class BlackHole:
    Mass = 0
    pos_x = 0
    pos_y = 0
    bake_time = 5000
    Radius = 0

    def __init__(self, x, y, mass, radius):
        self.pos_x = x
        self.pos_y = y
        self.velocity_x = 0
        self.velocity_y = 0
        self.acceleration_x = 0
        self.acceleration_y = 0
        self.Mass = mass
        self.Radius = radius
        self.bake_time = 200

    def draw(self, resolution, screen, game_scale, x_offset, y_offset, color):
        p = conv(game_scale, resolution, self.pos_x, self.pos_y, x_offset, y_offset)
        try:
            pygame.draw.circle(screen, color, [p[0], p[1]], max(2,int(self.Radius * game_scale)), 1)
        except:
            "OverflowError: Python int too large to convert to C long"