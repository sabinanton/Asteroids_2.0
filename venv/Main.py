import math
import random

import Celestial_bodies
import Constants
import Display_Functions
import Maps
import Screens
import Simulation_tools
import pygame
import sys
import time

game_started = False
now = 10 ** 25
future = 10000


def controls(event, Map):
    """
    This function describes how user inputs should translate into spacecraft actions
    :param event: The type of input the user enters into the computer
    :param Map: Represents the map where the spacecraft moves around
    :return:
    """
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        Map.SpaceShip.T_accelerate(12000000, Map.step)
    if keys[pygame.K_d]:
        Map.SpaceShip.Rotate(-1, 4 * 10 ** (-7))
    if keys[pygame.K_a]:
        Map.SpaceShip.Rotate(1, 4 * 10 ** (-7))
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

"""Describes the size and shape of the main game screen"""
resolution = (1080, 720)
screen = pygame.display.set_mode(resolution, pygame.RESIZABLE)

screct = screen.get_rect()
black = (0, 0, 0)
running = True
i = 0
"""Creates the large game map where the spacecraft moves"""
map = Maps.Game_Map(1 / 30000000, 25555)
"""Creates the minimap located in lower left corner of game screen (next two lines)"""
mini_map_scale = 1 / 3000000000
minimap_res = (int(300 / 1080 * resolution[1]), int(300 / 1080 * resolution[1]))
"""Creates health bar as independent surface (next three lines)"""
health_bar_res = (int((3 / 4) * minimap_res[0]), int(0.05 * resolution[1]))
health_bar_surface = pygame.Surface(health_bar_res)
Health_bar = Display_Functions.health_display(health_bar_res, health_bar_surface)

"""Creates deltaV bar as independent surface (next three lines)"""
deltaV_bar_res = (int((3 / 4) * minimap_res[0]), int(0.05 * resolution[1]))
deltaV_bar_surface = pygame.Surface(deltaV_bar_res)
deltaV_bar = Display_Functions.deltaV_display(deltaV_bar_res, deltaV_bar_surface)

"""Creates missiles counter as independent surface (next three lines)"""
missiles_bar_res = (int((1 / 4) * minimap_res[0]), int(0.05 * resolution[1]))
missiles_bar_surface = pygame.Surface(missiles_bar_res)
missiles_bar = Display_Functions.missiles_display(missiles_bar_res, missiles_bar_surface)

"""Creates laser bar as independent surface (next three lines)"""
laser_bar_res = (int((3 / 4) * minimap_res[0]), int(0.05 * resolution[1]))
laser_bar_surface = pygame.Surface(laser_bar_res)
laser_bar = Display_Functions.laser_display(laser_bar_res, laser_bar_surface)

"""Creates black hole counter as independent surface (next three lines)"""
black_hole_bar_res = (int((1 / 4) * minimap_res[0]), int(0.05 * resolution[1]))
black_hole_bar_surface = pygame.Surface(black_hole_bar_res)
black_hole_bar = Display_Functions.black_hole_display(black_hole_bar_res, black_hole_bar_surface)

"""Creates spacecraft information display as independent surface (next three lines)"""
spacecraft_bar_res = (abs(
    resolution[0] - minimap_res[0] - health_bar_res[0] - deltaV_bar_res[0] - missiles_bar_res[0] - laser_bar_res[0] -
    black_hole_bar_res[0]), int(0.5 * resolution[1]))
spacecraft_bar_surface = pygame.Surface(spacecraft_bar_res)
spacecraft_bar = Display_Functions.sc_info_display(spacecraft_bar_res, spacecraft_bar_surface)

"""Creates minerals counter as independent surface (next three lines)"""
minerals_bar_res = (int((1 / 2) * minimap_res[0]), int(0.05 * resolution[1]))
minerals_bar_surface = pygame.Surface(minerals_bar_res)
minerals_bar = Display_Functions.minerals_display(minerals_bar_res, minerals_bar_surface)

"""Creates rare gas counter as independent surface (next three lines)"""
rare_gas_bar_res = (int((1 / 2) * minimap_res[0]), int(0.05 * resolution[1]))
rare_gas_bar_surface = pygame.Surface(rare_gas_bar_res)
rare_gas_bar = Display_Functions.rare_gas_display(rare_gas_bar_res, rare_gas_bar_surface)

"""Creates profit counter as independent surface (next three lines)"""
profit_bar_res = (int((2 / 3) * minimap_res[0]), int(0.05 * resolution[1]))
profit_bar_surface = pygame.Surface(profit_bar_res)
profit_bar = Display_Functions.Profit_Display(profit_bar_res, profit_bar_surface)

"""Creates start screen as independent surface. Also adds the game cursor to game screen (next five lines)"""
start_screen = Screens.Start_Screen(screen, resolution)
cursor = pygame.image.load(Display_Functions.resource_path("Cursor.png"))
cursor = pygame.transform.scale(cursor, (25, 25))
pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
soundtrack = [pygame.mixer.Sound(Display_Functions.resource_path("Soundtrack.wav")),pygame.mixer.Sound(Display_Functions.resource_path("Soundtrack2.wav"))]
song = random.randint(0,1)
"""Creates start end screen (next line)"""
end_screen = Screens.end_screen(screen, resolution, map.SpaceShip.health, map.SpaceShip.deltaV,
                                map.SpaceShip.Number_of_missiles, map.SpaceShip.Minerals, map.SpaceShip.Rare_Gases)


def end_screen_check():
    """
    This function checks whether the end screen should be activated based on gameplay status
    :return:
    """
    if map.SpaceShip.health <= 0 or Simulation_tools.distance(map.SpaceShip.pos_x, map.SpaceShip.pos_y, map.Sun.pos_x,
                                                              map.Sun.pos_y) > 20 * Constants.AU:
        end_screen.end_is_active = True
        soundtrack[song].stop()


while running:
    keys = pygame.key.get_pressed()
    end_screen_check()
    """If statements used below are needed for start screen interaction with user commands"""
    if start_screen.start_is_active:
        start_screen.draw_start_screen()
        if start_screen.play.isReleased and start_screen.play.isHovered and start_screen.HowToPlayActive == False:
            start_screen.start_is_active = False
            map.SpaceShip.Name = start_screen.Name_SC.input
            soundtrack[song].play(-1)
        if start_screen.how_to_play.isReleased and start_screen.how_to_play.isHovered:
            start_screen.HowToPlayActive = True
        elif start_screen.HowToPlayActive and start_screen.HTPclose.isHovered and start_screen.HTPclose.isReleased:
            start_screen.HowToPlayActive = False

        """elif statement draws end screen surface if end screen becomes activated based on gameplay"""
    elif end_screen.end_is_active == True:
        dist = Simulation_tools.distance(map.SpaceShip.pos_x, map.SpaceShip.pos_y, map.Sun.pos_x, map.Sun.pos_y)
        end_screen.draw_end_screen(end_screen.calculate_score(map.SpaceShip.Minerals, map.SpaceShip.Rare_Gases,
                                                              map.SpaceShip.Number_of_missiles, map.SpaceShip.health,
                                                              dist))

        if end_screen.play_again.isReleased and end_screen.play_again.isHovered:
            """This if statement resets everything if the play again button is pressed"""
            game_started = False
            now = 10 ** 25
            future = 10000

            screct = screen.get_rect()
            black = (0, 0, 0)
            running = True
            i = 0
            map = Maps.Game_Map((1 / 30000000*resolution[1]/720), 25555)
            map.update_fixed_scale(map.Sun, mini_map_scale)

            health_bar_res = (int((3 / 4) * minimap_res[0]), int(0.05 * resolution[1]))
            health_bar_surface = pygame.Surface(health_bar_res)
            Health_bar = Display_Functions.health_display(health_bar_res, health_bar_surface)

            deltaV_bar_res = (int((3 / 4) * minimap_res[0]), int(0.05 * resolution[1]))
            deltaV_bar_surface = pygame.Surface(deltaV_bar_res)
            deltaV_bar = Display_Functions.deltaV_display(deltaV_bar_res, deltaV_bar_surface)


            missiles_bar_res = (int((1 / 4) * minimap_res[0]), int(0.05 * resolution[1]))
            missiles_bar_surface = pygame.Surface(missiles_bar_res)
            missiles_bar = Display_Functions.missiles_display(missiles_bar_res, missiles_bar_surface)


            laser_bar_res = (int((3 / 4) * minimap_res[0]), int(0.05 * resolution[1]))
            laser_bar_surface = pygame.Surface(laser_bar_res)
            laser_bar = Display_Functions.laser_display(laser_bar_res, laser_bar_surface)


            black_hole_bar_res = (int((1 / 4) * minimap_res[0]), int(0.05 * resolution[1]))
            black_hole_bar_surface = pygame.Surface(black_hole_bar_res)
            black_hole_bar = Display_Functions.black_hole_display(black_hole_bar_res, black_hole_bar_surface)


            spacecraft_bar_res = (abs(
                resolution[0] - minimap_res[0] - health_bar_res[0] - deltaV_bar_res[0] - missiles_bar_res[0] -
                laser_bar_res[0] -
                black_hole_bar_res[0]), int(0.5 * resolution[1]))
            spacecraft_bar_surface = pygame.Surface(spacecraft_bar_res)
            spacecraft_bar = Display_Functions.sc_info_display(spacecraft_bar_res, spacecraft_bar_surface)

            minerals_bar_res = (int((1 / 2) * minimap_res[0]), int(0.05 * resolution[1]))
            minerals_bar_surface = pygame.Surface(minerals_bar_res)
            minerals_bar = Display_Functions.minerals_display(minerals_bar_res, minerals_bar_surface)

            rare_gas_bar_res = (int((1 / 2) * minimap_res[0]), int(0.05 * resolution[1]))
            rare_gas_bar_surface = pygame.Surface(rare_gas_bar_res)
            rare_gas_bar = Display_Functions.rare_gas_display(rare_gas_bar_res, rare_gas_bar_surface)

            profit_bar_res = (int((2 / 3) * minimap_res[0]), int(0.05 * resolution[1]))
            profit_bar_surface = pygame.Surface(profit_bar_res)
            profit_bar = Display_Functions.Profit_Display(profit_bar_res, profit_bar_surface)

            start_screen.start_is_active = True
            end_screen.end_is_active = False
            end_screen.sound_played = False
            end_screen.loose_st.stop()
            end_screen.win_st.stop()
            song = random.randint(0,1)

        """Following else statement are drawing commands for when user is playing the game"""
    else:
        """All independent surfaces created earlier are blitted on the game screen here"""
        """ The size and position of the surfaces are fractions of the main game screen"""
        minimap = pygame.Surface(minimap_res)
        map.update(map.SpaceShip)
        spacecraft_bar.update_sc_info(map.SpaceShip.Name,
                                      math.sqrt(map.SpaceShip.velocity_x ** 2 + map.SpaceShip.velocity_y ** 2),
                                      math.sqrt(map.SpaceShip.acceleration_x ** 2 + map.SpaceShip.acceleration_y ** 2),
                                      Simulation_tools.distance(map.Earth.pos_x, map.Earth.pos_y, map.SpaceShip.pos_x,
                                                                map.SpaceShip.pos_y),
                                      Simulation_tools.distance(map.Sun.pos_x, map.Sun.pos_y, map.SpaceShip.pos_x,
                                                                map.SpaceShip.pos_y))
        map.draw(resolution, screen)
        map.update_fixed_scale(map.Sun, mini_map_scale)
        map.draw_fixed_scale(minimap_res, resolution, minimap, mini_map_scale, map.SpaceShip)
        screen.blit(minimap, [0, resolution[1] - minimap_res[1]])
        Health_bar.draw_health_bar(map.SpaceShip.health)
        screen.blit(health_bar_surface, [minimap_res[0], resolution[1] - health_bar_res[1]])
        deltaV_bar.draw_deltaV_bar(map.SpaceShip.deltaV)
        screen.blit(deltaV_bar_surface,
                    [int(minimap_res[0] + health_bar_res[0]), int(resolution[1] - deltaV_bar_res[1])])
        missiles_bar.draw_missiles_bar(map.SpaceShip.Number_of_missiles)
        screen.blit(missiles_bar_surface,
                    [int(minimap_res[0] + health_bar_res[0] + deltaV_bar_res[0] + laser_bar_res[0]),
                     int(resolution[1] - missiles_bar_res[1])])
        laser_bar.draw_laser_bar(map.SpaceShip.Laser_power)
        screen.blit(laser_bar_surface,
                    [int(minimap_res[0] + health_bar_res[0] + deltaV_bar_res[0]),
                     int(resolution[1] - laser_bar_res[1])])
        black_hole_bar.draw_black_hole_bar(map.SpaceShip.blackhole)
        screen.blit(black_hole_bar_surface,
                    [int(minimap_res[0] + health_bar_res[0] + deltaV_bar_res[0] + missiles_bar_res[0] + laser_bar_res[
                        0]),
                     int(resolution[1] - black_hole_bar_res[1])])
        spacecraft_bar.draw_sc_info()
        screen.blit(spacecraft_bar_surface,
                    [abs(minimap_res[0] + health_bar_res[0] + deltaV_bar_res[0] + missiles_bar_res[0] + laser_bar_res[
                        0] + black_hole_bar_res[0]),
                     int(resolution[1] - spacecraft_bar_res[1])])
        minerals_bar.draw_minerals_bar(map.SpaceShip.Minerals)
        screen.blit(minerals_bar_surface, (resolution[0] - minerals_bar_res[0], 0))
        map.sim.draw_circle_gain_minerals(math.pi / 6, 20, (255, 255, 255), 12, 50, screen, resolution)
        rare_gas_bar.draw_rare_gas_bar(map.SpaceShip.Rare_Gases)
        screen.blit(rare_gas_bar_surface, (resolution[0] - minerals_bar_res[0] - rare_gas_bar_res[0], 0))
        dist = Simulation_tools.distance(map.SpaceShip.pos_x, map.SpaceShip.pos_y, map.Sun.pos_x, map.Sun.pos_y)
        mission_profit = end_screen.calculate_score(map.SpaceShip.Minerals, map.SpaceShip.Rare_Gases,
                                                    map.SpaceShip.Number_of_missiles, map.SpaceShip.health, dist)
        map.SpaceShip.mission_profit = mission_profit
        profit_bar.draw_profit_bar(map.SpaceShip.mission_profit)
        screen.blit(profit_bar_surface,
                    (resolution[0] - minerals_bar_res[0] - rare_gas_bar_res[0] - profit_bar_res[0], 0))

    """The game only ends if user returns to Earth (or dies). This may not be confused for the beginning of the game 
    where the spacecraftis close to Earth initially. Therefore, following the entry of the first user entry, the 
    computer will wait 10 seconds for the player to leave. After this, the computer will recalculate the distance 
    between the spacecraft and Earth. If this distance is less than 0.15AU, then the user is considered "close to Earth"
    and the game will end"""

    if (keys[pygame.K_SPACE] or keys[pygame.K_d] or keys[pygame.K_a] or keys[pygame.K_w] or keys[
        pygame.K_s]) and game_started == False and start_screen.start_is_active == False:
        game_started = True
        now = time.time()
    if time.time() - now >= 15:
        if spacecraft_bar.distance_from_Earth < 0.12:
            end_screen.end_is_active = True
            soundtrack[song].stop()

    (x, y) = pygame.mouse.get_pos()
    screen.blit(cursor, (x, y))
    pygame.display.flip()
    """Keyboard Commands needed to end the game"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                sys.exit()
        if event.type == pygame.VIDEORESIZE:
            """When main game screen is resized, all independent surfaces created earlier should also be resized"""
            resolution = (event.w, event.h)
            screen = pygame.display.set_mode(resolution, pygame.RESIZABLE)
            start_screen.update(resolution, screen)
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
            missiles_bar_res = (int((1 / 4) * minimap_res[0]), int(0.05 * resolution[1]))
            missiles_bar_surface = pygame.Surface(missiles_bar_res)
            missiles_bar = Display_Functions.missiles_display(missiles_bar_res, missiles_bar_surface)
            laser_bar_res = (int((3 / 4) * minimap_res[0]), int(0.05 * resolution[1]))
            laser_bar_surface = pygame.Surface(laser_bar_res)
            laser_bar = Display_Functions.laser_display(laser_bar_res, laser_bar_surface)
            black_hole_bar_res = (int((1 / 4) * minimap_res[0]), int(0.05 * resolution[1]))
            black_hole_bar_surface = pygame.Surface(black_hole_bar_res)
            black_hole_bar = Display_Functions.black_hole_display(black_hole_bar_res, black_hole_bar_surface)
            spacecraft_bar_res = (
                abs(resolution[0] - minimap_res[0] - health_bar_res[0] - deltaV_bar_res[0] - missiles_bar_res[0] -
                    laser_bar_res[0] -
                    black_hole_bar_res[0]), int(0.5 * resolution[1]))
            spacecraft_bar_surface = pygame.Surface(spacecraft_bar_res)
            spacecraft_bar = Display_Functions.sc_info_display(spacecraft_bar_res, spacecraft_bar_surface)
            minerals_bar_res = (int((1 / 2) * minimap_res[0]), int(0.05 * resolution[1]))
            minerals_bar_surface = pygame.Surface(minerals_bar_res)
            minerals_bar = Display_Functions.minerals_display(minerals_bar_res, minerals_bar_surface)
            rare_gas_bar_res = (int((1 / 2) * minimap_res[0]), int(0.05 * resolution[1]))
            rare_gas_bar_surface = pygame.Surface(rare_gas_bar_res)
            rare_gas_bar = Display_Functions.rare_gas_display(rare_gas_bar_res, rare_gas_bar_surface)
            profit_bar_res = (int((2 / 3) * minimap_res[0]), int(0.05 * resolution[1]))
            profit_bar_surface = pygame.Surface(profit_bar_res)
            profit_bar = Display_Functions.Profit_Display(profit_bar_res, profit_bar_surface)
            end_screen.update(resolution, screen)
        if start_screen.start_is_active:
            start_screen.Name_SC.text_box_controls(event)
        if start_screen.start_is_active == False and end_screen.end_is_active == False:
            """Controls for map scaling and spacecraft actions are activated when start and end screen are inactive"""
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

    if start_screen.start_is_active == False:
        controls(event, map)
