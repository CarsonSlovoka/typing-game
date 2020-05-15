__all__ = ('TypingDropDown',)

import pygame

from time import time

from tkinter import *
from tkinter import messagebox
if 'tk withdraw':
    Tk().wm_withdraw()  # to hide the main window

import random
from pathlib import Path

from .api.utils import SafeMember
from .api.mixins.colors import TypingGameColorMixin
from .views import PyGameView, GameOverView, HomeView
from .controllers import PyGameKeyboard


class TypingDropDown(
    PyGameKeyboard,
    PyGameView,
    TypingGameColorMixin,
    SafeMember,
):
    __slots__ = ('_word_set',) + PyGameView.__slots__

    SPEED = 0.03

    def __init__(self, words_file: Path):
        PyGameView.__init__(self, caption_name='Typing Drop down')
        with open(str(words_file)) as f:
            self._word_set = f.read().splitlines()
        if len(self._word_set) == 0:
            raise RuntimeError(f'There is no content at the ``{words_file.absolute()}``')

    def new_word(self):
        chosen_word = random.choice(self._word_set)
        return chosen_word

    def init_game(self):
        # num_of_words = 0  # It is hard to count how words you typing since there are many languages in the world.
        total_chars = 0
        x = random.randint(self.WIDTH*0.2, self.WIDTH*0.7)
        y = 0
        chosen_word = self.new_word()
        pressed_word = ''
        return total_chars, x, y, chosen_word, pressed_word

    @staticmethod
    def generator_pm_info():
        while 1:
            t_s = time()
            total_chars = yield 0, 0
            while 1:
                if isinstance(total_chars, bool) and total_chars is True:  # reset
                    break
                cpm = int(60*total_chars/(time()-t_s))
                wpm = int(cpm/5)
                total_chars = yield cpm, wpm

    def start_game(self):
        fps = 60
        clock = pygame.time.Clock()
        total_chars, x_word, y_word, chosen_word, pressed_word = self.init_game()
        calculate_pm_info = self.generator_pm_info()
        cpm, wpm = calculate_pm_info.send(None)  # init
        game_over_view = GameOverView(caption_name='Game over')  # cache view
        while 1:
            self.clear_canvas()
            y_word += self.SPEED*fps
            self.draw_text(chosen_word, (x_word, y_word), font_name=self.FONT_NAME_CONSOLAS, font_color=self.FORE_COLOR)
            self.draw_text(f'{pressed_word}', (x_word, y_word), self.FONT_NAME_CONSOLAS, self.TYPING_CORRECT_COLOR)
            self.draw_text(f'{" " * len(pressed_word) + "_" }', (x_word, y_word+10), self.FONT_NAME_CONSOLAS, self.TYPING_CUR_POS_COLOR)
            self.draw_text(f'total chars:{total_chars}', (10, 5), self.FONT_NAME_COMIC_SANS_MS, self.INFO_COLOR)
            self.draw_text(f'CPM:{cpm}', (10, 45), self.FONT_NAME_COMIC_SANS_MS, self.INFO_COLOR)
            self.draw_text(f'WPM:{wpm}', (10, 85), self.FONT_NAME_COMIC_SANS_MS, self.INFO_COLOR)
            # self.draw_text(f'{pressed_word}', (10, 165), font_color=self.INFO_COLOR)
            self.view_update()
            for event in self.get_event():
                if self.is_quit_event(event):
                    self.exit_app()
                if self.is_key_down_event(event):
                    if self.is_press_escape_event(event):
                        return
                    pressed_key = self.get_press_key(event)
                    if chosen_word.startswith(pressed_word+pressed_key):
                        pressed_word += pressed_key
                        if chosen_word == pressed_word:
                            total_chars += len(chosen_word)
                            cpm, wpm = calculate_pm_info.send(total_chars)
                            _total_chars, x_word, y_word, chosen_word, pressed_word = self.init_game()
                            break
                    else:
                        pressed_word = pressed_word+' ' if pressed_key != '\b' else pressed_word[: -1]

            clock.tick(fps)  # Make sure that the FPS is keeping to this value.

            if y_word > self.HEIGHT - 5:
                flag = game_over_view.show()
                if flag is not None and flag == GameOverView.RTN_MSG_BACK_TO_HOME:
                    return  # back to the home page
                total_chars, x_word, y_word, chosen_word, pressed_word = self.init_game()
                cpm, wpm = calculate_pm_info.send(True)

    @staticmethod
    def ask_retry():
        # event = pygame.event.wait()
        # if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # press space to restart
        return messagebox.askokcancel('Game over', 'try again?')


class TypingGameApp(HomeView):
    __slots__ = () + HomeView.__slots__
    SPARK_IMAGE = Path(__file__).parent / Path('_static/home.jpg')

    def __init__(self):
        self.__is_running = True
        super().__init__(caption_name='Welcome to the Typing World.',
                         drop_down_process=lambda: TypingDropDown(Path('./words.txt')).start_game(),
                         article_process=None,
                         setting_process=None,
                         )
