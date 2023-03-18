
import pygame

import random

class FloatingText:

    to_show = None
    x = 0
    y = 0

    vel_x = 0
    vel_y = 0
    time = 0

    def is_dead(self):
        return self.time <= 0

    def __init__(self, text, game_font, type, x, y) -> None:
        self.type = type

        if type == "damage":
            self.to_show, _ = game_font.render(text, (255, 20, 20))
            self.vel_x = (random.random()*2)-1
            self.vel_y = -(random.random()+2)
            self.time = 60
        elif type == "crit":
            self.to_show, _ = game_font.render(text+"!", (101, 0, 194))
            self.vel_x = (random.random()*2)-1
            self.vel_y = -(random.random()+2)
            self.time = 60
        elif type == "level":
            self.to_show, _ = game_font.render(text,(255,255,255))
            self.vel_x = 0
            self.vel_y = -2;
            self.time = 240
        self.x = x
        self.y = y


    def draw(self,screen):
        screen.blit(self.to_show, (self.x,self.y))
        self.x += self.vel_x
        self.y += self.vel_y
        self.time -= 1

        if self.type == "damage" or self.type == "crit":
            self.vel_y += 0.1
