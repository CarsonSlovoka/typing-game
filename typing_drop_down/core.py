__all__ = ('TypingDropDown',)

import pygame

from time import time
from typing import Generator, Iterator

from tkinter import *
from tkinter import messagebox
if 'tk withdraw':
    Tk().wm_withdraw()  # to hide the main window

import random
from pathlib import Path

from .api.utils import SafeMember
from .api.mixins.colors import TypingGameColorMixin
from .api.mixins import  typings
from .views import PyGameView, GameOverView, HomeView
from .controllers import PyGameKeyboard
import abc
from typing import Tuple, Union
import re


class _TypingGameBase(
    PyGameKeyboard,
    PyGameView,
    TypingGameColorMixin,
    typings.StatisticianMixin,
    SafeMember,
):
    __slots__ = PyGameView.__slots__

    @abc.abstractmethod
    def init_game(self, *args):
        # return total_chars, x, y, chosen_word, pressed_word
        raise NotImplementedError

    @abc.abstractmethod
    def start_game(self, *args):
        ...


class TypingDropDown(_TypingGameBase):
    __slots__ = ('_word_set',) + _TypingGameBase.__slots__

    SPEED = 0.003

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

    def start_game(self):
        fps = 60
        clock = pygame.time.Clock()
        total_chars, x_word, y_word, chosen_word, pressed_word = self.init_game()
        cur_total_chars = 0
        calculate_pm_info = self.generator_pm_info()
        cpm, wpm = next(calculate_pm_info)  # init
        game_over_view = GameOverView(caption_name='Game over')  # cache view

        while 1:
            self.clear_canvas()
            y_word += self.SPEED*fps
            self.draw_text(chosen_word, (x_word, y_word), font_name=self.FONT_NAME_CONSOLAS, font_color=self.FORE_COLOR)
            self.draw_text(f'{pressed_word}', (x_word, y_word), self.FONT_NAME_CONSOLAS, self.TYPING_CORRECT_COLOR)
            self.draw_text(f'{" " * len(pressed_word) + "_" }', (x_word, y_word+10), self.FONT_NAME_CONSOLAS, self.TYPING_CUR_POS_COLOR)
            self.draw_text(f'total chars:{cur_total_chars}', (10, 5), self.FONT_NAME_COMIC_SANS_MS, self.INFO_COLOR)
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
                        cur_total_chars = len(pressed_word) + total_chars
                        cpm, wpm = calculate_pm_info.send(cur_total_chars)
                        if chosen_word == pressed_word:
                            total_chars += len(chosen_word)
                            _total_chars, x_word, y_word, chosen_word, pressed_word = self.init_game()
                            break
                    else:
                        if pressed_key != '\b':
                            if len(pressed_word + ' ') + 1 <= len(chosen_word):
                                pressed_word = pressed_word + ' '
                        else:
                            pressed_word = pressed_word[: -1]
                            cur_total_chars = len(pressed_word) + total_chars
                        cpm, wpm = calculate_pm_info.send(cur_total_chars)

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


class TypingArticle(_TypingGameBase):
    __slots__ = ('_article',) + _TypingGameBase.__slots__

    def __init__(self, article_dir: Path):
        PyGameView.__init__(self)
        self._article: Generator = self.generator_article(article_dir)
        self.article.send(None)  # init generator.

    def draw_article(self, article: str, x_init: int, y_init: int, font_color, y_gap=80):
        x, y = x_init, y_init
        for row_data in article.splitlines():
            self.draw_text(row_data, (x, y), self.FONT_NAME_CONSOLAS, font_color)
            y += y_gap

    @staticmethod
    def generator_article(article_dir: Path) -> Generator[Union[str, str], int, int]:
        """
        :return: If the level does not exist then return the int, else return the content and file.name.
        """

        article_list = [_ for _ in article_dir.glob('*.txt')]
        if len(article_list) == 0:
            raise FileExistsError(f'{article_dir.absolute()}')
        regex_rm_space_on_end = re.compile(r' +$', re.M)  # Remove redundant space on the line ends.
        while 1:
            n_level = yield
            if n_level >= len(article_list):
                return -1
            for cur_article_file in article_list[n_level:]:
                with open(str(cur_article_file), newline=None) as f:
                    content = f.read()
                    if len(content) == 0:
                        raise RuntimeError(f'There is no content at the ``{cur_article_file.absolute()}``')
                    # yield re.sub(r' +$', "", content, flags=re.M)
                    content = re.sub(regex_rm_space_on_end, "", content)
                    n_level = yield content, cur_article_file.name
                    if n_level is not None:
                        break
            return -1

    def init_game(self, x, y, n_level=None):
        total_chars = 0
        try:
            article, title = next(self.article) if n_level else self.article.send(n_level)
        except StopIteration as msg:
            print(msg.value)
            article = ""
            title = "Game over"
        self.set_caption(title)
        pressed_word = ''
        return total_chars, x, y, article, pressed_word

    def start_game(self, init_level: int):
        fps = 25
        clock = pygame.time.Clock()
        const_x_init = 50
        const_y_init = 150
        level = init_level
        total_chars, x_word, y_word, chosen_article, pressed_word = self.init_game(const_x_init, const_y_init, level)
        calculate_pm_info = self.generator_pm_info()
        cpm, wpm = next(calculate_pm_info)  # init
        game_over_view = GameOverView(caption_name='Game over')  # cache view
        while 1:
            self.clear_canvas()
            self.draw_text(f'total chars:{total_chars}', (10, 5), self.FONT_NAME_COMIC_SANS_MS, self.INFO_COLOR)
            self.draw_text(f'CPM:{cpm}', (10, 45), self.FONT_NAME_COMIC_SANS_MS, self.INFO_COLOR)
            self.draw_text(f'WPM:{wpm}', (10, 85), self.FONT_NAME_COMIC_SANS_MS, self.INFO_COLOR)
            self.draw_article(chosen_article, const_x_init, const_y_init, font_color=self.FORE_COLOR)
            self.draw_article(pressed_word, const_x_init, const_y_init, font_color=self.TYPING_CORRECT_COLOR)

            underline = re.sub(r'[^\n]', " ", pressed_word) + "_"  # Any characters except not space.
            self.draw_article(underline, const_x_init, const_y_init+10, font_color=self.TYPING_CUR_POS_COLOR)

            self.view_update()
            for event in self.get_event():
                if self.is_quit_event(event):
                    self.exit_app()
                if self.is_key_down_event(event):
                    if self.is_press_escape_event(event):
                        return
                    pressed_key = self.get_press_key(event)
                    if pressed_key == '\r':
                        pressed_key = '\n'
                    if chosen_article.startswith(pressed_word+pressed_key):
                        pressed_word += pressed_key
                        total_chars = len(pressed_word)
                        cpm, wpm = calculate_pm_info.send(total_chars)
                        if chosen_article == pressed_word:
                            level += 1
                            total_chars, x_word, y_word, chosen_article, pressed_word = \
                                self.init_game(const_x_init, const_y_init, level)
                            cpm, wpm = calculate_pm_info.send(True)
                            if chosen_article == "":
                                flag = game_over_view.show()
                                if flag is not None and flag == GameOverView.RTN_MSG_BACK_TO_HOME:
                                    return  # back to the home page
                    else:
                        if pressed_key != '\b':
                            if len(pressed_word + ' ') + 1 <= len(chosen_article):
                                pressed_word = pressed_word + ' '
                        else:
                            pressed_word = pressed_word[: -1]
                            total_chars = len(pressed_word)
                        cpm, wpm = calculate_pm_info.send(total_chars)

            clock.tick(fps)  # Make sure that the FPS is keeping to this value.


class TypingGameApp(HomeView):
    __slots__ = () + HomeView.__slots__
    SPARK_IMAGE = Path(__file__).parent / Path('_static/home.jpg')

    def __init__(self):
        self.__is_running = True
        super().__init__(caption_name='Welcome to the Typing World.',
                         drop_down_process=lambda: TypingDropDown(Path('./words.txt')).start_game(),
                         article_process=lambda: TypingArticle(Path('./article/')).start_game(init_level=0),
                         setting_process=None,
                         )
