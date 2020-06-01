__all__ = ('TypingGameApp', 'TypingDropDown',)

import pygame
from pygame import Surface

from typing import Generator

import random
from pathlib import Path

from .api.utils import SafeMember, after_end
from .api.mixins.colors import TypingGameColorMixin
from .api.mixins import typings
from .api.generics import RGBColor
from .views import PyGameView, GameOverView, HomeView, SelectLevelView
from .controllers import PyGameKeyboard
from . import config
import abc
from typing import Tuple, Union, List, Callable
import re
import types
from dataclasses import dataclass


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

    def draw_panel(self, *args, **kwargs):
        total_chars = kwargs.get('total_chars', 0)
        cpm = kwargs.get('cpm', 0)
        wpm = kwargs.get('wpm', 0)
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

    def start_game(self, parent=None):
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
            self.draw_panel(total_chars=cur_total_chars, cpm=cpm, wpm=wpm)
            # self.draw_text(f'{pressed_word}', (10, 165), font_color=self.INFO_COLOR)
            self.view_update()
            for event in self.get_event():
                if self.is_quit_event(event):
                    self.exit_app()
                if self.is_key_down_event(event):
                    if self.is_press_escape_event(event):
                        self.destroy_view() if parent is None else None
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
        from tkinter import messagebox, Tk

        if 'tk withdraw':
            Tk().wm_withdraw()  # to hide the main window
        # event = pygame.event.wait()
        # if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # press space to restart
        return messagebox.askokcancel('Game over', 'try again?')


class TypingArticle(_TypingGameBase):
    __slots__ = ('_article',) + _TypingGameBase.__slots__

    def __init__(self, article_dir: Path):
        PyGameView.__init__(self)
        self._article: Generator = self.generator_article(article_dir)
        self.article.send(None)  # init generator.

    def draw_panel(self, accuracy: Tuple[int, int], wpm: int) -> pygame.Rect:
        num_ok_char, num_error_char = accuracy
        total_char = max(num_ok_char + num_error_char, 1)
        self.draw_text(f'Accuracy:{(num_ok_char / total_char):<.2f}', (10, 5), self.FONT_NAME_COMIC_SANS_MS, self.INFO_COLOR)
        return self.draw_text(f'WPM:{wpm}', (10, 45), self.FONT_NAME_COMIC_SANS_MS, self.INFO_COLOR)

    def draw_article(self, article: str, x_init: int, y_init: int, font_color, y_gap: int):
        x, y = x_init, y_init
        for row_data in article.splitlines():
            pos = self.draw_text(row_data, (x, y), self.FONT_NAME_CONSOLAS, font_color)
            self.draw_text('↙', (pos[0], pos[1] - 9), self.FONT_NAME_MALGUNGOTHIC, font_color)
            y += y_gap

    @staticmethod
    def generator_article(article_dir: Union[Path, str]) -> Generator[Union[str, int], int, None]:
        """
        :return: Tuple(content, file.name, flag).  # The flag set to True means reset.
        """
        if isinstance(article_dir, str):
            article_dir = Path(article_dir)

        article_list = [_ for _ in article_dir.glob('*.*')]
        regex = re.compile("^[0-9]+.")
        level_info_list = [(regex.search(file_path.name).group().replace('.', ''), file_path) for file_path in article_list]
        article_list = [(n_level, file_path) for n_level, file_path in sorted(level_info_list, key=lambda e: int(e[0]))]

        if len(article_list) == 0:
            raise FileExistsError(f'{article_dir.absolute()}')
        regex_rm_space_on_end = re.compile(r' +$', re.M)  # Remove redundant space on the line ends.
        while 1:
            n_level = yield '', '', True
            if n_level not in [int(level) for level, _ in article_list] + [0]:
                break
            for idx, (_level, file_path) in enumerate(article_list):
                if n_level == int(_level):
                    n_level = idx
                    break
            for _level, cur_article_file in article_list[n_level:]:
                with open(str(cur_article_file), newline=None) as f:
                    content = f.read()
                    if len(content) == 0:
                        raise RuntimeError(f'There is no content at the ``{cur_article_file.absolute()}``')
                    # yield re.sub(r' +$', "", content, flags=re.M)
                    content = re.sub(regex_rm_space_on_end, "", content)
                    n_level = yield content, cur_article_file.name, False
                    if n_level is not None:
                        break

    def init_game(self, y_gap: int, n_level=None):

        @dataclass(eq=False)
        class InitGameStruct:
            __slots__ = ('reset_flag', 'surface_article', 'history_draw_list',
                         'draw_index', 'underline_index', 'num_ok_char', 'num_error_char',
                         'pos_list', 'chosen_article', 'pressed_words')
            reset_flag: bool  # If reset is true, it will get the article by the level which you passed, Otherwise return the next level correspond to the current level.
            surface_article: Surface  # A canvas that draws the article only.
            history_draw_list: List[Tuple[str, Tuple[int, int], bool, RGBColor, Callable]]  # It records every information of the character. Get more, please see the instance.
            draw_index: int  # represent the position of needs changing character while you pressed a key.
            underline_index: int  # the position of underline after you pressed a key.
            num_ok_char: int  # Numbers of character in which is correct.
            num_error_char: int  # Numbers of character in which is wrong.
            pos_list: List[Tuple[int, int]]  # The element means that the position that is for the character to draw.
            chosen_article: str  # The string for represent the article that is user provided.
            pressed_words: str  # To store the input string from the user

        article, title, reset_flag = next(self.article) if n_level is None else self.article.send(n_level)
        surface_article = Surface((self.WIDTH, self.HEIGHT))
        surface_article.fill(self.BACKGROUND_COLOR)

        # we are only interested in the `pos` only.
        init_pos = (0, 0)
        pos_list = []
        cur_pos = init_pos
        for idx, char in enumerate(article):
            if char == '\n':
                char = '↙'
                cur_pos = (cur_pos[0], cur_pos[1] - 9)
            pos_list.append(cur_pos)
            font_name = self.FONT_NAME_CONSOLAS if char != '↙' else self.FONT_NAME_MALGUNGOTHIC
            cur_pos = self.draw_text(char, cur_pos, font_name, self.FORE_COLOR,
                                     target=surface_article,
                                     ).topright
            if char == '↙':
                cur_pos = (init_pos[0], cur_pos[1] + y_gap)

        # Draw a character one by one and pass the current position to the next function.
        history_draw_list: List[Tuple[str, Tuple[int, int],
                                      bool,
                                      RGBColor,
                                      Union[Callable, None]]] = \
            [(char,
              pos,  # The position of drawing.
              False,  # It's a flag that can distinguish whether it is modified.
              self.FORE_COLOR,
              None) for pos, char in zip(pos_list, article)
             ]

        self.set_caption(title)

        draw_index = 0
        underline_index = 0
        num_ok_char, num_error_char = 0, 0
        pressed_word = ''
        return InitGameStruct(reset_flag, surface_article, history_draw_list, draw_index, underline_index,
                              num_ok_char, num_error_char, pos_list, article, pressed_word)

    def start_game(self, init_level: int):
        fps = 25
        clock = pygame.time.Clock()
        const_x_init = 50
        # const_y_init = 150
        const_y_gap = 50

        game = self.init_game(const_y_gap, init_level)
        calculate_pm_info = self.generator_pm_info()
        cpm, wpm = next(calculate_pm_info)  # init
        game_over_view = GameOverView(caption_name='Game over')  # cache view
        need_update = True
        panel_bottom = None
        while 1:
            if game.underline_index == len(game.chosen_article):
                # next level
                game = self.init_game(const_y_gap)
                if game.reset_flag:
                    flag = game_over_view.show()
                    if flag is not None and flag == GameOverView.RTN_MSG_BACK_TO_HOME:
                        return  # back to the home page

                    # set level to the init_level
                    game = self.init_game(const_y_gap, n_level=0)
                cpm, wpm = calculate_pm_info.send(True)
                continue

            if need_update:
                self.clear_canvas()
                init_panel_bottom = self.draw_panel((game.num_ok_char, game.num_error_char), wpm).bottomleft
                if panel_bottom is None:
                    panel_bottom = init_panel_bottom

                # self.draw_article(chosen_article, const_x_init, const_y_init, font_color=self.FORE_COLOR, y_gap=const_y_gap)
                for cur_char, pos, modify_flag, font_color, cur_draw in (game.history_draw_list[game.draw_index],):
                    if cur_draw is None:
                        continue
                    cur_draw(cur_char, pos, font_color) if cur_char != '\n' else \
                        self.draw_text('↙', pos, self.FONT_NAME_MALGUNGOTHIC, font_color, target=game.surface_article)

                # underline = re.sub(r'[^\n]', " ", pressed_word) + "_"  # Any characters except not space.
                # self.draw_article(underline, const_x_init, const_y_init + 10, font_color=self.TYPING_CUR_POS_COLOR, y_gap=const_y_gap)
                self._window.blit(game.surface_article, (const_x_init, panel_bottom[1] + const_y_gap))
                underline_pos = (game.pos_list[game.underline_index][0] + const_x_init,
                                 game.pos_list[game.underline_index][1] + 10 + panel_bottom[1] + const_y_gap)
                self.draw_text('_', underline_pos, self.FONT_NAME_CONSOLAS, self.TYPING_CUR_POS_COLOR)
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

                    if pressed_key == '\r':
                        pressed_key = '\n'

                    # typing correct
                    if game.chosen_article[game.underline_index] == pressed_key:
                        game.num_ok_char += 1
                        game.pressed_words += pressed_key
                        is_modify_flag = game.history_draw_list[game.underline_index][2]
                        font_color = self.TYPING_CORRECT_COLOR if not is_modify_flag else self.TYPING_MODIFY_COLOR
                        game.history_draw_list[game.underline_index] = (pressed_key, game.pos_list[game.underline_index], False, font_color,
                                                                        lambda char, _pos, color: self.draw_text(char, _pos, self.FONT_NAME_CONSOLAS, color, target=game.surface_article))
                        game.draw_index = game.underline_index
                        game.underline_index += 1
                    elif pressed_key == '\b':
                        pre_index = max(game.underline_index - 1, 0)
                        pre_color = game.history_draw_list[pre_index][3]
                        is_modify_flag = True if pre_color != self.TYPING_CORRECT_COLOR else False  # Only with typing wrong can set the True, so the original typing correct that doesn't affect.

                        if pre_color in (self.TYPING_CORRECT_COLOR, self.TYPING_MODIFY_COLOR):
                            game.num_ok_char -= 1
                        if pre_color == self.TYPING_ERROR_COLOR:
                            game.num_error_char -= 1

                        game.history_draw_list[pre_index] = (game.chosen_article[pre_index], game.pos_list[pre_index], is_modify_flag, self.FORE_COLOR,
                                                             lambda char, _pos, color: self.draw_text(char, _pos, self.FONT_NAME_CONSOLAS, color, target=game.surface_article))
                        game.pressed_words = game.pressed_words[: -1]
                        game.underline_index = max(game.underline_index - 1, 0)
                        game.draw_index = game.underline_index
                    else:  # typing wrong
                        if len(game.pressed_words + ' ') <= len(game.chosen_article):
                            game.num_error_char += 1
                            game.history_draw_list[game.underline_index] = (
                                game.chosen_article[game.underline_index], game.pos_list[game.underline_index], False, self.TYPING_ERROR_COLOR,
                                lambda char, _pos, color: self.draw_text(char, _pos, self.FONT_NAME_CONSOLAS, color, target=game.surface_article)
                            )
                            # pressed_word += ' '
                            game.pressed_words += game.chosen_article[game.underline_index]
                            game.draw_index = game.underline_index
                            game.underline_index += 1

                    cpm, wpm = calculate_pm_info.send(game.num_ok_char)

            clock.tick(fps)  # Make sure that the FPS is keeping to this value.


class TypingGameApp(HomeView, SafeMember):
    __slots__ = ('_config',) + HomeView.__slots__
    SPARK_IMAGE = Path(__file__).parent / Path('_static/home.jpg')

    def __init__(self, conf: config):
        if not isinstance(conf, types.ModuleType):
            raise TypeError("conf doesn't belong to types.ModuleType")
        self.__is_running = True
        super().__init__(caption_name='Welcome to the Typing World.',
                         drop_down_process=lambda: TypingDropDown(conf.DROPDOWN_TXT).start_game(parent=self),
                         article_process=lambda: SelectLevelView(config=conf,
                                                                 play_process=lambda n_stage: TypingArticle(conf.ARTICLE_DIR).start_game(init_level=n_stage)
                                                                 ).run(fps=15),  # call _create_view
                         setting_process=None,
                         )

    def start(self):
        return super().show()
