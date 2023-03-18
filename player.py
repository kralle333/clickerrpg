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

    upgrade_click_cost = [10, 50, 100, 200, 400, 600, 800, 1000, 1200]
    upgrade_click_benefit = [1, 1, 1, 2, 2, 2, 2, 2, 2]
    upgrade_dmg_cost = [5, 10, 20, 30, 50, 70, 100, 120, 150, 170,
                        190, 210, 220, 250, 300, 350, 400, 500, 600, 700, 800, 900, 1000]
    upgrade_dmg_benefit = [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
                           5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]

    upgrade_click_btn = None
    upgrade_dmg_btn = None

    health_bar = None

    def __init__(self, hp, game_font) -> None:
        self.max_hp = hp
        self.next_level_xp = 20
        self.speed = 80
        self.health_bar = ProgressBar(600, 70, 100, 24, 2, (0, 0, 0))
        self.health_bar.set_health_bar_colors()
        self.health_bar.set_progress(1)
        self.reset()

        btn_font = pygame.freetype.Font(
            os.path.join("art", "EightBitDragon-anqx.ttf"), 16)

        self.upgrade_click_btn = Button(
            500, 360, 80, 80,
            (0, 120, 192),
            (51, 179, 255),
            (0, 0, 0),
            "Click",
            btn_font)
        self.upgrade_dmg_btn = Button(
            615, 360, 80, 80,
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
            self.attack += random.randint(1, 3)
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

    def draw(self, screen, game_font):

        game_font.render_to(screen, (525, 20), "Player Info", (150, 0, 0))
        game_font.render_to(screen, (500, 70), "Health:", (0, 0, 0))
        self.health_bar.draw(screen)

        self.upgrade_dmg_btn.update()
        self.upgrade_click_btn.update()

        if self.upgrade_dmg_btn.is_click:
            cost = self.upgrade_dmg_cost[self.dmg_upgrade_index]
            if self.gold >= cost:
                self.gold -= cost
                self.attack += self.upgrade_dmg_benefit[self.dmg_upgrade_index]
                self.dmg_upgrade_index += 1
            else:
                pass  # floating text
        if self.upgrade_click_btn.is_click:
            cost = self.upgrade_click_cost[self.click_upgrade_index]
            if self.gold >= cost:
                self.gold -= cost
                self.click_dmg += self.upgrade_click_benefit[self.click_upgrade_index]
                self.click_upgrade_index += 1
            else:
                pass  # floating text

        game_font.render_to(screen, (525, 320), "Upgrades", (150, 0, 0))
        self.upgrade_dmg_btn.draw(screen)
        self.upgrade_click_btn.draw(screen)

        game_font.render_to(screen, (515, 410),
                            f"{self.upgrade_click_cost[self.click_upgrade_index]}g", (0, 0, 0))
        game_font.render_to(screen, (630, 410),
                            f"{self.upgrade_dmg_cost[self.dmg_upgrade_index]}g", (0, 0, 0))

        game_font.render_to(screen, (500, 110),
                            f"Level: {self.level}", (0, 0, 0))
        game_font.render_to(screen, (500, 150),
                            f"Xp: {self.xp}/{self.next_level_xp}", (0, 0, 0))
        game_font.render_to(screen, (500, 190),
                            f"Gold: {self.gold}", (0, 0, 0))
        game_font.render_to(screen, (500, 230),
                            f"Damage: {self.attack}", (0, 0, 0))
        game_font.render_to(screen, (500, 270),
                            f"Click Damage: {self.click_dmg}", (0, 0, 0))
