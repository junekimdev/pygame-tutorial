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
CONGRATS_SIZE = (300, 300)
BG_COLOR = (170, 238, 187)
GREETING_MSG = "안녕하세요"
COMPETE_MSG = "완성! 참 잘했어요!!"
FONT_SIZE = 32
FONT_COLOR = (10, 10, 10)
FONT_FILENAME = "GamjaFlower-Regular.ttf"
BG_IMG_FILENAME = "wood_fence_gray.jpg"
CONGRATS_IMG_FILENAME = "confetti.png"
PUZZLE_IMG_FILENAME = "velociraptor.jpg"
LEGAL_MOVE_AUD_FILENAME = "mixkit-legal-move.mp3"
ILLEGAL_MOVE_AUD_FILENAME = "mixkit-illegal-move.mp3"
COMPELTE_AUD_FILENAME = "mixkit-completion.mp3"
RESTART_AUD_FILENAME = "mixkit-restart.mp3"

PIECE_SIZE = 100
PIECE_GAP = 0
PIECE_BG = (255, 255, 255)
PIECE_NUM_ON = True


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


class Move(Enum):
    UNABLE = 0
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class EVENT:
    COMPLETE = pygame.USEREVENT


class Animation:
    def __init__(self, puzzle, update_piece, end_pos, duration=100):
        self.puzzle = puzzle
        puzzle.update_piece = update_piece
        self.end_pos = end_pos
        self.total_frames = FPS * duration // 1000
        self.gen_pos = self._generate_pos()

    def _generate_pos(self):
        start_x, start_y = self.puzzle.update_piece.pos.topleft
        end_x, end_y = self.end_pos.topleft

        def func(i, start, end):
            return start + (i+1) * (end-start) / self.total_frames

        if start_x != end_x:  # Moving horizonal
            li = [func(i, start_x, end_x) for i in range(self.total_frames)]
            for next_x in li:
                yield (next_x, end_y)

        elif start_y != end_y:  # Moving vertical
            li = [func(i, start_y, end_y) for i in range(self.total_frames)]
            for next_y in li:
                yield (end_x, next_y)

    def set_next_frame(self):
        try:
            x, y = next(self.gen_pos)
            self.puzzle.remove_area = self.puzzle.update_piece.pos.copy()
            self.puzzle.update_piece.move(x, y)
        except StopIteration:
            self.puzzle.clear_animation()


class Piece:
    def __init__(self, number, font, image, number_on=False):
        self.surf = self._assign_image(image, number)
        self.number = number
        self.pos = self.surf.get_rect()
        if number_on:
            draw_txt_centered(self.surf, font, str(number))

    def move(self, x, y):
        self.pos.x = x
        self.pos.y = y

    def is_mouse_on(self, mouse_pos):
        return self.pos.collidepoint(mouse_pos)

    def _get_pos_by_num(self, number):
        row = (number-1) // 4
        col = (number-1) % 4
        return PIECE_SIZE*col, PIECE_SIZE*row

    def _assign_image(self, image, number):
        x, y = self._get_pos_by_num(number)
        rect = pygame.Rect(x, y, PIECE_SIZE, PIECE_SIZE)
        return image.subsurface(rect)


class Puzzle:
    def __init__(self, font, background, image, number_on=False):
        self.background = background
        self.pieces = [Piece(i, font, image, number_on)
                       for i in get_init_list(16)]
        self._init_position()
        self.remove_area = None
        self.update_piece = None
        self.animation = None

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

    def _set_animation(self, piece, dest):
        self.animation = Animation(self, piece, dest)
        self._play_move_aud()

    def clear_animation(self):
        self.remove_area = None
        self.update_piece = None
        self.animation = None
        if self._is_complete():
            pygame.event.post(pygame.event.Event(EVENT.COMPLETE))

    def draw_all(self, surf):
        blit_args = []
        for piece in self.pieces:
            if piece.number == 16:
                blit_args.append((self.background, piece.pos, piece.pos))
            else:
                blit_args.append((piece.surf, piece.pos))
        surf.blits(blit_args)

    def draw_updates(self, surf):
        if self.animation:
            self.animation.set_next_frame()
        if not self.update_piece:
            return
        blit_args = []
        blit_args.append((self.background, self.remove_area,
                         self.remove_area))  # clear
        blit_args.append(
            (self.update_piece.surf, self.update_piece.pos))  # draw
        surf.blits(blit_args)

    def _play_move_aud(self):
        pygame.mixer.music.load(LEGAL_MOVE_AUD_FILENAME)
        pygame.mixer.music.play()

    def _play_illegal_move_aud(self):
        pygame.mixer.music.load((ILLEGAL_MOVE_AUD_FILENAME))
        pygame.mixer.music.play()

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

    def _permute_to_animate(self, index_update, index_empty):
        start_pos = self.pieces[index_update].pos.copy()
        dest_pos = self.pieces[index_empty].pos.copy()
        self.pieces[index_empty].pos = start_pos
        permute(self.pieces, index_update, index_empty)
        return dest_pos

    def move(self, i):
        direction = self._find_direction_to_move(i)
        update_piece = self.pieces[i]
        match direction:
            case Move.UP:
                dest_pos = self._permute_to_animate(i, i-4)
                self._set_animation(update_piece, dest_pos)
            case Move.DOWN:
                dest_pos = self._permute_to_animate(i, i+4)
                self._set_animation(update_piece, dest_pos)
            case Move.LEFT:
                dest_pos = self._permute_to_animate(i, i-1)
                self._set_animation(update_piece, dest_pos)
            case Move.RIGHT:
                dest_pos = self._permute_to_animate(i, i+1)
                self._set_animation(update_piece, dest_pos)
            case Move.UNABLE:
                self._play_illegal_move_aud()

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
                dest_pos = self._permute_to_animate(empty_idx+4, empty_idx)
                self._set_animation(update_piece, dest_pos)
            case pygame.K_DOWN if down_able:
                update_piece = self.pieces[empty_idx-4]
                dest_pos = self._permute_to_animate(empty_idx-4, empty_idx)
                self._set_animation(update_piece, dest_pos)
            case pygame.K_LEFT if left_able:
                update_piece = self.pieces[empty_idx+1]
                dest_pos = self._permute_to_animate(empty_idx+1, empty_idx)
                self._set_animation(update_piece, dest_pos)
            case pygame.K_RIGHT if right_able:
                update_piece = self.pieces[empty_idx-1]
                dest_pos = self._permute_to_animate(empty_idx-1, empty_idx)
                self._set_animation(update_piece, dest_pos)

    def _is_complete(self):
        complete = True
        for i, piece in enumerate(self.pieces):
            complete &= piece.number == i+1
            if not complete:
                break
        return complete


def load_image(size, filename, transparent=False):
    file = os.path.join(root_dir, filename)
    image = pygame.image.load(file)
    resized_image = pygame.transform.scale(image, size)
    return resized_image.convert_alpha() if transparent else resized_image.convert()


def load_congrats(font):
    image = load_image(CONGRATS_SIZE, CONGRATS_IMG_FILENAME, True)
    draw_txt_centered(image, font, COMPETE_MSG)
    return image


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
    cx = window.get_width()/2
    cy = window.get_height()/2
    background = load_image(WINDOW_SIZE, BG_IMG_FILENAME)
    window.blit(background, (0, 0))

    puzzle_size = (PIECE_SIZE*4, PIECE_SIZE*4)
    puzzle_img = load_image(puzzle_size, PUZZLE_IMG_FILENAME)
    puzzle = Puzzle(font, background, puzzle_img.copy(), PIECE_NUM_ON)
    puzzle.draw_all(window)

    while True:
        # Event management
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    sys.exit()
                case pygame.KEYDOWN:  # event attr: key, mod, unicode, scancode
                    if not puzzle.animation:
                        puzzle.move_to_empty(event.key)
                case pygame.MOUSEBUTTONUP:  # event attr: pos, button, touch
                    if not puzzle.animation and event.button == 1:
                        idx = puzzle.find_by_mouse(event.pos)
                        if idx != -1:
                            puzzle.move(idx)
                case EVENT.COMPLETE:
                    # Play completion audio
                    pygame.mixer.music.load(COMPELTE_AUD_FILENAME)
                    pygame.mixer.music.play()

                    # Congrats the gamer
                    congrats_img = load_congrats(font)
                    congrats_pos = congrats_img.get_rect(center=(cx, cy))
                    window.blit(congrats_img, congrats_pos)
                    pygame.display.update()
                    pygame.time.delay(1500)

                    # Show original image
                    complete_pos = puzzle_img.get_rect(center=(cx, cy))
                    window.blit(puzzle_img, complete_pos)
                    pygame.display.update()
                    pygame.time.delay(2000)

                    # Restart
                    pygame.mixer.music.load(RESTART_AUD_FILENAME)
                    pygame.mixer.music.play()
                    window.blit(background, (0, 0))
                    puzzle = Puzzle(font, background,
                                    puzzle_img.copy(), PIECE_NUM_ON)
                    puzzle.draw_all(window)

        # Drawing a frame
        puzzle.draw_updates(window)

        # This should be at the end of each drawing a frame
        pygame.display.update()

        # FPS control
        fps_clock.tick(FPS)


if __name__ == "__main__":
    main()
