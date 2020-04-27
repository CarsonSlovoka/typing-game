from .utils import SafeMember

import abc


class GameView(SafeMember):
    """RGB"""
    __slots__ = ('_window',)

    HEIGHT = 600
    WIDTH = 400

    BACKGROUND_COLOR = (255, 200, 150)
    FORE_COLOR = (0, 0, 255)  # blue
    POINT_COLOR = (0, 255, 0)  # green
    VIEW_CONTROLLER: object = None

    def __init__(self):
        assert self.VIEW_CONTROLLER is not None, NotImplementedError("please assign an object for VIEW_CONTROLLER")
        self._window = self.game_view_init()

    @abc.abstractmethod
    def game_view_init(self) -> object:
        raise NotImplementedError

    @abc.abstractmethod
    def view_update(self):
        raise NotImplementedError

    @abc.abstractmethod
    def clear_canvas(self):
        raise NotImplementedError
