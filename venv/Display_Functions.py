import pygame
from PIL import Image, ImageDraw


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
        life_bar = pygame.Rect(
            [int(0.25 * self.Resolution[0] + 6), 6, int((0.75 * self.Resolution[0] - 12) * (health / 100)),
             self.Resolution[1] - 12])
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
        self.image = pygame.transform.scale(self.heart, (25, 25))

    def draw_deltaV_bar(self, deltaV):
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

class missiles_display:
    def __init__(self, resolution, surface):
        self.Resolution = resolution
        self.Surface = surface
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.heart = pygame.image.load("Lib\\Asteroids_2_fuel_icon.png")
        self.image = pygame.transform.scale(self.heart, (25, 25))

    def draw_missiles_bar(self, Number_of_missiles):
        background = pygame.Rect([0, 0, self.Resolution[0], self.Resolution[1]])
        missile_bar = pygame.Rect(
            [int(0.25 * self.Resolution[0] + 6), 6, int(0.75 * self.Resolution[0] - 12), self.Resolution[1] - 12])
        gun_bar = pygame.Rect(
            [int(0.25 * self.Resolution[0] + 6), 6, int((0.75 * self.Resolution[0] - 12) * (Number_of_missiles / 60)),
             self.Resolution[1] - 12])
        pygame.draw.rect(self.Surface, self.black, background)
        pygame.draw.rect(self.Surface, self.white, background, 2)
        pygame.draw.rect(self.Surface, self.white, missile_bar, 2)
        pygame.draw.rect(self.Surface, self.white, gun_bar)
        self.Surface.blit(self.image, (25, 4))
