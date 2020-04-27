__all__ = ('TypingDropDown',)

from typing import Tuple
import pygame
import random
from pathlib import Path

from .api.utils import SafeMember, cached_property
from .api import mixins
from .api import generics


class TypingDropDown(
    mixins.FontModelMixin,
    # KeyboardController,
    generics.GameView,
    SafeMember,
):
    __slots__ = ('_word_set',) + generics.GameView.__slots__

    SPEED = 0.03

    FONT_NAME = 'ComicSansMs'
    VIEW_CONTROLLER = pygame

    def __init__(self, words_file: Path):
        generics.GameView.__init__(self)
        with open(str(words_file)) as f:
            self._word_set = f.read().splitlines()
        if len(self._word_set) == 0:
            raise RuntimeError(f'There is no content at the ``{words_file.absolute()}``')

    def game_view_init(self):
        self.view_obj.init()
        self.view_obj.display.set_caption('Typing Drop down')
        return self.view_obj.display.set_mode((self.WIDTH, self.HEIGHT))

    @property
    def view_obj(self):
        return self.VIEW_CONTROLLER

    @cached_property
    def font(self):
        return self.view_obj.font.SysFont(self.FONT_NAME, 32)

    def view_update(self):
        self.view_obj.display.update()

    def clear_canvas(self):
        self.window.fill(self.BACKGROUND_COLOR)  # clear all for redraw

    def draw_text(self, text: str, position: Tuple[int, int], font_color=None):
        """
        position: (x, y)
        """
        text = self.font.render(text, True, font_color)
        self.window.blit(text, position)

    def new_word(self):
        chosen_word = random.choice(self._word_set)
        return chosen_word

    def init_game(self):
        point = 0
        x = random.randint(100, 200)
        y = 0
        chosen_word = self.new_word()
        pressed_word = ''
        return point, x, y, chosen_word, pressed_word

    def create_game(self):
        point, x_word, y_word, chosen_word, pressed_word = self.init_game()
        while 1:
            self.window.fill(self.BACKGROUND_COLOR)  # clear all for redraw
            y_word += self.SPEED
            self.draw_text(chosen_word, (x_word, y_word), self.FORE_COLOR)
            self.draw_text(str(point), (10, 5), font_color=self.POINT_COLOR)
            self.view_update()
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
