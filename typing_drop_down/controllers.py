import pygame
from pygame.event import EventType

from .api import generics


class PyGameKeyboard(generics.KeyboardController):
    __slots__ = ()
    KEYBOARD_CONTROLLER = pygame

    def get_event(self):
        for event in pygame.event.get():
            yield event

    @staticmethod
    def is_key_down_event(event: EventType):
        return True if event.type == pygame.KEYDOWN else False

    @staticmethod
    def is_quit_event(event: EventType):
        return True if event.type == pygame.QUIT else False

    @staticmethod
    def is_press_escape_event(event: EventType):
        return True if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE else False

    @staticmethod
    def get_press_key(event) -> str:
        return event.unicode  # <- case-sensitive  # pygame.key.name(event.key)
