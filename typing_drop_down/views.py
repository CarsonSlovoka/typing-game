__all__ = ('PyGameView', 'GameOverView')

from typing import Tuple, Callable, List

from .api.mixins.font.name import FontNameListMixin
from .api.mixins.font.model import FontModelMixin
from .api.utils import cached_property, SafeMember
from .api import generics
from .controllers import PyGameKeyboard

import pygame
from pygame.event import EventType


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

    TYPING_CORRECT_COLOR = COLOR.GREEN
    TYPING_CUR_POS_COLOR = COLOR.BLUE
    TYPING_ERROR_COLOR = COLOR.RED

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
            self.command()


class GameOverView(
    PyGameKeyboard,
    PyGameView,
    SafeMember,
):
    __slots__ = ('_view',
                 '_is_running',
                 '_btn_continue', '_btn_exit') + PyGameView.__slots__

    def __init__(self, caption_name: str,
                 continue_fun: Callable = None, exit_fun: Callable = None):
        PyGameView.__init__(self, caption_name)
        self._is_running = True
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
        self._is_running = True
        self.view.send(None)

    def hide(self):
        self._is_running = False
        self.view.send(None)

    def on_click_continue_btn(self, sub_process: Callable = None):
        self._is_running = False
        if sub_process:
            sub_process()

    def on_click_exit_btn(self, sub_process: Callable = None):
        self._is_running = False
        if sub_process:
            sub_process()

    def _create_view(self):
        clock = pygame.time.Clock()
        dict_action = {self.key_enter: lambda: self.on_click_continue_btn(self.btn_continue.command),
                       self.key_escape: lambda: self.on_click_exit_btn(self.btn_exit.command)}
        while 1:
            yield
            while self.is_running:
                btn_list: List[PyGameButton] = [self.btn_continue, self.btn_exit]

                for event in self.get_event():
                    if self.is_key_down_event(event):
                        fun = dict_action.get(event.key)
                        if fun:
                            fun()

                    for obj in btn_list:
                        obj.handle_event(event)

                self.window.fill(self.BACKGROUND_COLOR)
                for obj in btn_list:
                    obj.draw(self.window)

                self.update()
                clock.tick(25)  # Make sure that the FPS is keeping to this value.
