import math
import Celestial_bodies
import Constants
import random
import collections
import pygame


def distance(x1, y1, x2, y2):
    return math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)


def angle(x1, y1, x2, y2):
    return math.atan2(y2 - y1, x2 - x1)


class Simulation:
    step = 0.1
    planetList = []
    asteroidList = []

    def __init__(self, pList, aList, Spaceship, stp):
        self.step = stp
        self.planetList = pList
        self.asteroidList = aList
        self.particleList = []
        self.Spaceship = Spaceship
        self.blackhole = None

    def updatePlanet(self, body, ax, ay, Step):
        if body != self.blackhole and body != self.planetList[0]:
            vx = body.velocity_x + ax*Step
            vy = body.velocity_y + ay*Step
            x = body.pos_x + vx*Step
            y = body.pos_y + vy*Step
            body.acceleration_x = ax
            body.acceleration_y = ay
            body.velocity_x = vx
            body.velocity_y = vy
            body.pos_x = x
            body.pos_y = y

    def updateAsteroid(self, body, ax, ay, omega, Step):
        vx = body.velocity_x + ax*Step
        vy = body.velocity_y + ay*Step
        x = body.pos_x + vx*Step
        y = body.pos_y + vy*Step
        body.tetha = body.tetha + (omega+body.omega)*Step
        body.acceleration_x = ax
        body.acceleration_y = ay
        body.velocity_x = vx
        body.velocity_y = vy
        body.pos_x = x
        body.pos_y = y

    def updateSpaceShip(self, body, ax, ay, omega, Step):
        vx = body.velocity_x + ax * Step
        vy = body.velocity_y + ay * Step
        x = body.pos_x + vx * Step
        y = body.pos_y + vy * Step
        body.tetha = body.tetha + (omega + body.omega) * Step
        if body.tetha > 2 * math.pi: body.tetha -= 2 * math.pi
        if body.tetha < 0: body.tetha += 2 * math.pi
        body.acceleration_x = ax
        body.acceleration_y = ay
        body.velocity_x = vx
        body.velocity_y = vy
        body.pos_x = x
        body.pos_y = y

    def updateMissile(self, body, ax, ay, omega, Step):
        vx = body.velocity_x + ax * Step
        vy = body.velocity_y + ay * Step
        x = body.pos_x + vx * Step
        y = body.pos_y + vy * Step
        body.tetha = body.tetha + (omega + body.omega) * Step
        body.acceleration_x = ax
        body.acceleration_y = ay
        body.velocity_x = vx
        body.velocity_y = vy
        body.pos_x = x
        body.pos_y = y

    def updateParticle(self, body, ax, ay, Step):
        vx = body.velocity_x + ax * Step
        vy = body.velocity_y + ay * Step
        x = body.pos_x + vx * Step
        y = body.pos_y + vy * Step
        body.acceleration_x = ax
        body.acceleration_y = ay
        body.velocity_x = vx
        body.velocity_y = vy
        body.pos_x = x
        body.pos_y = y
        body.life -= 1

    def collision(self, missile, asteroid):
        N_pieces = random.randint(4, 7)
        x = asteroid.pos_x
        y = asteroid.pos_y
        vx = asteroid.velocity_x
        vy = asteroid.velocity_y
        ratio = missile.Mass/asteroid.Mass*50
        if asteroid.Radius > 2*350000000:
            for i in range(N_pieces):
                tetha = random.uniform(0, 2*math.pi)
                v = math.sqrt(vx**2 + vy**2) * random.uniform(0.7, 1.4)
                v_x = v * math.cos(tetha)
                v_y = v * math.sin(tetha)
                x_i = x + random.uniform(-asteroid.Radius, asteroid.Radius)
                y_i = y + random.uniform(-asteroid.Radius, asteroid.Radius)
                omega = asteroid.omega * random.uniform(-1.2, 1.2)
                debree = Celestial_bodies.Asteroid("debree" + str(i), asteroid.Mass/N_pieces, asteroid.Radius/(N_pieces-1), x_i, y_i, v_x, v_y, asteroid.tetha, omega, asteroid.Type)
                self.asteroidList.append(debree)
        for i in range(N_pieces*10):
            tetha = random.uniform(0, 2*math.pi)
            v = math.sqrt(vx**2 + vy**2) * random.uniform(0.7, 1.4)
            v_x = v * math.cos(tetha)
            v_y = v * math.sin(tetha)
            x_i = x + random.uniform(-asteroid.Radius, asteroid.Radius)
            y_i = y + random.uniform(-asteroid.Radius, asteroid.Radius)
            debree1 = Celestial_bodies.Particle(140 + random.randint(-20, 20), x_i, y_i, v_x, v_y, asteroid.Type)
            self.particleList.append(debree1)
        asteroid = None

    def simulate_laser(self):
        Angle = 0
        Alpha = 0
        arm = 0
        Distance = 0
        Force_zero = 4 * 10**25
        ast = 0
        if self.Spaceship.Laser_fired:
            self.Spaceship.laser_length = 3 * 10 ** 12
        else: self.Spaceship.laser_length = 0
        for i in range(len(self.asteroidList)):
            if self.Spaceship.Laser_fired:
                #self.Spaceship.Laser_fired = False
                d = distance(self.asteroidList[i].pos_x, self.asteroidList[i].pos_y, self.Spaceship.pos_x, self.Spaceship.pos_y)
                phi = math.atan2(self.asteroidList[i].pos_y - self.Spaceship.pos_y, self.asteroidList[i].pos_x - self.Spaceship.pos_x)
                alpha = phi - (self.Spaceship.tetha - math.pi/2) + math.pi
                #if alpha < 0: alpha += math.pi * 2
                if alpha > math.pi *2: alpha -= math.pi * 2
                if alpha > math.pi : alpha = 2*math.pi - alpha
                #print(180/math.pi * alpha)
                R = d * math.sin(alpha)
                if -math.pi /2 < alpha < math.pi/2 and abs(R) < self.asteroidList[i].Radius * 1.25:
                    if self.Spaceship.laser_length > abs(d * math.cos(alpha) - self.asteroidList[i].Radius/4):
                        self.Spaceship.laser_length = abs(d * math.cos(alpha) - self.asteroidList[i].Radius/4)
                        Distance = d
                        Angle = self.Spaceship.tetha
                        arm = R
                        ast = i
                        Alpha = alpha
                #print(self.Spaceship.laser_length)
        if self.Spaceship.Laser_fired and self.Spaceship.Laser_power > 0:
            self.Spaceship.Laser_power = max(0,self.Spaceship.Laser_power)
            Force = Force_zero / (Distance**2+1)
            Force_x = Force * math.cos(self.Spaceship.tetha + math.pi/2)
            Force_y = Force * math.sin(self.Spaceship.tetha + math.pi/2)
            ax = Force_x / self.asteroidList[ast].Mass
            ay = Force_y / self.asteroidList[ast].Mass
            Torque = arm * Force
            aa = Torque / (0.5 * self.asteroidList[ast].Mass * self.asteroidList[ast].Radius**2)
            if Alpha < 0: Torque = - Torque
            self.asteroidList[ast].accelerate(ax, ay, aa, self.step)
            N_particles = int((30 + random.randint(-10, 30))/ ((Distance/11**10)**2+1))
            T = (self.Spaceship.tetha + math.pi / 2)
            x = self.Spaceship.pos_x + self.Spaceship.laser_length * math.cos(T)
            y = self.Spaceship.pos_y + self.Spaceship.laser_length * math.sin(T)
            vx = self.asteroidList[ast].velocity_x
            vy = self.asteroidList[ast].velocity_y
            spread = math.pi/6
            self.Spaceship.Laser_power -= 0.0001*self.step
            self.Spaceship.Laser_power = max(0,self.Spaceship.Laser_power)
            for i in range(N_particles):
                tetha = random.uniform(T - spread , T + spread) + math.pi
                v = math.sqrt(vx ** 2 + vy ** 2) * random.uniform(0.1, 0.5)
                v_x = vx + v * math.cos(tetha)
                v_y = vy + v * math.sin(tetha)
                debree1 = Celestial_bodies.Particle(30 + random.randint(-20, 20), x, y, v_x, v_y, self.asteroidList[ast].Type)
                self.particleList.append(debree1)
        elif self.Spaceship.Laser_fired == False and self.Spaceship.Laser_power<100:
            self.Spaceship.Laser_power += 0.00005*self.step


    def simulate(self):
        pList = self.planetList
        aList = self.asteroidList
        parList = self.particleList
        self.simulate_laser()
        for i in range(len(pList)):
            Force_x = 0
            Force_y = 0
            for j in range(len(pList)):
                if i != j:
                    d = distance(pList[i].pos_x, pList[i].pos_y, pList[j].pos_x, pList[j].pos_y)
                    if d < pList[i].Radius + pList[j].Radius:
                        Force = -Constants.G * pList[i].Mass * pList[j].Mass / d ** 2
                    else:
                        Force = Constants.G * pList[i].Mass * pList[j].Mass / d ** 2
                    gamma = angle(pList[i].pos_x, pList[i].pos_y, pList[j].pos_x, pList[j].pos_y)
                    Force_x += Force * math.cos(gamma)
                    Force_y += Force * math.sin(gamma)

            acc_x = Force_x / pList[i].Mass
            acc_y = Force_y / pList[i].Mass
            self.updatePlanet(pList[i], acc_x, acc_y, self.step)

        for i in self.asteroidList:
            Force_x = 0
            Force_y = 0
            omega = 0

            for j in range(len(pList)):

                d = distance(i.pos_x, i.pos_y, pList[j].pos_x, pList[j].pos_y)
                Force = Constants.G*i.Mass*pList[j].Mass/d**2
                gamma = angle(i.pos_x, i.pos_y, pList[j].pos_x, pList[j].pos_y)
                alpha = math.atan2(i.velocity_y, i.velocity_x)
                velocity = math.sqrt(i.velocity_x**2 + i.velocity_y**2)
                omega += (velocity*math.cos(alpha-gamma+math.pi/2))/d
                Force_x += Force*math.cos(gamma)
                Force_y += Force*math.sin(gamma)
            acc_x = Force_x / i.Mass
            acc_y = Force_y / i.Mass
            self.updateAsteroid(i, acc_x, acc_y, omega, self.step)
        omega = 0
        #if ang != 0: print(round(ang * 180 / math.pi))
        #self.Spaceship.Laser_fired = False
        for j in range(len(pList)):
            d = distance(self.Spaceship.pos_x, self.Spaceship.pos_y, pList[j].pos_x, pList[j].pos_y)

            if d > pList[j].Radius + self.Spaceship.Radius and pList[j] != self.blackhole: Force = Constants.G * self.Spaceship.Mass * pList[j].Mass / d ** 2
            else: Force = -Constants.G * self.Spaceship.Mass * pList[j].Mass / d ** 2 / 100
            dx = self.Spaceship.pos_x - pList[j].pos_x
            dy = self.Spaceship.pos_y - pList[j].pos_y
            gamma = angle(self.Spaceship.pos_x, self.Spaceship.pos_y, pList[j].pos_x, pList[j].pos_y)
            alpha = math.atan2(self.Spaceship.velocity_y, self.Spaceship.velocity_x)
            velocity = math.sqrt(self.Spaceship.velocity_x ** 2 + self.Spaceship.velocity_y ** 2)
            Force_x += Force * math.cos(gamma)
            Force_y += Force * math.sin(gamma)
        for j in range(len(aList)):
            d = distance(self.Spaceship.pos_x, self.Spaceship.pos_y, aList[j].pos_x,
                         aList[j].pos_y)
            gamma = angle(aList[j].pos_x, aList[j].pos_y, self.Spaceship.pos_x, self.Spaceship.pos_y)
            if d < aList[j].Radius + 10 ** (2):
                Force = 0#-Constants.G * self.Spaceship.Mass * aList[j].Mass * 10 ** (17) / d ** 2
            Force_x += Force * math.cos(gamma)
            Force_y += Force * math.sin(gamma)
        acc_x = Force_x / self.Spaceship.Mass
        acc_y = Force_y / self.Spaceship.Mass
        self.updateSpaceShip(self.Spaceship, acc_x, acc_y, omega, self.step)
        #print(self.Spaceship.missiles)
        for i in self.Spaceship.missiles:
            Force_x = 0
            Force_y = 0
            for j in range(len(pList)):
                d = distance(i.pos_x, i.pos_y, pList[j].pos_x, pList[j].pos_y)
                Force = Constants.G * i.Mass * pList[j].Mass / d ** 2
                gamma = angle(i.pos_x, i.pos_y, pList[j].pos_x, pList[j].pos_y)
                Force_x += Force * math.cos(gamma)
                Force_y += Force * math.sin(gamma)
            acc_x = Force_x / i.Mass
            acc_y = Force_y / i.Mass
            self.updateMissile(i, acc_x, acc_y, 0, self.step)
            for j in self.asteroidList:
                d = distance(i.pos_x, i.pos_y, j.pos_x,
                        j.pos_y)
                if i in self.Spaceship.missiles and d < j.Radius + i.Radius:
                    self.collision(i, j)
                    self.Spaceship.missiles.remove(i)
                    self.asteroidList.remove(j)
            d = distance(i.pos_x, i.pos_y, self.Spaceship.pos_x,
                        self.Spaceship.pos_y)
            if d > 300000000000:
                self.Spaceship.missiles.remove(i)
        compute = False
        for i in parList:
            if i in parList and i.life > 0:
                self.updateParticle(i, 0, 0, self.step)
                compute = True
            else:
                parList.remove(i)
        if compute == False: self.particleList = []
        self.collision_check()
        self.health_check()
        self.deltaV()
        self.simulate_blackhole()
        self.simulate_mining()

    def simulate_blackhole(self):
        if self.blackhole:
            if self.blackhole.bake_time > 0:
                self.blackhole.bake_time -= 1
            else:
                self.blackhole.Mass = 3 * 10**30
                if self.blackhole not in self.planetList:
                    self.planetList.append(self.blackhole)


    def collision_check(self):
        self.Spaceship.collision = False
        for i in self.planetList:
            if distance(self.Spaceship.pos_x, self.Spaceship.pos_y, i.pos_x,
                        i.pos_y) <= self.Spaceship.Radius + i.Radius:
                self.Spaceship.collision = True


        for j in self.asteroidList:
            if distance(self.Spaceship.pos_x, self.Spaceship.pos_y, j.pos_x,
                        j.pos_y) <= self.Spaceship.Radius + j.Radius and abs(self.Spaceship.velocity_x - j.velocity_x) >50\
                    and abs(self.Spaceship.velocity_y - j.velocity_y) > 50:
                self.Spaceship.collision = True
                e = 0.65
                alpha = math.atan2(j.pos_y - self.Spaceship.pos_y, j.pos_x - self.Spaceship.pos_x)
                phi = math.atan2(self.Spaceship.velocity_y, self.Spaceship.velocity_x)
                Phi = math.atan2(j.velocity_y, j.velocity_x)
                M = j.Mass * 100
                m = self.Spaceship.Mass
                V_m = math.sqrt(self.Spaceship.velocity_x ** 2 + self.Spaceship.velocity_y ** 2)
                V_M = math.sqrt(j.velocity_x ** 2 + j.velocity_y ** 2)
                tetha_m = phi - alpha
                tetha_M = Phi - alpha
                Vu_m = V_m * math.cos(tetha_m)
                Vv_m = V_m * math.sin(tetha_m)
                Vu_M = V_M * math.cos(tetha_M)
                Vv_M = V_M * math.sin(tetha_M)
                Vu_m_f = (m * Vu_m + M * Vu_M - e * M * (Vu_m - Vu_M)) / (M + m)
                Vu_M_f = (m * Vu_m + M * Vu_M + e * m * (Vu_m - Vu_M)) / (M + m)
                V_m_f = math.sqrt(Vu_m_f ** 2 + Vv_m ** 2)
                V_M_f = math.sqrt(Vu_M_f ** 2 + Vv_M ** 2)
                tetha_m_f = math.atan2(Vv_m, Vu_m_f)
                tetha_M_f = math.atan2(Vv_M, Vu_M_f)
                phi_f = alpha + tetha_m_f
                Phi_f = alpha + tetha_M_f
                self.Spaceship.velocity_x = V_m_f * math.cos(phi_f)
                self.Spaceship.velocity_y = V_m_f * math.sin(phi_f)
                D = self.Spaceship.Radius + j.Radius
                self.Spaceship.pos_x = j.pos_x + (D + 10) * math.cos(alpha + math.pi)
                self.Spaceship.pos_y = j.pos_y + (D + 10) * math.sin(alpha + math.pi)
                j.velocity_x = V_M_f * math.cos(Phi_f)
                j.velocity_y = V_M_f * math.sin(phi_f)
                d = distance(self.Spaceship.pos_x, self.Spaceship.pos_y, j.pos_x, j.pos_y)
                N_particles = int(30 + random.randint(-10, 30))
                T = (self.Spaceship.tetha + math.pi / 2)
                x = self.Spaceship.pos_x + d
                y = self.Spaceship.pos_y
                vx = self.Spaceship.velocity_x
                vy = self.Spaceship.velocity_y
                spread = math.pi / 6
                for i in range(N_particles):
                    tetha = random.uniform(0, math.pi * 2) + math.pi
                    x = 0.5 * (self.Spaceship.pos_x + j.pos_x)
                    y = 0.5 * (self.Spaceship.pos_y + j.pos_y)
                    v = math.sqrt(vx ** 2 + vy ** 2) * random.uniform(0.1, 0.5)
                    v_x = vx + v * math.cos(tetha)
                    v_y = vy + v * math.sin(tetha)
                    debree1 = Celestial_bodies.Particle(30 + random.randint(-20, 20), x, y, v_x, v_y, j.Type)
                    self.particleList.append(debree1)

    def health_check(self):
        if self.Spaceship.health >= 0:
            for i in self.planetList:
                if self.Spaceship.collision and self.Spaceship.health >= 0:
                    velocity_collision_planet = math.sqrt(
                        (self.Spaceship.velocity_x - i.velocity_x) ** 2 + (
                                    self.Spaceship.velocity_y - i.velocity_y) ** 2)
                    area_planet = math.pi * i.Radius ** 2
                    self.Spaceship.health -= 10 ** (-25) * (velocity_collision_planet * area_planet)
                    self.Spaceship.health = max(0, self.Spaceship.health)

            for j in self.asteroidList:
                if self.Spaceship.collision and self.Spaceship.health >= 0:
                    velocity_collision_asteroid = math.sqrt(
                        (self.Spaceship.velocity_x - j.velocity_x) ** 2 + (
                                    self.Spaceship.velocity_y - j.velocity_y) ** 2)
                    area_asteroid = math.pi * j.Radius ** 2
                    self.Spaceship.health -= 0.4 * 10 ** (-24) * (velocity_collision_asteroid * area_asteroid) / 2

    def deltaV(self):
        acc_sc = math.sqrt(self.Spaceship.acceleration_x ** 2 + self.Spaceship.acceleration_y ** 2)
        if acc_sc > 0 and self.Spaceship.Engine_fired:
            dV = 0.03*self.step
            self.Spaceship.deltaV -= 0.05*dV
            self.Spaceship.deltaV = max(0,self.Spaceship.deltaV)
            print(self.Spaceship.deltaV)

        if acc_sc>0 and (self.Spaceship.Left_stube_fired or self.Spaceship.Right_stube_fired):
            dV = 0.01 * self.step
            self.Spaceship.deltaV -= 0.005 * dV
            self.Spaceship.deltaV = max(0, self.Spaceship.deltaV)
            print(self.Spaceship.deltaV)

    def simulate_mining(self):
        self.Spaceship.collision = False
        for i in self.asteroidList:
            if self.Spaceship.hangar_open and self.Spaceship.Radius + i.Radius < distance(self.Spaceship.pos_x, self.Spaceship.pos_y, i.pos_x,
                        i.pos_y) <= (self.Spaceship.Radius + i.Radius)*2:
                if i.Type == "rare_gases" and i.content>0:
                    self.Spaceship.Rare_Gases += 2
                    i.content -= 2
                    self.Spaceship.Rare_Gases = min(self.Spaceship.Rare_Gases, self.Spaceship.Rare_Gases_Capacity)
                    print("Mining Rare Gas", self.Spaceship.Rare_Gases)

                elif i.content <= 0:
                    i.Type = "normal"

                if i.Type == "minerals" and i.content>0:
                    self.Spaceship.Minerals += 2
                    i.content -= 2
                    self.Spaceship.Minerals = min(self.Spaceship.Minerals, self.Spaceship.Minerals_Capacity)
                    print("Mining Minerals", self.Spaceship.Minerals)

                elif i.content <= 0:
                    i.Type = "normal"

    def draw_circle_gain_minerals(self, angle, radius, color, font_size, dist, screen, resolution):
        for i in self.asteroidList:
            if self.Spaceship.hangar_open and i.Type != "normal" and self.Spaceship.Radius + i.Radius < distance(self.Spaceship.pos_x, self.Spaceship.pos_y, i.pos_x, i.pos_y) <= (self.Spaceship.Radius + i.Radius)*2:
                font = pygame.font.SysFont("Consolas", 11)
                x = resolution[0]/2 + dist*math.cos(-angle)
                y = resolution[1]/2 + dist*math.sin(-angle)
                angle_fill = (1-(i.content / i.capacity))*2*math.pi
                percentage = round((1-(i.content/i.capacity))*100)
                text_percentage = str(percentage)+" %"
                text_mining = "Mining..."
                percentage_surface = font.render(text_percentage, True, (255,255,255))
                mining_surface = font.render(text_mining, True, (255,255,255))
                screen.blit(mining_surface, (int((x-font.size(text_percentage)[0]/2)+2.5*radius), int(y-font.size(text_percentage)[1]/2)))
                screen.blit(percentage_surface, (int(x-font.size(text_percentage)[0]/2), int(y-font.size(text_percentage)[1]/2)))
                pygame.draw.arc(screen, color, pygame.Rect(x-radius, y-radius, 2*radius, 2*radius), 0, angle_fill, 4)

