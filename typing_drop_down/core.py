__all__ = ('TypingDropDown',)

import pygame
from pygame.event import EventType

from time import time

from tkinter import *
from tkinter import messagebox
if 'tk withdraw':
    Tk().wm_withdraw()  # to hide the main window

import random
from pathlib import Path

from .api.utils import SafeMember
from .api import generics
from .views import PyGameView, GameOverView
from .controllers import PyGameKeyboard


class TypingDropDown(
    PyGameKeyboard,
    PyGameView,
    SafeMember,
):
    __slots__ = ('_word_set',
                 '_game_over_view'
                 ) + PyGameView.__slots__

    SPEED = 0.03

    def __init__(self, words_file: Path):
        PyGameView.__init__(self, caption_name='Typing Drop down')
        with open(str(words_file)) as f:
            self._word_set = f.read().splitlines()
        if len(self._word_set) == 0:
            raise RuntimeError(f'There is no content at the ``{words_file.absolute()}``')
        self._game_over_view = GameOverView(caption_name='Game over', exit_fun=lambda: self.exit_app())

    def new_word(self):
        chosen_word = random.choice(self._word_set)
        return chosen_word

    def init_game(self):
        num_of_words = 0
        point = 0
        x = random.randint(100, 200)
        y = 0
        chosen_word = self.new_word()
        pressed_word = ''
        return num_of_words, point, x, y, chosen_word, pressed_word

    @staticmethod
    def generator_wpm():
        while 1:
            num_of_words = 0
            t_s = time()
            reset_flag = yield 0
            while 1:
                num_of_words += 1
                if reset_flag is True:
                    break
                reset_flag = yield int(60*num_of_words/(time()-t_s))

    def create_game(self):
        fps = 60
        clock = pygame.time.Clock()
        num_of_words, point, x_word, y_word, chosen_word, pressed_word = self.init_game()
        calculate_wpm = self.generator_wpm()
        wpm = calculate_wpm.send(None)  # init
        while 1:
            self.clear_canvas()
            y_word += self.SPEED*fps
            self.draw_text(chosen_word, (x_word, y_word), self.FORE_COLOR)
            self.draw_text(f'points:{point}', (10, 5), font_color=self.POINT_COLOR)
            self.draw_text(f'WPM:{wpm}', (10, 45), font_color=self.POINT_COLOR)
            self.view_update()
            for event in self.get_event():
                if self.is_quit_event(event):
                    self.exit_app()
                if self.is_key_down_event(event):
                    pressed_word += self.get_press_key(event)
                    if chosen_word.startswith(pressed_word):
                        if chosen_word == pressed_word:
                            num_of_words += 1
                            wpm = calculate_wpm.send(None)
                            point += len(chosen_word)
                            _num_of_words, _point, x_word, y_word, chosen_word, pressed_word = self.init_game()
                            break
                    else:
                        pressed_word = ''

            clock.tick(fps)  # Make sure that the FPS is keeping to this value.

            if y_word > self.HEIGHT - 5:
                self.game_over_view.show()
                num_of_words, point, x_word, y_word, chosen_word, pressed_word = self.init_game()
                wpm = calculate_wpm.send(True)

    @staticmethod
    def ask_retry():
        # event = pygame.event.wait()
        # if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # press space to restart
        return messagebox.askokcancel('Game over', 'try again?')

    def exit_app(self):
        self.destroy_view()
        raise SystemExit
