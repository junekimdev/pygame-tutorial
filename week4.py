import sys
import os
import pygame

if not pygame.font:
    print("Warning, fonts disabled")
if not pygame.mixer:
    print("Warning, sound disabled")

root_dir = os.path.split(os.path.abspath(__file__))[0]

FPS = 60
GAME_TITLE = "15 퍼즐"
WINDOW_SIZE = (500, 500)
BG_COLOR = (170, 238, 187)
GREETING_MSG = "안녕하세요"
FONT_SIZE = 32
FONT_COLOR = (10, 10, 10)
FONT_FILENAME = "GamjaFlower-Regular.ttf"

PIECE_SIZE = 80
PIECE_GAP = 10
PIECE_BG = (255, 255, 255)


def drawTxtCentered(surface, font, str, color=FONT_COLOR):
    cx = surface.get_width() / 2
    cy = surface.get_height() / 2
    text_surf = font.render(str, True, color)
    text_rect = text_surf.get_rect(center=(cx, cy))
    surface.blit(text_surf, text_rect)


class Piece(pygame.Surface):
    def __init__(self, number, font):
        super().__init__((PIECE_SIZE, PIECE_SIZE))
        self.number = number
        self.pos = (0, 0)
        self.fill(PIECE_BG)
        drawTxtCentered(self, font, str(number))


class Puzzle:
    def __init__(self, font):
        self.pieces = [Piece(i+1, font) for i in range(16)]

    def draw(self, surf):
        i = 0
        pos_y = (WINDOW_SIZE[1] - (PIECE_SIZE*4 + PIECE_GAP*3))/2
        for row in range(4):
            pos_x = (WINDOW_SIZE[0] - (PIECE_SIZE*4 + PIECE_GAP*3))/2
            for col in range(4):
                num = self.pieces[i].number
                if not num == 16:
                    surf.blit(self.pieces[i], (pos_x, pos_y))
                pos_x += PIECE_SIZE + PIECE_GAP
                i += 1
            pos_y += PIECE_SIZE + PIECE_GAP


def main():
    pygame.init()
    pygame.display.set_caption(GAME_TITLE)
    fps_clock = pygame.time.Clock()
    window = pygame.display.set_mode(WINDOW_SIZE)
    font_file = os.path.join(root_dir, FONT_FILENAME)
    font = pygame.font.Font(font_file, FONT_SIZE)
    puzzle = Puzzle(font)

    # Splash Screen
    window.fill(BG_COLOR)
    drawTxtCentered(window, font, GREETING_MSG)
    pygame.display.update()
    pygame.time.delay(1000)

    while True:
        # Event management
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # Drawing a frame
        window.fill(BG_COLOR)
        puzzle.draw(window)

        # This should be at the end of each drawing a frame
        pygame.display.update()

        # FPS control
        fps_clock.tick(FPS)


if __name__ == "__main__":
    main()
