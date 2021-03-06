import pygame, Celestial_bodies, Constants, random, math, Simulation_tools


class Game_Map:
    
    scale = 1/18000000
    black = (0, 0, 0)
    white = (255, 255, 255)
    blue = (100, 100, 255)
    red = (255, 130, 100)
    map_white = (50,50,50)
    def __init__(self, scale, step):
        """
        This class represents the main map drawn on the screen
        :param scale: The scale of the simulation
        :param step: The differential time step of the simulation
        """
        self.SpaceShip = Celestial_bodies.SpaceShip("StarShip", 400000000, 147098070000 + 4844000000, 0, 0, 39051.33, 0, 0, 100000000)
        self.Earth = Celestial_bodies.Planet("Earth", 5.97219 * 10 ** 27, 63710000 * 25, 147098070000, 0, 0, 30040.49)
        self.Sun = Celestial_bodies.Planet("Sun", 1.989 * 10 ** 30, 13926800000/2, 0, 0, 0, 0)
        self.Mars = Celestial_bodies.Planet("Mars", 6.39 * 10 ** 23, 338950000 * 5/2, 1.38 * Constants.AU, 0, 0, 26500)
        self.Particles = []
        #self.Jupiter = Celestial_bodies.Planet("Jupiter", 1.898*10**28, 699110000, 5.034*Constants.AU, 0, 0, 13720)
        self.ast = self.generate_Asteroid_Belt(359115316000, 1285)
        #self.Moon = Celestial_bodies.Planet("Moon", 7.34767 * 10 ** 22, 173700000 * 5, 147098070000 + 4844000000, 0, 0, 39051.33)
        self.sim = Simulation_tools.Simulation([self.Sun, self.Earth, self.Mars], self.ast, self.SpaceShip,  step)
        self.x_offset = 0
        self.y_offset = 0
        self.scale = scale
        self.white = (255, 255, 255)
        self.blue = (100, 100, 255)
        self.red = (255, 130, 100)
        self.map_white = (150,150,150)
        self.black = (0,0,0)
        self.green = (30, 255, 30)
        self.yellow = (255, 255, 0)
        self.step = step

    def generate_Asteroid_Belt(self, radius, number_of_ast):
        """
        This function generates a randomised asteroid belt in the solar system
        :param radius: The average radius of the belt
        :param number_of_ast: The number of asteroids in the asteroid belt
        :return: Nothing
        """
        num = 0
        AstList = []
        while num < number_of_ast:
            r = random.randint(radius - 59500000000, radius + 59500000000)
            tetha = random.uniform(0, 2 * math.pi)
            x = r * math.cos(tetha)
            y = r * math.sin(tetha)
            d = math.sqrt(x ** 2 + y ** 2)
            v = math.sqrt(Constants.G * 1.989 * 10 ** 30 / d)
            angle = math.atan2(y, x) + math.pi / 2
            vx = v * math.cos(angle) * random.uniform(0.95, 1.05)
            vy = v * math.sin(angle) * random.uniform(0.95, 1.05)
            omega = random.uniform(-0.000005, 0.000005)
            mass = random.randint(50000, 100000000)
            types = ["minerals", "normal", "normal", "minerals", "minerals", "rare_gases", "normal", "normal", "normal", "normal",
                     "normal", "normal", "normal", "minerals", "normal", "rare_gases", "normal", "normal", "normal", "normal"]
            Type = random.choice(types)
            # print(x,y)
            AstList.append(
                Celestial_bodies.Asteroid("Ast" + str(num), mass, 350000000*2 + random.randint(-200000000*2, 300000000*2), x,
                                          y, vx, vy, 0, omega, Type))
            num += 1
        return AstList

    def update(self, focus_object):
        """
        This function calls the simulation function for every frame and updates the virtual camera prosition
        :param focus_object: The object the virtual camera follows
        :return: Nothing
        """
        self.sim.simulate()
        self.x_offset = -self.scale * focus_object.pos_x
        self.y_offset = self.scale * focus_object.pos_y

    def update_fixed_scale(self, focus_object, Scale):
        """
         This function calls the simulation function for every frame and updates the virtual camera position for the minimap
        :param focus_object: The object the virtual camera follows
        :param Scale: The scale of the minimap
        :return:
        """
        self.sim.simulate()
        self.x_offset = -Scale * focus_object.pos_x
        self.y_offset = Scale * focus_object.pos_y

    def draw(self, resolution, screen):
        """
        This function draws the elements of the main map on the screen
        :param resolution: The size of the surface to be drawn onto
        :param screen: The surface to be drawn onto
        :return: Nothing
        """
        screct = screen.get_rect()
        black = (0,0,0)
        pygame.draw.rect(screen, black, screct)
        self.Earth.draw(resolution, screen, self.x_offset, self.y_offset, self.scale, self.blue)
        self.Sun.draw(resolution, screen, self.x_offset, self.y_offset, self.scale, self.white)
        self.Mars.draw(resolution, screen, self.x_offset, self.y_offset, self.scale, self.red)
        #self.Moon.draw(resolution, screen, self.x_offset, self.y_offset, self.scale, self.white)
        self.SpaceShip.draw_trajectory(resolution, screen, self.scale, self.x_offset, self.y_offset, self.yellow, 800, self.Sun)
        self.SpaceShip.draw(resolution, screen, self.scale, self.x_offset, self.y_offset, self.white)
        if self.sim.blackhole:
            self.sim.blackhole.draw(resolution, screen, self.scale, self.x_offset, self.y_offset, self.map_white)
        for i in self.SpaceShip.missiles:
            i.draw(resolution, screen, self.scale, self.x_offset, self.y_offset, self.white)
        for i in self.sim.particleList:
            i.draw(resolution, screen, self.scale, self.x_offset, self.y_offset, None)
        #self.Jupiter.draw(resolution, screen, self.x_offset, self.y_offset, self.scale, self.white)
        # self.Moon.draw(resolution,screen, x_offset, y_offset)
        for j in self.ast:
            j.draw(resolution, screen, self.x_offset, self.y_offset, self.scale, None)

    def draw_fixed_scale(self, min_res, window_res, screen, Scale, focus_object):
        """
        This function draws the elements in the minimap onto the screen
        :param min_res: The minimap resolution
        :param window_res: The window size
        :param screen: The surface to be drawn onto
        :param Scale: The scale of the minimap
        :param focus_object: The reference object that shall be displayed in the middle of the minimap
        :return: Nothing
        """
        screct = screen.get_rect()
        ratio = Scale/self.scale
        width = window_res[0]*ratio
        height = window_res[1]*ratio
        focus_x = int(Scale * focus_object.pos_x + min_res[0] / 2 + self.x_offset) - width/2
        focus_y = int(min_res[1] / 2 - Scale * focus_object.pos_y + self.y_offset) - height/2
        focusrect = pygame.Rect(focus_x, focus_y, width, height)

        pygame.draw.rect(screen, self.black, screct)
        pygame.draw.rect(screen, self.white, screct, 2)
        self.Earth.draw(min_res, screen, self.x_offset, self.y_offset, Scale, self.blue)
        self.Sun.draw(min_res, screen, self.x_offset, self.y_offset, Scale, self.white)
        self.Mars.draw(min_res, screen, self.x_offset, self.y_offset, Scale, self.red)
        #self.Moon.draw(min_res, screen, self.x_offset, self.y_offset, Scale, self.white)
        self.SpaceShip.draw_trajectory(min_res, screen, Scale, self.x_offset ,self.y_offset , self.yellow, 100, self.Sun)
        self.SpaceShip.draw(min_res, screen, Scale, self.x_offset, self.y_offset, self.white)
        if self.sim.blackhole:
            self.sim.blackhole.draw(min_res, screen, Scale, self.x_offset, self.y_offset, self.white)
        for i in self.sim.particleList:
            i.draw(min_res, screen, Scale, self.x_offset, self.y_offset, self.map_white)
        for i in self.SpaceShip.missiles:
            i.draw(min_res, screen, Scale, self.x_offset, self.y_offset, self.white)
        #self.Jupiter.draw(min_res, screen, self.x_offset, self.y_offset, Scale, self.map_white)
        # self.Moon.draw(resolution,screen, x_offset, y_offset)
        for j in self.ast:
            if j.Type == "normal": j.draw(min_res, screen, self.x_offset, self.y_offset, Scale, self.map_white)
            else: j.draw(min_res, screen, self.x_offset, self.y_offset, Scale, None)
        pygame.draw.rect(screen, self.white, focusrect, 2)
