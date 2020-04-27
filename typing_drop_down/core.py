__all__ = ('TypingDropDown',)

from typing import Tuple
import pygame
from pygame.event import EventType

from tkinter import *
from tkinter import messagebox
if 'tk withdraw':
    Tk().wm_withdraw() # to hide the main window

import random
from pathlib import Path

from .api.utils import SafeMember, cached_property
from .api import mixins
from .api import generics


class PyGameView(
    mixins.FontModelMixin,
    generics.GameView,
):
    __slots__ = generics.GameView.__slots__
    VIEW_CONTROLLER = pygame
    FONT_NAME = 'ComicSansMs'

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Typing Drop down')
        generics.GameView.__init__(self, window=pygame.display.set_mode((self.WIDTH, self.HEIGHT)))

    @cached_property
    def view_obj(self):
        return self.VIEW_CONTROLLER

    def update(self):
        return pygame.display.update()

    def view_update(self):
        return PyGameView.update(self)

    def clear_canvas(self):
        self.window.fill(self.BACKGROUND_COLOR)  # clear all for redraw

    def destroy_view(self):
        pygame.quit()

    @cached_property
    def font(self):
        return pygame.font.SysFont(self.FONT_NAME, 32)

    def draw_text(self, text: str, position: Tuple[int, int], font_color=None):
        """
        position: (x, y)
        """
        text = self.font.render(text, True, font_color)
        self.window.blit(text, position)


class PyGameKeyboard(generics.KeyboardController):
    __slots__ = ()
    KEYBOARD_CONTROLLER = pygame

    def get_event(self):
        for event in pygame.event.get():
            yield event

    @staticmethod
    def is_key_down_event(event: EventType):
        return True if event.type == pygame.KEYDOWN else False

    @staticmethod
    def is_quit_event(event: EventType):
        return True if event.type == pygame.QUIT else False

    @staticmethod
    def get_press_key(event) -> str:
        return event.unicode  # <- case-sensitive  # pygame.key.name(event.key)


class TypingDropDown(
    PyGameKeyboard,
    PyGameView,
    SafeMember,
):
    __slots__ = ('_word_set',) + PyGameView.__slots__

    SPEED = 0.25

    def __init__(self, words_file: Path):
        PyGameView.__init__(self)
        with open(str(words_file)) as f:
            self._word_set = f.read().splitlines()
        if len(self._word_set) == 0:
            raise RuntimeError(f'There is no content at the ``{words_file.absolute()}``')

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
            self.clear_canvas()
            y_word += self.SPEED
            self.draw_text(chosen_word, (x_word, y_word), self.FORE_COLOR)
            self.draw_text(str(point), (10, 5), font_color=self.POINT_COLOR)
            self.view_update()
            for event in self.get_event():
                if self.is_quit_event(event):
                    self.exit_app()
                if self.is_key_down_event(event):
                    pressed_word += self.get_press_key(event)
                    if chosen_word.startswith(pressed_word):
                        if chosen_word == pressed_word:
                            point += len(chosen_word)
                            point, x_word, y_word, chosen_word, pressed_word = self.init_game()
                            break
                    else:
                        pressed_word = ''

            if y_word > self.HEIGHT - 5:
                if self.ask_retry():
                    point, x_word, y_word, chosen_word, pressed_word = self.init_game()
                else:
                    self.exit_app()

    @staticmethod
    def ask_retry():
        # event = pygame.event.wait()
        # if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # press space to restart
        return messagebox.askokcancel('Game over', 'try again?')

    def exit_app(self):
        self.destroy_view()
        raise SystemExit
