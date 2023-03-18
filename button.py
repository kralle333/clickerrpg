import pygame


class Button:

    x = 0
    y = 0
    width = 0
    height = 0
    color = (0, 0, 0)
    down_color = (0, 0, 0)
    border_color = (0, 0, 0)

    rect = (0, 0, 0, 0)
    border_rect = (0, 0, 0, 0)

    is_over = False
    is_click = False

    def __init__(self, x, y, width, height, color, down_color, border_color, text, font) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.rect = (x+2, y+2, width-4, height-4)
        self.border_rect = (x, y, width, height)

        self.text, _ = font.render(text, (255, 255, 255))
        self.color = color
        self.down_color = down_color
        self.border_color = border_color

    
    def update(self):
        x,y = pygame.mouse.get_pos()
        self.is_over =  x >= self.x and x < self.x+self.width and y >= self.y and y < self.y+self.height
        self.is_click = self.is_over and pygame.mouse.get_pressed()[0]

    def draw(self, screen):
        pygame.draw.rect(screen, self.border_color, self.border_rect)
        button_color = self.down_color if self.is_over else self.color

        pygame.draw.rect(screen, button_color, self.rect)
        screen.blit(self.text, (self.x+self.width/2 -
                    self.text.get_width()/2, self.y+10))
