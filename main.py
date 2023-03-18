from pygame.time import Clock
from game_controller import GameController
import pygame


border = 10


def main():
    pygame.init()

    screen = pygame.display.set_mode((720, 480))

    game = GameController()
    game.start_next_area()

    clock = pygame.time.Clock()

    running = True

    while running:
        clock.tick(60)
        screen.fill((0, 0, 0))
        
        pygame.draw.rect(screen, (0, 0, 0),
                         (480, 0, 720-480, 480))

        pygame.draw.rect(screen, (100, 100, 100),
                         (480+border, border, 720-480-border*2, 480-border*2))

        game.update(screen)

        pygame.display.flip()

        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False


if __name__ == '__main__':
    main()
