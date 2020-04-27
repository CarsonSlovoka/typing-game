__all__ = ('PyGameView', 'GameOverView')

from typing import Tuple, Callable, List

from .api import mixins
from .api.utils import cached_property, SafeMember
from .api import generics
from .controllers import PyGameKeyboard

import pygame
from pygame.event import EventType


class COLOR:
    """
    RGB
    """
    __slots__ = ()
    BLACK = (0, 0, 0)
    AZURE = (0, 127, 255)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    PURPLE = (255, 0, 255)
    YELLOW = (255, 255, 0)


class PyGameView(
    mixins.FontModelMixin,
    generics.GameView,
):
    __slots__ = generics.GameView.__slots__
    VIEW_CONTROLLER = pygame
    FONT_NAME = 'ComicSansMs'

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

    @cached_property
    def font(self):
        return pygame.font.SysFont(self.FONT_NAME, 32)

    def draw_text(self, text: str, position: Tuple[int, int], font_color=None):
        """
        position: (x, y)
        """
        text = self.font.render(text, True, font_color)
        self.window.blit(text, position)


class PyGameButton(SafeMember):
    __slots__ = ('_command', '_font',
                 '_canvas_normal', '_canvas_hovered', '_image',
                 '_image_rect',
                 '_is_hovered'
                 )

    def __init__(self, text, x=0, y=0, width=100, height=50, command: Callable = None,
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
    __slots__ = ('_is_running',
                 '_btn_continue', '_btn_exit') + PyGameView.__slots__

    def __init__(self, caption_name: str,
                 continue_fun: Callable = None, exit_fun: Callable = None):
        PyGameView.__init__(self, caption_name)
        self._is_running = True
        self._btn_continue = PyGameButton('Continue', x=200, y=50, width=140, height=50, command=lambda: self.on_click_continue_btn(continue_fun))
        self._btn_exit = PyGameButton('Exit', x=200, y=150, width=140, height=50, command=lambda: self.on_click_exit_btn(exit_fun))

    def start(self):
        self._is_running = True

    def stop(self):
        self._is_running = False

    def on_click_continue_btn(self, sub_process: Callable = None):
        self._is_running = False
        if sub_process:
            sub_process()

    def on_click_exit_btn(self, sub_process: Callable = None):
        self._is_running = False
        if sub_process:
            sub_process()

    def create_view(self):

        clock = pygame.time.Clock()

        while self.is_running:

            btn_list: List[PyGameButton] = [self.btn_continue, self.btn_exit]

            for event in self.get_event():
                if self.is_press_escape_event(event):
                    self._is_running = False

                for obj in btn_list:
                    obj.handle_event(event)

            self.window.fill(self.BACKGROUND_COLOR)
            for obj in btn_list:
                obj.draw(self.window)

            self.update()
            clock.tick(25)  # Make sure that the FPS is keeping to this value.
