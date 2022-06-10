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


def draw_txt_centered(surface, font, str, color=FONT_COLOR):
    cx = surface.get_width() / 2
    cy = surface.get_height() / 2
    text_surf = font.render(str, True, color)
    text_rect = text_surf.get_rect(center=(cx, cy))
    surface.blit(text_surf, text_rect)


class Piece:
    def __init__(self, number, font):
        self.surf = pygame.Surface((PIECE_SIZE, PIECE_SIZE))
        self.number = number
        self.pos = self.surf.get_rect()
        self.surf.fill(PIECE_BG)
        draw_txt_centered(self.surf, font, str(number))

    def move(self, x, y):
        self.pos.x = x
        self.pos.y = y


class Puzzle:
    def __init__(self, font, background):
        self.background = background
        self.pieces = [Piece(i+1, font) for i in range(16)]
        self._init_position()

    def _init_position(self):
        i = 0
        pos_y = (WINDOW_SIZE[1] - (PIECE_SIZE*4 + PIECE_GAP*3))/2
        for row in range(4):
            pos_x = (WINDOW_SIZE[0] - (PIECE_SIZE*4 + PIECE_GAP*3))/2
            for col in range(4):
                self.pieces[i].move(pos_x, pos_y)
                pos_x += PIECE_SIZE + PIECE_GAP
                i += 1
            pos_y += PIECE_SIZE + PIECE_GAP

    def draw_all(self, surf):
        blit_args = []
        for piece in self.pieces:
            if piece.number == 16:
                blit_args.append((self.background, piece.pos, piece.pos))
            else:
                blit_args.append((piece.surf, piece.pos))
        surf.blits(blit_args)


def load_background(size, color):
    background = pygame.Surface(size)
    background.fill(color)
    return background


def init_window(size, color):
    window = pygame.display.set_mode(size)
    window.fill(color)
    return window


def main():
    pygame.init()
    pygame.display.set_caption(GAME_TITLE)
    fps_clock = pygame.time.Clock()
    font_file = os.path.join(root_dir, FONT_FILENAME)
    font = pygame.font.Font(font_file, FONT_SIZE)

    # Splash Screen
    window = init_window(WINDOW_SIZE, BG_COLOR)
    draw_txt_centered(window, font, GREETING_MSG)
    pygame.display.update()
    pygame.time.delay(1000)

    # Load the game
    background = load_background(WINDOW_SIZE, BG_COLOR)
    window.blit(background, (0, 0))

    puzzle = Puzzle(font, background)
    puzzle.draw_all(window)

    while True:
        # Event management
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # Drawing a frame

        # This should be at the end of each drawing a frame
        pygame.display.update()

        # FPS control
        fps_clock.tick(FPS)


if __name__ == "__main__":
    main()
