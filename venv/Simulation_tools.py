import math
import Celestial_bodies
import Constants
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
        body.acceleration_x = ax
        body.acceleration_y = ay
        body.velocity_x = vx
        body.velocity_y = vy
        body.pos_x = x
        body.pos_y = y

    def simulate(self):
        pList = self.planetList
        aList = self.asteroidList
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
        for i in range(len(aList)):
            Force_x = 0
            Force_y = 0
            omega = 0
            for j in range(len(pList)):
                if i!=j :
                    d = distance(aList[i].pos_x, aList[i].pos_y, pList[j].pos_x, pList[j].pos_y)
                    if d < aList[i].Radius + aList[j].Radius: Force = -Constants.G*aList[i].Mass*pList[j].Mass/d**2
                    else: Force = Constants.G*aList[i].Mass*pList[j].Mass/d**2
                    gamma = angle(aList[i].pos_x, aList[i].pos_y, pList[j].pos_x, pList[j].pos_y)
                    alpha = math.atan2(aList[i].velocity_y, aList[i].velocity_x)
                    velocity = math.sqrt(aList[i].velocity_x**2 + aList[i].velocity_y**2)
                    omega += (velocity*math.cos(alpha-gamma+math.pi/2))/d
                    Force_x += Force*math.cos(gamma)
                    Force_y += Force*math.sin(gamma)
            acc_x = Force_x / aList[i].Mass
            acc_y = Force_y / aList[i].Mass
            self.updateAsteroid(aList[i], acc_x, acc_y, omega, self.step)
        omega = 0
        for j in range(len(pList)):
            d = distance(self.Spaceship.pos_x, self.Spaceship.pos_y, pList[j].pos_x, pList[j].pos_y)
            if d < self.Spaceship.Radius + self.Spaceship.Radius:
                Force = -Constants.G * self.Spaceship.Mass * pList[j].Mass / d ** 2
            else:
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
        self.Spaceship.compute_distance(pList[0])
                