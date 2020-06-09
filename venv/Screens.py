import numpy
import pygame
import Display_Functions
import math
import random
import Constants

class Start_Screen:
    def __init__(self, screen, resolution):
        self.Screen = screen
        self.Resolution = resolution
        self.start_is_active = True
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.play = Display_Functions.Button(self.Screen, "PLAY", self.black, int(0.5*self.Resolution[0]-(0.3*self.Resolution[0]/2)), int(0.6*self.Resolution[1]), int(0.3*self.Resolution[0]), int(0.1*self.Resolution[1]))
        self.how_to_play = Display_Functions.Button(self.Screen, "How to Play", self.black, int(0.5*self.Resolution[0]-(0.3*self.Resolution[0]/2)), int(0.7*self.Resolution[1]), int(0.3*self.Resolution[0]), int(0.1*self.Resolution[1]))
        self.Name_SC = Display_Functions.Text_box_Display(self.Screen, "Name:", self.black, int(0.5*self.Resolution[0]-(0.3*self.Resolution[0]/2)), int(0.5*self.Resolution[1]), int(0.3*self.Resolution[0]), int(0.1*self.Resolution[1]))
        self.HowToPlayActive = False
        self.HTPimage =  pygame.image.load(Display_Functions.resource_path("HowToPlay.png"))
        self.HTPimage = pygame.transform.scale(self.HTPimage, (int(0.5 * self.Resolution[0]) - 4, int(2 / 3 * self.Resolution[1]) - 4))
        self.HTPclose = Display_Functions.Button(self.Screen, "Close", self.black, int(0.5*self.Resolution[0]+(0.2*self.Resolution[0]/2)), int(0.75*self.Resolution[1]), int(0.1*self.Resolution[0]), int(0.05*self.Resolution[1]))



    def draw_start_screen(self):
        pygame.draw.rect(self.Screen, self.black, pygame.Rect(0,0,self.Resolution[0], self.Resolution[1]))
        self.play.draw()
        self.how_to_play.draw()
        self.Name_SC.draw_text_box()
        font = pygame.font.SysFont("Algerian", 110)
        text = "ASTEROIDS 2.0"
        title_surface = font.render(text, False, self.white)
        self.Screen.blit(title_surface, (int((self.Resolution[0]-font.size(text)[0])/2), int(0.15*self.Resolution[1])))
        if self.HowToPlayActive: self.draw_how_to_play()

    def update(self, new_resolution, new_screen):
        self.Screen = new_screen
        self.Resolution = new_resolution
        self.play.update(int(0.5*self.Resolution[0]-(0.3*self.Resolution[0]/2)), int(0.65*self.Resolution[1]), int(0.3*self.Resolution[0]), int(0.1*self.Resolution[1]))
        self.how_to_play.update(int(0.5*self.Resolution[0]-(0.3*self.Resolution[0]/2)), int(0.8*self.Resolution[1]), int(0.3*self.Resolution[0]), int(0.1*self.Resolution[1]))
        self.Name_SC.update(int(0.5*self.Resolution[0]-(0.3*self.Resolution[0]/2)), int(0.5*self.Resolution[1]), int(0.3*self.Resolution[0]), int(0.1*self.Resolution[1]))
        self.HTPimage = pygame.image.load(Display_Functions.resource_path("HowToPlay.png"))
        self.HTPimage = pygame.transform.scale(self.HTPimage, (int(0.5 * self.Resolution[0]) - 4, int(2 / 3 * self.Resolution[1]) - 4))
        self.HTPclose.update(int(0.5*self.Resolution[0]+(0.2*self.Resolution[0]/2)), int(0.75*self.Resolution[1]), int(0.1*self.Resolution[0]), int(0.05*self.Resolution[1]))

    def draw_how_to_play(self):
        width = int(0.5*self.Resolution[0])
        height = int(2/3*self.Resolution[1])
        x = int(0.5*self.Resolution[0] - width/2)
        y = int(0.5*self.Resolution[1] - height/2)
        pygame.draw.rect(self.Screen, self.black, pygame.Rect(x,y,width,height))
        pygame.draw.rect(self.Screen, self.white, pygame.Rect(x,y,width,height),2)
        font = pygame.font.SysFont("Consolas", 12)
        self.Screen.blit(self.HTPimage, (x + 2, y + 2))
        self.HTPclose.draw()

class end_screen:
    def __init__(self, screen, resolution, health, fuel, missiles, minerals, rare_gas):
        self.Screen = screen
        self.Resolution = resolution
        self.end_is_active = False
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.health = health
        self.fuel = fuel
        self.missiles = missiles
        self.minerals = minerals
        self.rare_gas = rare_gas
        self.cost_minerals = 25000
        self.cost_rare_gas = 15000
        self.cost_missiles = 5
        self.repair_factor = 5000
        self.initial_cost = 10000000

    def calculate_score(self, minerals, rare_gas, missiles, health, distance):
        if health <= 0:
            profit = -self.initial_cost
        if distance >= 20*Constants.AU:
            profit = -self.initial_cost
        else:
            profit = round((self.cost_minerals*minerals)+(self.cost_rare_gas*rare_gas)+(missiles*self.cost_missiles)-(1-health/100)*self.repair_factor - self.initial_cost)
        return profit

    def draw_end_screen(self, score):
        pygame.draw.rect(self.Screen, self.black, pygame.Rect(0, 0, self.Resolution[0], self.Resolution[1]))
        text_font = pygame.font.SysFont("Algerian", 80)
        over_text = "GAME OVER"
        over_surface = text_font.render(over_text, False, self.white)
        text_font2 = pygame.font.SysFont("Consolas", 30)
        self.Screen.blit(over_surface, (int((self.Resolution[0]-text_font.size(over_text)[0])/2), int(0.15*self.Resolution[1])))
        win_text = "MISSION SUCCESSFUL! YOUR PROFIT IS: "+str(int(score))+" $"
        win_surface = text_font2.render(win_text, False, self.white)
        lose_text = "MISSION FAILED! YOUR PROFIT IS: "+str(int(score))+" $"
        lose_surface = text_font2.render(lose_text, False, self.white)
        if score>0:
            self.Screen.blit(win_surface, (int((self.Resolution[0]-text_font2.size(win_text)[0])/2), int(0.45*self.Resolution[1])))
        if score<=0:
            self.Screen.blit(lose_surface, (int((self.Resolution[0]-text_font2.size(lose_text)[0])/2), int(0.45*self.Resolution[1])))

    def update(self, new_resolution, new_screen):
        self.Screen = new_screen
        self.Resolution = new_resolution




