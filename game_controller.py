from random import randint
import random
from floating_text import FloatingText
import pygame
import pygame.freetype  # Import the freetype module.
import os

from area import Area
from enemy import Enemy
from player import Player


class GameController:
    current_area_index = -1
    current_enemy = None
    won = False

    prev_press = False

    areas = []

    game_font = None

    screen = None

    player = None

    ticks = 0

    floating_texts = []

    def __init__(self) -> None:
        self.game_font = pygame.freetype.Font(
            os.path.join("art", "EightBitDragon-anqx.ttf"), 20)

        self.title_font = pygame.freetype.Font(
            os.path.join("art", "EightBitDragon-anqx.ttf"), 24)
        forest = Area("Forest", (0, 118, 2), "battleback1.png",
                      [0, 1, 1, 2, 1, 3, 2, 1, 3, 2])
        forest.add_enemy(
            Enemy("Slime", "slimeiii.png", 20, 120, 1, 2, 50, 1, 1))
        forest.add_enemy(
            Enemy("Bat", "Mountain Bat.png", 30, 30, 1, 2, 30, 2, 4))
        forest.add_enemy(
            Enemy("Mushroom", "Toxic Shroom A.png", 50, 120, 1, 10, 15, 10, 10))
        forest.add_enemy(Enemy("Friendly Tree",
                         "Forest Tree.png", 200, 500, 10, 30, 5, 20, 20))
        forest.level_min = 1
        forest.level_max = 3
        forest.set_boss(Enemy(
            "Forest Boss", "Boss Continental Turtle Rukkha.png", 1000, 500, 1, 100, 0, 500, 100))
        self.areas.append(forest)

        desert = Area("Desert", (210, 187, 0), "battleback3.png",
                      [0, 1, 2, 1, 2, 3, 2, 1, 3, 2])
        desert.add_enemy(Enemy("Snek", "Desert Sand Snake.png",
                         100, 60, 5, 10, 50, 4, 10))
        desert.add_enemy(
            Enemy("Bunny", "Desert Rock Bunny.png", 100, 15, 1, 10, 15, 50, 100))
        desert.add_enemy(
            Enemy("Cactus", "Toxic Cactus B.png", 300, 120, 10, 100, 30, 20, 15))
        desert.add_enemy(
            Enemy("Tentacles", "Desert Sand Tentacle.png", 500, 30, 1, 20, 15, 50, 100))
        desert.level_min = 5
        desert.level_max = 10
        desert.set_boss(Enemy(
            "Desert Boss", "Cave Dweller Worm.png", 2000, 160, 100, 200, 0, 1000, 500))
        self.areas.append(desert)

        ice = Area("Frozen Cave", (	0, 97, 159), "battleback2.png", [
                   0, 1, 2, 1, 2, 3, 2, 1, 3, 2])
        ice.add_enemy(Enemy("Ice Cave Bat", "Ice Cave Bat.png",
                      200, 60, 5, 10, 50, 4, 10))
        ice.add_enemy(
            Enemy("Ice Lion", "Ice Lion.png", 150, 15, 1, 10, 15, 50, 100))
        ice.add_enemy(
            Enemy("Ice Golem", "Ice Golem.png", 600, 120, 10, 100, 30, 20, 15))
        ice.add_enemy(
            Enemy("Frozen Birdie", "Ice Avian.png", 1000, 30, 1, 20, 15, 50, 100))
        ice.level_min = 15
        ice.level_max = 30
        ice.set_boss(Enemy(
            "Ice Cave Boss", "Boss Ice Titan Demeres.png", 5000, 100, 500, 1000, 0, 5000, 1000))
        self.areas.append(ice)

        self.player = Player(50)

    def start_area(self, area):
        self.current_area = area
        self.current_area.reset()
        self.current_area.load_gfx()
        self.set_current_enemy(area.get_next_enemy())

    def start_next_area(self):
        self.current_area_index += 1
        if self.current_area_index >= len(self.areas):
            self.won = True
        else:
            self.start_area(self.areas[self.current_area_index])

    def set_current_enemy(self, enemy):
        self.current_enemy = enemy
        self.current_enemy.load_gfx(self.title_font)

    def update(self):
        if self.won:
            return
            
        if self.ticks % self.player.speed == 0:
            dmg = self.player.get_dmg()
            is_crit = False
            if random.randint(0, 100) > 95:
                dmg *= 2
                is_crit = True

            self.current_enemy.damage(dmg, is_crit)
            self.floating_texts.append(FloatingText(
                str(dmg), self.game_font, "crit" if is_crit else "damage", 480/2, 480/2))

        if self.ticks % self.current_enemy.speed == 0:
            dmg = self.current_enemy.get_dmg()
            self.player.damage(dmg)
            self.floating_texts.append(FloatingText(
                str(dmg), self.game_font, "damage", 650, 70))

        x, y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] and self.prev_press == False and x <= 480 and y <= 480:
            dmg = self.player.click_dmg
            is_crit = False
            if random.randint(0, 100) > 99:
                dmg *= 2
                is_crit = True

            self.current_enemy.damage(dmg, is_crit)

            self.floating_texts.append(FloatingText(
                str(dmg), self.game_font, "crit" if is_crit else "damage", 480/2, 200))
        self.prev_press = pygame.mouse.get_pressed()[0]

        if self.current_enemy.current_hp <= 0:
            if self.player.on_defeat(self.current_enemy):
                self.floating_texts.append(FloatingText(
                    "LEVEL UP!", self.game_font, "level", 180, 200))
            if self.current_area.on_defeat() == False:
                self.set_current_enemy(self.current_area.get_next_enemy())
            else:
                self.start_next_area()

        if self.player.current_hp <= 0:
            self.current_area_index = -1
            self.start_next_area()
            self.player.reset()
            self.ticks = -100
            self.floating_texts = []
        else:
            self.player.update()

        self.ticks += 1


    def draw(self, screen):
        if self.won:
            pygame.draw.rect(screen, (40, 170, 40), (0, 0, 720, 480))
            self.game_font.render_to(screen, (235, 220),
                                        "You are victorious!", (255, 255, 255))
            return
        

        self.current_area.draw(screen)

        # Sidebar ui
        self.player.draw(screen, self.game_font)
        
        # game over screen
        if self.ticks < 0:
            pygame.draw.rect(screen, (255, 40, 40), (0, 0, 720, 480))
            self.game_font.render_to(screen, (205, 220),
                                        "You have been defeated!", (255, 255, 255))
            return
        
        self.current_enemy.draw(screen)
        self.current_area.draw_progress(screen, self.game_font)

        # floating texts
        i = (len(self.floating_texts)-1)
        while i >= 0:
            text = self.floating_texts[i]
            text.draw(screen)
            if text.is_dead():
                self.floating_texts.pop(i)
            i -= 1
