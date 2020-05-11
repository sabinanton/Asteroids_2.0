import pygame, Celestial_bodies, Constants, random, math, Simulation_tools


class Game_Map:
    
    scale = 1/10000000
    def __init__(self, scale):
        self.Earth = Celestial_bodies.Planet("Earth", 5.97219 * 10 ** 24, 637100000 * 5, 147098070000, 0, 0, 30280)
        self.Sun = Celestial_bodies.Planet("Sun", 1.989 * 10 ** 30, 13926800000, 0, 0, 0, 0)
        self.Mars = Celestial_bodies.Planet("Mars", 6.39 * 10 ** 23, 338950000 * 5, 1.38 * Constants.AU, 0, 0, 26500)
        #self.Jupiter = Celestial_bodies.Planet("Jupiter", 1.898*10**27, 699110000, 5.034*Constants.AU, 0, 0, 13720)
        self.ast = self.generate_Asteroid_Belt(329115316000, 2665)
        self.Moon = Celestial_bodies.Planet("Moon", 7.34767 * 10 ** 22, 17370000, 147098070000 + 384400000, 0, 0, 31298)
        self.sim = Simulation_tools.Simulation([self.Earth, self.Sun, self.Mars], self.ast, 55555)
        self.x_offset = 0
        self.y_offset = 0
        self.scale = scale

    def generate_Asteroid_Belt(self, radius, number_of_ast):
        num = 0
        AstList = []
        while num < number_of_ast:
            r = random.randint(radius - 19500000000, radius + 19500000000)
            tetha = random.uniform(0, 2 * math.pi)
            x = r * math.cos(tetha)
            y = r * math.sin(tetha)
            d = math.sqrt(x ** 2 + y ** 2)
            v = math.sqrt(Constants.G * 1.989 * 10 ** 30 / d)
            angle = math.atan2(y, x) + math.pi / 2
            vx = v * math.cos(angle) * random.uniform(0.97, 1.03)
            vy = v * math.sin(angle) * random.uniform(0.97, 1.03)
            omega = random.uniform(-0.000005, 0.000005)
            mass = random.randint(50000, 100000000)
            # print(x,y)
            AstList.append(
                Celestial_bodies.Asteroid("Ast" + str(num), mass, 300000000 + random.randint(-200000000, 300000000), x,
                                          y, vx, vy, 0, omega))
            num += 1
        return AstList

    def update(self):
        self.sim.simulate()
        self.x_offset = -self.scale * self.ast[7].pos_x
        self.y_offset = self.scale * self.ast[7].pos_y

    def draw(self, resolution, screen):
        screct = screen.get_rect()
        black = (0,0,0)
        pygame.draw.rect(screen, black, screct)
        self.Earth.draw(resolution, screen, self.x_offset, self.y_offset, self.scale)
        self.Sun.draw(resolution, screen, self.x_offset, self.y_offset, self.scale)
        self.Mars.draw(resolution, screen, self.x_offset, self.y_offset, self.scale)
        # self.Jupiter.draw(resolution, screen, x_offset, y_offset)
        # self.Moon.draw(resolution,screen, x_offset, y_offset)
        for j in self.ast:
            j.draw(resolution, screen, self.x_offset, self.y_offset, self.scale)


