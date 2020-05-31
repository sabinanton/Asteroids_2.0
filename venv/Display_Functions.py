import pygame


class health_display:
    def __init__(self, resolution, surface):
        self.Resolution = resolution
        self.Surface = surface
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.heart = pygame.image.load("Lib\\Asteroids_2_health_icon.png")
        self.image = pygame.transform.scale(self.heart,(25,25))

    def draw_health_bar(self, health):
        background = pygame.Rect([0, 0, self.Resolution[0], self.Resolution[1]])
        health_bar = pygame.Rect([int(0.25*self.Resolution[0]+6),6,int(0.75*self.Resolution[0]-12),self.Resolution[1]-12])
        try: life_bar = pygame.Rect([int(0.25*self.Resolution[0]+6),6,int((0.75*self.Resolution[0]-12)*(health/100)),self.Resolution[1]-12])
        except: "TypeError: Argument must be rect style object"
        pygame.draw.rect(self.Surface, self.black, background)
        pygame.draw.rect(self.Surface, self.white, background, 2)
        pygame.draw.rect(self.Surface, self.white, health_bar, 2)
        pygame.draw.rect(self.Surface,self.white,life_bar)
        self.Surface.blit(self.image, (6,6))
