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
        health_bar = pygame.Rect(
            [int(0.25 * self.Resolution[0] + 6), 6, int(0.75 * self.Resolution[0] - 12), self.Resolution[1] - 12])
        life_bar = pygame.Rect([0,0,0,0])
        try: life_bar = pygame.Rect(
            [int(0.25 * self.Resolution[0] + 6), 6, int((0.75 * self.Resolution[0] - 12) * (health / 100)),
             self.Resolution[1] - 12])
        except: "TypeError: Argument must be rect style object"
        pygame.draw.rect(self.Surface, self.black, background)
        pygame.draw.rect(self.Surface, self.white, background, 2)
        pygame.draw.rect(self.Surface, self.white, health_bar, 2)
        pygame.draw.rect(self.Surface, self.white, life_bar)
        self.Surface.blit(self.image, (25, 4))


class deltaV_display:
    def __init__(self, resolution, surface):
        self.Resolution = resolution
        self.Surface = surface
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.heart = pygame.image.load("Lib\\Asteroids_2_fuel_icon.png")
        self.image = pygame.transform.scale(self.heart, (29, 29))

    def draw_deltaV_bar(self, deltaV):
        print(self.Resolution[1])
        background = pygame.Rect([0, 0, self.Resolution[0], self.Resolution[1]])
        fuel_bar = pygame.Rect(
            [int(0.25 * self.Resolution[0] + 6), 6, int(0.75 * self.Resolution[0] - 12), self.Resolution[1] - 12])
        tank_bar = pygame.Rect(
            [int(0.25 * self.Resolution[0] + 6), 6, int((0.75 * self.Resolution[0] - 12) * (deltaV / 10000)),
             self.Resolution[1] - 12])
        pygame.draw.rect(self.Surface, self.black, background)
        pygame.draw.rect(self.Surface, self.white, background, 2)
        pygame.draw.rect(self.Surface, self.white, fuel_bar, 2)
        pygame.draw.rect(self.Surface, self.white, tank_bar)
        self.Surface.blit(self.image, (25, 4))

    def resize(self, res):
        self.Resolution = res
        self.Surface = pygame.Surface(self.Resolution)