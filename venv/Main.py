import pygame, sys
import random
import math
from pygame import gfxdraw
import Celestial_bodies
import Constants
import Simulation_tools, Maps






pygame.init()

resolution = (1080,720)
screen = pygame.display.set_mode(resolution, pygame.RESIZABLE)
screct = screen.get_rect()
black = (0,0,0)
running = True
i=0
map = Maps.Game_Map(1/10000000)

while running :
    map.update()
    map.draw(resolution, screen)
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
               map.scale /= scale_change
            if event.button == 5:
                map.scale *= scale_change



