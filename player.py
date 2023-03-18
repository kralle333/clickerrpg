import os
from button import Button
from progress_bar import ProgressBar
import pygame
import random


class Player:

    current_hp = 0
    max_hp = 0

    level = 1

    click_dmg = 1
    attack = 2
    gold = 0

    xp = 0
    next_level_xp = 0

    click_upgrade_index = 0
    dmg_upgrade_index = 0

    upgrade_click_cost = [1, 10, 20, 40, 80, 100, 150, 250, 500]
    upgrade_click_benefit = [1, 2, 3, 5, 8, 13, 21, 34, 55]
    upgrade_dmg_cost = [5, 10, 20, 50, 100, 150, 200, 300, 400, 500,
                        600, 700, 800, 900, 1000]
    upgrade_dmg_benefit = [20, 20, 20, 20, 20, 20,
                           20, 20, 20, 20, 20, 20, 20, 20, 20, 20]

    upgrade_click_btn = None
    upgrade_dmg_btn = None

    health_bar = None

    def __init__(self, initial_hp) -> None:
        self.max_hp = initial_hp
        self.next_level_xp = 110
        self.speed = 120
        self.health_bar = ProgressBar(580, 68, 105, 24, 2, (0, 0, 0))
        self.health_bar.set_health_bar_colors()
        self.health_bar.set_progress(1)
        self.reset()

        btn_font = pygame.freetype.Font(
            os.path.join("art", "EightBitDragon-anqx.ttf"), 16)

        self.upgrade_click_btn = Button(
            490, 360, 90, 80,
            (0, 120, 192),
            (51, 179, 255),
            (0, 0, 0),
            "Click",
            btn_font)
        self.upgrade_dmg_btn = Button(
            600, 360, 90, 80,
            (0, 120, 192),
            (51, 179, 255),
            (0, 0, 0),
            "Atk",
            btn_font)

    def reset(self):
        self.current_hp = self.max_hp

    def damage(self, dmg):
        self.current_hp -= dmg
        if self.current_hp < 0:
            self.current_hp = 0

        self.health_bar.set_progress(self.get_health_pct())

    def get_xp(self, xp):
        self.xp += xp
        leveledUp = self.xp >= self.next_level_xp
        while self.xp >= self.next_level_xp:
            self.level += 1
            self.xp = self.xp-self.next_level_xp
            self.next_level_xp = self.level * 20
            self.max_hp *= 1.2
            self.attack *= 1.1 + random.random() * (1.3 - 1.1);
            self.attack = int(self.attack)
            self.reset()
        return leveledUp

    def get_dmg(self):
        min_dmg = int(self.attack*0.8)
        max_dmg = int(self.attack*1.2)
        return random.randint(min_dmg, max_dmg)

    def get_health_pct(self):
        return self.current_hp/self.max_hp

    def on_defeat(self, enemy):
        self.gold += enemy.gold
        return self.get_xp(enemy.xp)

    def update(self):
        self.upgrade_dmg_btn.update()
        self.upgrade_click_btn.update()

        if self.upgrade_dmg_btn.is_click and self.dmg_upgrade_index < len(self.upgrade_dmg_cost):
            cost = self.upgrade_dmg_cost[self.dmg_upgrade_index]
            if self.gold >= cost:
                self.gold -= cost
                self.attack += self.upgrade_dmg_benefit[self.dmg_upgrade_index]
                self.dmg_upgrade_index += 1
            else:
                pass  # floating text
        if self.upgrade_click_btn.is_click and self.click_upgrade_index < len(self.upgrade_click_cost):
            cost = self.upgrade_click_cost[self.click_upgrade_index]
            if self.gold >= cost:
                self.gold -= cost
                self.click_dmg += self.upgrade_click_benefit[self.click_upgrade_index]
                self.click_upgrade_index += 1
            else:
                pass  # floating text

    def draw(self, screen, game_font):

        # BG
        pygame.draw.rect(screen, (100, 100, 100),
                         (480, 60, 220, 390))
        #game_font.render_to(screen, (525, 20), "Player Info", (0, 0, 0))
        game_font.render_to(screen, (490, 70), "Health:", (0, 0, 0))
        self.health_bar.draw(screen)

        game_font.render_to(screen, (490, 230),
                            f"Atk Damage: {self.attack}", (0, 0, 0))
        game_font.render_to(screen, (490, 270),
                            f"Click Damage: {self.click_dmg}", (0, 0, 0))

        game_font.render_to(screen, (528, 320), "Upgrades", (255, 255, 255))
        self.upgrade_dmg_btn.draw(screen)
        self.upgrade_click_btn.draw(screen)

        if len(self.upgrade_click_cost) <= self.click_upgrade_index:
            game_font.render_to(screen, (505, 410), "MAX", (0, 0, 0))
        else:
            game_font.render_to(screen, (505, 410),
                                f"{self.upgrade_click_cost[self.click_upgrade_index]}g", (0, 0, 0))
        if len(self.upgrade_dmg_cost) <= self.dmg_upgrade_index:
            game_font.render_to(screen, (615, 410), "MAX", (0, 0, 0))
        else:
            game_font.render_to(screen, (615, 410),
                                f"{self.upgrade_dmg_cost[self.dmg_upgrade_index]}g", (0, 0, 0))

        game_font.render_to(screen, (490, 110),
                            f"Level: {self.level}", (0, 0, 0))
        game_font.render_to(screen, (490, 150),
                            f"Xp: {self.xp}/{self.next_level_xp}", (0, 0, 0))
        game_font.render_to(screen, (490, 190),
                            f"Gold: {self.gold}", (0, 0, 0))
