import pygame
import Constants
import math
import os
import sys
import Screens


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class health_display:
    def __init__(self, resolution, surface):
        """
        Describes the in-game health display bar, which shows how health of spacecraft decreases after collisions
        :param resolution: The size of the display subsurface
        :param surface: Subsurface which will be blitted onto the game screen (which is the main surface)
        """
        self.Resolution = resolution
        self.Surface = surface
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.heart = pygame.image.load(resource_path("Asteroids_2_health_icon.png"))
        self.image = pygame.transform.scale(self.heart, ((int(0.85*self.Resolution[1]), int(0.85*self.Resolution[1]))))

    def draw_health_bar(self, health):
        """
        This function draws the actual health bar
        :param health: This represents the health of the spacecraft, as a fraction out of 100%
        :return:
        """
        background = pygame.Rect([0, 0, self.Resolution[0], self.Resolution[1]])
        health = min(100, max(health, 0))
        health_bar = pygame.Rect(
        [int(0.15 * self.Resolution[0] + 6), 6, int(0.85 * self.Resolution[0] - 12), self.Resolution[1] - 12])
        life_bar = pygame.Rect(
        [int(0.15 * self.Resolution[0] + 6), 6, int((0.85 * self.Resolution[0] - 12) * (health / 100)),
        int(self.Resolution[1] - 12)])
        pygame.draw.rect(self.Surface, self.black, background)
        pygame.draw.rect(self.Surface, self.white, background, 2)
        pygame.draw.rect(self.Surface, self.white, health_bar, 2)
        pygame.draw.rect(self.Surface, self.white, life_bar)
        self.Surface.blit(self.image, (int(0.02*self.Resolution[0]), int((self.Resolution[1]-self.image.get_rect().size[1])/2)))

class deltaV_display:
    def __init__(self, resolution, surface):
        """
        Describes the in-game deltaV display bar, which shows how available propellant is depleted following burns.
        :param resolution: The size of the display subsurface
        :param surface: Subsurface which will be blitted onto the game screen (which is the main surface)
        """
        self.Resolution = resolution
        self.Surface = surface
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.heart = pygame.image.load(resource_path("Asteroids_2_fuel_icon.png"))
        self.image = pygame.transform.scale(self.heart, (int(0.85*self.Resolution[1]), int(0.85*self.Resolution[1])))

    def draw_deltaV_bar(self, deltaV):
        """
        This function draws the actual delta V display
        :param deltaV: This represents the available propellant left in the spacecraft, as a fraction out of 10000.
        :return:
        """
        background = pygame.Rect([0, 0, self.Resolution[0], self.Resolution[1]])
        fuel_bar = pygame.Rect(
            [int(0.15 * self.Resolution[0] + 6), 6, int(0.85 * self.Resolution[0] - 12), self.Resolution[1] - 12])
        tank_bar = pygame.Rect(
            [int(0.15 * self.Resolution[0] + 6), 6, int((0.85 * self.Resolution[0] - 12) * (deltaV / 10000)),
             self.Resolution[1] - 12])
        pygame.draw.rect(self.Surface, self.black, background)
        pygame.draw.rect(self.Surface, self.white, background, 2)
        pygame.draw.rect(self.Surface, self.white, fuel_bar, 2)
        pygame.draw.rect(self.Surface, self.white, tank_bar)
        self.Surface.blit(self.image, (int(0.02*self.Resolution[0]), int((self.Resolution[1]-self.image.get_rect().size[1])/2)))


class missiles_display:
    def __init__(self, resolution, surface):
        """
        Describes the in-game missiles display counter, which shows how available ammunition is depleted after firing
        :param resolution: The size of the display subsurface
        :param surface: Subsurface which will be blitted onto the game screen (which is the main surface)
        """
        self.Resolution = resolution
        self.Surface = surface
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.missiles = pygame.image.load(resource_path("Asteroids_2_missle_icon.png"))
        self.image = pygame.transform.scale(self.missiles, (int(0.85*self.Resolution[1]), int(0.85*self.Resolution[1])))

    def draw_missiles_bar(self, Number_of_missiles):
        """
        This function draws the actual missile display bar
        :param Number_of_missiles: This represents the ammunition available in the spacecraft, as a fraction out of 30
        :return:
        """
        background = pygame.Rect([0, 0, self.Resolution[0], self.Resolution[1]])
        font = pygame.font.SysFont("Consolas", 20)
        text_line = "" + str(Number_of_missiles)
        text_surface = font.render(text_line, True, self.white)
        pygame.draw.rect(self.Surface, self.black, background)
        pygame.draw.rect(self.Surface, self.white, background, 2)
        self.Surface.blit(text_surface, (int(0.6*self.Resolution[0]), int((self.Resolution[1]-font.size(text_line)[1])/2)))
        self.Surface.blit(self.image, (int(0.05*self.Resolution[0]), int((self.Resolution[1]-self.image.get_rect().size[1])/2)))


class laser_display:
    def __init__(self, resolution, surface):
        """
        Describes the in-game laser display bar, which shows the available electrical power for the laser
        :param resolution: The size of the display subsurface
        :param surface: Subsurface which will be blitted onto the game screen (which is the main surface)
        """
        self.Resolution = resolution
        self.Surface = surface
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.heart = pygame.image.load(resource_path("Asteroids_2_laser_icon.png"))
        self.image = pygame.transform.scale(self.heart, (int(0.85*self.Resolution[1]), int(0.85*self.Resolution[1])))

    def draw_laser_bar(self, laser):
        """
        This function draws the actual display
        :param laser: This represents the available electrical power for the laser, as a fraction out of 100
        :return:
        """
        background = pygame.Rect([0, 0, self.Resolution[0], self.Resolution[1]])
        laser_bar = pygame.Rect(
            [int(0.15 * self.Resolution[0] + 6), 6, int(0.85 * self.Resolution[0] - 12), self.Resolution[1] - 12])
        device_bar = pygame.Rect(
            [int(0.15 * self.Resolution[0] + 6), 6, int((0.85 * self.Resolution[0] - 12) * (laser / 100)),
             self.Resolution[1] - 12])
        pygame.draw.rect(self.Surface, self.black, background)
        pygame.draw.rect(self.Surface, self.white, background, 2)
        pygame.draw.rect(self.Surface, self.white, laser_bar, 2)
        pygame.draw.rect(self.Surface, self.white, device_bar)
        self.Surface.blit(self.image, (int(0.02*self.Resolution[0]), int((self.Resolution[1]-self.image.get_rect().size[1])/2)))


class black_hole_display:
    def __init__(self, resolution, surface):
        """
        Describes the in-game black hole display counter, which shows how available blackholes are depleted after firing
        :param resolution: The size of the display subsurface
        :param surface: Subsurface which will be blitted onto the game screen (which is the main surface)
        """
        self.Resolution = resolution
        self.Surface = surface
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)

    def draw_black_hole_bar(self, Black_hole_count):
        """
        This function draws the actual display
        :param Black_hole_count: The available black holes that the spacecraft has for altering space and time
        :return:
        """
        background = pygame.Rect([0, 0, self.Resolution[0], self.Resolution[1]])
        font = pygame.font.SysFont("Consolas", 20)
        text_line = "" + str(Black_hole_count)
        text_surface = font.render(text_line, True, self.white)
        pygame.draw.rect(self.Surface, self.black, background)
        pygame.draw.rect(self.Surface, self.white, background, 2)
        pygame.draw.circle(self.Surface, self.white, (int(0.25*self.Resolution[0]), int(self.Resolution[1]/2)), int(0.4*self.Resolution[1]), 2)
        self.Surface.blit(text_surface, (int(0.6*self.Resolution[0]), int((self.Resolution[1]-font.size(text_line)[1])/2)))

class sc_info_display:
    def __init__(self,resolution,surface):
        """
        Describes the in-game display showing vital spacecraft information, like name, velocity and distance from Earth
        :param resolution: The size of the display subsurface
        :param surface: Subsurface which will be blitted onto the game screen (which is the main surface)
        """
        self.Resolution = resolution
        self.Surface = surface
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.name = ""
        self.velocity = 0
        self.acceleration = 0
        self.distance_from_Earth = 0
        self.distance_from_Sun = 0

    def draw_sc_info(self):
        """
        This function draws the actual display containing all the information
        :return:
        """
        n=6
        background = pygame.Rect([0,0,self.Resolution[0],self.Resolution[1]])
        pygame.draw.rect(self.Surface, self.black, background)
        pygame.draw.rect(self.Surface, self.white, background, 2)
        font = pygame.font.SysFont("Consolas", 14)
        name_text_line = "Spacecraft Name: " + str(self.name)
        name_text_surface = font.render(name_text_line, True, self.white)
        self.Surface.blit(name_text_surface, (((self.Resolution[0]-font.size(name_text_line)[0])/2), (self.Resolution[1]/n)))
        velocity_text_line = "Velocity: " + str(self.velocity) + " [km/s]"
        velocity_text_surface = font.render(velocity_text_line, True, self.white)
        self.Surface.blit(velocity_text_surface, (((self.Resolution[0]-font.size(velocity_text_line)[0])/2), (self.Resolution[1]*2/n)))
        acceleration_text_line = "Acceleration: " + str(self.acceleration) + " [m/s^2]"
        acceleration_text_surface = font.render(acceleration_text_line, True, self.white)
        self.Surface.blit(acceleration_text_surface, (((self.Resolution[0]-font.size(acceleration_text_line)[0])/2), (self.Resolution[1]*3/n)))
        distance_from_Earth_text_line = "Distance from Earth: " + str(self.distance_from_Earth) + " [AU]"
        distance_from_Earth_text_surface = font.render(distance_from_Earth_text_line, True, self.white)
        self.Surface.blit(distance_from_Earth_text_surface, (((self.Resolution[0]-font.size(distance_from_Earth_text_line)[0])/2), (self.Resolution[1]*4/n)))
        distance_from_Sun_text_line = "Distance from Sun: " + str(self.distance_from_Sun) + " [AU]"
        distance_from_Sun_text_surface = font.render(distance_from_Sun_text_line, True, self.white)
        self.Surface.blit(distance_from_Sun_text_surface, (((self.Resolution[0]-font.size(distance_from_Sun_text_line)[0])/2), (self.Resolution[1]*5/n)))

    def update_sc_info(self,name,velocity,acceleration,distance_from_Earth,distance_from_Sun):
        """
        This function updates all the information in the display after every time step of the simulation
        :param name: Name of Spacecraft, remains constant throughout game
        :param velocity: Velocity of Spacecraft, updates after every time step of the simulation
        :param acceleration: Acceleration of Spacecraft, updates after every time step of the simulation
        :param distance_from_Earth: Distance between Spacecraft and Earth, updates after every time step of simulation
        :param distance_from_Sun: Distance between Spacecraft and Sun, updates after every time step of the simulation
        :return:
        """
        self.name = name
        self.velocity = round(velocity/1000,1)
        self.acceleration = round(acceleration * 1000,2)
        self.distance_from_Earth = round(distance_from_Earth/Constants.AU,2)
        self.distance_from_Sun = round(distance_from_Sun/Constants.AU,2)

class minerals_display:
    def __init__(self, resolution, surface):
        """
        Describes the in-game minerals display counter, which shows how much minerals the spacecraft has mined
        :param resolution: The size of the display subsurface
        :param surface: Subsurface which will be blitted onto the game screen (which is the main surface)
        """
        self.Resolution = resolution
        self.Surface = surface
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.minerals = pygame.image.load(resource_path("Crystals_game2.png"))
        self.image = pygame.transform.scale(self.minerals, (int(0.85*self.Resolution[1]), int(0.85*self.Resolution[1])))

    def draw_minerals_bar(self, minerals_count):
        """
        This function draws the actual counter on the game screen
        :param minerals_count: The amount of minerals mined by the spacecraft, in tons
        :return:
        """
        background = pygame.Rect([0, 0, self.Resolution[0], self.Resolution[1]])
        font = pygame.font.SysFont("Consolas", 20)
        text_line = "" + str(minerals_count)
        text_surface = font.render(text_line, True, self.white)
        unit_measure = "ton"
        unit_surface = font.render(unit_measure, True, self.white)
        pygame.draw.rect(self.Surface, self.black, background)
        pygame.draw.rect(self.Surface, self.white, background, 2)
        self.Surface.blit(self.image, (int(0.05*self.Resolution[0]), int((self.Resolution[1]-self.image.get_rect().size[1])/2)))
        self.Surface.blit(text_surface, (int(0.35*self.Resolution[0]), int((self.Resolution[1]-font.size(text_line)[1])/2)))
        self.Surface.blit(unit_surface,
                          (int(0.55 * self.Resolution[0]), int((self.Resolution[1] - font.size(text_line)[1]) / 2)))
class rare_gas_display:
    def __init__(self, resolution, surface):
        """
        Describes the in-game rare gas display counter, which shows how much rare gas the spacecraft has mined
        :param resolution: The size of the display subsurface
        :param surface: Subsurface which will be blitted onto the game screen (which is the main surface)
        """
        self.Resolution = resolution
        self.Surface = surface
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.rare_gas = pygame.image.load(resource_path("Gas_barrels.png"))
        self.image = pygame.transform.scale(self.rare_gas, (int(0.95*self.Resolution[1]), int(0.95*resolution[1])))

    def draw_rare_gas_bar(self, rare_gas_count):
        """
        This function draws the actual counter on the game screen
        :param rare_gas_count: The amount of rare gas mined by the spacecraft, in tons
        :return:
        """
        background = pygame.Rect([0, 0, self.Resolution[0], self.Resolution[1]])
        font = pygame.font.SysFont("Consolas", 20)
        text_line = "" + str(rare_gas_count)
        text_surface = font.render(text_line, True, self.white)
        unit_measure = "ton"
        unit_surface = font.render(unit_measure, True, self.white)
        pygame.draw.rect(self.Surface, self.black, background)
        pygame.draw.rect(self.Surface, self.white, background, 2)
        self.Surface.blit(self.image, (int(0.05*self.Resolution[0]), int((self.Resolution[1]-self.image.get_rect().size[1])/2)))
        self.Surface.blit(text_surface, (int(0.35*self.Resolution[0]), int((self.Resolution[1]-font.size(text_line)[1])/2)))
        self.Surface.blit(unit_surface, (int(0.55*self.Resolution[0]), int((self.Resolution[1]-font.size(text_line)[1])/2)))


class Button:
    def __init__(self, surface, text, color, x, y, width, height):
        """
        Describes the various in-game buttons that are present, such as the "Play" and the "How to Play" buttons
        :param surface: Subsurface which will be blitted onto the game screen (which is the main surface)
        :param text: Text which will be printed on the button
        :param color: Color of the button
        :param x: X-position of top left corner of button on the game screen
        :param y: Y-position of top left corner of button on the game screen
        :param width: Width of button
        :param height: Height of button
        """
        self.Surface = surface
        self.Text = text
        self.Color = color
        self.X = x
        self.Y = y
        self.Width = width
        self.Height = height
        self.isHovered = False
        self.isPressed = False
        self.isReleased = False
        self.lastframe = False

    def draw(self):
        """
        Draws the actual buttons on the screen and how it interacts with the cursor on the screen
        :return:
        """
        self.isReleased = False

        color_o = (255 - self.Color[0], 255 - self.Color[1], 255 - self.Color[2])
        color_i = self.Color
        x, y = pygame.mouse.get_pos()
        i1, i2, i3 = pygame.mouse.get_pressed()
        self.isPressed = False
        self.isHovered = False
        if i1 == 1:
            self.isPressed = True
        if self.isPressed == False and self.lastframe == True:
            self.isReleased = True
        if self.X <= x <= self.X + self.Width and self.Y <= y <= self.Y + self.Height:
            self.isHovered = True
        if self.isPressed and self.isHovered:
            aux = color_o
            color_o = color_i
            color_i = aux
        elif self.isHovered:
            color_i = (50 + color_i[0], 50 + color_i[1], 50 + color_i[2])

        self.lastframe = self.isPressed

        rect = pygame.Rect(self.X, self.Y, self.Width, self.Height)
        pygame.draw.rect(self.Surface, color_i, rect)
        pygame.draw.rect(self.Surface, color_o, rect, 2)
        font = pygame.font.SysFont("Consolas", 20)
        text_surface = font.render(self.Text, True, color_o)
        self.Surface.blit(text_surface, (self.X + (self.Width - font.size(self.Text)[0])/2, self.Y + (self.Height - font.size(self.Text)[1])/2))

    def update(self, x, y, width, height):
        """
        Resizes and repositions the buttons if the game window is changed
        :param x: X-position of top left corner of button on the game screen
        :param y: Y-position of top left corner of button on the game screen
        :param width: Width of button
        :param height: Height of button
        :return:
        """
        self.X = x
        self.Y = y
        self.Width = width
        self.Height = height

class Text_box_Display:
    def __init__(self, surface, label, color, x, y, width, height):
        """
        Describes the text box on the start screen where spacecraft name is inputted by player
        :param surface: Subsurface which will be blitted onto the game screen (which is the main surface)
        :param label: The word "Name" which appears in front of text box where name is inputted
        :param color: Color of the text box
        :param x: X-position of top left corner of button on the game screen
        :param y: Y-position of top left corner of button on the game screen
        :param width: Width of button
        :param height: Height of button
        """
        self.Surface = surface
        self.Label = label
        self.Color = color
        self.Color_2 = (255 - self.Color[0], 255-self.Color[1], 255 - self.Color[2])
        self.X = x
        self.Y = y
        self.Width = width
        self.Height = height
        self.isHovered = False
        self.isPressed = False
        self.input = ""
        self.is_active = False
        self.Period = 100
        self.Cursor_on = True

    def draw_text_box(self):
        """
        Draws the actual text box and describes how it interacts with the user's inputs
        :return:
        """
        pygame.draw.rect(self.Surface, self.Color, (self.X,self.Y,self.Width,self.Height))
        pygame.draw.rect(self.Surface, self.Color_2, (self.X,self.Y,self.Width,self.Height), 2)
        font = pygame.font.SysFont("Consolas", 20)
        text_surface = font.render(self.Label, False, self.Color_2)
        self.Surface.blit(text_surface, (10 + self.X,self.Y+(self.Height-font.size(self.Label)[1])/2))
        x_input = font.size(self.Label)[0] + 5 + self.X
        y_input = self.Y + 5
        width_input = self.Width - (font.size(self.Label)[0] + 10)
        height_input = self.Height - 10
        pygame.draw.rect(self.Surface, self.Color, (x_input,y_input,width_input,height_input))
        input_surface = font.render(self.input, False, self.Color_2)
        self.Surface.blit(input_surface, (15+self.X+font.size(self.Label)[0],self.Y+(self.Height-font.size(self.input)[1])/2))
        if self.is_active == True:
            self.Period -= 1
            if self.Period == 0:
                self.Cursor_on = not self.Cursor_on
                self.Period = 100
            if self.Cursor_on: pygame.draw.rect(self.Surface, self.Color_2, (self.X+15+font.size(self.Label)[0]+font.size(self.input)[0], self.Y + 10, 2, self.Height - 20))

    def text_box_controls(self, event):
        """
        Describes when the text box should be active and thus, should be taking the user's keyboard inputs
        :param event: The type of input that the user enters in the computer
        :return:
        """
        x, y = pygame.mouse.get_pos()
        i1, i2, i3 = pygame.mouse.get_pressed()
        self.isPressed = False
        self.isHovered = False
        if i1 == 1: self.isPressed = True
        if self.X <= x <= self.X + self.Width and self.Y <= y <= self.Y + self.Height:
            self.isHovered = True
        if self.isPressed == True and self.isHovered == True:
            self.is_active = True
        elif self.isPressed == True:
            self.is_active = False

        if self.is_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.input = self.input[:-1]
                else:
                    font = pygame.font.SysFont("Consolas", 20)
                    if font.size(self.input)[0] < self.Width - (font.size(self.Label)[0] + 20):
                        self.input += event.unicode

    def update(self, x, y, width, height):
        """
        Resizes and repositions the text box on the screen when the game window is changed
        :param x: X-position of top left corner of button on the game screen
        :param y: Y-position of top left corner of button on the game screen
        :param width: Width of button
        :param height: Height of button
        :return:
        """
        self.X = x
        self.Y = y
        self.Width = width
        self.Height = height

class Profit_Display:
    def __init__(self, resolution, surface):
        """
        Describes the in-game display which shows how much profit the player has made through mining.
        :param resolution: The size of the display subsurface
        :param surface: Subsurface which will be blitted onto the game screen (which is the main surface)
        """
        self.Resolution = resolution
        self.Surface = surface
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)

    def draw_profit_bar(self, mission_profit):
        """
        This function actually displays the profit display on the game screen
        :param mission_profit: Initially this is negative as initial spacetravel costs are expensive. Debts must be paid
        :return:
        """
        background = pygame.Rect([0, 0, self.Resolution[0], self.Resolution[1]])
        font = pygame.font.SysFont("Consolas", 16)
        text_line = "Profit: " + str(mission_profit)
        text_surface = font.render(text_line, True, self.white)
        unit_measure = "$"
        unit_surface = font.render(unit_measure, True, self.white)
        pygame.draw.rect(self.Surface, self.black, background)
        pygame.draw.rect(self.Surface, self.white, background, 2)
        self.Surface.blit(text_surface, (int(0.05*self.Resolution[0]), int((self.Resolution[1]-font.size(text_line)[1])/2)))
        self.Surface.blit(unit_surface,
                          (int(0.9 * self.Resolution[0]), int((self.Resolution[1] - font.size(text_line)[1]) / 2)))



