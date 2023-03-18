from pygame.time import Clock
from game_controller import GameController
import pygame



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
        
        game.update()
        game.draw(screen)

        pygame.display.flip()

        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False


if __name__ == '__main__':
    main()
