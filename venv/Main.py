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
        Map.SpaceShip.T_accelerate(12000000, Map.step)
    if keys[pygame.K_d]:
        Map.SpaceShip.Rotate(-1, 4 * 10 **(-7))
    if keys[pygame.K_a]:
        Map.SpaceShip.Rotate(1, 4 * 10 **(-7))
    if keys[pygame.K_w]:
        Map.SpaceShip.a_impulse(4000000, -1, Map.step)
    if keys[pygame.K_s]:
        Map.SpaceShip.a_impulse(4000000, 1, Map.step)
    if keys[pygame.K_r]:
        Map.SpaceShip.Laser_fired = True
    else:
        Map.SpaceShip.Laser_fired = False
    if keys[pygame.K_e]:
        Map.SpaceShip.Missile_fired = True

pygame.init()

resolution = (1080,720)
screen = pygame.display.set_mode(resolution, pygame.RESIZABLE)

screct = screen.get_rect()
black = (0,0,0)
running = True
i=0
map = Maps.Game_Map(1/30000000, 25555)
mini_map_scale = 1/3000000000
minimap_res = (int(300/1080 * resolution[1]),int(300/1080 * resolution[1]))
health_bar_res = (int((3/4)*minimap_res[0]), int(0.05*resolution[1]))
health_bar_surface = pygame.Surface(health_bar_res)
Health_bar = Display_Functions.health_display(health_bar_res,health_bar_surface)

deltaV_bar_res = (int((3/4)*minimap_res[0]), int(0.05*resolution[1]))
deltaV_bar_surface = pygame.Surface(deltaV_bar_res)
deltaV_bar = Display_Functions.deltaV_display(deltaV_bar_res,deltaV_bar_surface)

missiles_bar_res = (int((1/4)*minimap_res[0]), int(0.05*resolution[1]))
missiles_bar_surface = pygame.Surface(missiles_bar_res)
missiles_bar = Display_Functions.missiles_display(missiles_bar_res,missiles_bar_surface)

laser_bar_res = (int((3/4)*minimap_res[0]), int(0.05*resolution[1]))
laser_bar_surface = pygame.Surface(laser_bar_res)
laser_bar = Display_Functions.laser_display(laser_bar_res,laser_bar_surface)

black_hole_bar_res = (int((1/4)*minimap_res[0]), int(0.05*resolution[1]))
black_hole_bar_surface = pygame.Surface(black_hole_bar_res)
black_hole_bar = Display_Functions.black_hole_display(black_hole_bar_res,black_hole_bar_surface)

spacecraft_bar_res = (abs(resolution[0]-minimap_res[0]-health_bar_res[0]-deltaV_bar_res[0]-missiles_bar_res[0]-laser_bar_res[0]-black_hole_bar_res[0]), int(0.5*resolution[1]))
spacecraft_bar_surface = pygame.Surface(spacecraft_bar_res)
spacecraft_bar = Display_Functions.sc_info_display(spacecraft_bar_res,spacecraft_bar_surface)

while running :
    minimap = pygame.Surface(minimap_res)
    map.update(map.SpaceShip)
    spacecraft_bar.update_sc_info(map.SpaceShip.Name,math.sqrt(map.SpaceShip.velocity_x**2 + map.SpaceShip.velocity_y**2),math.sqrt(map.SpaceShip.acceleration_x**2 + map.SpaceShip.acceleration_y**2),Simulation_tools.distance(map.Earth.pos_x,map.Earth.pos_y,map.SpaceShip.pos_x,map.SpaceShip.pos_y),Simulation_tools.distance(map.Sun.pos_x, map.Sun.pos_y, map.SpaceShip.pos_x,map.SpaceShip.pos_y))
    map.draw(resolution, screen)
    map.update_fixed_scale(map.Sun, mini_map_scale)
    map.draw_fixed_scale(minimap_res, resolution,  minimap, mini_map_scale, map.SpaceShip)
    screen.blit(minimap, [0, resolution[1]-minimap_res[1]])
    Health_bar.draw_health_bar(map.SpaceShip.health)
    screen.blit(health_bar_surface, [minimap_res[0],resolution[1]-health_bar_res[1]])
    deltaV_bar.draw_deltaV_bar(map.SpaceShip.deltaV)
    screen.blit(deltaV_bar_surface, [int(minimap_res[0]+health_bar_res[0]), int(resolution[1] - deltaV_bar_res[1])])
    missiles_bar.draw_missiles_bar(map.SpaceShip.Number_of_missiles)
    screen.blit(missiles_bar_surface, [int(minimap_res[0] + health_bar_res[0] + deltaV_bar_res[0]+laser_bar_res[0]), int(resolution[1] - missiles_bar_res[1])])
    laser_bar.draw_laser_bar(map.SpaceShip.Laser_power)
    screen.blit(laser_bar_surface,
                [int(minimap_res[0] + health_bar_res[0] + deltaV_bar_res[0]), int(resolution[1] - laser_bar_res[1])])
    black_hole_bar.draw_black_hole_bar(map.SpaceShip.blackhole)
    screen.blit(black_hole_bar_surface,
                [int(minimap_res[0] + health_bar_res[0] + deltaV_bar_res[0]+missiles_bar_res[0]+laser_bar_res[0]),
                 int(resolution[1]-black_hole_bar_res[1])])
    spacecraft_bar.draw_sc_info()
    screen.blit(spacecraft_bar_surface,
                [abs(minimap_res[0] + health_bar_res[0] + deltaV_bar_res[0]+missiles_bar_res[0]+laser_bar_res[0]+black_hole_bar_res[0]),
                 int(resolution[1]-spacecraft_bar_res[1])])
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
            minimap_res = (int(300 / 720 * resolution[1]), int(300 / 720 * resolution[1]))
            screen = pygame.display.set_mode(resolution, pygame.RESIZABLE)
            screct = screen.get_rect()
            deltaV_bar_res = (int((3 / 4) * minimap_res[0]), int(0.05 * resolution[1]))
            deltaV_bar_surface = pygame.Surface(deltaV_bar_res)
            deltaV_bar = Display_Functions.deltaV_display(deltaV_bar_res, deltaV_bar_surface)
            health_bar_res = (int((3 / 4) * minimap_res[0]), int(0.05 * resolution[1]))
            health_bar_surface = pygame.Surface(health_bar_res)
            Health_bar = Display_Functions.health_display(health_bar_res, health_bar_surface)
            missiles_bar_res = (int((1/4) * minimap_res[0]), int(0.05 * resolution[1]))
            missiles_bar_surface = pygame.Surface(missiles_bar_res)
            missiles_bar = Display_Functions.missiles_display(missiles_bar_res, missiles_bar_surface)
            laser_bar_res = (int((3 / 4) * minimap_res[0]), int(0.05 * resolution[1]))
            laser_bar_surface = pygame.Surface(laser_bar_res)
            laser_bar = Display_Functions.laser_display(laser_bar_res, laser_bar_surface)
            black_hole_bar_res = (int((1 / 4) * minimap_res[0]), int(0.05 * resolution[1]))
            black_hole_bar_surface = pygame.Surface(black_hole_bar_res)
            black_hole_bar = Display_Functions.black_hole_display(black_hole_bar_res, black_hole_bar_surface)
            spacecraft_bar_res = (
                        abs(resolution[0] - minimap_res[0] - health_bar_res[0] - deltaV_bar_res[0] - missiles_bar_res[0] - laser_bar_res[0] -
                        black_hole_bar_res[0]), int(0.5*resolution[1]))
            spacecraft_bar_surface = pygame.Surface(spacecraft_bar_res)
            spacecraft_bar = Display_Functions.sc_info_display(spacecraft_bar_res, spacecraft_bar_surface)
        if event.type == pygame.MOUSEBUTTONDOWN:
            scale_change = 0.9
            if event.button == 4:
               map.scale /= scale_change
            if event.button == 5:
                map.scale *= scale_change
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                map.SpaceShip.hangar_open = not map.SpaceShip.hangar_open
            if event.key == pygame.K_e:
                map.SpaceShip.fire_missile(40000)
            if event.key == pygame.K_b:
                if map.SpaceShip.blackhole > 0:
                    map.sim.blackhole = Celestial_bodies.BlackHole(map.SpaceShip.pos_x, map.SpaceShip.pos_y, 0,
                                                                   15 * 10 ** 8)
                    map.SpaceShip.blackhole -= 1
    controls(event, map)


