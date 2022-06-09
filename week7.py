import sys
import os
import random
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


def permute(list, index_1, index_2):
    value_1 = list[index_1]
    value_2 = list[index_2]
    list[index_1] = value_2
    list[index_2] = value_1


def random_permute(list, end, *, start=0):
    index_1 = random.randrange(start, end)
    index_2 = random.randrange(start, end)
    while(index_1 == index_2):
        index_2 = random.randrange(start, end)
    permute(list, index_1, index_2)


def get_init_list(n, iter=10):
    li = [i+1 for i in range(n-1)]
    for i in range(iter):
        random_permute(li, n-1)
        random_permute(li, n-1)
    li.append(n)
    return li


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

    def is_mouse_on(self, mouse_pos):
        return self.pos.collidepoint(mouse_pos)


class Puzzle:
    def __init__(self, font, background):
        self.background = background
        self.pieces = [Piece(i, font) for i in get_init_list(16)]
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

    def find_by_mouse(self, mouse_pos):
        for i, piece in enumerate(self.pieces):
            if piece.is_mouse_on(mouse_pos):
                return i
        return -1


def load_background(size):
    background = pygame.Surface(size)
    background.fill(BG_COLOR)
    return background


def init_window(size):
    window = pygame.display.set_mode(size, pygame.RESIZABLE)
    window.fill(BG_COLOR)
    return window


def main():
    pygame.init()
    pygame.display.set_caption(GAME_TITLE)
    fps_clock = pygame.time.Clock()
    font_file = os.path.join(root_dir, FONT_FILENAME)
    font = pygame.font.Font(font_file, FONT_SIZE)

    # Splash Screen
    window = init_window(WINDOW_SIZE)
    draw_txt_centered(window, font, GREETING_MSG)
    pygame.display.update()
    pygame.time.delay(1000)

    # Load the game
    background = load_background(WINDOW_SIZE)
    puzzle = Puzzle(font, background)
    window.blit(background, (0, 0))
    puzzle.draw_all(window)

    while True:
        # Event management
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    sys.exit()
                case pygame.KEYDOWN:  # event attr: key, mod, unicode, scancode
                    match event.key:
                        case pygame.K_UP:
                            print("Up")
                        case pygame.K_DOWN:
                            print("Down")
                        case pygame.K_LEFT:
                            print("Left")
                        case pygame.K_RIGHT:
                            print("Right")
                case pygame.MOUSEBUTTONUP:  # event attr: pos, button, touch
                    if event.button == 1:
                        idx = puzzle.find_by_mouse(event.pos)
                        if idx != -1:
                            print(idx)

        # Drawing a frame

        # This should be at the end of each drawing a frame
        pygame.display.update()

        # FPS control
        fps_clock.tick(FPS)


if __name__ == "__main__":
    main()
