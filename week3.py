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
GREETING_MSG = "안녕하세요"
FONT_SIZE = 32
FONT_COLOR = (10, 10, 10)
FONT_FILENAME = "GamjaFlower-Regular.ttf"


def drawTxtCentered(surface, font, str, color=FONT_COLOR):
    cx = surface.get_width() / 2
    cy = surface.get_height() / 2
    text_surf = font.render(str, True, color)
    text_rect = text_surf.get_rect(center=(cx, cy))
    surface.blit(text_surf, text_rect)


def init_window(size):
    window = pygame.display.set_mode(size, pygame.RESIZABLE)
    background = pygame.Surface(size)
    background.fill(BG_COLOR)
    return window, background


def main():
    pygame.init()
    pygame.display.set_caption(GAME_TITLE)
    fps_clock = pygame.time.Clock()
    font_file = os.path.join(root_dir, FONT_FILENAME)
    font = pygame.font.Font(font_file, FONT_SIZE)

    # Splash Screen
    window, background = init_window(WINDOW_SIZE)
    window.blit(background, (0, 0))
    drawTxtCentered(window, font, GREETING_MSG)
    pygame.display.update()

    while True:
        # Event management
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                window, background = init_window(event.size)
                window.blit(background, (0, 0))
                drawTxtCentered(window, font, GREETING_MSG)

        # Drawing a frame

        # This should be at the end of each drawing a frame
        pygame.display.update()

        # FPS control
        fps_clock.tick(FPS)


if __name__ == "__main__":
    main()
