import sys
import os
import pygame

if not pygame.font:
    print("Warning, fonts disabled")
if not pygame.mixer:
    print("Warning, sound disabled")

root_dir = os.path.split(os.path.abspath(__file__))[0]

FPS = 60
GAME_TITLE = "My Game"
WINDOW_SIZE = (500, 500)
BG_COLOR = (170, 238, 187)


def main():
    pygame.init()
    pygame.display.set_caption(GAME_TITLE)
    fps_clock = pygame.time.Clock()
    window = pygame.display.set_mode(WINDOW_SIZE)

    # Splash Screen
    window.fill(BG_COLOR)
    pygame.display.update()

    while True:
        # Event management
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # This should be at the end of each drawing a frame
        pygame.display.update()

        # FPS control
        fps_clock.tick(FPS)


if __name__ == "__main__":
    main()
