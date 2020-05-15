__all__ = ('PyGameView', 'GameOverView')

from abc import ABC
from typing import Tuple, Callable, List, Generator, Union

from .api.mixins.font.name import FontNameListMixin
from .api.mixins.font.model import FontModelMixin
from .api.utils import cached_property, SafeMember, WindowHelper, ABCSafeMember
from .api import generics
from .controllers import PyGameKeyboard, SwitchViewControl

import pygame
from pygame import Surface
from pygame.event import EventType
from pathlib import Path


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
    WIDTH = 1200

    def __init__(self, caption_name: str):
        pygame.init()
        pygame.display.set_caption(caption_name)
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

    def draw_text(self, text: str, position: Tuple[int, int],
                  font_name: FontNameListMixin, font_color=None, font_size=32, ):
        """
        position: (x, y)
        """
        font = pygame.font.SysFont(font_name, font_size)
        text = font.render(text, True, font_color)
        self.window.blit(text, position)

    def exit_app(self):
        self.destroy_view()
        raise SystemExit


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
        PyGameView.__init__(self, caption_name)
        self.__is_running = True
        btn_width, btn_height = 140, 50
        x = (self.WIDTH - btn_width) / 2
        y = (self.HEIGHT - (2 * btn_height)) / 5  # Divide into 5 equal parts that share 2 buttons.
        self._btn_continue = PyGameButton('Restart', x, int(y * 2), btn_width, btn_height,
                                          command=lambda: self.on_click_continue_btn(continue_fun))
        self._btn_exit = PyGameButton('Exit', x, int(y * 3), btn_width, btn_height,
                                      command=lambda: self.on_click_exit_btn(exit_fun))
        self._view = self._create_view()
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

    def _create_view(self) -> Generator[None, None, Union[str, None]]:
        clock = pygame.time.Clock()
        dict_event = {self.key_enter: lambda: self.on_click_continue_btn(self.btn_continue.command),
                      self.key_escape: lambda: self.on_click_exit_btn(self.btn_exit.command)
                      }
        btn_list: List[PyGameButton] = [self.btn_continue, self.btn_exit]
        while 1:
            yield
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
                                return GameOverView.RTN_MSG_BACK_TO_HOME

                    # click
                    for obj in btn_list:
                        event_result = obj.handle_event(event)
                        if event_result == GameOverView.RTN_MSG_BACK_TO_HOME:
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

        SwitchViewControl.__init__(self, fps=10)

    def _create_view(self, fps: int):
        clock = pygame.time.Clock()
        btn_list: List[PyGameButton] = [self.btn_drop_down, self.btn_article,  # <-- game
                                        self.btn_settings,
                                        self.btn_exit,
                                        ]
        while 1:
            for event in self.get_event():
                if self.is_press_escape_event(event) or self.is_quit_event(event):
                    self.exit_app()

                for obj in btn_list:
                    obj.handle_event(event)

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
