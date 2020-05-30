import math
import Celestial_bodies
import Constants
import random
import collections
def distance(x1, y1, x2, y2):
    return math.sqrt((y2-y1)**2+(x2-x1)**2)

def angle(x1, y1, x2, y2):
    return math.atan2(y2-y1, x2-x1)

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

    def updatePlanet(self, body, ax, ay, Step):
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
                debree = Celestial_bodies.Asteroid("debree" + str(i), asteroid.Mass/N_pieces, asteroid.Radius/(N_pieces-1), x_i, y_i, v_x, v_y, asteroid.tetha, omega)
                self.asteroidList.append(debree)
        for i in range(N_pieces*10):
            tetha = random.uniform(0, 2*math.pi)
            v = math.sqrt(vx**2 + vy**2) * random.uniform(0.7, 1.4)
            v_x = v * math.cos(tetha)
            v_y = v * math.sin(tetha)
            x_i = x + random.uniform(-asteroid.Radius, asteroid.Radius)
            y_i = y + random.uniform(-asteroid.Radius, asteroid.Radius)
            debree1 = Celestial_bodies.Particle(140 + random.randint(-20, 20), x_i, y_i, v_x, v_y)
            self.particleList.append(debree1)
        asteroid = None

    def simulate_laser(self):
        Angle = 0
        Alpha = 0
        arm = 0
        Distance = 0
        Force_zero = 4 * 10**6
        ast = None
        if self.Spaceship.Laser_fired:
            self.Spaceship.laser_length = 3 * 10 ** 12
        else: self.Spaceship.laser_length = 0
        for i in self.asteroidList:
            if self.Spaceship.Laser_fired:
                #self.Spaceship.Laser_fired = False
                d = distance(i.pos_x, i.pos_y, self.Spaceship.pos_x, self.Spaceship.pos_y)
                phi = math.atan2(i.pos_y - self.Spaceship.pos_y, i.pos_x - self.Spaceship.pos_x)
                alpha = phi - (self.Spaceship.tetha - math.pi/2) + math.pi
                #if alpha < 0: alpha += math.pi * 2
                if alpha > math.pi *2: alpha -= math.pi * 2
                if alpha > math.pi : alpha = 2*math.pi - alpha
                #print(180/math.pi * alpha)
                R = d * math.sin(alpha)
                if -math.pi /2 < alpha < math.pi/2 and abs(R) < i.Radius * 1.25:
                    if self.Spaceship.laser_length > abs(d * math.cos(alpha) - i.Radius/4):
                        self.Spaceship.laser_length = abs(d * math.cos(alpha) - i.Radius/4)
                        Distance = d
                        Angle = self.Spaceship.tetha + math.pi/2
                        arm = R
                        ast = i
                        Alpha = alpha
                #print(self.Spaceship.laser_length)
        Force = Force_zero / Distance**2
        Force_x = Force * math.cos(Angle)
        Force_y = Force * math.sin(Angle)
        Torque = arm * Force
        if Alpha < 0: Torque = - Torque
        
        self.Spaceship.Laser_fired = False

    def simulate(self):
        pList = self.planetList
        aList = self.asteroidList
        parList = self.particleList
        for i in range(len(pList)):
            Force_x = 0
            Force_y = 0
            for j in range(len(pList)):
                if i!=j :
                    d = distance(pList[i].pos_x, pList[i].pos_y, pList[j].pos_x, pList[j].pos_y)
                    if d < pList[i].Radius + pList[j].Radius: Force = -Constants.G*pList[i].Mass*pList[j].Mass/d**2
                    else: Force = Constants.G*pList[i].Mass*pList[j].Mass/d**2
                    gamma = angle(pList[i].pos_x, pList[i].pos_y, pList[j].pos_x, pList[j].pos_y)
                    Force_x += Force*math.cos(gamma)
                    Force_y += Force*math.sin(gamma)
                    
            acc_x = Force_x/pList[i].Mass
            acc_y = Force_y/pList[i].Mass
            self.updatePlanet(pList[i], acc_x, acc_y, self.step)

        for i in self.asteroidList:
            Force_x = 0
            Force_y = 0
            omega = 0

            for j in range(len(pList)):

                d = distance(i.pos_x, i.pos_y, pList[j].pos_x, pList[j].pos_y)
                if d < i.Radius + pList[j].Radius: Force = -Constants.G*i.Mass*pList[j].Mass/d**2
                else: Force = Constants.G*i.Mass*pList[j].Mass/d**2
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
        if ang != 0: print(round(ang * 180 / math.pi))
        self.Spaceship.Laser_fired = False
        for j in range(len(pList)):
            d = distance(self.Spaceship.pos_x, self.Spaceship.pos_y, pList[j].pos_x, pList[j].pos_y)

            Force = Constants.G * self.Spaceship.Mass * pList[j].Mass / d ** 2
            dx = self.Spaceship.pos_x - pList[j].pos_x
            dy = self.Spaceship.pos_y - pList[j].pos_y
            gamma = angle(self.Spaceship.pos_x, self.Spaceship.pos_y, pList[j].pos_x, pList[j].pos_y)
            alpha = math.atan2(self.Spaceship.velocity_y, self.Spaceship.velocity_x)
            velocity = math.sqrt(self.Spaceship.velocity_x ** 2 + self.Spaceship.velocity_y ** 2)
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
            if i in parList and i.life>0:
                self.updateParticle(i, 0, 0, self.step)
                compute = True
            else: parList.remove(i)
        if compute == False: self.particleList = []