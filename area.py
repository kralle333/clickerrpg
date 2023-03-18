from progress_bar import ProgressBar, ProgressColor
import random
import copy


def get_enemy_chance(e):
    return e.spawn_chance


class Area:

    name = ""
    enemies = []
    boss = None
    level_min = 0
    level_max = 0
    bg_image = ""
    bg_color = (0, 0, 0)

    total_chance = 0

    area_progress = 0
    enemies_beaten = 0
    enemies_to_beat = []

    progress_bar = None

    def __init__(self, name, color, enemies_to_beat) -> None:
        self.bg_color = color
        self.name = name
        self.enemies_to_beat.clear()
        self.progress_bar = ProgressBar(100, 440, 280, 20, 2, (0, 0, 0))
        self.progress_bar.set_progress_colors(
            [ProgressColor(0, (255, 255, 255))])

        for enemy in enemies_to_beat:
            self.enemies_to_beat.append(enemy)

    def add_enemy(self, enemy):
        self.enemies.append(enemy)

    def set_boss(self, boss):
        self.boss = boss

    def reset(self):
        self.enemies_beaten = 0
        self.progress_bar.set_progress(0)

    def get_next_enemy(self):
        if self.enemies_beaten >= len(self.enemies_to_beat):
            return self.boss
        else:
            return self.get_enemy_instance(self.enemies[self.enemies_to_beat[self.enemies_beaten]])

    def on_defeat(self):
        self.enemies_beaten += 1

        progress = self.enemies_beaten/(len(self.enemies_to_beat)+1)
        if progress > 1:
            progress = 1
        self.progress_bar.set_progress(progress)
        return progress >= 1

    def get_enemy_instance(self, enemyTemplate):
        instance = copy.deepcopy(enemyTemplate)
        instance.level = random.randint(self.level_min, self.level_max+1)
        return instance

    def draw_progress(self, screen, game_font):
        game_font.render_to(screen, (100, 395),
                            f"{self.name} Progress:", (255, 255, 255))
        self.progress_bar.draw(screen)

##################
### old: unused
##################
    def get_first_enemy(self):
        return self.get_enemy_instance(self.enemies[-1])

    def get_enemy(self):
        to_get = random.randint(0, self.total_chance)
        for enemy in self.enemies:
            if to_get < enemy.spawn_chance:
                return self.get_enemy_instance(enemy)
            to_get -= enemy.spawn_chance

        return self.get_first_enemy()

    def sort_and_stuff(self):
        for enemy in self.enemies:
            self.total_chance += enemy.spawn_chance
        self.enemies.sort(reverse=False, key=get_enemy_chance)
