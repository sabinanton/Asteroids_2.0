import pygame, sys
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
        r = random.randint(radius-19500000000, radius+19500000000)
        tetha = random.uniform(0,2*math.pi)
        x = r*math.cos(tetha)
        y = r*math.sin(tetha)
        d = math.sqrt(x**2 + y**2)
        v = math.sqrt(Constants.G*1.989*10**30/d)
        angle = math.atan2(y, x)+math.pi/2
        vx = v*math.cos(angle)*random.uniform(0.97,1.03)
        vy = v*math.sin(angle)*random.uniform(0.97,1.03)
        mass = random.randint(500, 1000000)
        print(x,y)
        AstList.append(Celestial_bodies.Asteroid("Ast"+str(num), mass, 300000000 + random.randint(-200000000, 300000000), x, y, vx, vy))
        num+=1
    return AstList


Earth = Celestial_bodies.Planet("Earth", 5.97219*10**24, 63710000, 147098070000, 0, 0, 30280)
Sun = Celestial_bodies.Planet("Sun", 1.989*10**30, 6963400000, 0, 0, 0, 0)
Mars = Celestial_bodies.Planet("Mars", 6.39*10**23, 33895000, 1.38*Constants.AU, 0, 0, 26500)
#Jupiter = Celestial_bodies.Planet("Jupiter", 1.898*10**27, 699110000, 5.034*Constants.AU, 0, 0, 13720)
ast = generate_Asteroid_Belt(329115316000, 1665)
Moon = Celestial_bodies.Planet("Moon", 7.34767*10**22, 17370000, 147098070000 + 384400000, 0, 0, 31298)
sim = Simulation_tools.Simulation([Earth, Sun, Mars],ast, 15555)
pygame.init()

resolution = (1080,720)
screen = pygame.display.set_mode(resolution, pygame.RESIZABLE)
screct = screen.get_rect()
black = (0,0,0)
running = True
i=0

while running :
    sim.simulate()
    x_offset = -Constants.scale * Earth.pos_x
    y_offset = Constants.scale * Earth.pos_y
    pygame.draw.rect(screen, black, screct)
    Earth.draw(resolution,screen, x_offset, y_offset)
    Sun.draw(resolution, screen, x_offset, y_offset)
    Mars.draw(resolution, screen, x_offset, y_offset)
    #Jupiter.draw(resolution, screen, x_offset, y_offset)
    #Moon.draw(resolution,screen, x_offset, y_offset)
    for j in ast:
        j.draw(resolution,screen, x_offset, y_offset)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                pygame.QUIT
                sys.exit()
        if event.type == pygame.VIDEORESIZE:
            resolution = (event.w, event.h)
            screen = pygame.display.set_mode(resolution, pygame.RESIZABLE)
            screct = screen.get_rect()
        if event.type == pygame.MOUSEBUTTONDOWN:
            scale_change = 0.9
            if event.button == 4:
                Constants.scale /= scale_change
            if event.button == 5:
                Constants.scale *= scale_change



