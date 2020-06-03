import pygame
import Constants

class health_display:
    def __init__(self, resolution, surface):
        self.Resolution = resolution
        self.Surface = surface
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.heart = pygame.image.load("Lib\\Asteroids_2_health_icon (1).png")
        self.image = pygame.transform.scale(self.heart, (25, 25))

    def draw_health_bar(self, health):
        background = pygame.Rect([0, 0, self.Resolution[0], self.Resolution[1]])
        try:
            health_bar = pygame.Rect(
            [int(0.15 * self.Resolution[0] + 6), 6, int(0.85 * self.Resolution[0] - 12), self.Resolution[1] - 12])
            life_bar = pygame.Rect(
            [int(0.15 * self.Resolution[0] + 6), 6, int((0.85 * self.Resolution[0] - 12) * (health / 100)),
             int(self.Resolution[1] - 12)])
            pygame.draw.rect(self.Surface, self.black, background)
            pygame.draw.rect(self.Surface, self.white, background, 2)
            pygame.draw.rect(self.Surface, self.white, health_bar, 2)
            pygame.draw.rect(self.Surface, self.white, life_bar)
            self.Surface.blit(self.image, (10, 4))
        except: "TypeError: Argument must be rect style object"


class deltaV_display:
    def __init__(self, resolution, surface):
        self.Resolution = resolution
        self.Surface = surface
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.heart = pygame.image.load("Lib\\Asteroids_2_fuel_icon.png")
        self.image = pygame.transform.scale(self.heart, (25, 25))

    def draw_deltaV_bar(self, deltaV):
        background = pygame.Rect([0, 0, self.Resolution[0], self.Resolution[1]])
        fuel_bar = pygame.Rect(
            [int(0.15 * self.Resolution[0] + 6), 6, int(0.85 * self.Resolution[0] - 12), self.Resolution[1] - 12])
        tank_bar = pygame.Rect(
            [int(0.15 * self.Resolution[0] + 6), 6, int((0.85 * self.Resolution[0] - 12) * (deltaV / 10000)),
             self.Resolution[1] - 12])
        pygame.draw.rect(self.Surface, self.black, background)
        pygame.draw.rect(self.Surface, self.white, background, 2)
        pygame.draw.rect(self.Surface, self.white, fuel_bar, 2)
        pygame.draw.rect(self.Surface, self.white, tank_bar)
        self.Surface.blit(self.image, (10, 10))


class missiles_display:
    def __init__(self, resolution, surface):
        self.Resolution = resolution
        self.Surface = surface
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.missiles = pygame.image.load("Lib\\Asteroids_2_missle_icon.png")
        self.image = pygame.transform.scale(self.missiles, (25, 25))

    def draw_missiles_bar(self, Number_of_missiles):
        background = pygame.Rect([0, 0, self.Resolution[0], self.Resolution[1]])
        font = pygame.font.SysFont("Consolas", 20)
        text_line = "" + str(Number_of_missiles)
        text_surface = font.render(text_line, True, self.white)
        pygame.draw.rect(self.Surface, self.black, background)
        pygame.draw.rect(self.Surface, self.white, background, 2)
        self.Surface.blit(text_surface, (40, 12))
        self.Surface.blit(self.image, (10, 10))


class laser_display:
    def __init__(self, resolution, surface):
        self.Resolution = resolution
        self.Surface = surface
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.heart = pygame.image.load("Lib\\Asteroids_2_laser_icon.png")
        self.image = pygame.transform.scale(self.heart, (25, 25))

    def draw_laser_bar(self, laser):
        background = pygame.Rect([0, 0, self.Resolution[0], self.Resolution[1]])
        laser_bar = pygame.Rect(
            [int(0.15 * self.Resolution[0] + 6), 6, int(0.85 * self.Resolution[0] - 12), self.Resolution[1] - 12])
        device_bar = pygame.Rect(
            [int(0.15 * self.Resolution[0] + 6), 6, int((0.85 * self.Resolution[0] - 12) * (laser / 100)),
             self.Resolution[1] - 12])
        pygame.draw.rect(self.Surface, self.black, background)
        pygame.draw.rect(self.Surface, self.white, background, 2)
        pygame.draw.rect(self.Surface, self.white, laser_bar, 2)
        pygame.draw.rect(self.Surface, self.white, device_bar)
        self.Surface.blit(self.image, (10, 10))


class black_hole_display:
    def __init__(self, resolution, surface):
        self.Resolution = resolution
        self.Surface = surface
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)

    def draw_black_hole_bar(self, Black_hole_count):
        background = pygame.Rect([0, 0, self.Resolution[0], self.Resolution[1]])
        font = pygame.font.SysFont("Consolas", 20)
        text_line = "" + str(Black_hole_count)
        text_surface = font.render(text_line, True, self.white)
        pygame.draw.rect(self.Surface, self.black, background)
        pygame.draw.rect(self.Surface, self.white, background, 2)
        pygame.draw.circle(self.Surface, self.white, (30, 20), 15, 2)
        self.Surface.blit(text_surface, (55, 12))

class sc_info_display:
    def __init__(self,resolution,surface):
        self.Resolution = resolution
        self.Surface = surface
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.name = ""
        self.velocity = 0
        self.acceleration = 0
        self.distance_from_Earth = 0
        self.distance_from_Sun = 0

    def draw_sc_info(self):
        n=6
        background = pygame.Rect([0,0,self.Resolution[0],self.Resolution[1]])
        pygame.draw.rect(self.Surface, self.black, background)
        pygame.draw.rect(self.Surface, self.white, background, 2)
        font = pygame.font.SysFont("Consolas", 12)
        name_text_line = "Name of Spacecraft: " + str(self.name)
        name_text_surface = font.render(name_text_line, True, self.white)
        self.Surface.blit(name_text_surface, (((self.Resolution[0]-font.size(name_text_line)[0])/2), (self.Resolution[1]/n)))
        velocity_text_line = "Current velocity: " + str(self.velocity) + " [km/s]"
        velocity_text_surface = font.render(velocity_text_line, True, self.white)
        self.Surface.blit(velocity_text_surface, (((self.Resolution[0]-font.size(velocity_text_line)[0])/2), (self.Resolution[1]*2/n)))
        acceleration_text_line = "Current Acceleration: " + str(self.acceleration) + " [km/s^2]"
        acceleration_text_surface = font.render(acceleration_text_line, True, self.white)
        self.Surface.blit(acceleration_text_surface, (((self.Resolution[0]-font.size(acceleration_text_line)[0])/2), (self.Resolution[1]*3/n)))
        distance_from_Earth_text_line = "Distance from Earth: " + str(self.distance_from_Earth) + " [AU]"
        distance_from_Earth_text_surface = font.render(distance_from_Earth_text_line, True, self.white)
        self.Surface.blit(distance_from_Earth_text_surface, (((self.Resolution[0]-font.size(distance_from_Earth_text_line)[0])/2), (self.Resolution[1]*4/n)))
        distance_from_Sun_text_line = "Distance from Sun: " + str(self.distance_from_Sun) + " [AU]"
        distance_from_Sun_text_surface = font.render(distance_from_Sun_text_line, True, self.white)
        self.Surface.blit(distance_from_Sun_text_surface, (((self.Resolution[0]-font.size(distance_from_Sun_text_line)[0])/2), (self.Resolution[1]*5/n)))

    def update_sc_info(self,name,velocity,acceleration,distance_from_Earth,distance_from_Sun):
        self.name = name
        self.velocity = round(velocity/1000,1)
        self.acceleration = round(acceleration,4)
        self.distance_from_Earth = round(distance_from_Earth/Constants.AU,2)
        self.distance_from_Sun = round(distance_from_Sun/Constants.AU,2)



