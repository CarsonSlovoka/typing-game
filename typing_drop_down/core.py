__all__ = ('TypingDropDown',)

import pygame

from typing import Generator

from tkinter import *
from tkinter import messagebox

if 'tk withdraw':
    Tk().wm_withdraw()  # to hide the main window

import random
from pathlib import Path

from .api.utils import SafeMember
from .api.mixins.colors import TypingGameColorMixin
from .api.mixins import typings
from .api.generics import RGBColor
from .views import PyGameView, GameOverView, HomeView
from .controllers import PyGameKeyboard
import abc
from typing import Tuple, Union, List, Callable
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

    def draw_panel(self, total_chars: int, cpm: int, wpm: int):
        self.draw_text(f'total chars:{total_chars}', (10, 5), self.FONT_NAME_COMIC_SANS_MS, self.INFO_COLOR)
        self.draw_text(f'CPM:{cpm}', (10, 45), self.FONT_NAME_COMIC_SANS_MS, self.INFO_COLOR)
        self.draw_text(f'WPM:{wpm}', (10, 85), self.FONT_NAME_COMIC_SANS_MS, self.INFO_COLOR)


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
        x = random.randint(self.WIDTH * 0.2, self.WIDTH * 0.7)
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
            y_word += self.SPEED * fps
            self.draw_text(chosen_word, (x_word, y_word), font_name=self.FONT_NAME_CONSOLAS, font_color=self.FORE_COLOR)
            self.draw_text(f'{pressed_word}', (x_word, y_word), self.FONT_NAME_CONSOLAS, self.TYPING_CORRECT_COLOR)
            self.draw_text(f'{" " * len(pressed_word) + "_"}', (x_word, y_word + 10), self.FONT_NAME_CONSOLAS, self.TYPING_CUR_POS_COLOR)
            self.draw_panel(cur_total_chars, cpm, wpm)
            # self.draw_text(f'{pressed_word}', (10, 165), font_color=self.INFO_COLOR)
            self.view_update()
            for event in self.get_event():
                if self.is_quit_event(event):
                    self.exit_app()
                if self.is_key_down_event(event):
                    if self.is_press_escape_event(event):
                        return
                    pressed_key = self.get_press_key(event)
                    if chosen_word.startswith(pressed_word + pressed_key):
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

    def draw_article(self, article: str, x_init: int, y_init: int, font_color, y_gap: int):
        x, y = x_init, y_init
        for row_data in article.splitlines():
            self.draw_text(row_data, (x, y), self.FONT_NAME_CONSOLAS, font_color)
            y += y_gap

    @staticmethod
    def generator_article(article_dir: Path) -> Generator[Union[str, str, int], int, None]:
        """
        :return: Tuple(content, file.name, flag).  # The flag set to True means reset.
        """

        article_list = [_ for _ in article_dir.glob('*.txt')]
        if len(article_list) == 0:
            raise FileExistsError(f'{article_dir.absolute()}')
        regex_rm_space_on_end = re.compile(r' +$', re.M)  # Remove redundant space on the line ends.
        while 1:
            n_level = yield '', '', True
            if n_level >= len(article_list):
                break
            for cur_article_file in article_list[n_level:]:
                with open(str(cur_article_file), newline=None) as f:
                    content = f.read()
                    if len(content) == 0:
                        raise RuntimeError(f'There is no content at the ``{cur_article_file.absolute()}``')
                    # yield re.sub(r' +$', "", content, flags=re.M)
                    content = re.sub(regex_rm_space_on_end, "", content)
                    n_level = yield content, cur_article_file.name, False
                    if n_level is not None:
                        break

    def init_game(self, n_level=None) -> Tuple[bool, List[Tuple[str, bool, RGBColor, Callable]], int, int, str, str]:

        """
        :param n_level: Increase automatically by default.
        :returns reset_flag, history_draw_list, total_chars, article, pressed_word
        """
        total_chars = 0
        article, title, reset_flag = next(self.article) if n_level is None else self.article.send(n_level)

        # Draw a character one by one and pass the current position to the next function.
        history_draw_list: List[Tuple[str,
                                      bool,
                                      RGBColor,
                                      Callable[[str, Tuple[int, int], RGBColor], Tuple[int, int]]]] = \
            [(char,
              False,  # It's a flag that can distinguish whether it is modified.
              self.FORE_COLOR,
              lambda char, pos, font_color: self.draw_text(char, pos, self.FONT_NAME_CONSOLAS, font_color)) for char in article]

        self.set_caption(title)
        pressed_word = ''
        underline_index = 0
        return reset_flag, history_draw_list, underline_index, total_chars, article, pressed_word

    def start_game(self, init_level: int):
        fps = 25
        clock = pygame.time.Clock()
        const_x_init = 50
        const_y_init = 150
        const_y_gap = 50
        cur_pos = (const_x_init, const_y_init)
        _, history_draw_list, underline_index, total_chars, chosen_article, pressed_word = self.init_game(init_level)
        calculate_pm_info = self.generator_pm_info()
        cpm, wpm = next(calculate_pm_info)  # init
        game_over_view = GameOverView(caption_name='Game over')  # cache view
        need_update = True
        while 1:
            if need_update:
                self.clear_canvas()
                self.draw_panel(total_chars, cpm, wpm)
                for cur_char, modify_flag, font_color, cur_draw in history_draw_list:
                    if cur_char == '\n':
                        cur_char = ''
                        cur_pos = (const_x_init, cur_pos[1] + const_y_gap)
                    cur_pos = cur_draw(cur_char, cur_pos, font_color)
                cur_pos = (const_x_init, const_y_init)
                underline = re.sub(r'[^\n]', " ", pressed_word) + "_"  # Any characters except not space.
                self.draw_article(underline, const_x_init, const_y_init + 10, font_color=self.TYPING_CUR_POS_COLOR, y_gap=const_y_gap)
                self.view_update()
                need_update = False
            for event in self.get_event():
                if self.is_quit_event(event):
                    self.exit_app()
                if self.is_key_down_event(event):
                    if self.is_press_escape_event(event):
                        return

                    pressed_key = self.get_press_key(event)
                    all_keys = pygame.key.get_pressed()

                    if len([_ for _ in all_keys if _ == 1]) == 1 and (all_keys[pygame.K_CAPSLOCK] or all_keys[pygame.K_LSHIFT] or all_keys[pygame.K_RSHIFT]):
                        continue

                    need_update = True

                    if underline_index == len(chosen_article):
                        # next level
                        reset_flag, history_draw_list, underline_index, total_chars, chosen_article, pressed_word = self.init_game()
                        if reset_flag:
                            flag = game_over_view.show()
                            if flag is not None and flag == GameOverView.RTN_MSG_BACK_TO_HOME:
                                return  # back to the home page

                            # set level to the init_level
                            _, history_draw_list, underline_index, total_chars, chosen_article, pressed_word = self.init_game(init_level)
                        cpm, wpm = calculate_pm_info.send(True)
                        break

                    if pressed_key == '\r':
                        pressed_key = '\n'

                    # typing correct
                    if chosen_article[underline_index] == pressed_key:
                        pressed_word += pressed_key
                        is_modify_flag = history_draw_list[underline_index][1]
                        font_color = self.TYPING_CORRECT_COLOR if not is_modify_flag else self.TYPING_MODIFY_COLOR
                        history_draw_list[underline_index] = (pressed_key, False, font_color, lambda char, pos, color: self.draw_text(char, pos, self.FONT_NAME_CONSOLAS, color))
                        total_chars = len(pressed_word)
                        cpm, wpm = calculate_pm_info.send(total_chars)
                        underline_index += 1
                    else:  # typing wrong
                        if pressed_key != '\b':
                            if len(pressed_word + ' ') <= len(chosen_article):
                                history_draw_list[underline_index] = (
                                    chosen_article[underline_index], False, self.TYPING_ERROR_COLOR, lambda char, pos, color: self.draw_text(char, pos, self.FONT_NAME_CONSOLAS, color)
                                )
                                # pressed_word += ' '
                                pressed_word += chosen_article[underline_index]
                                underline_index += 1
                        else:
                            pre_index = max(underline_index - 1, 0)
                            history_draw_list[pre_index] = (chosen_article[pre_index], True, self.FORE_COLOR, lambda char, pos, color: self.draw_text(char, pos, self.FONT_NAME_CONSOLAS, color))
                            pressed_word = pressed_word[: -1]
                            underline_index = max(underline_index - 1, 0)
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
