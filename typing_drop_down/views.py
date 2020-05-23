__all__ = ('PyGameView', 'GameOverView', 'HomeView', 'SelectLevelView')

from abc import ABC
from typing import Tuple, Callable, List, Generator, Union
import types

from .api.mixins.font.name import FontNameListMixin
from .api.mixins.font.model import FontModelMixin
from .api.utils import cached_property, SafeMember, WindowHelper, ABCSafeMember
from .api import generics
from .controllers import PyGameKeyboard, SwitchViewControl

import pygame
from pygame import Surface
from pygame.event import EventType

import pygame_menu

from pathlib import Path
import sys
import abc
import re
from time import sleep


class COLOR(generics.RGBColor):
    ...


class PyGameView(
    FontNameListMixin,  # Do not use the proportional spacing font for typing use.
    FontModelMixin,
    generics.GameView,
):
    __slots__ = generics.GameView.__slots__
    VIEW_CONTROLLER = pygame
    INFO_COLOR = COLOR.GREEN  # green  # points, CPM, WPM...

    BACKGROUND_COLOR = (255, 200, 150)
    FORE_COLOR = (0, 0, 0)

    HEIGHT = 600
    WIDTH = 1600

    def __init__(self, caption_name: str = None):
        pygame.init()
        pygame.display.set_caption(caption_name) if caption_name else None
        generics.GameView.__init__(self, window=pygame.display.set_mode((self.WIDTH, self.HEIGHT)))  # ,pygame.FULLSCREEN

    @staticmethod
    def set_caption(caption_name: str):
        pygame.display.set_caption(caption_name)

    @staticmethod
    def get_caption() -> str:
        title, icon_title = pygame.display.get_caption()  # Returns the title and icontitle for the display Surface. These will often be the same value.
        return title

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

    def draw_text(self, text: str, position: Tuple[int, int],
                  font_name: FontNameListMixin, font_color=None, font_size=32, font=None):
        """
        position: (x, y)
        """
        if font is None:
            font = pygame.font.SysFont(font_name, font_size)
        text = font.render(text, True, font_color)
        rect = self.window.blit(text, position)
        return rect.topright

    def exit_app(self):
        self.destroy_view()
        raise SystemExit(1)


class PyGameButton(SafeMember):
    __slots__ = ('_command', '_font',
                 '_canvas_normal', '_canvas_hovered', '_image',
                 '_image_rect',
                 '_is_hovered'
                 )

    def __init__(self, text, x, y, width, height, command: Callable = None,
                 default_color: COLOR = COLOR.GREEN,
                 hovered_color: COLOR = COLOR.RED):
        self._command = command

        self._font = pygame.font.SysFont('ComicSansMs', 32)  # pygame.font.Font('Microsoft YaHei.ttf', 15)

        self._canvas_normal = pygame.Surface((width, height))
        self.canvas_normal.fill(default_color)

        self._canvas_hovered = pygame.Surface((width, height))
        self.canvas_hovered.fill(hovered_color)

        self._image = self.canvas_normal
        self._image_rect = self.image.get_rect()

        text_image = self.font.render(text, True, COLOR.WHITE)
        text_rect = text_image.get_rect(
            center=self.image_rect.center  # change rect.center to here.
        )

        self.canvas_normal.blit(text_image, text_rect)
        self.canvas_hovered.blit(text_image, text_rect)

        self.image_rect.topleft = (x, y)  # you can't use it before `blit`

        self._is_hovered = False

    def draw(self, surface):
        # Decide which object can draw.
        if self.is_hovered:
            self._image = self.canvas_hovered
        else:
            self._image = self.canvas_normal
        surface.blit(self.image, self.image_rect)

    def handle_event(self, event: EventType):
        """hovered or not, and command."""
        if event.type == pygame.MOUSEMOTION:
            self._is_hovered = self.image_rect.collidepoint(event.pos)
            return
        if event.type == pygame.MOUSEBUTTONDOWN and self._is_hovered and self.command:
            return self.command()


class GameOverView(
    PyGameKeyboard,
    PyGameView,
    SafeMember,
):
    __slots__ = ('_view',
                 '__is_running',
                 '_btn_continue', '_btn_exit') + PyGameView.__slots__

    RTN_MSG_BACK_TO_HOME = 'back to home'

    def __init__(self, caption_name: str,
                 continue_fun: Callable = None, exit_fun: Callable = None):
        PyGameView.__init__(self)
        self.__is_running = True
        btn_width, btn_height = 140, 50
        x = (self.WIDTH - btn_width) / 2
        y = (self.HEIGHT - (2 * btn_height)) / 5  # Divide into 5 equal parts that share 2 buttons.
        self._btn_continue = PyGameButton('Restart', x, int(y * 2), btn_width, btn_height,
                                          command=lambda: self.on_click_continue_btn(continue_fun))
        self._btn_exit = PyGameButton('Exit', x, int(y * 3), btn_width, btn_height,
                                      command=lambda: self.on_click_exit_btn(exit_fun))
        self._view = self._create_view(caption_name)
        self._view.send(None)  # init

    def show(self):
        self.__is_running = True
        try:
            self.view.send(None)
        except StopIteration as response:
            return response.value

    def hide(self):
        self.__is_running = False
        self.view.send(None)

    def on_click_continue_btn(self, sub_process: Callable = None):
        self.__is_running = False
        if sub_process:
            sub_process()

    def on_click_exit_btn(self, sub_process: Callable = None):
        self.__is_running = False
        if sub_process:
            sub_process()
        return GameOverView.RTN_MSG_BACK_TO_HOME

    def _create_view(self, caption_name='game over') -> Generator[None, None, Union[str, None]]:
        clock = pygame.time.Clock()
        dict_event = {self.key_enter: lambda: self.on_click_continue_btn(self.btn_continue.command),
                      self.key_escape: lambda: self.on_click_exit_btn(self.btn_exit.command)
                      }
        btn_list: List[PyGameButton] = [self.btn_continue, self.btn_exit]
        org_caption = self.get_caption()
        while 1:
            self.set_caption(org_caption)
            yield
            self.set_caption(caption_name)
            while self.__is_running:
                for event in self.get_event():
                    if self.is_quit_event(event):
                        self.exit_app()
                    # key
                    if self.is_key_down_event(event):
                        handle_event = dict_event.get(event.key)
                        if handle_event:
                            event_result = handle_event()
                            if event_result == GameOverView.RTN_MSG_BACK_TO_HOME:
                                self.set_caption(org_caption)
                                return GameOverView.RTN_MSG_BACK_TO_HOME

                    # click
                    for obj in btn_list:
                        event_result = obj.handle_event(event)
                        if event_result == GameOverView.RTN_MSG_BACK_TO_HOME:
                            self.set_caption(org_caption)
                            return GameOverView.RTN_MSG_BACK_TO_HOME

                self.window.fill(self.BACKGROUND_COLOR)
                for obj in btn_list:
                    obj.draw(self.window)

                self.update()
                clock.tick(25)  # Make sure that the FPS is keeping to this value.


class HomeViewBase(PyGameView):
    """ create spark image"""

    __slots__ = ('_spark_image',) + PyGameView.__slots__

    SPARK_IMAGE: Path = None

    def __init__(self, caption_name: str):
        PyGameView.__init__(self, caption_name)
        assert self.SPARK_IMAGE is not None, NotImplementedError('SPARK_IMAGE is not set')
        spark_image: Surface = pygame.image.load(str(self.SPARK_IMAGE))
        self._spark_image = pygame.transform.scale(spark_image, (self.WIDTH, self.HEIGHT))

    def draw_spark_image(self):
        img_w, img_h = self.spark_image.get_size()
        center_x, center_y = WindowHelper.get_xy_for_move_to_center(self.WIDTH, self.HEIGHT, img_w, img_h)
        self.window.blit(self.spark_image, (center_x, center_y))


class HomeView(PyGameKeyboard, SwitchViewControl, HomeViewBase, SafeMember):
    __slots__ = ('_btn_drop_down', '_btn_article', '_btn_settings', '_btn_exit') + \
                SwitchViewControl.__other_slots__ + HomeViewBase.__slots__

    def __init__(self, caption_name='Index',
                 drop_down_process: Callable = None,
                 article_process: Callable = None,
                 setting_process: Callable = None,
                 exit_fun: Callable = None,
                 ):
        HomeViewBase.__init__(self, caption_name)
        self.__is_running = True

        btn_width, btn_height = 180, 66
        x = (self.WIDTH - btn_width) / 2
        y = (self.HEIGHT - (4 * btn_height)) / 8  # Divide into 8 equal parts that share 4 buttons.

        self._btn_drop_down = PyGameButton('Drop Down', x, int(y * 2), btn_width, btn_height,
                                           command=lambda: self.on_click_btn(drop_down_process))

        self._btn_article = PyGameButton('Article', x, int(y * 4), btn_width, btn_height,
                                         command=lambda: self.on_click_btn(article_process))

        self._btn_settings = PyGameButton('Settings', x, int(y * 6), btn_width, btn_height,
                                          command=lambda: self.on_click_btn(setting_process))

        self._btn_exit = PyGameButton('Exit', x, int(y * 8), btn_width, btn_height,
                                      command=lambda: self.on_click_btn(self.exit_app))

        SwitchViewControl.__init__(self, fps=10)  # call self._create_view

    def _create_view(self, fps: int):
        clock = pygame.time.Clock()
        btn_list: List[PyGameButton] = [self.btn_drop_down, self.btn_article,  # <-- game
                                        self.btn_settings,
                                        self.btn_exit,
                                        ]
        org_caption = self.get_caption()
        while 1:
            yield
            while self.__is_running:
                for event in self.get_event():
                    if self.is_press_escape_event(event) or self.is_quit_event(event):
                        self.exit_app()

                    for obj in btn_list:
                        obj.handle_event(event)
                        self.set_caption(org_caption)

                self.window.fill(self.BACKGROUND_COLOR)
                self.draw_spark_image()
                for obj in btn_list:
                    obj.draw(self.window)

                self.update()
                clock.tick(fps)

    @staticmethod
    def on_click_btn(sub_process: Callable = None):
        if sub_process:
            sub_process()


class _SelectLevelViewBase(PyGameKeyboard, PyGameView, ABCSafeMember):
    """
    To use this class, you are only implementing the method ``_build_level_menu`` and it enough.
    """

    __slots__ = ('_menu_level', '_is_running') + PyGameView.__slots__

    TITLE = 'Select the Level'

    def __init__(self, *args, **kwargs):
        PyGameView.__init__(self)

        self._is_running = True
        self._menu_level: pygame_menu.Menu = self._build_level_menu(*args, **kwargs)

    @abc.abstractmethod
    def _build_level_menu(self, *args, **kwargs) -> pygame_menu.Menu:
        ...

    def exit_app(self):
        self._is_running = False

    def run(self, fps: int):
        clock = pygame.time.Clock()
        org_caption = self.get_caption()
        self.set_caption(self.TITLE)
        sleep(0.25)
        while self._is_running:
            for event in self.get_event():
                if self.is_quit_event(event):
                    self.exit_app()

                if self.is_press_escape_event(event):
                    self.set_caption(org_caption)
                    return

                # self._menu_level.mainloop(self.window, self.main_background, disable_loop=False, fps_limit=fps)
                self._menu_level.draw(surface=self.window, clear_surface=True)
                self._menu_level.update([event])

            self.update()
            clock.tick(fps)


class SelectLevelView(_SelectLevelViewBase, SafeMember):
    __slots__ = ('_config',) + PyGameView.__slots__

    TITLE = 'Select the Stage'

    def __init__(self, config: types.ModuleType, play_process: Callable):
        assert hasattr(config, 'ARTICLE_DIR'), AttributeError('config missing ARTICLE_DIR')
        self._config = config
        _SelectLevelViewBase.__init__(self, play_process)

    def _build_level_menu(self, play_process: Callable, *args):
        regex = re.compile("^[0-9]+.")
        submenu_theme = pygame_menu.themes.THEME_ORANGE.copy()

        submenu_theme.widget_font_size = 30
        submenu_theme.widget_font = self.FONT_NAME_CONSOLAS
        # submenu_theme.title_font = pygame_menu.font.FONT_MUNRO

        menu_stage = pygame_menu.Menu(
            height=self.HEIGHT * 0.5,
            theme=submenu_theme,
            onclose=lambda: self.exit_app(),  # optional
            title='Stage',
            width=self.WIDTH * 0.7,
        )
        source_dir = Path(self.config.ARTICLE_DIR)
        level_info_list = [(regex.search(file_path.name).group().replace('.', ''), file_path.stem) for file_path in source_dir.glob('*.*')]  # 1.apple.txt => (1., 1.apple)  => (1, 1.apple)
        level_info_list = [(n_level, name.replace(n_level+'.', '')) for n_level, name in sorted(level_info_list, key=lambda e: int(e[0]))]  # (1, apple)

        for level, name in level_info_list:

            article_name = f'{level + " " * (4-len(level))} {name}' if len(level) < 4 else f'{level} {name}'
            article_name = article_name[:12] + '...' if 16 - len(article_name) < 0 else article_name + ' ' * (16 - len(article_name))
            menu_stage.add_button(f'{article_name:<16s}', play_process, int(level))
        menu_stage.add_button(f'{"RETURN":<11s}', lambda: self.exit_app())
        return menu_stage
