import pygame, sys
import random
import math
from pygame import gfxdraw
import Celestial_bodies
import Constants
import Simulation_tools, Maps
import Display_Functions




def controls(event, Map):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        Map.SpaceShip.T_accelerate(0.03, Map.step)
    if keys[pygame.K_d]:
        Map.SpaceShip.Rotate(-1, 1/2000000)
    if keys[pygame.K_a]:
        Map.SpaceShip.Rotate(1, 1/2000000)
    if keys[pygame.K_w]:
        Map.SpaceShip.a_impulse(0.01, -1, Map.step)
    if keys[pygame.K_s]:
        Map.SpaceShip.a_impulse(0.01, 1, Map.step)
    if keys[pygame.K_r]:
        Map.SpaceShip.Laser_fired = True
    



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
health_bar_res = (minimap_res[0], int(0.05*resolution[1]))
health_bar_surface = pygame.Surface(health_bar_res)
Health_bar = Display_Functions.health_display(health_bar_res,health_bar_surface)

while running :
    minimap = pygame.Surface(minimap_res)
    map.update(map.SpaceShip)
    map.draw(resolution, screen)
    map.update_fixed_scale(map.Sun, mini_map_scale)
    map.draw_fixed_scale(minimap_res, resolution,  minimap, mini_map_scale, map.SpaceShip)
    screen.blit(minimap, [0, resolution[1]-minimap_res[1]])
    Health_bar.draw_health_bar(map.SpaceShip.health)
    screen.blit(health_bar_surface, [0,resolution[1]-minimap_res[1]-health_bar_res[1]])
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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                map.SpaceShip.fire_missile(40000)
    controls(event, map)


