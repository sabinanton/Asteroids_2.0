import pygame, sys
import random
import math
from pygame import gfxdraw
import Celestial_bodies
import Constants
import Simulation_tools, Maps




def controls(event, Map):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        Map.SpaceShip.T_accelerate(0.03, Map.step)
        print("ACC")
    if keys[pygame.K_d]:
        Map.SpaceShip.Rotate(-1, 1/2000000)
    if keys[pygame.K_a]:
        Map.SpaceShip.Rotate(1, 1/2000000)
    if keys[pygame.K_w]:
        Map.SpaceShip.a_impulse(0.01, -1, Map.step)
    if keys[pygame.K_s]:
        Map.SpaceShip.a_impulse(0.01, 1, Map.step)


pygame.init()

resolution = (1080,720)
screen = pygame.display.set_mode(resolution, pygame.RESIZABLE)

screct = screen.get_rect()
black = (0,0,0)
running = True
i=0
map = Maps.Game_Map(1/30000000, 25555)
mini_map_scale = 1/3000000000
minimap_res = (300,300)
while running :
    minimap = pygame.Surface(minimap_res)
    map.update(map.SpaceShip)
    map.draw(resolution, screen)
    map.update_fixed_scale(map.Sun, mini_map_scale)
    map.draw_fixed_scale(minimap_res, resolution,  minimap, mini_map_scale, map.SpaceShip)
    screen.blit(minimap, [0, resolution[1]-minimap_res[1]])
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
    controls(event, map)



