from typing import Tuple, Generator
import pygame
from pygame.event import EventType

from .api import generics
from .api.utils import ABCSafeMember, SafeMember
import abc


class PyGameKeyboard(generics.KeyboardController):
    __slots__ = ()
    KEYBOARD_CONTROLLER = pygame

    def get_event(self) -> Tuple[EventType]:
        for event in pygame.event.get():
            yield event

    @staticmethod
    def is_key_down_event(event: EventType) -> bool:
        return True if event.type == pygame.KEYDOWN else False

    @staticmethod
    def is_quit_event(event: EventType):
        return True if event.type == pygame.QUIT else False

    @staticmethod
    def is_press_escape_event(event: EventType):
        return True if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE else False

    @staticmethod
    def is_press_enter_event(event: EventType):
        return True if event.type == pygame.KEYDOWN and event.key == pygame.K_KP_ENTER else False

    @staticmethod
    def get_press_key(event) -> str:
        return event.unicode if event.key != 32 else ' '  # <- case-sensitive  # pygame.key.name(event.key)

    @property
    def key_escape(self):
        return pygame.K_ESCAPE

    @property
    def key_enter(self):
        return pygame.K_RETURN


class SwitchViewControl(abc.ABC):
    # __slots__ = ()
    __other_slots__ = ('__is_running', '_view')

    def __init__(self, fps):
        self.__is_running = True
        self._view = self._create_view(fps)
        self._view.send(None)  # init

    @abc.abstractmethod
    def _create_view(self, fps: int) -> Generator[None, None, None]:
        clock = pygame.time.Clock()
        # dict_action = {self.key_enter: lambda: self.on_click_xxx_btn(self.btn_xxx.command),}
        event_list = []
        # btn_list: List[PyGameButton] = [self.btn_continue, self.btn_exit]
        while 1:
            yield
            while self.__is_running:
                for event in event_list:
                    ...

                    """
                    for obj in btn_list:
                        obj.handle_event(event)
                    """

                # update canvvas
                clock.tick(fps)

    def show(self):
        self.__is_running = True
        try:
            self._view.send(None)
        except StopIteration as response:
            return response.value

    def hide(self):
        self.__is_running = False
        self._view.send(None)
