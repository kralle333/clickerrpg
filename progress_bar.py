

import pygame
import math


class ProgressColor:

    color = (0, 0, 0)
    progress = 0

    def __init__(self, progress, color) -> None:
        self.progress = progress
        self.color = color


class ProgressBar:
    x = 0
    y = 0
    width = 0
    height = 0
    border_rect = (0, 0, 0, 0)
    progress = 0

    border_size = 0
    border_color = (0, 0, 0)
    progress_colors = []
    progress_color = (0, 0, 0)

    def __init__(self, x, y, width, height, border_size, border_color) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.border_size = border_size
        self.border_rect = (x, y, width, height)
        self.border_color = border_color

    def set_progress_colors(self, colors):
        self.progress_colors = colors

    def set_health_bar_colors(self):
        self.progress_colors = [
            ProgressColor(0.7, (0, 255, 0)),
            ProgressColor(0.25, (255, 255, 0)),
            ProgressColor(0, (255, 0, 0))
        ]

    def set_progress(self, progress):
        self.progress = progress
        for progress_color in self.progress_colors:
            if progress >= progress_color.progress:
                self.progress_color = progress_color.color
                return

    def draw(self, screen):

        pygame.draw.rect(screen, self.border_color, self.border_rect)
        w = (self.width*self.progress) - self.border_size*2
        if w < 0:
            w = 0
        rect = (self.x+self.border_size, self.y+self.border_size,
                w, self.height-self.border_size*2)
        pygame.draw.rect(screen, self.progress_color, rect)
