from typing import Tuple

from .api import mixins
from .api.utils import cached_property
from .api import generics

import pygame


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