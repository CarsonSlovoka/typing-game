import pygame
import random
from pathlib import Path

pygame.init()

X = 600
Y = 400


class GameView:
    __slots__ = ()
    # RGB
    BACKGROUND_COLOR = background = (255, 200, 150)
    DEFAULT_COLOR = (0, 0, 255)  # blue
    POINT_COLOR = (0, 255, 0)  # green
    FONT = ''


class DropDownController:
    __slots__ = ()
    SPEED = 0.03


class GameWindow:
    __slots__ = ()
    HEIGHT = 600
    WIDTH = 400


class TypingDropDown(
    GameWindow,
    DropDownController,
    GameView
):
    __slots__ = ('_word_set', '_window')
    FONT = pygame.font.SysFont("ComicSansMs", 32)

    def __init__(self, words_file: Path):
        pygame.init()
        self._window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Typing Drop down')
        with open(str(words_file)) as f:
            self._word_set = f.read().splitlines()

    @property
    def window(self):
        return self._window

    def new_word(self):
        chosen_word = random.choice(self._word_set)
        return chosen_word

    def draw_text(self, text: str, x, y, font_color=None):
        text = self.FONT.render(text, True, self.DEFAULT_COLOR)
        self.window.blit(text, (x, y))

    def init_game(self):
        point = 0
        x = random.randint(100, 200)
        y = 0
        chosen_word = self.new_word()
        pressed_word = ''
        return point, x, y, chosen_word, pressed_word

    def game_start(self):
        point, x_word, y_word, chosen_word, pressed_word = self.init_game()
        while 1:
            self.window.fill(self.BACKGROUND_COLOR)  # clear all for redraw
            y_word += self.SPEED
            self.draw_text(chosen_word, x_word, y_word)
            point_caption = self.FONT.render(str(point), True, self.POINT_COLOR)
            self.window.blit(point_caption, (10, 5))
            pygame.display.update()
            for event in pygame.event.get():
                event_type = event.type
                if event_type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event_type == pygame.KEYDOWN:
                    pressed_word += event.unicode  # <- case-sensitive  # pygame.key.name(event.key)
                    if chosen_word.startswith(pressed_word):
                        if chosen_word == pressed_word:
                            point += len(chosen_word)
                            point, x_word, y_word, chosen_word, pressed_word = self.init_game()
                            break
                    else:
                        pressed_word = ''

            if y_word > self.HEIGHT - 5:  # dead
                event = pygame.event.wait()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # press space to restart
                    point, x_word, y_word, chosen_word, pressed_word = self.init_game()


obj = TypingDropDown(Path('words.txt'))
obj.game_start()
