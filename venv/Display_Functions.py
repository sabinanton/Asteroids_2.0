import pygame


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
        except: "TypeError: Argument must be rect style object"
        pygame.draw.rect(self.Surface, self.black, background)
        pygame.draw.rect(self.Surface, self.white, background, 2)
        pygame.draw.rect(self.Surface, self.white, health_bar, 2)
        pygame.draw.rect(self.Surface, self.white, life_bar)
        self.Surface.blit(self.image, (10, 4))


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
