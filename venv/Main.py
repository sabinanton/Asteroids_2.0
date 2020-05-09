import pygame
import random
import math
from pygame import gfxdraw
import Celestial_bodies
import Constants
import Simulation_tools


def generate_Asteroid_Belt(radius, number_of_ast):
    num = 0
    AstList = []
    while num < number_of_ast:
        r = random.randint(radius-5000000, radius+5000000)
        tetha = random.uniform(0,2*math.pi)
        x = r*math.cos(tetha)
        y = r*math.sin(tetha)
        d = math.sqrt(x**2 + y**2)
        v = math.sqrt(Constants.G*5.97219*10**24/d)
        angle = math.atan2(y, x)+math.pi/2
        vx = v*math.cos(angle)*random.uniform(0.95,1.05)
        vy = v*math.sin(angle)*random.uniform(0.95,1.05)
        mass = random.randint(500, 1000000)
        print(x,y)
        AstList.append(Celestial_bodies.Asteroid("Ast"+str(num), mass, 300000 + random.randint(-200000, 300000), x, y, vx, vy))
        num+=1
    return AstList


Earth = Celestial_bodies.Planet("Earth", 5.97219*10**24, 6371000, 0, 0, 0, 0)
ast = generate_Asteroid_Belt(138440000, 565)
Moon = Celestial_bodies.Planet("Moon", 7.34767*10**22, 2737000, 384400000, 0, 0, 1018)
sim = Simulation_tools.Simulation([Earth, Moon],ast, 865)
pygame.init()

resolution = (1080,720)
screen = pygame.display.set_mode(resolution)
screct = screen.get_rect()
black = (0,0,0)
running = True
i=0

while running :
    i+=1
    sim.simulate()
    pygame.draw.rect(screen, black, screct)
    Earth.draw(resolution,screen)
    Moon.draw(resolution, screen)
    for j in ast:
        j.draw(resolution,screen)
    pygame.display.flip()
    if i >69000: running = False


pygame.quit()