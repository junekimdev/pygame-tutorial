import sys
import os
import random
from enum import Enum
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
    list[index_1], list[index_2] = list[index_2], list[index_1]


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


class Move(Enum):
    UNABLE = 0
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


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
        self.remove_area = None
        self.update_piece = None

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

    def _set_update(self, remove_pos, update_piece):
        self.remove_area = remove_pos
        self.update_piece = update_piece

    def draw_all(self, surf):
        blit_args = []
        for piece in self.pieces:
            if piece.number == 16:
                blit_args.append((self.background, piece.pos, piece.pos))
            else:
                blit_args.append((piece.surf, piece.pos))
        surf.blits(blit_args)

    def draw_updates(self, surf):
        if not self.update_piece:
            return
        blit_args = []
        blit_args.append((self.background, self.remove_area,
                         self.remove_area))  # clear
        blit_args.append(
            (self.update_piece.surf, self.update_piece.pos))  # draw
        surf.blits(blit_args)
        self.update_piece = None
        self.remove_area = None

    def find_by_mouse(self, mouse_pos):
        for i, piece in enumerate(self.pieces):
            if piece.is_mouse_on(mouse_pos):
                return i
        return -1

    def _find_direction_to_move(self, i):
        up_able = i > 3
        down_able = i < 12
        left_able = (i % 4) != 0
        right_able = (i % 4) != 3
        if up_able and self.pieces[i-4].number == 16:
            return Move.UP
        if down_able and self.pieces[i+4].number == 16:
            return Move.DOWN
        if left_able and self.pieces[i-1].number == 16:
            return Move.LEFT
        if right_able and self.pieces[i+1].number == 16:
            return Move.RIGHT
        return Move.UNABLE

    def _permute(self, index_1, index_2):
        self.pieces[index_1].pos, self.pieces[index_2].pos = (
            self.pieces[index_2].pos, self.pieces[index_1].pos)
        permute(self.pieces, index_1, index_2)

    def move(self, i):
        direction = self._find_direction_to_move(i)
        update_piece = self.pieces[i]
        remove_area = update_piece.pos
        match direction:
            case Move.UP:
                self._permute(i, i-4)
                self._set_update(remove_area, update_piece)
            case Move.DOWN:
                self._permute(i, i+4)
                self._set_update(remove_area, update_piece)
            case Move.LEFT:
                self._permute(i, i-1)
                self._set_update(remove_area, update_piece)
            case Move.RIGHT:
                self._permute(i, i+1)
                self._set_update(remove_area, update_piece)
            case Move.UNABLE:
                pass

    def _find_empty(self):
        for i, piece in enumerate(self.pieces):
            if piece.number == 16:
                return i

    def move_to_empty(self, key):
        empty_idx = self._find_empty()
        up_able = empty_idx < 12
        down_able = empty_idx > 3
        left_able = (empty_idx % 4) != 3
        right_able = (empty_idx % 4) != 0
        match key:
            case pygame.K_UP if up_able:
                update_piece = self.pieces[empty_idx+4]
                remove_area = update_piece.pos
                self._permute(empty_idx, empty_idx+4)
                self._set_update(remove_area, update_piece)
            case pygame.K_DOWN if down_able:
                update_piece = self.pieces[empty_idx-4]
                remove_area = update_piece.pos
                self._permute(empty_idx, empty_idx-4)
                self._set_update(remove_area, update_piece)
            case pygame.K_LEFT if left_able:
                update_piece = self.pieces[empty_idx+1]
                remove_area = update_piece.pos
                self._permute(empty_idx, empty_idx+1)
                self._set_update(remove_area, update_piece)
            case pygame.K_RIGHT if right_able:
                update_piece = self.pieces[empty_idx-1]
                remove_area = update_piece.pos
                self._permute(empty_idx, empty_idx-1)
                self._set_update(remove_area, update_piece)


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
            match event.type:
                case pygame.QUIT:
                    sys.exit()
                case pygame.KEYDOWN:  # event attr: key, mod, unicode, scancode
                    puzzle.move_to_empty(event.key)
                case pygame.MOUSEBUTTONUP:  # event attr: pos, button, touch
                    if event.button == 1:
                        idx = puzzle.find_by_mouse(event.pos)
                        if idx != -1:
                            puzzle.move(idx)

        # Drawing a frame
        puzzle.draw_updates(window)

        # This should be at the end of each drawing a frame
        pygame.display.update()

        # FPS control
        fps_clock.tick(FPS)


if __name__ == "__main__":
    main()
