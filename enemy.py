import os
from progress_bar import ProgressBar
import pygame
import random


class Enemy:

    name = ""
    sprite = ""

    current_hp = 0
    max_hp = 0

    min_dmg = 0
    max_dmg = 0
    speed = 0
    gold = 0
    xp = 0
    spawn_chance = 0

    image = None
    name_text = None
    health_bar = None

    level = 0

    pos_x = 0
    pos_y = 0

    shake_x = 0
    shake_y = 0

    health_bar = None

    def __init__(self, name, sprite, hp, speed, min_dmg, max_dmg, chance, gold, xp) -> None:
        self.name = name
        self.sprite = os.path.join("art", "enemies", sprite)
        self.current_hp = self.max_hp = hp
        self.spawn_chance = chance
        self.min_dmg = min_dmg
        self.max_dmg = max_dmg
        self.speed = speed
        self.gold = gold
        self.xp = xp

    def get_health_pct(self):
        return self.current_hp/self.max_hp

    def load_gfx(self, game_font):
        self.image = pygame.image.load(self.sprite)
        self.name_text, _ = game_font.render(
            f"ENEMY: {self.name} lvl {self.level}", (255, 255, 255))

        self.pos_x = 480/2 - self.image.get_width() / 2
        self.pos_y = 480/2 - self.image.get_height()/2

        self.health_bar = ProgressBar(
            480/2-50, self.pos_y-40, 100, 24, 2, (0, 0, 0))
        self.health_bar.set_health_bar_colors()
        self.health_bar.set_progress(1)

    def damage(self, damage, is_crit):
        self.current_hp -= damage
        if self.current_hp < 0:
            self.current_hp = 0
        self.health_bar.set_progress(self.get_health_pct())

        if is_crit:
            self.shake_x = random.randint(-10, 10)
            self.shake_y = random.randint(-10, 10)
        else:
            self.shake_x = random.randint(-5, 5)
            self.shake_y = random.randint(-5, 5)

    def get_dmg(self):
        return random.randint(self.min_dmg, self.max_dmg)

    def draw(self, screen):

        if self.shake_x > 0:
            self.shake_x -= 0.2
        if self.shake_y > 0:
            self.shake_y -= 0.2

        if self.shake_x < 0:
            self.shake_x += 0.2
        if self.shake_y < 0:
            self.shake_y += 0.2

        screen.blit(self.image, (self.pos_x+self.shake_x,
                    self.pos_y+self.shake_y))
        screen.blit(self.name_text, (480/2 -
                                     self.name_text.get_width()/2, 10))
        self.health_bar.draw(screen)
